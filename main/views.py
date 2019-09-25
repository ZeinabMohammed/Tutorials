from django.shortcuts import render, redirect
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django.http import HttpResponse
from django.contrib.auth.models import User

def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    categories = [c.slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            series_urls[m] = part_one.tutorial_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by('tutorial_published')
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request=request,
        	template_name='main/tutorial.html',
                      context={"tutorial": this_tutorial,
                      "sidebar": tutorials_from_series,
                      "this_tut_idx": this_tutorial_idx})
    return render(request=request,
        	template_name='main/tutorial.html',
                      context={'categories':categories})
# def single_slug(request, single_slug):
# 	categories = [c.slug for c in TutorialCategory.objects.all()]
	
# 	if single_slug in categories:
# 		matching_series =TutorialSeries.objects.filter(tutorial_category__slug= single_slug)
# 		series_urls = { }
# 		for m in matching_series.all():
# 			part_one = Tutorial.objects.filter(tutorial_series__tutorial_series= m.tutorial_series).earliest("tutorial_published")
# 			series_urls[m] = part_one.tutorial_slug
# 		return render(request, "main/category.html", {"tutorial_series":matching_series, "part_ones": series_urls})
	
# 	tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
# 	if single_slug in tutorials:
# 		this_tutorial=Tutorial.objects.get(tutorial_slug= single_slug)
# 		tutorials_from_series= Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
# 		this_tutorial_idx= list(tutorials_from_series).index(this_tutorial)

		
	# return render(request,
	# 				  "main/tutorial.html",
	# 				  {"tutorial": this_tutorial,
	# 				   "sidebar": tutorials_from_series,
	# 				    "this_tutorial_idx": this_tutorial_idx })
	


def homepage(request):
	return render(request=request, template_name="main/categories.html",
					context={"categories":TutorialCategory.objects.all})



def register(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST or None)
		if form.is_valid():
				print(form.cleaned_data)
				username = form.cleaned_data.get("username")
				email 	 = form.cleaned_data.get("email")
				password = form.cleaned_data.get("password")
				
				new_user = User.objects.create_user(username, email, password)
				print(new_user)
		#User.objects.create_user(username, email, password)
	form = NewUserForm()
	return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "logged out succesfully!")
	return redirect("main:homepage")

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username= form.cleaned_data.get("username")
			password= form.cleaned_data.get("password")
			user =authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f"You have logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")


	form = AuthenticationForm()
	
	return render(request, "main/login.html", {"form":form})