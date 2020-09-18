from django.core.validators import RegexValidator, validate_email
from django import forms

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

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

class Level0UpdateUserDetails(forms.Form):
	"""Used validate the updates/changes to the user's account details"""

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
			"required": "Last name is missing... Please add a Last name.",
			"min_length": "Last name is too short.. Please make it longer.",
			"max_length": "Last name is too long... Please make it shorter."
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
