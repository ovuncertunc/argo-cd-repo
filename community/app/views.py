from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from .models import Community, Posts, UserProfile, UserCommunityMembership, CommunitySpecificTemplate
from .forms import CommunityCreationForm, PostForm, UserProfileForm, CommunitySpecificTemplateForm
from datetime import datetime
from django.conf import settings
import json, ast

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

    for post in posts:
        post_author = post.author_username
        user_profile = UserProfile.objects.get(username=post_author)
        post.author_profile_picture = user_profile.profile_picture
        post.template_dict = ast.literal_eval(post.template_dict)

    all_communities = Community.objects.exclude(name__in=joined_communities)
    return render(request, 'home.html',  {'communities': all_communities, "MEDIA_URL": settings.MEDIA_URL, "posts": posts})

def my_communities(request):
    username = request.user.username
    joined_communities = UserCommunityMembership.objects.filter(username=username).values_list('community', flat=True)
    communities=Community.objects.filter(name__in=joined_communities)
    return render(request, 'my_communities.html', {'communities': communities})

def create_community(request):
    if request.method == 'POST':
        form = CommunityCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Extracting data from the form
            community_name = form.cleaned_data['name']
            community_privacy = form.cleaned_data['privacy']
            description = form.cleaned_data['description']
            community_photo = form.cleaned_data['community_photo']
            owner = request.user

            # Creating and saving a new community object
            new_community = Community(name=community_name, privacy=community_privacy, owner=owner, description=description, community_photo=community_photo)
            new_community.save()

            # Community creator is automatically joined to the community
            new_community_membership = UserCommunityMembership(username=request.user.username, community=community_name)
            new_community_membership.save()

            return render(request, 'community_home.html', {'community_name': community_name, "community_photo": new_community.community_photo, "MEDIA_URL": settings.MEDIA_URL, "is_owner": True, "is_joined": True})
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
    community_photo = community.community_photo
    if is_joined or is_public:
        posts = Posts.objects.filter(community_name=community_name)

        for post in posts:
            post_author = post.author_username
            user_profile = UserProfile.objects.get(username=post_author)
            post.author_profile_picture = user_profile.profile_picture
            post.template_dict = ast.literal_eval(post.template_dict)

    else:
        posts = []

    return render(request, 'community_home.html', {'community_name': community_name, "community_photo": community_photo, "MEDIA_URL": settings.MEDIA_URL, "is_owner": is_owner, "description": description, "posts": posts, "is_joined": is_joined})


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
    community_photo = community.community_photo
    description = community.description
    is_owner = community.owner == request.user.username
    return render(request, 'community_home.html', {'community_name': community_name, "community_photo": community_photo, "MEDIA_URL": settings.MEDIA_URL, "is_owner": is_owner, "description": description, "posts": posts, "is_joined": True})


def create_post(request):
    community_name = request.GET["community_name"]
    templates = CommunitySpecificTemplate.objects.filter(community_name=community_name).values_list('template_name', flat=True)

    if request.method == 'POST':

        template_name = request.POST["template_name"]
        author_username = request.user.username
        created_at = datetime.now().date()

        if template_name == "Default Template":
            # Extracting data from the form
            title = request.POST['Title']
            content = request.POST['Content']
            event_date = request.POST['Event Date']
            template_dict = {"Title": title, "Content": content, "Event Date": event_date}

            # Creating and saving a new community object
            new_post = Posts(template_name=template_name, template_dict=template_dict, community_name=community_name, author_username=author_username, created_at=created_at)
            new_post.save()

            return community_home(request)
            #return render(request, 'community_home.html', {'community_name': community_name, "is_owner": True})
        else:
            post_content_json = request.POST["form_data"]
            new_post = Posts(template_name=template_name, template_dict=post_content_json, community_name=community_name, author_username=author_username, created_at=created_at)
            new_post.save()

            return community_home(request)

    return render(request, 'create_post.html', {'community_name': community_name, "templates": templates, "select_dropdown_list": True})


def display_community_specific_template_post(request):
    template_name = request.POST["selected_template"]
    community_name = request.POST["community_name"]

    if template_name == "Default Template":
        template_dict = {"Title": "text", "Content": "text", "Event Date": "date"}
    else:
        template_dict_str = CommunitySpecificTemplate.objects.get(template_name=template_name).template_dict
        template_dict = ast.literal_eval(template_dict_str)

    return render(request, "create_post.html", {'community_name': community_name, "template_name": template_name, "template_dict": template_dict, "select_dropdown_list": False})


def edit_profile(request):
    url = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        username = request.user.username
        existing_user = UserProfile.objects.filter(username=username).exists()
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birthdate = form.cleaned_data['birthdate']
            about_me = form.cleaned_data['about_me']
            profile_picture = form.cleaned_data['profile_picture']
            if existing_user:
                user = UserProfile.objects.get(username=username)
                user.first_name = first_name
                user.last_name = last_name
                user.birthdate = birthdate
                user.about_me = about_me
                if profile_picture:
                    user.profile_picture.save(profile_picture.name, profile_picture)
                user.save()
                return render(request, "my_profile.html", {"user_profile": user, "MEDIA_URL": settings.MEDIA_URL})
            else:
                user_profile = UserProfile(username=username, first_name=first_name, last_name=last_name, birthdate=birthdate, about_me=about_me)
                if profile_picture:
                    user_profile.profile_picture.save(profile_picture.name, profile_picture)
                user_profile.save()

                return render(request, "my_profile.html", {"user_profile": user_profile,"MEDIA_URL": settings.MEDIA_URL})
    else:
        username = request.user.username
        existing_user = UserProfile.objects.filter(username=username).exists()
        if existing_user:
            # Add existing field values to the corresponding boxes in the html form
            user = UserProfile.objects.get(username=username)
            form = UserProfileForm(instance=user)
            profile_picture = form.initial["profile_picture"]
        else:
            form = UserProfileForm()
            profile_picture = None
    return render(request, "edit_profile.html", {"form": form, "profile_picture": profile_picture})

def my_profile(request):
    username = request.user.username
    if UserProfile.objects.filter(username=username).exists():
        user_profile = UserProfile.objects.get(username=username)
        return render(request, "my_profile.html", {"user_profile": user_profile, "MEDIA_URL": settings.MEDIA_URL})
    else:
        return edit_profile(request)


def create_template(request):
    if request.method == 'POST':
        template_dict_json = request.POST.get("template_dict")
        template_dict = json.loads(template_dict_json)
        template_name = request.POST.get("template_name")
        community_name = request.POST["community_name"]

        new_template = CommunitySpecificTemplate(community_name=community_name, template_name=template_name, template_dict=template_dict)
        new_template.save()

        return redirect(reverse("community_home") + f"?community_name={community_name}")
    else:
        community_name = request.GET["community_name"]
        form = CommunitySpecificTemplateForm()
        return render(request, "create_template.html", {"form": form, "community_name": community_name})
