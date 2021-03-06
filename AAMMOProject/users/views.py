import random
import urllib2

import django.contrib.auth
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import send_mail
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from social.apps.django_app.default.models import UserSocialAuth

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
	# Defaults for facebook image upload. image_request_url defines a default value for the facebook image a false
	# until it is actually used. That is because the sign up, img and disconnect tags in the template check for its
	# existence to be displayed or not.
	image_request_url = False
	# The facebook image used is a flag that is true or false whether the user is going to use the facebook image or
	# not. If he will, the database doesn't store the selected file from the file chooser.
	facebook_image_used = False

	# If the user is not logged in.
	if 'logged' not in request.session:
		# If the request method is post, then this page was loaded because the user submitted the form,
		# not just navigated to it.
		if request.method == 'POST':

			# If a facebook user was defined, then make sure that the profile picture is loaded by sending its link
			# to the context to the view page to preview it. Note that if the user selected another file,
			# it takes precedence over it.
			if request.user and not request.user.is_anonymous():
				facebook_id = UserSocialAuth.objects.get(id=request.user.id).uid
				image_request_url = 'http://graph.facebook.com/'+facebook_id+'/picture?type=large'

			# If the user didn't choose a file from the for file chooser create a form with post data only.
			if 'user_image' not in request.FILES:
				# Create the registration form object with the received data only.
				registration_form = RegisterForm(request.POST)
				facebook_image_used = True
			else:
				# Create the registration form object with the received data and files.
				registration_form = RegisterForm(request.POST, request.FILES)

			# The is_valid() method validates the fields of the form and returns true if they are all validated
			# correctly. It also passes the form parameters (fields) into a dictionary called cleaned_data, which you can
			# use for additional validation.
			if registration_form.is_valid():

					# SUCCESSFUL LOGIN
					# Create new user based on the received data and save that user to the database.
					if facebook_image_used:
						new_user = create_user(request.POST, image_request_url)
					else:
						new_user = create_user(request.POST, request.FILES)

					# Set the logged session variable to true to indicate that the user is logged in.
					request.session['logged'] = True
					# Set the logged user name to the logged in username.
					request.session['username'] = new_user.user_name
					# Set the logged user profile picture path if available
					if new_user.user_image_path:
						request.session['user_image'] = str(new_user.user_image_path)

					# Set the admin flag based on whether the user is an admin or not.
					if new_user.user_admin_status:
						request.session['is_admin'] = True

					# Format: subject,body,host to use,recipients,fail_silently
					send_mail(
						'Welcome to our website!',
						'Welcome to our website '+new_user.user_name+'! We hope you enjoy it!',
						settings.EMAIL_HOST_USER,
						[new_user.user_email],
						fail_silently=False
					)

					# The URL to go to.
					route_url = '/article/index/'

					# Go to the index page since you successfully logged in.
					return redirect(route_url)

		# The method was GET, that means the user just navigated to the register form page or the form was redirected
		#  from a facebook register request.
		else:
			# If a facebook user was defined
			if request.user and not request.user.is_anonymous():
				# Get the facebook user name, email and id from the database.
				facebook_username = request.user.username
				facebook_email = request.user.email
				facebook_id = UserSocialAuth.objects.get(id=request.user.id).uid

				# Create a url GET request to get the profile picture of the user.
				image_request_url = 'http://graph.facebook.com/'+facebook_id+'/picture?type=large'

				register_initial_data = {
					'user_name': facebook_username,
					'user_email': facebook_email,
				}

				# Create new registration form with facebook info
				registration_form = RegisterForm(register_initial_data)

			else:
				# Create new empty registration form.
				registration_form = RegisterForm()

		# The registration form data to the register page.
		context = {
			'register_form': registration_form,
			'user_image': image_request_url
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
		source_path = '/article/index/'
		response = redirect(source_path)
	else:

		# Get source page path for redirect
		source_path = request.POST['source_path']
		response = redirect(source_path)

		# Get the username and password that the user used to log in.
		logged_username = request.POST['username']
		logged_password = request.POST['user_password']

		# The default login status is failure
		request.session['login_failure'] = True

		try:
			# Get the user object
			logged_user = Users.objects.get(user_name=logged_username)
			# Get the password for the provided user name. Throws DoesNotExist exception if user is not found.
			saved_user_password = logged_user.user_password
			# Compare passwords to check they are correct.
			is_similar = check_password(logged_password, saved_user_password)
			# If the passwords are similar, then the user has successfully logged in.
			if is_similar:
				# Set the session variable to logged.
				request.session['logged'] = True
				# Set the logged user name to the logged in username.
				request.session['username'] = logged_username
				# Set the user's profile picture session variable.
				request.session['user_image'] = str(logged_user.user_image_path)
				# Set the admin flag based on whether the user is an admin or not.
				if logged_user.user_admin_status:
					request.session['is_admin'] = True
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
			request.session['login_failure'] = True

	return response


def login_facebook(request):
	"""
	This function performs the actions necessary to login with facebook. If the email is matched with an email in the
	database, check if the facebook id of that email exists or not, if it doesn't, add it. If it does, just login. If
	the email doesn't match, then go to the registration page.
	:param request:
	:return:
	"""
	# The facebook user data has been received successfully.
	if request.user and not request.user.is_anonymous():
		# Get the user's facebook registered email.
		facebook_email = request.user.email
		# The true Facebook id is in the python_auth_social migrated tables. You index it with the ID in the user object
		# returned from facebook.
		facebook_id = UserSocialAuth.objects.get(id=request.user.id).uid

		# Try getting the user with the given email from the "local" database.
		try:
			# Query the database with the facebook email.
			logged_user = Users.objects.get(user_email=facebook_email)

			# A user was found with the same facebook email and his facebook id is still null. Add it.
			if not logged_user.user_facebook_id:
				# Set the user's Facebook id with the Facebook received id and save it to the database.
				logged_user.user_facebook_id = facebook_id
				logged_user.save()

			# Login the user. Set the session variable to logged.
			request.session['logged'] = True
			# Set the logged user name to the logged in username.
			request.session['username'] = logged_user.user_name
			# Set the logged user profile picture path.
			request.session['user_image'] = str(logged_user.user_image_path)
			# Set the admin flag based on whether the user is an admin or not.
			if logged_user.user_admin_status:
				request.session['is_admin'] = True

		# The user doesn't exist in the first place. Redirect to the registration page.
		except Users.DoesNotExist:
			return redirect("/users/register/")

	# Facebook did not return any data. An error has occurred.
	else:
		raise Http404("Could not fetch Facebook information!")

	# Get the page where the original login request occurred from.
	original_page = request.GET['next']

	return redirect(original_page)


def logout(request):
	"""
	This function performs the log out functionality of the page. It logs the user out by deleting the session and
	the user saved cookie.
	:param request: The request received from the user.
	:return: Returns the same page the user was in but without being logged on.
	"""

	# Makes sure that the logout was performed from logout press or from the disconnect Facebook link.
	if 'source_path' not in request.POST and 'source_path' not in request.GET:
		source_path = '/article/index/'
		response = redirect(source_path)
	else:

		# Get source page path for redirect
		try:
			source_path = request.POST['source_path']
		except MultiValueDictKeyError:
			source_path = request.GET['source_path']

		# Logout from the social backend, which simply clears all session variables.
		django.contrib.auth.logout(request)

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

	if 'logged' not in request.session:
		return redirect('/article/index/')

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
			if 'user_name' in request.POST and request.POST['user_name'] != "":
				current_user.user_name = request.POST['user_name']
				request.session['username'] = request.POST['user_name']

			# Update the user's email if it was filled in the fields.
			if 'user_email' in request.POST and request.POST['user_email'] != "":
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

				# A flag that indicates that the image has been altered.
				changed_image = True
			else:
				# Indicate that the image has not changed.
				changed_image = False

			# Save updates to the current user.
			current_user.save()

			# The image has changed, I needed to have saved the object first to get the true URL for the image
			if changed_image:
				# Save the current profile picture in the session variable.
				request.session['user_image'] = str(current_user.user_image_path)

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

	# Get the just uploaded image if it exists.
	if 'user_image' in uploaded_image:
		user_image = uploaded_image['user_image']

		# Get the image's extension
		image_extension = user_image.name.split('.')[1]

		# Assign the image a new name, with p_user_id as its name.
		user_image.name = 'p_' + str(new_user.user_id) + '.' + image_extension

		# Assign the user the renamed image and save it in the database.
		new_user.user_image_path = user_image
		new_user.save()

	# If the uploaded image is a url to the image to download from facebook.
	elif uploaded_image:
		# Fetch the image from the remote URL.
		fetched_image = urllib2.urlopen(uploaded_image).read()
		# Create temporary file to download image.
		fetched_image_file = NamedTemporaryFile(delete=True)
		# Write the fetched image's data in the temporary file.
		fetched_image_file.write(fetched_image)
		# Flush the written data to the file.
		fetched_image_file.flush()
		# Create the file's name.
		fetched_image_path = 'p_' + str(new_user.user_id) + '.' + 'jpg'
		# Save the image path. Arguments: path, image file, save boolean
		new_user.user_image_path.save(fetched_image_path, ImageFile(fetched_image_file), save=True)

	return new_user


def list_users(request):

	# Get all the users in the database.
	users = Users.objects.all()

	# Create context to send to the template.
	context = {
		'users': users
	}

	return render(request,'user_list.html',context)


def delete_user(request, user_id):
	"""
	This function simple queries the database for the user with the ID given and removes him/her from the database.
	:param request:
	:param user_id: The user ID to delete.
	:return: A redirect to the listing function.
	"""

	# Delete the user given by this ID.
	Users.objects.get(user_id=user_id).delete()

	# Return to the same page via this url.
	return redirect('/users/list_users/')