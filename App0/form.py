from django.core.validators import RegexValidator, validate_email
from django import forms

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

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
