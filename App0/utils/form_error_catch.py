# This will look through the validation form and find the error messages
from django.contrib import messages

def form_error_catcher(request, form, array_list=[], extra_tags=None):
	""" Requires the ``form`` to be present and a ``list`` of input variable names to look for """

	for _inputs in array_list:
		try:
			# Check if the error return has the '_inputs' details of why it's invalid
			if form.errors.get_json_data()[_inputs] and form.errors.get_json_data()[_inputs][0]["code"] in ["required", "max_length", "min_length", "invalid"]:
				messages.error(request, f"{form.errors.get_json_data()[_inputs][0]['message']}", extra_tags=extra_tags)
			elif form.errors.get_json_data()[_inputs]:
				messages.error(request, form.errors.get_json_data()[_inputs][0]["message"], extra_tags=extra_tags)
		except KeyError:
			print(f"Form validation error '{_inputs}' cannot be found!")
