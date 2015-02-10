from captcha.fields import CaptchaField
from django import forms
from users.models import Users


class RegisterForm(forms.Form):
	"""
	This is the class that defines a login form for the user. It will appear in the header as a drop down menu only
	when the user is not logged in.
	"""

	# The username field for the login form.
	user_name = forms.CharField(
		label="Enter user name",
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Enter username here ...'})
	)

	# The email field for the login form.
	user_email = forms.EmailField(
		label="Enter your email",
		max_length=200,
		widget=forms.EmailInput(attrs={'placeholder': 'Enter email here ...'})
	)

	# The password field for the login form
	user_password = forms.CharField(
		label="Enter your password",
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here ...'})
	)

	# The password confirmation field for the login form.
	user_password_confirm = forms.CharField(
		label="Confirm your password",
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password here ...'})
	)

	# The image selection field for the login form.
	user_image = forms.ImageField(
		label="Choose your profile picture",
		help_text="Maximum: 4 Mb"
	)

	# Create captcha field.
	user_captcha = CaptchaField()

	# clean_<field_name> method in a form class is used to do custom validation for the field. The data is inside a
	# dictionary called cleaned_data.
	def clean_user_password_confirm(self):
		"""
		This function validates the form by checking whether the two passwords match or not. If they don't an error
		is rendered back to the user.
		:return:
		"""

		# Get the two passwords from the form data.
		password1 = self.cleaned_data['user_password']
		password2 = self.cleaned_data['user_password_confirm']

		# Check if the entered passwords match
		if password1 != password2:
			raise forms.ValidationError("Entered passwords don't match!")
		else:
			return password2

	def clean_user_image(self):
		"""
		This function checks whether the image chosen is smaller than the maximum allowable size for the image.
		"""

		# The maximum allowable size for the image in bytes.
		maximum_image_size = 4 * 1024 * 1024

		# Get the chosen image element.
		image = self.cleaned_data['user_image']

		# If the image was uploaded successfully
		if image:
			# Make sure the image size is not larger than the maximum allowable size.
			if image._size > maximum_image_size:
				raise forms.ValidationError("The image exceeds maximum image size (4 Mb)!")
			else:
				return image
		else:
			raise forms.ValidationError("Could not read uploaded image! Type not supported!")

	def clean_user_name(self):
		"""
		This function checks whether the username is duplicated or not.
		:return:
		"""

		# The user's user name.
		filled_user_name = self.cleaned_data['user_name']

		try:
			# Query the database with the filled user name.
			Users.objects.get(user_name=filled_user_name)
		except Users.DoesNotExist:
			found_users = False
		else:
			found_users = True

		# The user name is duplicated. Raise validation error.
		if found_users:
			raise forms.ValidationError("The user name already exists! Please choose another one.")
		else:
			return filled_user_name