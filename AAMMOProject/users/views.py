import random

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from AAMMOProject import settings
from users.forms import RegisterForm, RecoverPasswordForm, EditForm
from users.models import Users


def register(request):
	"""
	This function displays the registration form for the user to create a new account. If the user is already logged
	in, it displays a message that the user is already logged in. When the user clicks the submit button, it will
	process the form, validate it and send him back to the index page with logged in status as True.
	:param request: The incoming request object from the user.
	:return: A redirect to the index page or the registration form
	"""
	# The default url to return to is the same file, unless the form was correctly filled.
	route_url = 'register.html'
	# The default context is empty. Nothing should be sent if the user doesn't need the registration form.
	context = {}

	# Check for the existence of the session variable logged and set it to false if it doesn't exist. The user is
	# obviously not logged in.
	try:
		request.session['logged']
	except KeyError:
		request.session['logged'] = False

	# If the user is not logged in.
	if request.session['logged'] is False:
		# If the request method is post, then this page was loaded because the user submitted the form,
		# not just navigated to it.
		if request.method == 'POST':

			# Create the registration form object with the received data and files.
			registration_form = RegisterForm(request.POST, request.FILES)

			# The is_valid() method validates the fields of the form and returns true if they are all validated
			# correctly. It also passes the form parameters (fields) into a dictionary called cleaned_data, which you can
			# use for additional validation.
			if registration_form.is_valid() and registration_form.clean_user_password_confirm() and \
				registration_form.clean_user_image() and registration_form.clean_user_image() and \
				registration_form.clean_user_email():

					# SUCCESSFUL LOGIN
					# Create new user based on the received data and save that user to the database.
					new_user = create_user(request.POST, request.FILES)

					# Set the logged session variable to true to indicate that the user is logged in.
					request.session['logged'] = True
					request.session['username'] = new_user.user_name

					# Format: subject,body,host to use,recipients,fail_silently
					send_mail(
						'Welcome to our website!',
						'Welcome to our website '+new_user.user_name+'! We hope you enjoy it!',
						settings.EMAIL_HOST_USER,
						[new_user.user_email],
						fail_silently=False
					)

					# The URL to go to.
					route_url = '/index/'

					# Go to the index page since you successfully logged in.
					return redirect(route_url)

		# The method was GET, that means the user just navigated to the register form page.
		else:
			# Create new empty registration form.
			registration_form = RegisterForm()

		# The registration form data to the register page.
		context = {
			'register_form': registration_form,
		}

	# This displays the register page again with the defined context.
	return render(request, route_url, context)


def login(request):
	"""
	This function performs the login process. It receives a user name and password from the login form and checks the
	database against them. If the user does not exist, then an error should be returned.
	:param request: The request received from the user.
	:return:
	"""

	# The user logged in by copying the URL in the bar.
	if 'source_path' not in request.POST:
		source_path = '/index/'
		response = redirect(source_path)
	else:

		# Get source page path for redirect
		source_path = request.POST['source_path']
		response = redirect(source_path)

		# Get the username and password that the user used to log in.
		logged_username = request.POST['username']
		logged_password = request.POST['user_password']

		# The default data to send to the page is empty
		context = {}
		# The default login status is failure
		request.session['login_failure'] = True

		try:
			# Get the password for the provided user name. Throws DoesNotExist exception if user is not found.
			saved_user_password = Users.objects.get(user_name=logged_username).user_password
			# Compare passwords to check they are correct.
			is_similar = check_password(logged_password, saved_user_password)
			# If the passwords are similar, then the user has successfully logged in.
			if is_similar:
				# Set the session variable to logged.
				request.session['logged'] = True
				# Set the logged user name to the logged in username.
				request.session['username'] = logged_username
				# Delete the extra session variable.
				del request.session['login_failure']
				# If the remember me option is checked, then save a cookie with the user name of the logged user.
				if 'remember_me' in request.POST:
					response.set_cookie('logged_user', logged_username)
				else:
					response.delete_cookie('logged_user')

			# The user has not logged in successfully.
			else:
				raise Users.DoesNotExist()

		# The user didn't log in successfully.
		except Users.DoesNotExist:
			request.session['logged'] = False
			request.session['login_failure'] = True

	return response


def logout(request):
	"""
	This function performs the log out functionality of the page. It logs the user out by deleting the session and
	the user saved cookie.
	:param request: The request received from the user.
	:return: Returns the same page the user was in but without being logged on.
	"""

	if 'source_path' not in request.POST:
		source_path = '/index/'
		response = redirect(source_path)
	else:
		# Get source page path for redirect
		source_path = request.POST['source_path']

		# Set the logged session variable to false and delete username session variable.
		request.session['logged'] = False
		del request.session['username']

		# Delete the saved cookie that contains the logged user name if it exists.
		response = redirect(source_path)
		response.delete_cookie('logged_user')

	return response


def recover_password(request):
	"""
	This function displays the email form to send the logged user's forgotten password.
	:param request: The request object that the user sends
	:return: The page response.
	"""

	# Default context data
	context = {}

	# The user has filled the form and submitted it.
	if request.method == 'POST':
		# Create new form with the received request info.
		recovery_form = RecoverPasswordForm(request.POST)

		if recovery_form.is_valid():
			# Get the filled in email.
			recipient_email = request.POST['user_email']

			# Get the user that matches this user name.
			user_object = Users.objects.get(user_email=recipient_email)

			# Create new random password
			new_password = random.getrandbits(32)

			# Create new hashed password from the random password.
			new_hashed_password = make_password(new_password)

			# Update the user's password to the new generated one.
			user_object.user_password = new_hashed_password
			user_object.save()

			# Email message to send to the user.
			email_message = "This is an automatic email. Please do not reply to this address. You have requested to " \
				"change your password. Your new password is "+str(new_password)+". Login to change " \
				"your password."

			# Format: subject,body,host to use,recipients,fail_silently
			send_mail(
				'Password recovery .. Do not reply',
				email_message,
				settings.EMAIL_HOST_USER,
				[recipient_email],
				fail_silently=False
			)

			# Notify the user that the email has been sent
			context = {
				'sent_email': True
			}
		# The form was not filled correctly. Send back the validation errors.
		else:
			context = {
				'recovery_form': recovery_form
			}

	# The user has navigated to the form page. Create new recovery form.
	else:
		recovery_form = RecoverPasswordForm()
		context = {
			'recovery_form': recovery_form
		}

	return render(request, 'forgot_password.html', context)


def edit(request):
	"""
	This function handles the user information editing form submissions.
	:param request: The request object from the user.
	:return:
	"""

	# Default context
	context = {}

	# The user has filled the form itself.
	if request.method == 'POST':

		# Create new form with data received from the user.
		edit_form = EditForm(request.POST, request.FILES)

		if edit_form.is_valid():
			# Get the currently logged in user.
			current_user_name = request.session['username']

			# Get the current user object
			current_user = Users.objects.get(user_name=current_user_name)

			# Update the user's name if it was filled in the fields.
			if 'user_name' in request.POST:
				current_user.user_name = request.POST['user_name']

			# Update the user's email if it was filled in the fields.
			if 'user_email' in request.POST:
				current_user.user_email = request.POST['user_email']

			# Update the user's profile pic if it was filled in the fields.
			if 'user_image' in request.FILES:
				# Get the just uploaded image.
				user_image = request.FILES['user_image']

				# Get the image's extension
				image_extension = user_image.name.split('.')[1]

				# Assign the image a new name, with p_user_id as its name.
				user_image.name = 'p_' + str(current_user.user_id) + '.' + image_extension

				# Assign the modified image to the current user image path.
				current_user.user_image_path = user_image

			# Save updates to the current user.
			current_user.save()

			context = {
				'edit_status': True
			}

	# The user has navigated to the form. Display the empty form.
	else:
		# Create new form.
		edit_form = EditForm()

		# Add form to the context variable
		context = {
			'edit_form': edit_form
		}

	return render(request, 'edit_info.html', context)


def create_user(uploaded_data, uploaded_image):
	"""
	This function creates a new user object based on the data received from the request.
	:param uploaded_data: The request post object, that contains all the user data.
	:param uploaded_image: The request file object, that contains the uploaded file data.
	:return: The newly created user object.
	"""

	# Create the new user object.
	new_user = Users()

	# Populate the user object with the data collected from the form.
	new_user.user_name = uploaded_data['user_name']
	new_user.user_email = uploaded_data['user_email']
	new_user.user_password = make_password(uploaded_data['user_password'])

	# Save the user data without the image to get the user id.
	new_user.save()

	# Get the just saved user id.
	new_user = Users.objects.get(user_name=uploaded_data['user_name'])

	# Get the just uploaded image.
	user_image = uploaded_image['user_image']

	# Get the image's extension
	image_extension = user_image.name.split('.')[1]

	# Assign the image a new name, with p_user_id as its name.
	user_image.name = 'p_' + str(new_user.user_id) + '.' + image_extension

	# Assign the user the renamed image and save it in the database.
	new_user.user_image_path = user_image
	new_user.save()

	return new_user
