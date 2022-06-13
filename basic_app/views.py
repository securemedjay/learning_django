from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# the following are required for the user_login view
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, "basic_app/index.html")


def user_login(request):
    # user's username and password
    if request.method == "POST":
        username = request.POST.get("username")  # using request.POST.get("username") instead of
        # request.POST["username"] because we are getting the value from a html form with a variable called
        # name="username"
        password = request.POST.get("password")

        # authenticate user
        user = authenticate(username=username, password=password)  # user is a User object

        if user:  # if user is authenticated,
            if user.is_active:  # check if the account is active
                login(request, user)  # log user in
                return HttpResponseRedirect(reverse("index"))  # redirect to the index page

            else:  # if account is not active
                return HttpResponse("Account is not active")

        else:  # if user is not authenticated
            print("Someone tried to login and failed")
            print(f"Username:{username}, Password:{password}")
            return HttpResponse("Invalid username and/or password")

    else:  # request method is not POST then display the login page
        return render(request, "basic_app/login.html")


# be careful not to give your functions the same name as the imported functions otherwise you'll override the import
# functions
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # hashing the password
            user.save()

            profile = profile_form.save(commit=False)  # to get the instance from form but only 'in memory', not in
            # database because you want to make some changes before you save it.
            profile.user = user

            if "profile_pic" in request.FILES:  # request.FILES returns a dictionary
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:  # if forms are not valid print error
            print(user_form.errors, profile_form.errors)

    else:  # if request.method is not post, then render forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered,
    }

    return render(request, "basic_app/registration.html", context=context)
