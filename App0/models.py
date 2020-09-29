from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Google Storage
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.

class Profile(models.Model):
	"""To store additional information about user"""

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	aboutme = models.TextField(max_length=1600, default="")
	profile_picture = models.ImageField(upload_to="static/teeker/assets/uploads", storage=gd_storage, default="/static/teeker/assets/default_img/avatar/avataaar.png", blank=True, null=True)
	banner_picture = models.ImageField(upload_to="static/teeker/assets/uploads", storage=gd_storage, default="/static/teeker/assets/default_img/banner/banner1.png", blank=True, null=True)
	suspended = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)
	developer = models.BooleanField(default=False)
	founder = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=True)
	browser_notifications = models.BooleanField(default=False)
	socialmedialinks = models.TextField(default="", blank=True, null=True)
	recommended = models.TextField(default="", blank=True, null=True)
	user_chasing = models.TextField(default="", blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Content(models.Model):
	"""Content details"""
	
	content_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
	owner = models.BigIntegerField(null=False)
	content_type = models.CharField(max_length=600, null=False)
	shared_link = models.CharField(max_length=6000, null=False)
	title = models.CharField(max_length=1200, null=False)
	description = models.TextField(max_length=3200, null=False)
	tags = models.TextField(max_length=1600)
	status = models.CharField(max_length=2, default="PB")
	suspended = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"""
		Content Type: {self.content_type}
		Shared Link: {self.shared_link}
		Title: {self.title}
		Description: {self.description}
		Tags: {self.tags}
		Status: {self.status}
		Suspended: {self.suspended}
		Date Shared: {self.date}"""

class History(models.Model):
	"""Keeps track of users interactions with Content"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_history")
	content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="contents_history")
	vote = models.IntegerField(null=True)

	def __str__(self):
		return f"""
		User: {self.user}
		Content: {self.content}
		Vote: {self.vote}"""

class Comment(models.Model):
	"""Keeps track of all the content comments"""

	content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="content_comments")
	comment = models.TextField(max_length=999999, null=False)

	def __str__(self):
		return f"""
		Content: {self.content}
		Comment: {self.comment}
		"""
	
class ReportContent(models.Model):
	"""Holds all the reported content by user's"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_owner")
	content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="content_reported")
	reason = models.CharField(max_length=1600, null=False)

	
