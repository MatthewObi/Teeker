from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Decorations
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Additional Database queries
from django.db.models import Q, Avg, Count

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from PIL import Image
from io import BytesIO

import os
import time

# Get the models from models.py
from .models import Content, History, Comment

# Get the validation forms from forms.py
from .form import UploadProfilePictures, UploadBannerPictures, Level0UpdateUserDetails, Level0SearchUsers

# Used for social media link extractions
import re
from bs4 import BeautifulSoup

# Used for reading JSON
import json

# Create your views here.

# CUSTOM ERROR HANDLERS
#############################################################
def handler404(request, *args, **argv):
    return render(request, "teeker/error/404.html", status=404)

def handler403(request, *args, **argv):
    return render(request, "teeker/error/403.html", status=403)

def handler500(request, *args, **argv):
    return render(request, "teeker/error/500.html", status=500)

def csrf_failure(request, reason=""):
	return render(request, "teeker/error/403.html", status=403)
#############################################################

def login_page(request):
	"""Login Page to log the user in"""

	if request.method == "POST":
		
		if not request.POST.get("cdinput"):
			messages.warning(request, "Username/E-mail is missing")
			return HttpResponseRedirect(reverse("login_page"))
		elif not request.POST.get("pwd"):
			messages.warning(request, "Password is missing")
			return HttpResponseRedirect(reverse("login_page"))
		else:
			user = authenticate(request, username=str(request.POST.get("cdinput")), password=str(request.POST.get("pwd")))
			if user:
				login(request, user)
				return HttpResponseRedirect(reverse("index"))
			else:
				messages.warning(request, "Username/E-mail or password is wrong!")
				return HttpResponseRedirect(reverse("login_page"))
	elif request.method == "GET":
		return render(request, "teeker/site_templates/login.html")


def logout_page(request):
	"""Logout the user"""

	if request.method == "GET":
		
		# Log out the user
		logout(request)

		return HttpResponseRedirect(reverse("login_page"))


def register(request):
	"""Register page for the user to register for an account (Sign Up Page)"""

	if request.method == "POST":

		# Check if a required field are filled
		if not request.POST.get("username"):
			messages.warning(request, "Please provide a username!")
			return HttpResponseRedirect(reverse("register"))
		elif not request.POST.get("firstname"):
			messages.warning(request, "Please enter your first name!")
			return HttpResponseRedirect(reverse("register"))
		elif not request.POST.get("lastname"):
			messages.warning(request, "Please enter your last name")
			return HttpResponseRedirect(reverse("register"))
		elif not request.POST.get("email"):
			messages.warning(request, "Please enter a E-mail to use!")
			return HttpResponseRedirect(reverse("register"))
		elif not request.POST.get("pwd"):
			messages.warning(request, "Please provide a password! 8 - 128 Characters long.")
			return HttpResponseRedirect(reverse("register"))
		elif not request.POST.get("cpwd"):
			messages.warning(request, "Plese privide the confirmation password!")
			return HttpResponseRedirect(reverse("register"))
		else:
			
			# Check if the password and confirm password match
			if str(request.POST.get("pwd")) == str(request.POST.get("cpwd")):
				
				# Check if the email address is in use already
				try:
					user = User.objects.get(email=str(request.POST.get("email")))
					if user:
						messages.warning(request, "That e-mail address is already being used!")
						return HttpResponseRedirect(reverse("register"))
				except User.DoesNotExist:
					print("Email is cleared...")

				# Check if the username is already in use
				try:
					user = User.objects.get(username=str(request.POST.get("username")))
					if user:
						messages.warning(request, "Username is already in use by another user!")
						return HttpResponseRedirect(reverse("register"))
				except User.DoesNotExist:
					print("Username is cleared...")

				# Create user in the Database
				User.objects.create_user(
					username=str(request.POST.get("username")),
					first_name=str(request.POST.get("firstname")),
					last_name=str(request.POST.get("lastname")),
					email=str(request.POST.get("email")),
					password=str(request.POST.get("cpwd")) # Passwords will be automatically hashed by Django's hasher (Check settings.py for Hasher type)
				).save()

				# Fill the profile for the users account
				user = User.objects.get(username=str(request.POST.get("username")))
				user.profile.aboutme = """I'm new to Teeker."""
				#user.profile.profile_picture = os.getcwd()+"/static/teeker/assets/default_img/avatar/avataaar.png"
				user.save()

				# Attempt to automatically login the user
				ready_user = authenticate(request, username=str(request.POST.get("username")), password=str(request.POST.get("cpwd")))
				if ready_user:
					login(request, ready_user)
					messages.success(request, "Successfully Registered! Welcome to TeeKer :D")
					return HttpResponseRedirect(reverse("account"))
				else:
					messages.warning(request, "Registered successfully! But failed to log in automatically.")
					return HttpResponseRedirect(reverse("login"))
			else:
				messages.warning(request, "Password and confirm password do not match each other!")
				return HttpResponseRedirect(reverse("register"))
	elif request.method == "GET":
		return render(request, "teeker/site_templates/register.html")


def forgot_pwd(request, option):
	"""Used to send a recovery code to an account email if in the system"""

	if request.method == "GET":

		if option == "email_pwd_code":
			return render(request, "teeker/site_templates/forgot_pwd/email_pwd_code.html")
		else:
			return HttpResponseRedirect(reverse("login_page"))


def emailcode(request):
	"""Sends the code to the e-mail"""

	if request.method == "POST":
		
		if not request.POST.get("email"):
			messages.warning(request, "Please provide an e-mail address!")
			return HttpResponseRedirect(reverse("forgot_pwd", args=("email_pwd_code",)))
		else:
			messages.success(request, "If this e-mail address is in our system, it will receive an email from us.")
			return HttpResponseRedirect(reverse("forgot_pwd", args=("email_pwd_code",)))
	else:
		return HttpResponseRedirect(reverse("forgot_pwd", args=("email_pwd_code",)))


def index_posts(request):
	"""Add more content to the feed (JSON)"""

	if request.method == "GET":
		if request.GET.get("last_id"):

			# Check if the ID is a digit
			if request.GET.get("last_id").isdigit():
				try:
					content_get_id = int(json.loads(request.GET.get("last_id")))
				except json.JSONDecodeError:
					content_get_id = ""

				# Check if the input is a digit (number)
				if content_get_id:
					try:
						content_id = Content.objects.get(pk=int(content_get_id))
					except Content.DoesNotExist:
						return JsonResponse({"content_data": None})
					
					try:
						content_data = Content.objects.all().order_by("-date").filter(date__lte=content_id.date)[1:10]
					except Content.DoesNotExist:
						content_data = []

					# Get the recommended list of the user logged in
					try:
						if request.user.is_authenticated:
							recommended_list = json.loads(request.user.profile.recommended)
						else:
							recommended_list = []
					except json.JSONDecodeError:
						recommended_list = []

					json_content = []
					for item in content_data:

						# Check if the content is already in the recommended list
						if item.pk in recommended_list:
							recommended_status = True
						else:
							recommended_status = False

						# Add the username and profile picture of the content
						try:
							user = User.objects.get(pk=int(item.owner))
							username = user.username
							profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
						except User.DoesNotExist:
							username = "N/A"
							profile_picture = "/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

						json_content.append({
							"pk": item.pk,
							"owner": item.owner,
							"username": str(username),
							"profile_picture": profile_picture,
							"content_type": item.content_type,
							"shared_link": item.shared_link,
							"title": item.title,
							"recommended_status": recommended_status,
							"fire": int(item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0,
							"date": str(item.date.year)+" - "+str(item.date.month)+" - "+str(item.date.day)
						})

					time.sleep(1)

					return JsonResponse({"content_data": json_content})
				else:
					return JsonResponse({"content_data": []})
			else:
				return JsonResponse({"content_data": []})
		else:
			return JsonResponse({"content_data": []})

def index(request):
	"""Home page"""

	if request.method == "GET":

		try:
			content_data = Content.objects.all().order_by("-date").filter(suspended=False)[:2]
		except Content.DoesNotExist:
			content_data = ""

		# Get the recommended list of the user logged in
		try:
			if request.user.is_authenticated:
				recommended_list = json.loads(request.user.profile.recommended)
			else:
				recommended_list = []
		except json.JSONDecodeError:
			recommended_list = []

		for a in range(len(content_data)):

			# Check if the content is already in the recommended list
			if content_data[a].pk in recommended_list:
				content_data[a].recommended_status = True
			else:
				content_data[a].recommended_status = False

			# Get the username and profile picture of the content owner
			try:
				user = User.objects.get(pk=int(content_data[a].owner))
				content_data[a].username = user.username
				content_data[a].profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
			except User.DoesNotExist:
				content_data[a].username = "N/A"
				content_data[a].profile_picture = "/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

			# Get the average FIRE rating of the content
			try:
				content_data[a].fire = int(content_data[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
			except History.DoesNotExist:
				content_data[a].fire = 0

		html_content = {
			"content_data": content_data
		}

		return render(request, "teeker/site_templates/index.html", html_content)


def trending(request):
	"""Trending page. Displays the most popular content on TeeKer"""

	if request.method == "GET":

		html_content = {
			"content": ""
		}

		return render(request, "teeker/site_templates/trending.html", html_content)


def world_posts(request):
	"""Add more content to the feed (JSON)"""

	if request.method == "POST":

		if request.POST.get("contents"):
			
			try:
				content_ex = json.loads(request.POST.get("contents"))
			except json.JSONDecodeError:
				content_ex = None

			if content_ex:
				try:
					content_data = Content.objects.all().order_by("?").exclude(pk__in=content_ex)[:10]
				except Content.DoesNotExist:
					content_data = []

				# Get the recommended list of the user logged in
				try:
					if request.user.is_authenticated:
						recommended_list = json.loads(request.user.profile.recommended)
					else:
						recommended_list = []
				except json.JSONDecodeError:
					recommended_list = []

				json_content = []
				for item in content_data:

					# Check if the content is already in the recommended list
					if item.pk in recommended_list:
						recommended_status = True
					else:
						recommended_status = False

					# Add the username and profile picture to the content
					try:
						user = User.objects.get(pk=int(item.owner))
						username = user.username
						profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
					except User.DoesNotExist:
						username = "N/A"
						profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"

					json_content.append({
						"pk": item.pk,
						"owner": item.owner,
						"username": str(username),
						"profile_picture": profile_picture,
						"content_type": item.content_type,
						"shared_link": item.shared_link,
						"title": item.title,
						"recommended_status": recommended_status,
						"fire": int(item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0,
						"date": str(item.date.year)+" - "+str(item.date.month)+" - "+str(item.date.day)
					})

				time.sleep(1)

				return JsonResponse({"content_data": json_content})
			else:
				return JsonResponse({"content_data": []})

			return JsonResponse({"content_data": []})
		else:
			return JsonResponse({"content_data": []})

def world(request):
	"""World page. Displays the world of TeeKer"""

	if request.method == "GET":

		# Get a random selection of content
		try:
			content_data = Content.objects.all().order_by("?")[:3]
		except Content.DoesNotExist:
			content_data = ""

		# Get the recommended list of the user logged in
		try:
			if request.user.is_authenticated:
				recommended_list = json.loads(request.user.profile.recommended)
			else:
				recommended_list = []
		except json.JSONDecodeError:
			recommended_list = []

		# Add the username and profile picture to the content
		for c in range(len(content_data)):
			
			# Check if the content is already in the recommended list
			if content_data[c].pk in recommended_list:
				content_data[c].recommended_status = True
			else:
				content_data[c].recommended_status = False

			# Add the Username and Profile
			try:
				user_c = User.objects.get(pk=int(content_data[c].owner))
				content_data[c].username = user_c.username
				try:
					content_data[c].profile_picture = (user_c.profile.profile_picture.url).replace("&export=download", "") if user_c.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
				except AttributeError:
					content_data[c].profile_picture = "/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"
			except User.DoesNotExist:
				content_data[c].username = "N/A"
				content_data[c].profile_picture = "/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

			# Get the average FIRE rating of the content
			try:
				content_data[c].fire = int(content_data[c].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data[c].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
			except History.DoesNotExist:
				content_data[c].fire = 0

		# Get a random selection of user's
		try:
			user_data = User.objects.all().order_by("?")[:15]
		except User.DoesNotExist:
			user_data = ""
		user_list = []
		for u in user_data:
			try:
				# Catch any errror well getting the profile picture
				try:
					profile_picture = (u.profile.profile_picture.url).replace("&export=download", "") if u.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
				except AttributeError:
					profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"

				user_list.append({
					"pk": u.pk,
					"profile_picture": profile_picture,
					"username": u.username
				})
			except ValueError:
				user_list.append({
					"pk": u.pk,
					"profile_picture": "/static/teeker/assets/default_img/avatar/avataaars.png",
					"username": u.username
				})

		html_content = {
			"content_data": content_data,
			"user_list": user_list
		}

		return render(request, "teeker/site_templates/world.html", html_content)


@login_required
def recommend_system(request):
	"""Add the content to the recommended list of the user"""

	if request.method == "POST":
		
		# Check if the content ID is present
		if request.POST.get("content"):

			# Check if the content ID is a digit
			if request.POST.get("content").isdigit():
				# Check if the Content is available
				try:
					content_data = Content.objects.get(pk=int(request.POST.get("content")))
				except Content.DoesNotExist:
					return JsonResponse({"STATUS": False})

				if content_data:
					# Get the user's recommended list
					recommended_list = []
					user = User.objects.get(pk=request.user.pk)
					try:
						recommended_list = json.loads(user.profile.recommended)
					except json.JSONDecodeError:
						recommended_list = []
					
					# Check if the content is in the recommended list already
					if request.POST.get("content") in recommended_list:

						# Remove the content from the recommended list
						recommended_list.remove(int(request.POST.get("content")))

						# Add the updated list to the user's profile recommended list
						user.profile.recommended = json.dumps(recommended_list)
						user.save() # Commit

						return JsonResponse({"STATUS": True, "recommended": False})
					else:
						# Add the content to the recommended list
						recommended_list.append(int(request.POST.get("content")))

						# Add the updated recommended list to the user's profile
						user.profile.recommended = json.dumps(recommended_list)
						user.save() # Commit

						return JsonResponse({"STATUS": True, "recommended": True})
				else:
					return JsonResponse({"STATUS": False})
			else:
				return JsonResponse({"STATUS": False})
		else:
				return JsonResponse({"STATUS": False})


@login_required
def vote_system(request):
	"""Controls the voting/rating of the content"""

	if request.method == "POST":

		if request.POST.get("content_id") and request.POST.get("votestatus"):
			
			if request.POST.get("content_id").isdigit() and request.POST.get("votestatus").isdigit():
				
				try:
					# Get the Content's hisotry
					history_data = History.objects.get(
						Q(user__pk=int(request.user.pk)) & Q(content__pk=int(request.POST.get("content_id")))
					)

					# Check if the VOTE is a up vote or down vote
					if int(request.POST.get("votestatus")) >= 1:
						history_data.vote = 1
					elif int(request.POST.get("votestatus")) <= 0:
						history_data.vote = 0
					
					history_data.save() # Commit
				except History.DoesNotExist:
					try:
						content_data = Content.objects.get(pk=int(request.POST.get("content_id")))
						
						# Check if the VOTE is a up vote or down vote
						if int(request.POST.get("votestatus")) >= 1:
							vote = 1
						elif int(request.POST.get("votestatus")) <= 0:
							vote = 0
						else:
							# If failed to determine the if statements stop the process
							return JsonResponse({"STATUS": False})

						# Create a new History for the Content
						History(
							user=request.user,
							content=content_data,
							vote=vote
						).save()
					except Content.DoesNotExist:
						return JsonResponse({"STATUS": False})

				# Get the average vote (0 - 10)
				try:
					history_data = History.objects.filter(content__pk=int(request.POST.get("content_id"))).aggregate(Avg("vote"))
					fire_avg = history_data["vote__avg"] * 10
					history_data_count_0 = History.objects.filter(Q(content__pk=int(request.POST.get("content_id")))&Q(vote=1))
					history_data_count_1 = History.objects.filter(Q(content__pk=int(request.POST.get("content_id")))&Q(vote=0))
				except History.DoesNotExist:
					return JsonResponse({"STATUS": False})

				return JsonResponse({
					"STATUS": True,
					"FIRE": fire_avg,
					"UP": len(history_data_count_0),
					"DOWN": len(history_data_count_1)
					})
			else:
				return JsonResponse({"STATUS": False})
		else:
			return JsonResponse({"STATUS": False})


@login_required
def comment_posts(request):
	"""Add comments and get comments for view page
		User must be logged in to be able to leave comments
		"""

	if request.method == "POST":
		"""Add the cooments to the comtent"""

		# Check if the content ID is provided
		if request.POST.get("content_id"):

			# Check if it is to delete the comment
			if request.POST.get("delete"):
				
				try:

					# Get the History of the user with the content
					history_data = History.objects.get(
						Q(content__pk=int(request.POST.get("content_id"))) & Q(user__pk=int(request.POST.get("user_id")))
						)

					try:
						# Load the comment JSON and delete it from the comments
						comment_data = json.loads(history_data.comment)
						for a in range(len(comment_data)):
							if a < len(comment_data):
								if int(request.POST.get("comment_id")) == comment_data[a]["id"]:
									del comment_data[a]

						# Update the Database
						history_data.comment = json.dumps(comment_data)
						history_data.save() # Commit

						return JsonResponse({"STATUS": True})
					except json.JSONDecodeError:
						return JsonResponse({"STATUS": False})
				except History.DoesNotExist:
					return JsonResponse({"STATUS": False})
			else:

				#if request.POST.get("comment"):

				#	comment_data = request.POST.get("comment")

				#	print(len(comment_data.split(" ")))
				#	print(len(comment_data.split("\n")))
				#	print(comment_data.isalnum())
				#	print(comment_data.isalpha())
				#	print(bool(re.match('^[a-zA-Z!-@]+$', comment_data)))

				#	messages.warning(request, "Testing...")
				#	return HttpResponseRedirect(reverse("view_page", args=(request.POST.get("content_id"),)))

				if not request.POST.get("comment"):
					messages.warning(request, "Missing comment... Please provide a comment.")
					return HttpResponseRedirect(reverse("view_page", args=(request.POST.get("content_id"),)))
					
				else:

					try:
						content_data = Content.objects.get(pk=int(request.POST.get("content_id")))

						# Check if theres any history for this content
						if content_data.contents_history.all():
							contents_history = History.objects.filter(content=content_data)
							
							for a in range(len(contents_history)):
								
								# Check if the user already has a comment for this content
								if contents_history[a].user.pk == request.user.pk:
									if contents_history[a].comment:

										# Load the string JSON
										comment_list = json.loads(contents_history[a].comment)

										# Create a ID for the comment
										add_id = 0
										for b in range(len(comment_list)):
											add_id = comment_list[b]["id"] + 1

										comment_list.append({
											"id": add_id,
											"content_id": int(request.POST.get("content_id")),
											"comment": str(request.POST.get("comment")),
											"date": f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
										})

										# Add and save the comment
										contents_history[a].comment = json.dumps(comment_list)
										contents_history[a].save()

									else:
										comment = [{
											"id": 0,
											"content_id": int(request.POST.get("content_id")),
											"comment": str(request.POST.get("comment")),
											"date": f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
										}]

										# Add and save the comment
										contents_history[a].comment = json.dumps(comment)
										contents_history[a].save()

								# If the user hasn't made a comment create a JSON
								else:
									comment = [{
											"id": 0,
											"content_id": int(request.POST.get("content_id")),
											"comment": str(request.POST.get("comment")),
											"date": f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
										}]
									History(
										user=request.user,
										content=content_data,
										comment=json.dumps(comment)
									).save()
									
						else:
							comment = [{
									"id": 0,
									"content_id": int(request.POST.get("content_id")),
									"comment": str(request.POST.get("comment")),
									"date": f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
								}]
							History(
								user=request.user,
								content=content_data,
								comment=json.dumps(comment)
							).save()

					except Content.DoesNotExist:
						messages.error(request, "COMMENT E0: Failed to add comment")
						return HttpResponseRedirect(reverse("view_page", args=("e0",)))

					messages.success(request, "Comment successfully added!")
					return HttpResponseRedirect(reverse("view_page", args=(request.POST.get("content_id"),)))
		else:
			messages.error(request, "COMMENT E0: Failed to add comment")
			return HttpResponseRedirect(reverse("view_page", args=("e0",)))


def view_page(request, content_id=None):
	"""Displays the content in a more detailed way"""

	if request.method == "GET":
		
		if content_id:
			if content_id.isdigit():
				try:

					# Get the contents details
					content_data = Content.objects.get(pk=int(content_id))
					content_data.fire = int(content_data.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
					
					try:
						# Get all the available comments of this particular content
						history_data = content_data.contents_history.all()
						
						content_comments = []
						for a in history_data:
							if a.comment:
								for b in json.loads(a.comment):
									content_comments.append({
										"id": b["id"],
										"content_id": b["content_id"],
										"profile_picture": (a.user.profile.profile_picture.url).replace("&export=download", "") if a.user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png",
										"username": a.user.username,
										"user_id": a.user.pk,
										"comment": b["comment"],
										"date": b["date"]
									})

					except json.JSONDecodeError:
						content_data['contents_history']['comment'] = []

					# Check if the content isn't suspended
					if content_data.suspended and not request.user.is_staff:
						content_data = {
							"title": "CONTENT UNAVAILABLE"
						}

					# Check if the user is logged in
					if request.user.is_authenticated:
						# Check if the content is in the logged in user's recommended list
						try:
							if content_id in json.loads(request.user.profile.recommended):
								content_data.recommended = True
							else:
								content_data.recommended = False
						except json.JSONDecodeError:
							content_data.recommended = False
					else:
						content_data.recommended = False
						
				except Content.DoesNotExist:
					content_data = {
						"title": "CONTENT UNAVAILABLE"
					}
			else:
				content_data = {
						"title": "CONTENT UNAVAILABLE"
					}
		else:
			content_data = {
				"title": "CONTENT UNAVAILABLE"
			}

		html_content = {
			"content_data": content_data,
			"content_comments": content_comments
		}

		return render(request, "teeker/site_templates/view.html", html_content)


def view_teeker_page_posts(request):
	"""Get the content of the account.
	Used on the Account and Teeker View Account pages.
	Only returns in JsonResponse."""

	if request.method == "GET":

		# The user ID of the Teeker account being viewed
		print(request.GET.get("user"))

		# The content ID of the last content on the page
		print(request.GET.get("lastid"))

		# The section (Home or Recommended) to know what content to look for
		print(request.GET.get("section"))

		if request.GET.get("user") and request.GET.get("lastid") and request.GET.get("section"):
			print("FIRST LINE PASSED")
			print(f"USER ID: {request.GET.get('user').isdigit()}")
			print(f"LAST ID: {request.GET.get('lastid').isdigit()}")
			print(f"SECTION: {request.GET.get('section').isalpha()}")
			if request.GET.get("user").isdigit() and request.GET.get("lastid").isdigit() and request.GET.get("section").isalpha():
				print("SECOND LINE PASSED")

				if request.GET.get("section") == "home":
					print("HOME ACCESSED")
					content_get_id = int(request.GET.get("lastid"))

					# Check if the input is a digit (number)
					if content_get_id:
						try:
							content_id = Content.objects.get(pk=int(content_get_id))
						except Content.DoesNotExist:
							return JsonResponse({"content_data": None})
						
						try:
							content_data = Content.objects.all().order_by("-date").filter(date__lte=content_id.date).filter(content_owner__pk=int(request.GET.get("user")))[1:10]
						except Content.DoesNotExist:
							content_data = []

						json_content = []
						for item in content_data:

							try:
								user = User.objects.get(pk=int(item.owner))
								username = user.username
								try:
									profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
								except AttributeError:
									profile_picture = "/static/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"
							except User.DoesNotExist:
								username = "N/A"
								profile_picture = "/static/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

							json_content.append({
								"pk": item.pk,
								"owner": item.owner,
								"username": str(username),
								"profile_picture": profile_picture,
								"content_type": item.content_type,
								"shared_link": item.shared_link,
								"title": item.title,
								"fire": int(item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0,
								"date": str(item.date.year)+" - "+str(item.date.month)+" - "+str(item.date.day)
							})

						time.sleep(1)

						return JsonResponse({"content_data": json_content})

				elif request.GET.get("section") == "recommended":
					print("RECOMMENDED ACCESSED")
					try:
						# Get the user's Data from the Database
						user = User.objects.get(pk=int(request.GET.get("user")))

						try:
							# List of the current content on the page
							current_recommended = json.loads(request.GET.get('list'))

							# Load the JSON list of the recommended content
							recommended_list = json.loads(user.profile.recommended)
							
							# Delete all the items from the last till the last ID
							for a in range(len(current_recommended)):
								
								if a < len(current_recommended):

									# Check if the current recommended list is digits
									if current_recommended[a].isdigit():
										if int(current_recommended[a]) in recommended_list:
											recommended_list.remove(int(current_recommended[a]))
									else:
										recommended_list = []

							if recommended_list:
								try:
									content_data = Content.objects.filter(pk__in=recommended_list).exclude(suspended=True)[:10]

									json_content = []
									for item in content_data:

										try:
											user = User.objects.get(pk=int(item.owner))
											username = user.username
											try:
												profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
											except AttributeError:
												profile_picture = "/static/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"
										except User.DoesNotExist:
											username = "N/A"
											profile_picture = "/static/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

										json_content.append({
											"pk": item.pk,
											"owner": item.owner,
											"username": str(username),
											"profile_picture": profile_picture,
											"content_type": item.content_type,
											"shared_link": item.shared_link,
											"title": item.title,
											"fire": int(item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if item.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0,
											"date": str(item.date.year)+" - "+str(item.date.month)+" - "+str(item.date.day)
										})

									time.sleep(1)

									return JsonResponse({"content_data": json_content})
								except Content.DoesNotExist:
									return JsonResponse({"content_data": []})
							else:
								return JsonResponse({"content_data": []})

						except json.JSONDecodeError:
							return JsonResponse({"content_data": []})
					except User.DoesNotExist:
						return JsonResponse({"content_data": []})
				
				elif request.GET.get("section") == "history":
					print("HISTORY ACCESSED")
					print(request.GET.get("list"))

					# Check if the user is in the Database
					try:
						user = User.objects.get(pk=int(request.GET.get("user")))

						# Check if the list is a JSON object
						try:
							current_history = json.loads(request.GET.get("list"))

							# Get the content the user has interacted with (History)
							try:
								content_data_history = user.users_history.all()
								
								json_content = []
								for b in range(len(content_data_history)):
									if b < len(content_data_history):
										if str(content_data_history[b].content.pk) not in current_history:
											# Get the average FIRE rating of the content
											try:
												content_data_history[b].fire = int(content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
											except History.DoesNotExist:
												content_data_history[b].fire = 0

											try:
												profile_picture = (content_data_history[b].user.profile.profile_picture.url).replace("&export=download", "") if content_data_history[b].user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
											except AttributeError:
												profile_picture = "/static/teeker/assets/img/avataaars.png?h=1af48d52c424c9305613100e47709852"

											json_content.append({
												"pk": content_data_history[b].content.pk,
												"owner": content_data_history[b].content.owner,
												"username": content_data_history[b].user.username,
												"profile_picture": profile_picture,
												"content_type": content_data_history[b].content.content_type,
												"shared_link": content_data_history[b].content.shared_link,
												"title": content_data_history[b].content.title,
												"fire": int(content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0,
												"date": str(content_data_history[b].content.date.year)+" - "+str(content_data_history[b].content.date.month)+" - "+str(content_data_history[b].content.date.day)
											})
								
								time.sleep(1)
								return JsonResponse({"content_data": json_content})

							except History.DoesNotExist:
								return JsonResponse({"content_data": []})

						except json.JSONDecodeError:
							return JsonResponse({"content_data": []})

					except User.DoesNotExist:
						return JsonResponse({"content_data": []})

					return JsonResponse({"content_data": []})

				else:
					return JsonResponse({"content_data": []})
			else:
				return JsonResponse({"content_data": []})
		else:
			return JsonResponse({"content_data": []})
		return JsonResponse({"content_data": []})


def view_teeker_page(request, user_id=None):
	"""Display the page of Teeker User's"""

	if request.method == "POST":

		if request.POST.get("chase"):
			if request.POST.get("user_id") and request.user.is_authenticated:

				# Check if the input is a digit
				if request.POST.get("user_id").isdigit():
					
					# Check if the user is trying to chase themselves
					# Tell them they already chasing themselves
					if int(request.POST.get("user_id")) == request.user.pk:
						return JsonResponse({"STATUS": True, "CHASING": True})

					try:
						chasing_list = json.loads(request.user.profile.user_chasing)
						
						# Check if the user is already chasing the user
						if int(request.POST.get("user_id")) in chasing_list:
							for a in range(len(chasing_list)):
								
								# Remove the user from the list
								if a < len(chasing_list):
									if chasing_list[a] == int(request.POST.get("user_id")):
										del chasing_list[a]
										break

							# Update the Database
							request.user.profile.user_chasing = json.dumps(chasing_list)
							request.user.save()
							return JsonResponse({"STATUS": True, "CHASING": False})

						else:
							
							# If the user isn't in the list add them
							chasing_list.append(int(request.POST.get("user_id")))

							# Update the Database
							request.user.profile.user_chasing = json.dumps(chasing_list)
							request.user.save()
							return JsonResponse({"STATUS": True, "CHASING": True})

					except json.JSONDecodeError:

						# If the user doesn't have a JSON list of user his chasing
						# we'll make one here

						chasing_list = []
						chasing_list.append(int(request.POST.get("user_id")))
						
						# Update the Database
						request.user.profile.user_chasing = json.dumps(chasing_list)
						request.user.save()

					return JsonResponse({"STATUS": True, "CHASING": True})
				else:
					return JsonResponse({"STATUS": False})
			else:
				return JsonResponse({"STATUS": False})
		else:
			return JsonResponse({"STATUS": False})

	elif request.method == "GET":

		# Avoid out of bound error
		aboutme_show = None
		content_data = None
		content_data_recommend = None

		if user_id.isdigit():
			try:
				user = User.objects.get(pk=int(user_id))
				
				# Check if the user isn't suspended but if the logged in user is a staff member allow them to view the suspended account
				if user.profile.suspended and not request.user.is_staff:
					user_data = {
						"username": "User is suspended.",
						"profile_picture": "/static/teeker/assets/default_img/avatar/avataaars.png",
						"banner_picture": "/static/teeker/assets/default_img/banner/banner1.jpg"
					}
				else:

					# Get all the social media links the account has
					try:
						socialmedialinks = json.loads(user.profile.socialmedialinks)
					except json.JSONDecodeError:
						socialmedialinks = []

					# Check if the user is viewing their own account
					# Make Chasing True if they viewing their own account
					if int(user_id) == request.user.pk:
						chasing_btn = True
					else:
						if request.user.is_authenticated:
							try:
								chasing_list = json.loads(request.user.profile.user_chasing)
								if int(user_id) in chasing_list:
									chasing_btn = True
								else:
									chasing_btn = False
							except json.JSONDecodeError:
								chasing_btn = False
						else:
							chasing_btn = False

					# Check for Profile Picture
					try:
						profile_picture = (user.profile.profile_picture.url).replace("&export=download", "") if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
					except AttributeError:
						profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"

					# Check for the banner picture
					try:
						banner_picture = (user.profile.banner_picture.url).replace("&export=download", "") if user.profile.banner_picture else "/static/teeker/assets/default_img/banner/banner1.jpg"
					except AttributeError:
						banner_picture = "/static/teeker/assets/default_img/banner/banner1.jpg"

					user_data = {
						"user_id": user_id,
						"username": user.username,
						"aboutme": user.profile.aboutme,
						"profile_picture": profile_picture,
						"banner_picture": banner_picture,
						"is_staff": user.is_staff,
						"verified": user.profile.verified,
						"developer": user.profile.developer,
						"founder": user.profile.founder,
						"social_media_link": socialmedialinks,
						"chasing_btn": chasing_btn
					}

					# Make the about me information that shows bellow the username shorter if it passes 20 characters
					if len(user.profile.aboutme) >= 50:
						aboutme_show = str(user.profile.aboutme)[:50]+"..."
					else:
						aboutme_show = user.profile.aboutme

					# Get the recommended content by the user
					try:
						content_list = json.loads(user.profile.recommended)

						try:
							content_data_recommend = Content.objects.filter(pk__in=content_list).exclude(suspended=True)[:1]

							for a in range(len(content_data_recommend)):
								
								# Add the username and profile picture to the content for the HTML
								try:
									user_a = User.objects.get(pk=int(content_data_recommend[a].owner))
									content_data_recommend[a].username = user_a.username
									try:
										content_data_recommend[a].profile_picture = (user_a.profile.profile_picture.url).replace("&export=download", "") if user_a.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
									except AttributeError:
										content_data_recommend[a].profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"
								except User.DoesNotExist:
									content_data_recommend[a].username = "N/A"
									content_data_recommend[a].profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"

								# Get the average FIRE rating of the content
								try:
									content_data_recommend[a].fire = int(content_data_recommend[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data_recommend[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
								except History.DoesNotExist:
									content_data_recommend[a].fire = 0

						except Content.DoesNotExist:
							content_data_recommend = []
					except json.JSONDecodeError:
						content_data_recommend = []

					# Get the content the user owns/posted themselves
					try:
						if request.user.pk == int(user_id) or request.user.is_staff:
							content_data = Content.objects.filter(owner=int(user_id)).order_by("-date")[:1]
						else:
							content_data = Content.objects.filter(owner=int(user_id)).filter(suspended=False).order_by("-date")[:1]
						
						# Add the FIRE avg
						for b in range(len(content_data)):
							if b < len(content_data):
								# Get the average FIRE rating of the content
								try:
									content_data[b].fire = int(content_data[b].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data[b].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
								except History.DoesNotExist:
									content_data[b].fire = 0
					except ObjectDoesNotExist:
						content_data = ""

			except User.DoesNotExist:
				user_data = {
					"username": "User unavailable.",
					"profile_picture": "/static/teeker/assets/default_img/avatar/avataaars.png",
					"banner_picture": "/static/teeker/assets/default_img/banner/banner1.jpg"
				}
		else:
			user_data = {
				"username": "User unavailable.",
				"profile_picture": "/static/teeker/assets/default_img/avatar/avataaars.png",
				"banner_picture": "/static/teeker/assets/default_img/banner/banner1.jpg"
			}

		html_content = {
			"user_data": user_data,
			"aboutme_show": aboutme_show if aboutme_show else "N/A",
			"content_data": content_data if content_data else None,
			"content_data_recommend": content_data_recommend if content_data_recommend else None
		}

		return render(request, "teeker/site_templates/TK/view.html", html_content)


@login_required
def account_page(request):
	"""Account Page. The personal account page for the logged in user."""

	if request.method == "GET":

		# Get the content the user owns
		try:
			content_data = Content.objects.filter(owner=request.user.pk).order_by("-date")[:1]
		except Content.DoesNotExist:
			content_data = ""
		
		# Add the FIRE avg
		for b in range(len(content_data)):
			if b < len(content_data):
				# Get the average FIRE rating of the content
				try:
					content_data[b].fire = int(content_data[b].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data[b].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
				except History.DoesNotExist:
					content_data[b].fire = 0

		# Get the content the user has interacted with (History)
		try:
			content_data_history = request.user.users_history.all()[:1]
			
			for b in range(len(content_data_history)):
				if b < len(content_data_history):
					# Get the average FIRE rating of the content
					try:
						content_data_history[b].fire = int(content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data_history[b].content.contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
					except History.DoesNotExist:
						content_data_history[b].fire = 0

		except History.DoesNotExist:
			content_data_history = []

		# Get the content the user is recommending
		try:
			content_data_recommend = Content.objects.filter(pk__in=json.loads(request.user.profile.recommended)).exclude(suspended=True)[:1]

			# Add the username and profile picture to the content data recommended
			for a in range(len(content_data_recommend)):

				# Check if the user details are available
				try:
					user = User.objects.get(pk=int(content_data_recommend[a].owner))
					content_data_recommend[a].username = user.username
					content_data_recommend[a].profile_picture = user.profile.profile_picture.url if user.profile.profile_picture else "/static/teeker/assets/default_img/avatar/avataaars.png"
				except User.DoesNotExist:
					content_data_recommend[a].username = "N/A"
					content_data_recommend[a].profile_picture = "/static/teeker/assets/default_img/avatar/avataaars.png"

				# Get the average FIRE rating of the content
				try:
					content_data_recommend[a].fire = int(content_data[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] * 10) if content_data_recommend[a].contents_history.all().aggregate(Avg("vote"))["vote__avg"] else 0
				except History.DoesNotExist:
					content_data_recommend[a].fire = 0

		except json.JSONDecodeError:
			content_data_recommend = []

		# Get the social media links of the user
		try:
			profile_social_media = json.loads(request.user.profile.socialmedialinks)
		except json.JSONDecodeError:
			profile_social_media = ""

		# Make the about me information that shows bellow the username shorter if it passes 20 characters
		if len(request.user.profile.aboutme) >= 50:
			aboutme_show = str(request.user.profile.aboutme)[:50]+"..."
		else:
			aboutme_show = request.user.profile.aboutme

		html_content = {
			"aboutme_show": aboutme_show,
			"content_data": content_data,
			"content_data_history": content_data_history,
			"content_data_recommend": content_data_recommend,
			"social_media": profile_social_media
		}

		return render(request, "teeker/site_templates/account.html", html_content)


@login_required
def editcontent(request):
	"""Allow for content to be editable"""

	if request.method == "POST":

		# Check if the content ID is provided
		if request.POST.get("content"):
			
			# Make sure the content ID is a digit
			if request.POST.get("content").isdigit():

				# Check if the title is provided
				if not request.POST.get("title"):
					messages.warning(request, "Missing title... Need to fill in title.")
					return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")
				
				# Check if the description is provided
				elif not request.POST.get("des"):
					messages.warning(request, "Missing description... Need to fill in the description.")
					return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")

				# Check if the tags meet requirements
				elif request.POST.get("tags") and len(request.POST.get("tags")) < 1:
					messages.warning(request, "Weak tags... Need to provide one tag.")
					return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")

				else:

					try:
						content_data = Content.objects.get(pk=int(request.POST.get("content")))

						# Check if the logged in user is the owner of the content being edited
						if content_data.owner == request.user.pk:
							
							# Update the details
							content_data.title = str(request.POST.get("title"))
							content_data.description = str(request.POST.get("des"))
							content_data.tags = str(request.POST.get("tags"))
							content_data.save # commit changes

							messages.success(request, "Successfully updated the content's details!")
							return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")

						else:
							messages.warning(request, "EDIT PAGE: E3. You are not allowed to edit this content")
							return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")

					except Content.DoesNotExist:
						messages.error(request, "EDIT PAGE: E2. Failed to find content to edit.")
						return HttpResponseRedirect(f"/editcontent?content={request.POST.get('content')}")
			else:
				messages.error(request, "EDIT PAGE: E1. Somethings wrong with the contents ID!")
				return HttpResponseRedirect(reverse("editcontent"))	
		else:
			messages.error(request, "EDIT PAGE: E0. Couldn't find the content to edit!")
			return HttpResponseRedirect(reverse("editcontent"))

	elif request.method == "GET":

		# Make sure there is a content ID provided
		if request.GET.get("content"):

			# Check if the input is only a digit
			if request.GET.get("content").isdigit():
				try:

					# Get all the details of the content
					content_data = Content.objects.get(pk=int(request.GET.get("content")))

					# Make sure the person trying to edit content owns it
					if content_data.owner != request.user.pk:
						messages.warning(request, "You do not have permissions to edit that content!")
						return HttpResponseRedirect(reverse("account"))

				except Content.DoesNotExist:
					content_data = {
						"title": "Unavailable"
					}
			else:
				content_data = {
					"title": "Unavailable"
				}
		else:
			content_data = {}

		html_content = {
			"content_data": content_data
		}

		return render(request, "teeker/site_templates/editcontent.html", html_content)


@login_required
def upload(request, content_type=None):
	"""Share Page better know as Upload page. People can share/upload their content from other social media"""

	if request.method == "POST":

		# Handles Instagram post sharing
		if content_type == "instagram":
			if not request.POST.get("instagram_link"):
				messages.warning(request, "Missing Instagram link to content!")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("title"):
				messages.warning(request, "Missing title...")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("description"):
				messages.warning(request, "Missing description...")
				return HttpResponseRedirect(reverse("upload"))
			else:
				
				# Check if the URL link is a Instagram one
				result = re.match("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", str(request.POST.get("instagram_link")))
				if result:
					if result[0] == "https://www.instagram.com":
						shared_link= ""
						for i in str(request.POST.get("instagram_link")):
							if i == "?":
								break
							shared_link += i
						
						if len(shared_link) > 1:
							shared_link += "embed"
							Content(
								content_owner=request.user,
								owner=request.user.pk,
								content_type=str(content_type),
								shared_link=str(shared_link),
								title=str(request.POST.get("title")),
								description=str(request.POST.get("description")),
								tags=str(request.POST.get("tags"))
							).save()
							
							messages.success(request, "Successfully shared your post!")
							#return HttpResponseRedirect(reverse("view_content"))
							return HttpResponseRedirect(reverse("upload"))
					else:
						messages.error(request, "Link does not match Instagrams links!")
						return HttpResponseRedirect(reverse("upload"))
				else:
					messages.error(request, "Sorry the social media link for Instagram is invalid!")
					return HttpResponseRedirect(reverse("upload"))
		
		# Handles YouTube post sharing
		elif content_type == "youtube":
			if not request.POST.get("youtube_link"):
				messages.warning(request, "Missing youtube link to content!")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("title"):
				messages.warning(request, "Missing title...")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("description"):
				messages.warning(request, "Missing description...")
				return HttpResponseRedirect(reverse("upload"))
			else:
				
				# Extract the YouTube Video ID
				youtube_links = request.POST.get('youtube_link')
				pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
				result = re.findall(pattern, youtube_links, re.MULTILINE | re.IGNORECASE)
				
				# Check if the YouTube video ID is available
				if result:
					if len(result[0]) > 1:
						shared_link = "https://www.youtube.com/embed/"+result[0]
						Content(
							content_owner=request.user,
							owner=request.user.pk,
							content_type=str(content_type),
							shared_link=str(shared_link),
							title=str(request.POST.get("title")),
							description=str(request.POST.get("description")),
							tags=str(request.POST.get("tags"))
						).save()

						messages.success(request, "Successfully shared your post!")
						#return HttpResponseRedirect(reverse("view_content"))
						return HttpResponseRedirect(reverse("upload"))
				else:
					messages.error(request, "Sorry the social media link for YouTube is invalid! (Did not contain video ID)")
					return HttpResponseRedirect(reverse("upload"))

		# Handles Vimeo post sharing
		elif content_type == "vimeo":
			if not request.POST.get("vimeo_link"):
				messages.warning(request, "Missing vimeo link to content!")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("title"):
				messages.warning(request, "Missing title...")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("description"):
				messages.warning(request, "Missing description...")
				return HttpResponseRedirect(reverse("upload"))
			else:

				# Extract the Vimeo Video ID
				vimeo_links = request.POST.get('vimeo_link')
				pattern = r'^(http://)?(www\.)?(vimeo\.com/)?(\d+)'
				result = re.search(r'^(https://)?(www\.)?(vimeo\.com/)?(\d+)', vimeo_links)

				if result:
					if len(result[0]) > 1:
						shared_link = "https://player.vimeo.com/video/"+result.group(4)
						Content(
							content_owner=request.user,
							owner=request.user.pk,
							content_type=str(content_type),
							shared_link=str(shared_link),
							title=str(request.POST.get("title")),
							description=str(request.POST.get("description")),
							tags=str(request.POST.get("tags"))
						).save()

						messages.success(request, "Successfully shared your post!")
						#return HttpResponseRedirect(reverse("view_content"))
						return HttpResponseRedirect(reverse("upload"))
				else:
					messages.error(request, "Sorry the social media link for Vimeo is invalid! (Did not contain video ID)")
					return HttpResponseRedirect(reverse("upload"))

		# Handles SoundCloud post sharing
		elif content_type == "soundcloud":
			if not request.POST.get("soundcloud_embed"):
				messages.warning(request, "Missing soundcloud link to content!")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("title"):
				messages.warning(request, "Missing title...")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("description"):
				messages.warning(request, "Missing description...")
				return HttpResponseRedirect(reverse("upload"))
			else:

				word_replace = str(request.POST.get('soundcloud_embed')).replace("auto_play=true", "auto_play=false").replace("width=", "width='100%' ").replace("height=", "height='300' ")

				soup = BeautifulSoup(word_replace, features="html.parser")
				if soup:

					# Check if the Embed is a SoundCloud one
					result = None
					try:
						src_attribute = soup.find("iframe")["src"]
						result = re.match("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", src_attribute)
					except TypeError:
						messages.error(request, "Please place SoundCloud's Embed Code in the field and nothing else. Check the Share Options.")
						return HttpResponseRedirect(reverse("upload"))

					if result:
						result = re.match('https?://([A-Za-z_0-9.-]+).*', result[0])
						result = str(result.group(1))
						if "soundcloud.com" in result:
							
							shared_link = word_replace
							Content(
								content_owner=request.user,
								owner=request.user.pk,
								content_type=str(content_type),
								shared_link=str(shared_link),
								title=str(request.POST.get("title")),
								description=str(request.POST.get("description")),
								tags=str(request.POST.get("tags"))
							).save()

							messages.success(request, "Successfully shared your post!")
							#return HttpResponseRedirect(reverse("view_content"))
							return HttpResponseRedirect(reverse("upload"))
						else:
							messages.warning(request, "The Embed does not bellong to SoundCloud!")
							return HttpResponseRedirect(reverse("upload"))
					else:
						messages.error(request, "Sorry the social media link for SoundCloud is invalid!")
						return HttpResponseRedirect(reverse("upload"))
				else:
					messages.error(request, "Please place SoundCloud's Embed Code in the field and nothing else. Check the Share Options.")
					return HttpResponseRedirect(reverse("upload"))

		# Handles Spotify post sharing
		elif content_type == "spotify":
			if not request.POST.get("spotify_embed"):
				messages.warning(request, "Missing spotify link to content!")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("title"):
				messages.warning(request, "Missing title...")
				return HttpResponseRedirect(reverse("upload"))
			elif not request.POST.get("description"):
				messages.warning(request, "Missing description...")
				return HttpResponseRedirect(reverse("upload"))
			else:

				word_replace = str(request.POST.get('spotify_embed')).replace("width=", "width='100%' ").replace("height=", "height='380' ")
				soup = BeautifulSoup(word_replace, features="html.parser")
				if soup:

					# Check if the Embed is a Spotify one
					result = None
					try:
						src_attribute = soup.find("iframe")["src"]
						result = re.match("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", src_attribute)
					except TypeError:
						messages.error(request, "Please place Spotify's Embed Code in the field and nothing else. Check the Share Options.")
						return HttpResponseRedirect(reverse("upload"))

					if result:
						result = re.match('https?://([A-Za-z_0-9.-]+).*', result[0])
						result = str(result.group(1))
						if "spotify.com" in result:
							
							shared_link = word_replace
							Content(
								content_owner=request.user,
								owner=request.user.pk,
								content_type=str(content_type),
								shared_link=str(shared_link),
								title=str(request.POST.get("title")),
								description=str(request.POST.get("description")),
								tags=str(request.POST.get("tags"))
							).save()

							messages.success(request, "Successfully shared your post!")
							#return HttpResponseRedirect(reverse("view_content"))
							return HttpResponseRedirect(reverse("upload"))
						else:
							messages.warning(request, "The Embed does not bellong to Spotify!")
							return HttpResponseRedirect(reverse("upload"))
					else:
						messages.error(request, "Sorry the social media link for Spotify is invalid!")
						return HttpResponseRedirect(reverse("upload"))
				else:
					messages.error(request, "Please place Spotify's Embed Code in the field and nothing else. Check the Share Options.")
					return HttpResponseRedirect(reverse("upload"))
		
		# If the the content type doesn't match the options available (Reload the page)
		else:
			messages.error(request, "Sorry failed to find the content type you choose!")
			return HttpResponseRedirect(reverse("upload"))

	elif request.method == "GET":
		return render(request, "teeker/site_templates/upload.html")


@login_required
def inbox_page(request):
	"""Show the user notifications of their account"""

	if request.method == "GET":

		return render(request, "teeker/site_templates/inbox.html")


def support_page(request):
	"""Used to send messages to the Teeker Team"""

	if request.method == "POST":

		if not request.POST.get("name"):
			messages.warning(request, "Missing full name! Please provide your full name.")
			return HttpResponseRedirect(reverse("support_page"))
		elif not request.POST.get("email"):
			messages.warning(request, "Missing e-mail Address! Please provide your E-mail Address.")
			return HttpResponseRedirect(reverse("support_page"))
		elif not request.POST.get("report_type"):
			messages.warning(request, "Missing report type! Please select the report type.")
			return HttpResponseRedirect(reverse("support_page"))
		elif not request.POST.get("msg"):
			messages.warning(request, "Missing report message! Please provide the detailed message of your report.")
			return HttpResponseRedirect(reverse("support_page"))
		else:
			print(f"Full Name: {request.POST.get('name')}")
			print(f"E-mail Address: {request.POST.get('email')}")
			print(f"Report Type: {request.POST.get('report_type')}")
			print(f"Report Message: {request.POST.get('msg')}")

			messages.success(request, "Successfully submitted your report! We'll reply to you in 2-7 business days.")
			return HttpResponseRedirect(reverse("support_page"))

	elif request.method == "GET":
		return render(request, "teeker/site_templates/support.html")


@login_required
def settings_page(request, option=None):
	"""Displays the account settings and allows for changes to the account"""

	if request.method == "POST":

		# For uploading profile picture
		if option == "npp":

			try:
				if not request.FILES["npp"]:
					messages.warning(request, "Missing the new profile picture!")
					return HttpResponseRedirect(reverse("settings_page"))
				else:
					
					uploaded_image = Image.open(request.FILES['npp'])

					# Make sure the image is an allowed format
					if uploaded_image.format.lower() in ["jpeg", "png"]:

						# Remove the EXIF from the images due to Privacy Policies
						# EXIF is a risk to the user (DO NOT REMOVE THIS FUNCTION)
						image_data = list(uploaded_image.getdata())
						image_n_exif = Image.new(uploaded_image.mode, uploaded_image.size)
						image_n_exif.putdata(image_data)
						image_file_name = "pic"+str(time.localtime().tm_sec)+str(time.localtime().tm_min)+str(time.localtime().tm_hour)+"."+str(uploaded_image.format.lower())
						image_io = BytesIO()
						image_n_exif.save(image_io, uploaded_image.format, quality=85)

						# Check the image size and make sure its not larger then 2Mbs
						byte_size = int(image_io.tell() / 1024)
						if byte_size <= 2000:

							# Upload it to Google Drive and Store the path on the Database
							user = User.objects.get(pk=request.user.pk)

							# Check if the user already has a profile picture and delete it
							if user.profile.profile_picture:
								user.profile.profile_picture.delete()

							user.profile.profile_picture = File(image_io, name=image_file_name)
							user.save()

							messages.success(request, "Successfully uploaded the new profile picture!")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "Image is larger then 2Mbs! Please upload a smaller one.")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "Image format not allowed! (PNG or JPEG only)")
						return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E0 NPP. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))

		# For uploading banner picture
		elif option == "nbp":

			try:
				if not request.FILES["nbp"]:
					messages.warning(request, "Missing the new banner picture!")
					return HttpResponseRedirect(reverse("settings_page"))
				else:
					
					uploaded_image = Image.open(request.FILES['nbp'])

					# Make sure the image is an allowed format
					if uploaded_image.format.lower() in ["jpeg", "png"]:

						# Remove the EXIF from the images due to Privacy Policies
						# EXIF is a risk to the user (DO NOT REMOVE THIS FUNCTION)
						image_data = list(uploaded_image.getdata())
						image_n_exif = Image.new(uploaded_image.mode, uploaded_image.size)
						image_n_exif.putdata(image_data)
						image_file_name = "pic"+str(time.localtime().tm_sec)+str(time.localtime().tm_min)+str(time.localtime().tm_hour)+"."+str(uploaded_image.format.lower())
						image_io = BytesIO()
						image_n_exif.save(image_io, uploaded_image.format, quality=85)

						# Check the image size and make sure its not larger then 2Mbs
						byte_size = int(image_io.tell() / 1024)
						if byte_size <= 2000:
							
							# Upload it to Google Drive and Store the path on the Database
							user = User.objects.get(pk=request.user.pk)

							# Check if the user already has a banner picture and delete it
							if user.profile.profile_picture:
								user.profile.profile_picture.delete()

							user.profile.banner_picture = File(image_io, name=image_file_name)
							user.save()

							messages.success(request, "Successfully uploaded the new banner picture!")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "Image is larger then 2Mbs! Please upload a smaller one.")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "Image format not allowed! (PNG or JPEG only)")
						return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E1 NBP. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))

		# For updating account details
		elif option == "updatedetails":

			try:
				# Change the username of the account
				if request.POST.get("nusername"):
					if not request.user.is_superuser:
						if len(request.POST.get("nusername")) >= 5 and len(request.POST.get("nusername")) <= 1600:
							try:
								user = User.objects.get(username=str(request.POST.get("nusername")))
								if user:
									messages.warning(request, f"{request.POST.get('nusername')} is already being used.")
									return HttpResponseRedirect(reverse("settings_page"))
							except User.DoesNotExist:
								user = User.objects.get(pk=request.user.pk)
								user.username = str(request.POST.get("nusername"))
								user.save()
								messages.success(request, f"Successfully changed the username to {request.POST.get('nusername')}")
								return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "Username does not meet our requirements!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "YOU CANNOT CHANGE USERNAME!")
						return HttpResponseRedirect(reverse("settings_page"))

				# Change the first name of the account
				elif request.POST.get("nfirstname"):
					if not request.user.is_superuser:
						if len(request.POST.get("nfirstname")) >= 1 and len(request.POST.get("nfirstname")) <= 1600:
							user = User.objects.get(pk=request.user.pk)
							user.first_name = str(request.POST.get("nfirstname"))
							user.save()
							messages.success(request, f"Successfully changed your First name to {request.POST.get('nfirstname')}")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "First name does not meet our requirements!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "YOU CANNOT CHANGE FIRST NAME!")
						return HttpResponseRedirect(reverse("settings_page"))

				# Change the last name of the account
				elif request.POST.get("nlastname"):
					if not request.user.is_superuser:
						if len(request.POST.get("nlastname")) >= 1 and len(request.POST.get("nlastname")) <= 1600:
							user = User.objects.get(pk=request.user.pk)
							user.last_name = str(request.POST.get("nlastname"))
							user.save()
							messages.success(request, f"Successfully changed your Last name to {request.POST.get('nlastname')}")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "Last name does not meet our requirements!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "YOU CANNOT CHANGE LAST NAME!")
						return HttpResponseRedirect(reverse("settings_page"))

				# Change the about me of the account
				elif request.POST.get("naboutme"):
					if not request.user.is_superuser:
						if len(request.POST.get("naboutme")) >= 1 and len(request.POST.get("naboutme")) <= 1600:
							user = User.objects.get(pk=request.user.pk)
							user.profile.aboutme = str(request.POST.get("naboutme"))
							user.save()
							messages.success(request, f"Successfully changed your About me to {request.POST.get('naboutme')}")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "About me does not meet our requirements!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "YOU CANNOT CHANGE ABOUT ME!")
						return HttpResponseRedirect(reverse("settings_page"))

				else:
					messages.warning(request, "Nothing updated.")
					return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E2 UD. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))

		# For removing the social links
		elif option == "removesocial":
			try:
				if request.POST.get("social_media_id"):
					user = User.objects.get(pk=request.user.pk)
					
					try:
						current_socialmedialinks = json.loads(user.profile.socialmedialinks)
					except json.JSONDecodeError:
						return JsonResponse({"STATUS": True})

					# Find and delete the social link from the user's JSON
					for a in range(len(current_socialmedialinks)):
						if current_socialmedialinks[a]["id"] == int(request.POST.get("social_media_id")):
							del current_socialmedialinks[a]
							
					user.profile.socialmedialinks = json.dumps(current_socialmedialinks)
					user.save()
					return JsonResponse({"STATUS": True})
				else:
					return JsonResponse({"STATUS": False})
			except KeyError:
				return JsonResponse({"STATUS": False})

		# For adding social media links
		elif option == "addsocial":
			try:
				if not request.POST.get("sociallink"):
					messages.warning(request, "Missing a Social Media Link to add!")
					return HttpResponseRedirect(reverse("settings_page"))
				else:

					# Open the file containing a JSON of allowed social media links
					with open(os.getcwd()+"/tools/social_media.json") as f:
						allowed_social_media = json.loads(f.read())

					result = re.match("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", request.POST.get('sociallink'))
					result = re.match('https?://([A-Za-z_0-9.-]+).*', result[0])
					
					for a in allowed_social_media:
						if a["social_media_link"] in result.group(1):
							user = User.objects.get(pk=request.user.pk)

							# Check if the user already has social media links
							try:
								users_current_links = json.loads(user.profile.socialmedialinks)

								# Check if the limit of social links has been reached
								if len(users_current_links) >= 16:
									messages.warning(request, "You have reached the limit of how many Social media links you can have!")
									return HttpResponseRedirect(reverse("settings_page"))

							except json.JSONDecodeError:
								users_current_links = []

							social_link_id = 1
							for b in range(len(users_current_links)):
								social_link_id += b + 1
							
							users_current_links.append({
								"id": social_link_id,
								"social_icon": a["social_media_icon"],
								"social_media_link": str(request.POST.get('sociallink'))
							})

							# Save the link to the users profile
							user.profile.socialmedialinks = json.dumps(users_current_links)
							user.save()

							messages.success(request, "Successfully added social link!")
							return HttpResponseRedirect(reverse("settings_page"))

					messages.warning(request, "The link you are trying to add is not allowed!")
					return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E3 AS. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))
		
		# For changing the account password
		elif option == "updatepwd":

			try:
				if not request.POST.get("opwd"):
					messages.warning(request, "Missing old password!")
					return HttpResponseRedirect(reverse("settings_page"))
				elif not request.POST.get("npwd"):
					messages.warning(request, "Missing new password!")
					return HttpResponseRedirect(reverse("settings_page"))
				elif not request.POST.get("cpwd"):
					messages.warning(request, "Missing confirm password!")
					return HttpResponseRedirect(reverse("settings_page"))
				else:

					# Check if the old password is the password currently being used by the account
					if request.user.check_password(str(request.POST.get("opwd"))):
						
						# Check if the new password meets requirements
						if str(request.POST.get("npwd")) == str(request.POST.get("cpwd")):
							
							# Check if the password lengths are good
							if len(str(request.POST.get("cpwd"))) >= 8 and len(str(request.POST.get("cpwd"))) <= 128:

								# Update the Users password
								user = User.objects.get(pk=request.user.pk)
								user.set_password(str(request.POST.get("cpwd")))
								user.save()

								# Log user back in
								user = authenticate(request, username=request.user.username, password=str(request.POST.get("cpwd")))
								login(request, user)

								messages.success(request, "Successfully update the password!")
								return HttpResponseRedirect(reverse("settings_page"))

							else:
								if len(str(request.POST.get("cpwd"))) < 8:
									messages.warning(request, "New password is less then 8 characters! Make it more longer, but not longer then 128.")
								elif len(str(request.POST.get("cpwd"))) > 128:
									messages.warning(request, "New password is greater then 128 characters! Make it less, but not lesser then 8.")
								return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "New password and Confirm password do not match!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "Wrong password! Please enter the old account password.")
						return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E4 UPWD. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))

		# For changing the account e-mail address
		elif option == "cemail":

			try:
				if not request.POST.get("email"):
					messages.warning(request, "Missing e-mail address to change to!")
					return HttpResponseRedirect(reverse("settings_page"))
				elif not request.POST.get("cpwd"):
					messages.warning(request, "Missing password to confirm and approve the change of e-mail address!")
					return HttpResponseRedirect(reverse("settings_page"))
				else:

					# Check if the password provided is valid
					if request.user.check_password(str(request.POST.get("cpwd"))):
						
						# Check if the account is not a superuser
						if not request.user.is_superuser:

							# Change the e-mail address
							user = User.objects.get(pk=request.user.pk)
							user.email = str(request.POST.get("email"))
							user.save()
							messages.success(request, "Successfully changed the account e-mail address!")
							return HttpResponseRedirect(reverse("settings_page"))
						else:
							messages.warning(request, "YOU ARE NOT ALLOWED TO CHANGE THIS ACCOUNTS E-MAIL ADDRESS!")
							return HttpResponseRedirect(reverse("settings_page"))
					else:
						messages.warning(request, "Wrong password! Please provide the password of the account.")
						return HttpResponseRedirect(reverse("settings_page"))
			except KeyError:
				messages.error(request, "SETTINGS PAGE ERROR: E5 CEM. Try again...")
				return HttpResponseRedirect(reverse("settings_page"))

		# For the toggle switches
		elif option == "toggle":
			
			try:
				# Know which switch has been toggle
				if request.POST.get("toggle_switch") == "formCheck-2":
					if request.POST.get('switch') == "true":
						user = User.objects.get(pk=request.user.pk)
						user.profile.newsletter = True
						user.save()
					elif request.POST.get('switch') == "false":
						user = User.objects.get(pk=request.user.pk)
						user.profile.newsletter = False
						user.save()
					return JsonResponse({"STATUS": True})
				
				elif request.POST.get("toggle_switch") == "formCheck-3":
					if request.POST.get('switch') == "true":
						user = User.objects.get(pk=request.user.pk)
						user.profile.browser_notifications = True
						user.save()
					elif request.POST.get('switch') == "false":
						user = User.objects.get(pk=request.user.pk)
						user.profile.browser_notifications = False
						user.save()
					return JsonResponse({"STATUS": True})
			except KeyError:
				return JsonResponse({"STATUS": False})
		
		# Handle empty option
		else:
			messages.error(request, "SETTINGS PAGE ERROR: EXXX. Try again...")
			return HttpResponseRedirect(reverse("settings_page"))

	elif request.method == "GET":
		
		# Get the social links the user has
		try:
			socialmedialinks = json.loads(request.user.profile.socialmedialinks)
		except json.JSONDecodeError:
			socialmedialinks = ""

		html_content = {
			"socialmedialinks": socialmedialinks
		}

		return render(request, "teeker/site_templates/settings.html", html_content)


def termsandconditions(request):
	"""Shows the Terms and Conditions of the website."""

	if request.method == "GET":
		return render(request, "teeker/site_templates/termsandconditions.html")


# LEVEL 0
# From here on its all LEVEL 0 pages
@login_required
@staff_member_required
def level0_users(request):
	"""View all the users on the App"""

	if request.method == "GET":

		if request.GET.get("search"):
			
			form = Level0SearchUsers(request.GET)

			# Check if the form is valid
			if form.is_valid():
				users_data = User.objects.filter(
					Q(pk__contains=form.cleaned_data["search"]) | Q(username__contains=form.cleaned_data["search"]) | Q(email__contains=form.cleaned_data["search"])
					)

				# Add users return from the database to the content_data for the HTML template
				if users_data:
					content_data = {
						"users": users_data,
						"n_users": len(users_data)
					}
				else:
					content_data = {
						"users": None,
						"n_users": 0
					}

				# Notify the user of how many results came out
				if len(users_data) == 1:
					messages.success(request, f"Found {len(users_data)} user")
				else:
					messages.success(request, f"Found {len(users_data)} users")
			else:
				# Check if any errors were returned
				if form.errors.get_json_data():
					try:
						# Check if the error return has the 'search' details of why it's invalid
						if form.errors.get_json_data()["search"] and form.errors.get_json_data()["search"][0]["code"] in ["required", "max_length", "min_length"]:
							messages.warning(request, f"{form.errors.get_json_data()['search'][0]['message']}")
						elif form.errors.get_json_data()["search"]:
							messages.warning(request, "Search value is invalid! Please try another one...")
					except KeyError:
						messages.error(request, "Form error 'search' cannot be found!")
				else:
					messages.error(request, "Search form invalid with no errors...")
				
				# Set all values to empty
				content_data = {
					"users": None,
					"n_users": 0
				}

		else:
			users_data = User.objects.all()

			# Add users return from the database to the content_data for the HTML template
			if users_data:
				content_data = {
					"users": users_data,
					"n_users": len(users_data)
				}
			else:
				content_data = {
					"users": None,
					"n_users": 0
				}

		return render(request, "teeker/site_templates/level0/users.html", content_data)


@login_required
@staff_member_required
def level0_users_view(request, option=None):
	"""View details of a certain user that was selected and allow changes to be made"""

	if request.method == "POST":
		
		# Check if the user ID is present
		if request.POST.get("user"):
			
			# Check if the user ID is a digit
			if request.POST.get("user").isdigit():
				
				# Change the user's Profile Picture
				if option == "newpp":
					
					# Validate the users input
					form = UploadProfilePictures(request.POST, request.FILES)

					if form.is_valid():
						if not form.cleaned_data["npp"]:
							messages.warning(request, "Missing the new profile picture!")
							return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
						else:
							
							uploaded_image = Image.open(form.cleaned_data["npp"])

							# Make sure the image is an allowed format
							if uploaded_image.format.lower() in ["jpeg", "png"]:

								# Remove the EXIF from the images due to Privacy Policies
								# EXIF is a risk to the user (DO NOT REMOVE THIS FUNCTION)
								image_data = list(uploaded_image.getdata())
								image_n_exif = Image.new(uploaded_image.mode, uploaded_image.size)
								image_n_exif.putdata(image_data)
								image_file_name = "pic"+str(time.localtime().tm_sec)+str(time.localtime().tm_min)+str(time.localtime().tm_hour)+"."+str(uploaded_image.format.lower())
								image_io = BytesIO()
								image_n_exif.save(image_io, uploaded_image.format, quality=85)

								# Check the image size and make sure its not larger then 2Mbs
								byte_size = int(image_io.tell() / 1024)
								if byte_size <= 2000:

									# Upload it to Google Drive and Store the path on the Database
									try:
										user = User.objects.get(pk=int(request.POST.get("user")))
									except User.DoesNotExist:
										messages.error(request, "User does not exist!")
										return HttpResponseRedirect(reverse("level0_users"))

									# Check if the user already has a profile picture and delete it
									if user.profile.profile_picture:
										user.profile.profile_picture.delete()

									user.profile.profile_picture = File(image_io, name=image_file_name)
									user.save()

									messages.success(request, "Successfully uploaded the new profile picture!")
									return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
								else:
									messages.warning(request, "The image file is too big! Try a smaller sized image...")
									return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
							else:
								messages.warning(request, "Image format not allowed! (PNG or JPEG only)")
								return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
					else:
						messages.warning(request, "Invalid File input! Try again...")
						return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
				
				# Change the user's Banner Picture
				elif option == "newbp":
					
					# Validate the users input
					form = UploadBannerPictures(request.POST, request.FILES)

					# Check if the form is valid
					if form.is_valid():
						if not form.cleaned_data["nbp"]:
							messages.warning(request, "Missing the new profile picture!")
							return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
						else:
							
							uploaded_image = Image.open(form.cleaned_data["nbp"])

							# Make sure the image is an allowed format
							if uploaded_image.format.lower() in ["jpeg", "png"]:

								# Remove the EXIF from the images due to Privacy Policies
								# EXIF is a risk to the user (DO NOT REMOVE THIS FUNCTION)
								image_data = list(uploaded_image.getdata())
								image_n_exif = Image.new(uploaded_image.mode, uploaded_image.size)
								image_n_exif.putdata(image_data)
								image_file_name = "pic"+str(time.localtime().tm_sec)+str(time.localtime().tm_min)+str(time.localtime().tm_hour)+"."+str(uploaded_image.format.lower())
								image_io = BytesIO()
								image_n_exif.save(image_io, uploaded_image.format, quality=85)

								# Check the image size and make sure its not larger then 2Mbs
								byte_size = int(image_io.tell() / 1024)
								if byte_size <= 2000:

									# Upload it to Google Drive and Store the path on the Database
									try:
										user = User.objects.get(pk=int(request.POST.get("user")))
									except User.DoesNotExist:
										messages.error(request, "User does not exist!")
										return HttpResponseRedirect(reverse("level0_users"))

									# Check if the user already has a profile picture and delete it
									if user.profile.banner_picture:
										user.profile.banner_picture.delete()

									user.profile.banner_picture = File(image_io, name=image_file_name)
									user.save()

									messages.success(request, "Successfully uploaded the new profile picture!")
									return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
								else:
									messages.warning(request, "The image file is too big! Try a smaller sized image...")
									return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
							else:
								messages.warning(request, "Image format not allowed! (PNG or JPEG only)")
								return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
					else:
						messages.warning(request, "Invalid File input! Try again...")
						return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")

				elif option == "eacc":

					# Validate the users input
					form = Level0UpdateUserDetails(request.POST)

					# Check if the inputs pass validation
					if form.is_valid():

						# Update the user's datails
						try:
							user = User.objects.get(pk=int(request.POST.get("user")))
						except User.DoesNotExist:
							messages.error(request, "User does not exist!")
							return HttpResponseRedirect(reverse("level0_users"))

						# Make sure not to be able to edit Superuser account
						if user.is_superuser:
							messages.error(request, "You are not allowed to modify this user!")
							return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
						else:

							# If any changes have been made the status will change to True
							changes_make = False

							# Update the username if it's different
							if user.username != form.cleaned_data["username"]:
								user.username = form.cleaned_data["username"]
								changes_make = True

							# Update the First name if it's different
							if user.first_name != form.cleaned_data["firstname"]:
								user.first_name = form.cleaned_data["firstname"]
								changes_make = True

							# Update the Last name if it's different
							if user.last_name != form.cleaned_data["lastname"]:
								user.last_name = form.cleaned_data["lastname"]
								changes_make = True

							# Update the E-mail address if it's different
							if user.email != form.cleaned_data["email"]:
								user.email = form.cleaned_data["email"]
								changes_make = True

							# Update the About me if it's different
							if user.profile.aboutme != form.cleaned_data["aboutme"]:
								user.profile.aboutme = form.cleaned_data["aboutme"]
								changes_make = True

							if changes_make:
								# Save all the changes to the user's details
								user.save()
								messages.success(request, "Successfully updated account details!")
							else:
								messages.warning(request, "No changes have been made to the account!")
								
						return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
					else:

						# Choose the right error message
						if form.errors.get_json_data():
							
							# Catch KeyError for username
							try:
								# Check if the error is the username
								if form.errors.get_json_data()["username"] and form.errors.get_json_data()["username"][0]["code"] in ["required", "max_length", "min_length"]:
									messages.warning(request, f"{form.errors.get_json_data()['username'][0]['message']}")
								elif form.errors.get_json_data()["username"]:
									messages.warning(request, "Username is invalid! Please try another one...")
							except KeyError:
								print("""Username is cleared and passed validation""")

							# Catch KeyError for First name
							try:
								# Check if the error is the First name
								if form.errors.get_json_data()["firstname"] and form.errors.get_json_data()["firstname"][0]["code"] in ["required", "max_length", "min_length"]:
									messages.warning(request, f"{form.errors.get_json_data()['firstname'][0]['message']}")
								elif form.errors.get_json_data()["firstname"]:
									messages.warning(request, "First name is invalid! Please try another one...")
							except KeyError:
								print("""First name is cleared and passed validation""")

							# Catch KeyError for Last name
							try:
								# Check if the error is the Last name
								if form.errors.get_json_data()["lastname"] and form.errors.get_json_data()["lastname"][0]["code"] in ["required", "max_length", "min_length"]:
									messages.warning(request, f"{form.errors.get_json_data()['lastname'][0]['message']}")
								elif form.errors.get_json_data()["lastname"]:
									messages.warning(request, "Last name is invalid! Please try another one...")
							except KeyError:
								print("""Last name is cleared and passed validation""")

							# Catch KeyError for E-mail address
							try:
								# Check if the error is the E-mail address
								if form.errors.get_json_data()["email"] and form.errors.get_json_data()["email"][0]["code"] in ["required", "max_length", "min_length"]:
									messages.warning(request, f"{form.errors.get_json_data()['email'][0]['message']}")
								elif form.errors.get_json_data()["email"]:
									messages.warning(request, "E-mail address is invalid! Please try another one...")
							except KeyError:
								print("""E-mail address is cleared and passed validation""")

							# Catch KeyError for About me
							try:
								# Check if the error is the About me
								if form.errors.get_json_data()["aboutme"] and form.errors.get_json_data()["aboutme"][0]["code"] in ["required", "max_length", "min_length"]:
									messages.warning(request, f"{form.errors.get_json_data()['aboutme'][0]['message']}")
								elif form.errors.get_json_data()["aboutme"]:
									messages.warning(request, "About me is invalid! Please try another one...")
							except KeyError:
								print("""About me is cleared and passed validation""")
						else:
							messages.warning(request, "Invalid form. Try again...")

						return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
				else:
					messages.error(request, "Invalid option! Try again...")
					return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/level0/users")
			else:
				messages.error(request, "Invalid user ID! Try again...")
				return HttpResponseRedirect(reverse("level0_users"))
		else:
			messages.error(request, "Missing user ID to update Profile/Banner picture! Try again...")
			return HttpResponseRedirect(reverse("level0_users"))

	elif request.method == "GET":

		# Check if the ID of the user is present
		if request.GET.get("u"):

			# Check if the ID is a digit
			if request.GET.get("u").isdigit():

				# Check if the user exists in the Databse
				try:
					# Get the user's Data from the Database
					user_data = User.objects.get(pk=int(request.GET.get("u")))
					content_data = {
						"user_data": user_data
					}
					return render(request, "teeker/site_templates/level0/users/viewuser.html", content_data)

				except User.DoesNotExist:
					messages.warning(request, "User does not exits!")
					return HttpResponseRedirect(reverse("level0_users"))
			else:
				messages.error(request, "User ID is invalid!")
				return HttpResponseRedirect(reverse("level0_users"))
		else:
			messages.error(request, "Missing the user ID to view the account!")
			return HttpResponseRedirect(reverse("level0_users"))


@login_required
@staff_member_required
def level0_users_content(request):
	"""Shows all the content of the App"""

	if request.method == "GET":

		content_data = Content.objects.all()

		html_data = {
			"content_data": content_data,
			"n_content": len(content_data)
		}

		return render(request, "teeker/site_templates/level0/content.html", html_data)
