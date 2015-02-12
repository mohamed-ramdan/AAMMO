from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from users.forms import RegisterForm
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
				registration_form.clean_user_image() and registration_form.clean_user_image():

					# SUCCESSFUL LOGIN
					# Create new user based on the received data and save that user to the database.
					new_user = create_user_object(request.POST, request.FILES)
					new_user.save()

					# Set the logged session variable to true to indicate that the user is logged in.
					request.session['logged'] = True
					request.session['username'] = new_user.user_name

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

	# Get source page path for redirect
	source_path = request.POST['source_path']

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
			request.session['logged'] = True
			del request.session['login_failure']
			# The user has not logged in successfully.
		else:
			raise Users.DoesNotExist()
	# The user didn't log in successfully.
	except Users.DoesNotExist:
		request.session['logged'] = False
		request.session['login_failure'] = True

	return redirect(source_path)


def logout(request):
	"""
	This function performs the log out functionality of the page. It logs the user out by deleting the session and
	the user saved cookie.
	:param request: The request received from the user.
	:return: Returns the same page the user was in but without being logged on.
	"""

	# Get source page path for redirect
	source_path = request.POST['source_path']

	# Set the logged session variable to false
	request.session['logged'] = False

	# Delete the saved cookie if it exists.

	return redirect(source_path)


def create_user_object(uploaded_data, uploaded_image):
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
	new_user.user_image_path = uploaded_image['user_image']

	return new_user
