import bcrypt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FriendForm
from .models import Friend, Users
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FriendSerializer

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        user = Users(username=username, email=email, password=hashed)
        user.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

        password_bytes = password.encode('utf-8')
        hashed = user.password.encode('utf-8')

        if bcrypt.checkpw(password_bytes, hashed):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def index(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    friends = Friend.objects.filter(created_by_id=user_id)
    return render(request, 'index.html', {'friends': friends})

def create_friend(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    user = get_object_or_404(Users, id=user_id)

    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.created_by = user
            friend.save()
            return redirect('index')
    else:
        form = FriendForm()

    return render(request, 'friend_form.html', {'form': form})

def update_friend(request, pk):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    friend = get_object_or_404(Friend, pk=pk, created_by_id=user_id)

    if request.method == 'POST':
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FriendForm(instance=friend)

    return render(request, 'friend_form.html', {'form': form})

def delete_friend(request, pk):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    friend = get_object_or_404(Friend, pk=pk, created_by_id=user_id)
    friend.delete()
    return redirect('index')

@api_view(['GET'])
def friends_api(request):
    friends = Friend.objects.all()
    serializer = FriendSerializer(friends, many=True)
    return Response(serializer.data)


