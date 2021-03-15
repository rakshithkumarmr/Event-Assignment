from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
import re
from Event import settings as se
from .models import Event , Like
from django.db.models import Case,When
from django.core.paginator import Paginator
from django.contrib.auth import logout

def home(request):
  event = Event.objects.all()
  ids = []
  for x in event:
    ids.append(x.id)
  preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
  data = Event.objects.filter(id__in=ids).order_by(preserved).reverse()
  paginator = Paginator(data, per_page=6)
  page_number = request.GET.get('page', 1)
  page_obj = paginator.get_page(page_number)
  return render(request, 'index.html',{"events": page_obj.object_list, 'paginator': paginator})

def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      from django.contrib.auth import login
      login(request, user)
      return redirect('/')
    else:
        message = "Invalid username or password"
        return render(request, "login.html", {"mess": message})
  return render(request, "login.html")

def signup(request):
  if request.method == "POST":
    email = request.POST['email']
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']
    if User.objects.filter(username=username).exists():
      messages.error(request, "Username is  already taken. please try another one !")
      return redirect('signup')
    if User.objects.filter(email=email).exists():
      messages.error(request, "Email-id is  already taken. please try another one !")
      return redirect('signup')
    if len(username) > 15:
      messages.error(request, "Username must be less tahn 15 characters")
      return redirect('signup')
    if not username.isalnum():
      messages.error(request, "Username should only contain letters")
      return redirect('signup')
    if pass1 != pass2:
      messages.error(request, "Password Do not Match")
      return redirect('signup')
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, pass1)
    if len(pass1) > 5 and len(pass1) < 21:
      if mat:
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.error(request, "Successfully registerd Your Account")
        return redirect('login')
      else:
        messages.error(request,"Password should have at least one uppercase letter,lowercse,one number and one special symbol.")
        return redirect('signup')
    else:
      messages.error(request, "Password lengnth shoul be 6-20.")
      return redirect('signup')
  return render(request, "signup.html")


def logout_user(request):
  logout(request)
  return redirect('/')


def create_event(request):
  if request.user.is_authenticated == True:
    if request.method == "POST":
      title = request.POST['title']
      organizer = request.POST['organizer']
      location = request.POST['location']
      image = request.FILES['image']
      data= Event( img=image, title=title, organizer=organizer,location=location , user=request.user)
      try:
        data.save()
        messages.success(request, "successfully created")
        return render(request, 'create_event.html')
      except:
        mess = "Something went wrong"
        return render(request, 'create_event.html', {"mess": mess})
    return render(request, 'create_event.html')
  else:
    return redirect('login')


def like_post(request):
  user = request.user
  if request.method == 'POST':
    if request.user.is_authenticated == True:
      post_id = request.POST.get('post_id')
      post_obj = Event.objects.get(id=post_id)

      if user in post_obj.liked.all():
        post_obj.liked.remove(user)
      else:
        post_obj.liked.add(user)
      like ,created = Like.objects.get_or_create(user=user, post_id=post_id)

      if not created:
        if like.value == 'Like':
          like.value = 'Unlike'
        else:
          like.value = 'Like'
      like.save()
    else:
      messages.error(request, "Please login first.")
  return redirect('home')


def my_likes(request):
  event = []
  ids = []
  username = request.user
  user_id = User.objects.get(username=username).id
  likes = Like.objects.all()
  for x in likes:
    if user_id == x.user_id:
      if x.value == 'Like':
        ev = Event.objects.filter(id=x.post_id)
        for y in ev.values():
          ids.append(y['id'])
  print(ids)
  event = Event.objects.all()
  return render(request, 'liked.html',{"events":event,"ids":ids})