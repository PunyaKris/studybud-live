from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


# rooms = [
#     {'id': 1 , 'name': "Python For Bigenner"},
#     {'id': 2 , 'name': "Learn React"},
#     {'id': 3 , 'name': "Backend in Django"},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home page')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, "User does not exist")
            return redirect("login")

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            print("login happens")
            return redirect('home page')
        else:
            messages.error(request, "Password and Username doesn't match")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home page')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home page')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home_page(request):
    print("User:", request.user)
    print("Authenticated:", request.user.is_authenticated)
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    all_rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).order_by('-update')

    rooms = all_rooms[:7]

    all_comments = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    ).order_by('-update')[:7]
    rooms_count = all_rooms.count()
    topics = Topic.objects.all()[:9]
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, "all_comments": all_comments}
    return render(request, 'base/home.html', context)

def room_page(request, pk):
    our_room = Room.objects.get(id = pk)
    participants = our_room.participants.all()
    if request.method == "POST":
        Message.objects.create(
            user = request.user, 
            room = our_room, 
            body = request.POST.get('new_comment')
        )
        our_room.participants.add(request.user)
        return redirect('room page', pk = pk)
    comments = our_room.message_set.all()
    context = {'room': our_room, 'comments': comments, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'all_comments': comments, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def create_room(request):
    print("create_room was called with Methord: ", request.method)

    form = RoomForm()
    if request.method == 'POST': 
        print("POST DATA:", request.POST)

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description') 
        )
        
        return redirect('home page')
        
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You Are Not The Host!")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect("home page")
    topics = Topic.objects.all()
    form = RoomForm(instance = room)
    context = {'room': room, 'form': form, 'topics': topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You Are Not The Host!")
    if request.method == "POST":
        print('post req occured')
        room.delete()
        return redirect("home page")
    context = {'obj': room}
    return render(request, "base/delete_form.html", context)

@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Message.objects.get(id = pk)
    if request.user != comment.user:
        return HttpResponse("You Are Not Allowed here!!")
    if request.method == "POST":
        print('post req occured')
        comment.delete()
        return redirect("home page")
    context = {'obj': comment}
    return render(request, "base/delete_form.html", context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance = user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    return render(request, "base/update-user.html", {'form': form})

def browse_topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(
        Q(name__icontains = q) 
    )
    room_count = Room.objects.count()
    context = {'topics': topics, 'room_count': room_count}
    return render(request, 'base/browse_topics.html', context)

def recent_activities(request):
    comments = Message.objects.all()
    context = {'comments': comments}
    return render(request, 'base/recent_activities.html', context)