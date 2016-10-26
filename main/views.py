from django.shortcuts import render, redirect
from models import Country, Review
from django.http import HttpResponse
from forms import CreateCountryForm, CreateUserForm, LoginForm, CreateReviewForm, EditReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime

# only admin ALLOWED
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def countrylist(request):
	context = {}
	countries = Country.objects.all()
	context['country_list'] = countries
	print context
	return render(request, 'country_list.html', context)

def countrydetail(request, pk):

	context = {}

	country = Country.objects.get(pk=pk)

	context['country'] = country
	# return HttpResponse(country)
	context['form'] = CreateReviewForm()

	if request.method == 'POST':
		form = CreateReviewForm(request.POST)
		context['form'] = form
		if form.is_valid():
			review = form.save(commit=False)
			review.date = datetime.now()
			review.country = country
			review.user = request.user
			review.save()
			return redirect('/countrylist/')
	return render(request, 'country_detail.html', context)

	# from django.http import HttpResponse

@login_required
def createcountry(request):
	context = {}
	context['form'] = CreateCountryForm()

	#add to database
	if request.method == 'POST':
		#make sure form is valid
		form = CreateCountryForm(request.POST, request.FILES)
		context['form'] = form

		if form.is_valid():
			form.save()
			return render(request, 'countrycreated.html', context)
		#save form to database
	return render(request, 'createcountry.html', context)

def sign_up(request):
	context = {}
	context['form'] = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		context['form'] = form
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']

			new_user = User.objects.create_user(username=username , password=password )
			new_user.save()

			auth_user = authenticate(username=username, password=password)

			login(request, auth_user)

			return redirect('/countrylist/')

	return render(request, 'sign_up.html', context)

def logout_view(request):
	logout(request)
	return redirect('/countrylist/')


def login_view(request):
	context = {}
	context['form'] = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		context['form'] = form
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password3']
			try:
				auth_user = authenticate(username=username, password=password)

				login(request, auth_user)
				return redirect('/countrylist/')
			except Exception, e:
				return HttpResponse('Wrong username or password !! please <a href="/login/">try again</a>')


	return render(request, 'login.html', context)

@login_required
def editreview(request, pk):
	context = {}
	review = Review.objects.get(pk=pk)
	if request.user == review.user:
		context['review'] = review
		form = EditReviewForm(request.POST or None, instance=review)

		context['form'] = form

		if form.is_valid():
			form.save()
			return redirect('/countrylist/')
	else:
		return HttpResponse('GO AWAY HACKER !!')

	return render(request, 'editreview.html', context)

def deletereview(request, pk):
	review = Review.objects.get(pk=pk)
	if request.user == review.user:
		review.delete()

	return redirect('/countrylist/')