from django import forms
from main.models import Country, Review

class CreateCountryForm(forms.ModelForm):
	class Meta:
		model = Country
		fields = '__all__'

class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=30)
	password1 = forms.CharField(max_length=30,widget=forms.PasswordInput())
	email = forms.EmailField(required=False)


class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password3 = forms.CharField(max_length=30,widget=forms.PasswordInput())

class CreateReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		exclude = ('date','country','user',)
		#fields = '__all__'

class EditReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		exclude = ('date','country','user',)