from PIL import Image
from django.db import models


class Users(models.Model):
	"""
	This is the user's model class. It contains information pertaining to each user. A user can also be an admin,
	whom have enhanced privileges.
	"""

	# The user's ID field
	user_id = models.AutoField(primary_key=True)

	# The user's facebook id field.
	user_facebook_id = models.CharField(unique=True, null=True, max_length=255)

	# The user's name field.
	user_name = models.CharField(unique=True, max_length=100)

	# The user's password field.
	user_password = models.CharField(max_length=100)

	# The user's email field
	user_email = models.EmailField(max_length=255, unique=True)

	# The path to the user's profile picture. This will be created in the MEDIA_ROOT path folder.
	user_image_path = models.FileField(upload_to='profile_pics/%Y/%m/%d', null=True)

	# The user's admin status, default => Not an admin
	user_admin_status = models.BooleanField(default=False)

	def save(self):
		"""
		Override the model's save function to resize the photo to 100x100 first.
		:return:
		"""
		super(Users, self).save()

		if self.user_image_path:
			image_path = str(self.user_image_path.path)
			image_object = Image.open(image_path)

			image_object.thumbnail((100, 100), Image.ANTIALIAS)
			image_object.save(image_path)