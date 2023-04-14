from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.db import transaction
from functools import partial

DateInput = partial(
    forms.DateInput, {'class': 'datepicker'})


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        max_length=60, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()
        return user


class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        max_length=60, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        admin_user = Admin_User.objects.create(user=user)
        admin_user.save()
        return user


class CustomerUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class AdminUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id_number', 'profile_pic', 'contacts', 'location']


class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Admin_User
        fields = ['id_number', 'location', 'profile_pic', 'contacts']


class group_tour_form(forms.ModelForm):
    class Meta:
        model = Group_tours
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        fields = ['tour_name', 'desc', 'price',
                  'start_date', 'end_date', 'location', 'pictures']

        def __init__(self, *args, **kwargs):
            super(group_tour_form, self).__init__(*args, **kwargs)
            self.fields['tour_name'].required = True
            self.fields['start_date'].required = True
            self.fields['end_date'].required = True
            self.fields['location'].required = True
            self.fields['desc'].required = True
            # self.fields['pictures'].required = True


class road_trip_form(forms.ModelForm):
    class Meta:
        model = Road_trips
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        fields = ['trip_name', 'desc', 'price',
                  'start_date', 'end_date', 'location', 'pictures']

        def __init__(self, *args, **kwargs):
            super(road_trip_form, self).__init__(*args, **kwargs)
            self.fields['trip_name'].required = True
            self.fields['start_date'].required = True
            self.fields['end_date'].required = True
            self.fields['location'].required = True
            self.fields['desc'].required = True
            # self.fields['pictures'].required = True


class adventures_safarisForm(forms.ModelForm):
    class Meta:
        model = Adventures_safaris
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        fields = ['name', 'desc', 'price',
                  'start_date', 'end_date', 'location', 'pictures']

        def __init__(self, *args, **kwargs):
            super(adventures_safarisForm, self).__init__(*args, **kwargs)
            self.fields['name'].required = True
            self.fields['start_date'].required = True
            self.fields['end_date'].required = True
            self.fields['location'].required = True
            self.fields['desc'].required = True
            # self.fields['pictures'].required = True


class galleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        widgets = {'date': DateInput()}
        fields = ['pic_desc', 'date', 'pic']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Message, please add your contacts after the message.'}), required=True)

    def __str__(self):
        return self.from_email

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['from_email'].widget.attrs['placeholder'] = self.fields['from_email'].label or 'email@address.com'
        self.fields['subject'].widget.attrs['placeholder'] = self.fields['subject'].label or 'Subject'


class MembersForm(forms.Form):
    members = forms.IntegerField(required=True)

    def __str__(self):
        return self.members

    def __init__(self, *args, **kwargs):
        super(MembersForm, self).__init__(*args, **kwargs)
        self.fields['members'].widget.attrs['placeholder'] = self.fields['members'].label or 'How many are you'
