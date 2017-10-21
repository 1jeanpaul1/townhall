from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# *************USER AND PERMISSION MODELS*********************
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# There are two roles: Entreprenuer and Citizen
class Role(models.Model):
    role_name = models.CharField(
        max_length=255,
        unique=True)
    display_name = models.CharField(
        max_length=255,
        unique=True)
    permissions = models.ManyToManyField(Permission,
            related_name='permission_roles', db_table='appauth_role_permission')

    def __str__(self):
        return self.display_name


class AppUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser):
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    first_name = models.CharField(
        max_length=255)
    last_name = models.CharField(
        max_length=255,
        blank=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True)
    city = models.CharField(
        max_length=255,
        blank=True)
    state = models.CharField(
        max_length=255,
        blank=True)
    zipcode = models.CharField(
        max_length=255,
        blank=True)

    # This is maintained for backward compatibility
    country = models.CharField(
        max_length=255,
        blank=True)

    # profile_image = models.ImageField(upload_to='users/profile_pictures', blank=True)
    roles = models.ManyToManyField(
        Role,
        related_name='role_appuser',
        blank=True)
    is_active = models.BooleanField(
        default=True)
    is_admin = models.BooleanField(
        default=False)
    is_verified = models.BooleanField(
        default=False)
    added_on = models.DateTimeField(
        auto_now_add=True)
    reset_password_token = models.CharField(
        max_length=8,
        blank=True)
    is_citizen = models.BooleanField(default=True)
    is_entrepreneur = models.BooleanField(default=False)
    interests = models.ManyToManyField(
        Interest,
        related_name='user_interests',
        blank=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    ALREADY_EXISTS = 'The user already exists'

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, *args, **kwargs):
        return True

    class Meta:
        verbose_name = 'User'

# PROBABLY SHOULD HAVE THIS IN SEPERATE FILES BECAUSE THEY DEAL WITH DIFFERENT THINGS BUT SINCE IT'S A HACKATHON FUCK IT
# FOR NOW

# *************USER IDEAS********************

class UserPosts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_post', on_delete=models.CASCADE,)
    title = models.CharField(max_length=255)
    #Need to figure out the image logic
    # post_image1 = models.ImageField(upload_to='posts/images', blank=True)
    # post_image2 = models.ImageField(upload_to='posts/images', blank=True)
    # post_image3 = models.ImageField(upload_to='posts/images', blank=True)
    # post_image4 = models.ImageField(upload_to='posts/images', blank=True)
    # post_image5 = models.ImageField(upload_to='posts/images', blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    city = models.CharField(
        max_length=255,
        blank=True)
    state = models.CharField(
        max_length=255,
        blank=True)
    zipcode = models.CharField(
        max_length=255,
        blank=True)
    added_on = models.DateTimeField(
        auto_now_add=True)
    liked = models.IntegerField()
    disliked = models.IntegerField()
    is_idea = models.BooleanField()
    # could go in either Category or Product class
    categories = models.ManyToManyField(
        Category,
        related_name='post_category',
        blank=True)

    @property
    def aggregate_reactions(self):
        return self.liked - self.disliked

    class Meta:
        verbose_name = 'User Posts'

    #need category field that this will have a many to many relationship with


class Category(models.Model):
    related_interests = models.ManyToManyField(
        Interest,
        related_name='category_interests',
        blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='products/category_images', storage=OverwriteStorage(), blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=False)

    ALREADY_EXISTS = 'The category already exists'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# The user will have interests
class Interest(models.Model):
    name = models.CharField(max_length=50)
    added_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=False)

    ALREADY_EXISTS = 'The Interest already exists'


# useful if we want to write comments outside of posts
# class Comment(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_post')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     content = models.TextField()
#     added_on = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comment', on_delete=models.CASCADE)
    post = models.ForeignKey(UserPosts, related_name='post_comment', on_delete=models.CASCADE)
    content = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)




