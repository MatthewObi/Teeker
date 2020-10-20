from django.core.validators import RegexValidator, validate_email
from django import forms

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

# Used for the Login Page
#---------------------------------------
class LoginForm(forms.Form):
	"""Login Form to validate the login credentials"""

	cdinput = forms.CharField(
		max_length=128,
		min_length=3,
		required=True,
		help_text="Used to check the username/email",
		error_messages={
			"required": "Username/E-mail is required to login.",
			"max_length": "Username/E-mail is too long...",
			"min_length": "Username/E-mail is too short...",
			"invalid": "Username/E-mail is invalid!"
		}
	)

	pwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Used to check if the password matches the user's password",
		error_messages={
			"required": "Password is required to login.",
			"max_length": "Password is too long...",
			"min_length": "Password is too short...",
			"invalid": "Password is invalid!"
		}
	)
#---------------------------------------

# Used for Emailing Code Page
#---------------------------------------
class EmailCodeForm(forms.Form):
	"""Email validation for Emailing recovery code"""

	email = forms.EmailField(
		required=True,
		help_text="Email address needs to be provided",
		label="E-mail address recovery code",
		validators=[validate_email],
		error_messages={
			"required": "E-mail address is required!",
			"invalid": "There's something wrong with that e-mail address!"
		}
	)
#---------------------------------------

# Used for the Register Page
#---------------------------------------
class RegisterForm(forms.Form):
	"""Used to validate the register form for when a user is registering"""

	username = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="Username needs to be longer then 2 char or less then 1600",
		label="Username",
		error_messages={
			"required": "Username is missing... Please add a username.",
			"min_length": "Username is too short.. Please make it longer.",
			"max_length": "Username is too long... Please make it shorter.",
			"invalid": "Username cannot be used! Try another one."
		}
	)

	firstname = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="First name needs to be longer then 2 char or less then 1600",
		label="First name",
		error_messages={
			"required": "First name is missing... Please add a First name.",
			"min_length": "First name is too short.. Please make it longer.",
			"max_length": "First name is too long... Please make it shorter.",
			"invalid": "First name cannot be used! Invalid charater/s."
		}
	)

	lastname = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="Last name needs to be longer then 2 char or less then 1600",
		label="Last name",
		error_messages={
			"required": "Last name is missing... Please add a Last name.",
			"min_length": "Last name is too short.. Please make it longer.",
			"max_length": "Last name is too long... Please make it shorter.",
			"invalid": "Last name cannot be used! Invalid charater/s."
		}
	)

	email = forms.EmailField(
		max_length=254,
		min_length=2,
		required=True,
		help_text="Email address needs to be longer then 2 and less then 254.",
		label="E-mail address",
		error_messages={
			"required": "E-mail address is missing... Please add a E-mail address.",
			"min_length": "E-mail address is too short.. Please make it longer.",
			"max_length": "E-mail address is too long... Please make it shorter.",
			"invalid": "E-mail address cannot be used! Try another one."
		},
		validators=[validate_email]
	)

	pwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		}
	)

	cpwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		}
	)

class RegisterCheckForm(forms.Form):
	"""Used to validate the Register Check form"""

	register_check = forms.BooleanField(
		required=True,
		help_text="Register Check is a boolean sent by the JavaScript",
		error_messages={
			"required": True
		}
	)

	username = forms.CharField(
		required=False,
		max_length=1600,
		min_length=2,
		help_text="Username needs to be longer then 1 char or less then 1600",
		label="Username",
		error_messages={
			"min_length": "Username is too short...  Needs to be 2 - 1200 of length",
			"max_length": "Username is too long... Needs to be 2 - 1200 of length",
			"invalid": "Username is invalid! Try another one."
		}
	)

	email = forms.EmailField(
		max_length=254,
		min_length=5,
		required=False,
		help_text="Email address needs to be longer then 5 and less then 254.",
		label="E-mail address",
		error_messages={
			"min_length": "E-mail address is too short...  Needs to be 5 - 254 of length",
			"max_length": "E-mail address is too long... Needs to be 5 - 254 of length",
			"invalid": "E-mail address is invalid! Try another one."
		},
		validators=[validate_email]
	)
#---------------------------------------

# Used for posting comments on content
#---------------------------------------
class CommentForm(forms.Form):

	content_id = forms.IntegerField(
		required=True,
		label="Content ID",
		help_text="Content ID is used to find the content the comment will go to",
		error_messages={
			"required": "Content ID is required! This is handled automatically, please refresh and re-try",
			"invalid": "The Content ID is invalid! Please refresh the page and re-try"
		}
	)

	comment = forms.CharField(
		required=True,
		max_length=1200,
		min_length=1,
		label="Comment",
		help_text="Comment is required and most be length of 1-1200",
		error_messages={
			"required": "Comment is missing... Please provide a comment.",
			"min_length": "Comment is too short! Needs to be length 1-1200.",
			"max_length": "Comment is too long! Nedds to be length 1-1200.",
			"invalid": "Comment is invalid! Please remove any special charaters."
		}
	)
#---------------------------------------

# Used for the Upload/Share forms
#---------------------------------------
class InstagramForm(forms.Form):
	"""When instagram Content being uploaded"""

	instagram_link = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the ID of the Instagram Content",
		label="Instagram Link",
		error_messages={
			"required": "Missing the Instagram Link... Please provide the link to the instagram post.",
			"max_length": "Instagram link is too long... Please provide one less then 1200.",
			"invalid": "Instagram link is invalid... Please re-try or provide a valid one."
		}
	)

	title = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the Title of the content to be shown on Teeker.",
		label="Title",
		error_messages={
			"required": "Missing the Title... Please provide a title for your content.",
			"max_length": "Title is too long... Please provide one less then 1200.",
			"invalid": "Title is invalid... Please provide one that will be valid."
		}
	)

	description = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to get the Descriptions of the content to be shown on Teeker.",
		label="Description",
		error_messages={
			"required": "Missing the Description... Please provide a description for the content.",
			"max_length": "Description is too long... Please make the description less then 1200",
			"invalid": "Description is invalid... Please check your description for any invalid characters."
		}
	)

	tags = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to keep tags that make content related together",
		label="Tags",
		error_messages={
			"required": "Tags are required!",
			"max_length": "There are too many tags. Please reduce them.",
			"invalid": "Tags are invalid!"
		}
	)

class YouTubeForm(forms.Form):
	"""When Youtube Content being uploaded"""

	youtube_link = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the ID of the Youtube Content",
		label="Youtube Link",
		error_messages={
			"required": "Missing the Youtube Link... Please provide the link to the Youtube post.",
			"max_length": "Youtube link is too long... Please provide one less then 1200.",
			"invalid": "Youtube link is invalid... Please re-try or provide a valid one."
		}
	)

	title = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the Title of the content to be shown on Teeker.",
		label="Title",
		error_messages={
			"required": "Missing the Title... Please provide a title for your content.",
			"max_length": "Title is too long... Please provide one less then 1200.",
			"invalid": "Title is invalid... Please provide one that will be valid."
		}
	)

	description = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to get the Descriptions of the content to be shown on Teeker.",
		label="Description",
		error_messages={
			"required": "Missing the Description... Please provide a description for the content.",
			"max_length": "Description is too long... Please make the description less then 1200",
			"invalid": "Description is invalid... Please check your description for any invalid characters."
		}
	)

	tags = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to keep tags that make content related together",
		label="Tags",
		error_messages={
			"required": "Tags are required!",
			"max_length": "There are too many tags. Please reduce them.",
			"invalid": "Tags are invalid!"
		}
	)

class VimeoForm(forms.Form):
	"""When Vimeo Content being uploaded"""

	vimeo_link = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the ID of the Vimeo Content",
		label="Vimeo Link",
		error_messages={
			"required": "Missing the Vimeo Link... Please provide the link to the Vimeo post.",
			"max_length": "Vimeo link is too long... Please provide one less then 1200.",
			"invalid": "Vimeo link is invalid... Please re-try or provide a valid one."
		}
	)

	title = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the Title of the content to be shown on Teeker.",
		label="Title",
		error_messages={
			"required": "Missing the Title... Please provide a title for your content.",
			"max_length": "Title is too long... Please provide one less then 1200.",
			"invalid": "Title is invalid... Please provide one that will be valid."
		}
	)

	description = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to get the Descriptions of the content to be shown on Teeker.",
		label="Description",
		error_messages={
			"required": "Missing the Description... Please provide a description for the content.",
			"max_length": "Description is too long... Please make the description less then 1200",
			"invalid": "Description is invalid... Please check your description for any invalid characters."
		}
	)

	tags = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to keep tags that make content related together",
		label="Tags",
		error_messages={
			"required": "Tags are required!",
			"max_length": "There are too many tags. Please reduce them.",
			"invalid": "Tags are invalid!"
		}
	)

class SoundCloudForm(forms.Form):
	"""When SoundCloud Content being uploaded"""

	soundcloud_link = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the ID of the SoundCloud Content",
		label="SoundCloud Link",
		error_messages={
			"required": "Missing the SoundCloud Link... Please provide the link to the SoundCloud post.",
			"max_length": "SoundCloud link is too long... Please provide one less then 1200.",
			"invalid": "SoundCloud link is invalid... Please re-try or provide a valid one."
		}
	)

	title = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the Title of the content to be shown on Teeker.",
		label="Title",
		error_messages={
			"required": "Missing the Title... Please provide a title for your content.",
			"max_length": "Title is too long... Please provide one less then 1200.",
			"invalid": "Title is invalid... Please provide one that will be valid."
		}
	)

	description = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to get the Descriptions of the content to be shown on Teeker.",
		label="Description",
		error_messages={
			"required": "Missing the Description... Please provide a description for the content.",
			"max_length": "Description is too long... Please make the description less then 1200",
			"invalid": "Description is invalid... Please check your description for any invalid characters."
		}
	)

	tags = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to keep tags that make content related together",
		label="Tags",
		error_messages={
			"required": "Tags are required!",
			"max_length": "There are too many tags. Please reduce them.",
			"invalid": "Tags are invalid!"
		}
	)

class SpotifyForm(forms.Form):
	"""When Spotify Content being uploaded"""

	spotify_link = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the ID of the Spotify Content",
		label="Spotify Link",
		error_messages={
			"required": "Missing the Spotify Link... Please provide the link to the Spotify post.",
			"max_length": "Spotify link is too long... Please provide one less then 1200.",
			"invalid": "Spotify link is invalid... Please re-try or provide a valid one."
		}
	)

	title = forms.CharField(
		max_length=1200,
		required=True,
		help_text="Used to get the Title of the content to be shown on Teeker.",
		label="Title",
		error_messages={
			"required": "Missing the Title... Please provide a title for your content.",
			"max_length": "Title is too long... Please provide one less then 1200.",
			"invalid": "Title is invalid... Please provide one that will be valid."
		}
	)

	description = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to get the Descriptions of the content to be shown on Teeker.",
		label="Description",
		error_messages={
			"required": "Missing the Description... Please provide a description for the content.",
			"max_length": "Description is too long... Please make the description less then 1200",
			"invalid": "Description is invalid... Please check your description for any invalid characters."
		}
	)

	tags = forms.CharField(
		max_length=1200,
		required=False,
		help_text="Used to keep tags that make content related together",
		label="Tags",
		error_messages={
			"required": "Tags are required!",
			"max_length": "There are too many tags. Please reduce them.",
			"invalid": "Tags are invalid!"
		}
	)
#---------------------------------------

# Used for when user's upload Pictures to the Cloud
#---------------------------------------
class UploadProfilePictures(forms.Form):
	"""Used to validate the Profile Pictures being uploaded"""

	npp = forms.FileField(
		allow_empty_file=False,
		label="Select a Profile picture.",
		help_text="Max 2MegaBytes"
	)

class UploadBannerPictures(forms.Form):
	"""Used to validate the Banner Pictures being uploaded"""

	nbp = forms.FileField(
		allow_empty_file=False,
		label="Select a Banner picture.",
		help_text="Max 2MegaBytes"
	)
#---------------------------------------

# Used for Level0 Search user Page
#---------------------------------------
class Level0SearchUsers(forms.Form):
	"""Used to validate the search value for the Level 0 user page"""

	search = forms.CharField(
		max_length=1600,
		min_length=1,
		required=True,
		help_text="Search for the user based on (ID, username or e-mail)",
		label="Search",
		error_messages={
			"required": "Search is empty... Please enter a user's (ID, username or e-mail)",
			"min_length": "Search value is too short... Needs to be at least 1 charater!",
			"max_length": "Search value is too long... Needs to be less then 1600 charaters!"
		}
	)
#---------------------------------------

# Used for Level0 Update/Change user Details
#---------------------------------------
class Level0UpdateUserDetails(forms.Form):
	"""Used to validate the updates/changes to the user's account details. For LEVEL0 use only"""

	username = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="Username needs to be longer then 1 char or less then 1600",
		label="Username",
		error_messages={
			"required": "Username is missing... Please add a username.",
			"min_length": "Username is too short.. Please make it longer.",
			"max_length": "Username is too long... Please make it shorter."
		}
	)

	firstname = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="First name needs to be longer then 2 char or less then 1600",
		label="First name",
		error_messages={
			"required": "First name is missing... Please add a First name.",
			"min_length": "First name is too short.. Please make it longer.",
			"max_length": "First name is too long... Please make it shorter."
		}
	)

	lastname = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="Last name needs to be longer then 2 char or less then 1600",
		label="Last name",
		error_messages={
			"required": "Last name is missing... Please add a Last name.",
			"min_length": "Last name is too short.. Please make it longer.",
			"max_length": "Last name is too long... Please make it shorter."
		}
	)

	email = forms.EmailField(
		max_length=254,
		min_length=2,
		required=True,
		help_text="Email address needs to be longer then 2 and less then 254.",
		label="E-mail address",
		error_messages={
			"required": "E-mail address is missing... Please add a E-mail address.",
			"min_length": "E-mail address is too short.. Please make it longer.",
			"max_length": "E-mail address is too long... Please make it shorter."
		},
		validators=[validate_email]
	)

	aboutme = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="About me needs to be longer then 2 char or less then 1600",
		label="About me",
		error_messages={
			"required": "About me is missing... Please add a About me.",
			"min_length": "About me is too short.. Please make it longer.",
			"max_length": "About me is too long... Please make it shorter."
		}
	)
#---------------------------------------

# Used for Level0 Update/Change Content Details
#---------------------------------------
class Leve0UpdateContentDetails(forms.Form):
	"""Used to validate the updates/changes to the details of the content. For LEVEL0 use only"""

	title = forms.CharField(
		max_length=1300,
		min_length=2,
		required=True,
		help_text="Title needs to be lengths 2-1200. And is required",
		label="Content Title"
	)
#---------------------------------------

# Used for Support Page
#---------------------------------------
class SupportPageForm(forms.Form):
	"""Used to validate the Support Page form"""

	name = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="name needs to be longer then 2 char or less then 1600",
		label="name",
		error_messages={
			"required": "name is missing... Please add a name.",
			"min_length": "name is too short.. Please make it longer.",
			"max_length": "name is too long... Please make it shorter.",
			"invalid": "name cannot be used! Try another one."
		}
	)

	email = forms.EmailField(
		max_length=254,
		min_length=2,
		required=True,
		help_text="Email address needs to be longer then 2 and less then 254.",
		label="E-mail address",
		error_messages={
			"required": "E-mail address is missing... Please add a E-mail address.",
			"min_length": "E-mail address is too short.. Please make it longer.",
			"max_length": "E-mail address is too long... Please make it shorter.",
			"invalid": "E-mail address cannot be used! Try another one."
		},
		validators=[validate_email]
	)

	msg = forms.CharField(
		required=True,
		max_length=1600,
		min_length=2,
		help_text="Message needs to be longer then 2 char or less then 1600",
		label="Message",
		error_messages={
			"required": "Message is missing... Please add a Message.",
			"min_length": "Message is too short.. Please make it longer.",
			"max_length": "Message is too long... Please make it shorter.",
			"invalid": "Message cannot be used! Try another one."
		}
	)

	CHOICES = (("12", "Feedback"), ("13", "Bug"), ("14", "Other"),)
	report_type = forms.ChoiceField(
		choices=CHOICES,
		required=True,
		error_messages={
			"required": "A report type is required to filter and sort your feedback to the right place",
			"invalid": "Report Type is invalid! Please select one of the options provided already."
		}
	)
#---------------------------------------
