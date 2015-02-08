from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
	"""
	This is the class that defines a login form for the user. It will appear in the header as a drop down menu only
	when the user is not logged in.
	"""

	# The username field for the login form.
	user_name = forms.CharField(
		label="Enter user name: ",
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Enter username here ...'})
	)

	# The email field for the login form.
	user_email = forms.EmailField(
		label="Enter your email: ",
		max_length=200,
		widget=forms.EmailInput(attrs={'placeholder': 'Enter email here ...'})
	)

	# The password field for the login form
	user_password = forms.CharField(
		label="Enter your password: ",
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here ...'})
	)

	# The password confirmation field for the login form.
	user_password_confirm = forms.CharField(
		label="Enter your password: ",
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password here ...'})
	)

	# The image selection field for the login form.
	user_image = forms.ImageField(
		label="Choose your profile picture: "
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


class LoginForm(forms.Form):
	"""
	This is the class that defines a login form for the user. It will appear in the header as a drop down menu only
	when the user is not logged in.
	"""

	# The username field for the login form.
	user_name = forms.CharField(
		label="Enter user name: ",
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Enter username here ...'})
	)

	# The password field for the login form
	user_password = forms.CharField(
		label="Enter your password: ",
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here ...'})
	)