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
	route_url = 'users.views.register'

	# If the request method is post, then this page was loaded because the user submitted the form,
	# not just navigated to it.
	if request.method == 'POST':

		# Create the registration form object with the received data and files.
		registration_form = RegisterForm(request.POST, request.FILES)

		# The is_valid() method validates the fields of the form and returns true if they are all validated
		# correctly. It also passes the form parameters (fields) into a dictionary called cleaned_data, which you can
		# use for additional validation.
		if registration_form.is_valid():
			# Check that the passwords match and the image is does not exceed the maximum size
			if registration_form.clean_user_password_confirm() and registration_form.clean_user_image():
				# Set the logged session variable to true to indicate that the user is logged in.
				request.session['logged'] = True

				# Create new user based on the received data and save that user to the database.
				new_user = create_user_object(request.POST, request.FILES)
				new_user.save()

				# The url to go to is going to be the index page.
				route_url = ''
	else:
		# Create new empty registration form.
		registration_form = RegisterForm()

	context = {
		'register_form': registration_form
	}

	# logged_status = request.session['logged']
	#
	# # The user is already logged in.
	# if logged_status:
	# 	do_something = "Hello"
	# else:
	# 	do_something = "HELLO!"

	return redirect(request, reverse(route_url), context)


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
	new_user.user_password = uploaded_data['user_password']
	new_user.user_image_path = uploaded_image['user_image']

	return new_user
