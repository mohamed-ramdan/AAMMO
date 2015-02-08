from django.db import models


class Users(models.Model):
	"""
	This is the user's model class. It contains information pertaining to each user. A user can also be an admin,
	whom have enhanced privileges.
	"""

	# The user's ID field
	user_id = models.IntegerField(primary_key=True)

	# The user's facebook id field.
	user_facebook_id = models.IntegerField(unique=True)

	# The user's name field.
	user_name = models.CharField(max_length=100)

	# The user's password field.
	user_password = models.CharField(max_length=100)

	# The user's email field
	user_email = models.CharField(max_length=200)

	# The path to the user's profile picture.
	user_image_path = models.CharField(max_length=255)

	# The user's admin status, default => Not an admin
	user_admin_status = models.BooleanField(default=False)