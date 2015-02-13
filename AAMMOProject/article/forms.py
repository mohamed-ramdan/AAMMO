from django import forms


class UploadImageForm(forms.Form):
	"""Image upload form."""
	image = forms.ImageField()