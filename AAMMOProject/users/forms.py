from captcha.fields import CaptchaField
from django import forms

from users.models import Users


class RegisterForm(forms.Form):
	"""
	This is the class that defines a register form for the user. It will appear in a separate page when the user
	clicks on the registration button.
	"""

	# The username field for the login form.
	user_name = forms.CharField(
		label="Enter user name",
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Enter username here ...'}),
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
		help_text="Maximum: 4 Mb",
		required=False,
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
			return image

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

	def clean_user_email(self):
		"""
		This function checks whether the email is duplicated or not. If it is, it raises an exception for the form to
		handle; the user must enter another email.
		:return: Returns the cleaned data on success or throws an exception if the data is duplicated.
		"""

		filled_user_email = self.cleaned_data['user_email']

		try:
			# Query the database with the filled user email.
			Users.objects.get(user_email=filled_user_email)
		except Users.DoesNotExist:
			found_email = False
		else:
			found_email = True

		# The email is duplicated. Raise validation error.
		if found_email:
			raise forms.ValidationError("The email is already in use! Please choose another one.")
		else:
			return filled_user_email


class EditForm(forms.Form):
	"""
	This form edits the user's information. It can only edit the user name, email, image
	"""
	# The username field for the login form.
	user_name = forms.CharField(
		label="Enter user name",
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Enter username here ...'}),
		required=False
	)

	# The email field for the login form.
	user_email = forms.EmailField(
		label="Enter your email",
		max_length=200,
		widget=forms.EmailInput(attrs={'placeholder': 'Enter email here ...'}),
		required=False
	)

	# The image selection field for the login form.
	user_image = forms.ImageField(
		label="Choose your profile picture",
		help_text="Maximum: 4 Mb",
		required=False
	)


class RecoverPasswordForm(forms.Form):
	"""
	This form is for when the user forgets his/her password. A new password is generated and sent to the user via the
	email supplied in this form.
	"""

	# The email field for the login form.
	user_email = forms.EmailField(
		label="Enter your email",
		max_length=200,
		widget=forms.EmailInput(attrs={'placeholder': 'Enter email here ...'})
	)

	def clean_user_email(self):
		"""
		This function checks that the email is actually in the database; that iit actually belongs to an existing
		user. It will validate error if it doesn't find it.
		:return:
		"""

		# Get the email that the user submitted in the form.
		user_email = self.cleaned_data['user_email']

		try:
			Users.objects.get(user_email=user_email)
			return user_email
		except Users.DoesNotExist:
			raise forms.ValidationError("The email does not exist! Make sure you have entered correctly")