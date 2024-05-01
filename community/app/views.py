from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from .models import Community, Posts, UserProfile, UserCommunityMembership
from .forms import CommunityCreationForm, PostForm, UserProfileForm
from datetime import datetime
from django.conf import settings

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login_user'))  # Redirect to the login page
    return wrapper


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "authenticate/login.html",{'error_message': 'Invalid form. Please correct the errors.'} )
    else:

        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    return redirect("login_user")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_user")
        else:
            return render(request, 'authenticate/register.html',
                          {'error_message': 'Invalid form. Please correct the errors.'})
    return render(request, 'authenticate/register.html', {})

def home(request=None):
    username = request.user.username
    joined_communities = UserCommunityMembership.objects.filter(username=username).values_list('community', flat=True)
    posts = Posts.objects.filter(community_name__in=joined_communities).order_by('-created_at')[:3]

    all_communities = Community.objects.exclude(name__in=joined_communities)
    return render(request, 'home.html',  {'communities': all_communities, "posts": posts})

def my_communities(request):
    username = request.user.username
    joined_communities = UserCommunityMembership.objects.filter(username=username).values_list('community', flat=True)
    communities=Community.objects.filter(name__in=joined_communities)
    return render(request, 'my_communities.html', {'communities': communities})

def create_community(request):
    if request.method == 'POST':
        form = CommunityCreationForm(request.POST)
        if form.is_valid():
            # Extracting data from the form
            community_name = form.cleaned_data['name']
            community_privacy = form.cleaned_data['privacy']
            description = form.cleaned_data['description']
            owner = request.user

            # Creating and saving a new community object
            new_community = Community(name=community_name, privacy=community_privacy, owner=owner, description=description)
            new_community.save()

            # Community creator is automatically joined to the community
            new_community_membership = UserCommunityMembership(username=request.user.username, community=community_name)
            new_community_membership.save()

            return render(request, 'community_home.html', {'community_name': community_name, "is_owner": True, "is_joined": True})
    else:
        form = CommunityCreationForm()

    return render(request, 'create_community.html', {'form': form})

def community_home(request):

    username = request.user.username
    community_name = request.GET["community_name"]
    community_membership = UserCommunityMembership.objects.filter(username=username, community=community_name)

    is_joined = len(community_membership) == 1
    community = Community.objects.get(name=community_name)
    description = community.description
    is_public = community.privacy == "public"
    is_owner = community.owner == request.user.username

    if is_joined or is_public:
        posts = Posts.objects.filter(community_name=community_name)
    else:
        posts = []

    return render(request, 'community_home.html', {'community_name': community_name, "is_owner": is_owner, "description": description, "posts": posts, "is_joined": is_joined})


def join_community(request):
    username = request.user.username
    community_name = request.GET["community_name"]

    community_membership = UserCommunityMembership.objects.filter(username=username, community=community_name)
    if not community_membership:
        # Creating and saving a new community object
        new_community_membership = UserCommunityMembership(username=username, community=community_name)
        new_community_membership.save()

    # Displaying posts at the community home page
    posts = Posts.objects.filter(community_name=community_name)

    community = Community.objects.get(name=community_name)
    description = community.description
    is_owner = community.owner == request.user.username
    return render(request, 'community_home.html', {'community_name': community_name, "is_owner": is_owner, "description": description, "posts": posts, "is_joined": True })


def create_post(request):
    community_name = request.GET["community_name"]
    if request.method == 'POST':
        form = Posts(request.POST)
        if form.is_valid():
            # Extracting data from the form
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            event_date = form.cleaned_data['event_date']
            author_username = request.user.username
            created_at = datetime.now().date()
            # Creating and saving a new community object
            new_post = Posts(title=title, content=content, event_date=event_date, community_name=community_name, author_username=author_username, created_at=created_at)
            new_post.save()
            return community_home(request)
            #return render(request, 'community_home.html', {'community_name': community_name, "is_owner": True})

    return render(request, 'create_post.html', {'community_name': community_name})


def edit_profile(request):
    url = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        username = request.user.username
        existing_user = UserProfile.objects.get(username=username)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birthdate = form.cleaned_data['birthdate']
            about_me = form.cleaned_data['about_me']
            profile_picture = form.cleaned_data['profile_picture']
            if existing_user:
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.birthdate = birthdate
                existing_user.about_me = about_me
                if profile_picture:
                    existing_user.profile_picture.save(profile_picture.name, profile_picture)
                existing_user.save()
                return render(request, "my_profile.html", {"user_profile": existing_user, "MEDIA_URL": settings.MEDIA_URL})
            else:
                user_profile = UserProfile(username=username, first_name=first_name, last_name=last_name, birthdate=birthdate, about_me=about_me)
                if profile_picture:
                    user_profile.profile_picture.save(profile_picture.name, profile_picture)
                user_profile.save()

                return render(request, "my_profile.html", {"user_profile": user_profile,"MEDIA_URL": settings.MEDIA_URL})
    else:
        username = request.user.username
        existing_user = UserProfile.objects.get(username=username)
        if existing_user:
            # Add existing field values to the corresponding boxes in the html form
            form = UserProfileForm(instance=existing_user)
            url = form.initial["profile_picture"].url
        else:
            form = UserProfileForm()
    return render(request, "edit_profile.html", {"form": form, "url": url})

def my_profile(request):
    username = request.user.username
    user_profile = UserProfile.objects.get(username=username)

    return render(request, "my_profile.html", {"user_profile": user_profile, "MEDIA_URL": settings.MEDIA_URL})