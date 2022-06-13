from django.db import models
from django.contrib.auth.models import User


# The goal of the code below is to add more fields (portfolio_site and profile_pic) to the built-in User model of
# Django admin
class UserProfileInfo(models.Model):

    # creating a one-to-one link with the built-in User model. One-to-one link creates a regular Django model(user)
    # that’s has its own database table and holds a One-To-One relationship with the existing model(User)through a
    # OneToOneField. It is used when you need to store extra information about the existing Model that’s not related to
    # core function of the model. It is a good practice to name the one-to-one field with the same name as that of the
    # related model, lowercase.
    user = models.OneToOneField(User, models.CASCADE)

    # creating additional fields
    portfolio_site = models.URLField(blank=True)  # blank=True means users may leave it blank and not fill
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)  # upload_to="profile_pics" to set the folder
    # to upload the image to. Profile_pics should be created as a subdirectory in media directory

    def __str__(self):
        return self.user.username