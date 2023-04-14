# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django import template
register = template.Library()

# Create your models here.


class User(AbstractUser):

    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    @classmethod
    def get_profile(cls, search_profile):
        profile = cls.objects.filter(first_name__icontains=search_profile)
        return profile


class Customer(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    id_number = models.IntegerField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='customer_pics/',
                                    blank=True)
    contacts = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/media/default.png"

    def save_customer(self):
        self.save()

    def update_customer(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_customer(self):
        self.delete()


class Admin_User(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    id_number = models.IntegerField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='admin_pics/',
                                    blank=True)
    contacts = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    @ property
    def profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/media/default.png"

    def save_admin_user(self):
        self.save()

    def update_admin_user(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_admin_user(self):
        self.delete()


class Road_trips(models.Model):
    trip_name = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True,)
    price = models.IntegerField(blank=True, null=True)
    desc = models.TextField(max_length=250, blank=True)
    start_date = models.DateField(blank=True, null=True,)
    end_date = models.DateField(blank=True, null=True,)
    location = models.CharField(max_length=100, blank=True)
    pictures = models.ImageField(upload_to='trips/',
                                 blank=True)
    # members = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.trip_name

    def save_road_trips(self):
        self.save()

    def update_road_trips(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_road_trips(self):
        self.delete()

    @ property
    def pictures_url(self):
        if self.pictures and hasattr(self.pictures, 'url'):
            return self.pictures.url
        else:
            return "/media/gallery_1_h2s7iTb.jpg"


# class Members(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, blank=True, null=True,)
#     members = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return self.members

#     def save_members(self):
#         self.save()

#     def update_members(self, using=None, fields=None, **kwargs):
#         if fields is not None:
#             fields = set(fields)
#             deferred_fields = self.get_deferred_fields()
#             if fields.intersection(deferred_fields):
#                 fields = fields.union(deferred_fields)
#         super().refresh_from_db(using, fields, **kwargs)

#     def delete_members(self):
#         self.delete()

    # @classmethod
    # def get_tour(cls, search_tour):
    #     tour = cls.objects.filter(trip_name__icontains=search_tour)
    #     return tour


class Group_tours(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tour_name = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    desc = models.TextField(max_length=250, blank=True)
    start_date = models.DateField(blank=True, null=True,)
    end_date = models.DateField(blank=True, null=True,)
    location = models.CharField(max_length=100, blank=True)
    pictures = models.ImageField(upload_to='tours/',
                                 blank=True)

    def __str__(self):
        return self.tour_name

    def save_group_tours(self):
        self.save()

    def update_group_tours(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_group_tours(self):
        self.delete()

    @ property
    def pictures_url(self):
        if self.pictures and hasattr(self.pictures, 'url'):
            return self.pictures.url
        else:
            return "/media/gallery_1_h2s7iTb.jpg"


class Adventures_safaris(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    desc = models.TextField(max_length=250, blank=True)
    start_date = models.DateField(blank=True, null=True,)
    end_date = models.DateField(blank=True, null=True,)
    location = models.CharField(max_length=100, blank=True)
    pictures = models.ImageField(upload_to='gallery/',
                                 blank=True)

    def __str__(self):
        return self.name

    def save_adventures_safaris(self):
        self.save()

    def update_adventures_safaris(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_adventures_safaris(self):
        self.delete()

    @ property
    def pictures_url(self):
        if self.pictures and hasattr(self.pictures, 'url'):
            return self.pictures.url
        else:
            return "/media/gallery_1_h2s7iTb.jpg"


class Gallery(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    pic_desc = models.TextField(max_length=250, blank=True)
    date = models.DateField(blank=True, null=True,)
    pic = models.ImageField(upload_to='pics/',
                            blank=True)


    def __str__(self):
        return str(self.id)

    def save_gallery(self):
        self.save()

    def update_gallery(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_gallery(self):
        self.delete()

    @ property
    def pic_url(self):
        if self.pic and hasattr(self.pic, 'url'):
            return self.pic.url
        else:
            return "/media/gallery_1_h2s7iTb.jpg"


# class Hiking(models.Model):
#     hike_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)


# class Team_building(models.Model):
#     tb_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)


# class Camping(models.Model):
#     camping_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)

# class Honeymoon(models.Model):
#     honeymoon_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)

# class Airport_transfers(models.Model):
#     at_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)

# class Student_tours(models.Model):
#     tour_name = models.CharField(max_length=50, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     desc = models.TextField(max_length=250, blank=True)
#     start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     location = models.CharField(max_length=100, blank=True)
#     pictures = models.ImageField(upload_to='gallery/',
#                                  blank=True)

# class Hotel_bookings(models.Model):
#     tour_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
    #    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)

# class Ticketing(models.Model):
#     hotel_name = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
#    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)

    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)

# class Flight_bookings(models.Model):
#     flight = models.CharField(max_length=50, blank=True)
    #   price = models.DecimalField(max_digits=10, decimal_places=2)
    #   desc = models.TextField(max_length=250, blank=True)
#    start_date = models.DateField(blank=True, null=True,)
#     end_date = models.DateField(blank=True, null=True,)
    #   user = models.OneToOneField(
    # User, on_delete=models.CASCADE, primary_key=True)
    # location  = models.CharField(max_length=100, blank=True)
    # pictures = models.ImageField(upload_to='gallery/',
    # blank=True)
