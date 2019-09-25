from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from apps.wish_app.models import *
import bcrypt

#### github test
def index(request):
    return render(request, 'wish_app/index.html')

def register(request):

    existing_users = User.objects.filter(email=request.POST['email'])
    
    if existing_users:
        return redirect('/')

    if not User.objects.reg_valid(request):
        return redirect('/')
    


    hashed = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())

    new_user = User.objects.create(first_name=request.POST["first_name"],
                                   last_name=request.POST["last_name"],
                                   email=request.POST["email"],
                                   password=hashed)

    request.session["uid"] = new_user.id

    return redirect("/wishes")

def login(request):
    existing_users = User.objects.filter(email=request.POST['email'])

    if existing_users:
        user = existing_users[0]

        pw_matched = bcrypt.checkpw(request.POST['password'].encode(),
                                    user.password.encode())
        if pw_matched:
            request.session['uid'] = user.id
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Please try again")
        return redirect("/")

    return redirect("/wishes")

def logout(request):
    request.session.clear()
    # print('home')
    return redirect('/')

def wishes(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    context ={
        'ungranted': Wish.objects.filter(isGranted=False).filter(wisher=uid),
        'granted':Wish.objects.filter(isGranted=True),
        'user': User.objects.get(id=uid),
        # 'likers_num': Wish.likers.all(),
    }

    return render(request, 'wish_app/wishes.html', context)

def new(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")
    
    context={
        'user': User.objects.get(id=uid),
    }
    return render(request, 'wish_app/new.html',context)

def create_wish(request):
    uid = request.session.get("uid")
    
    if not Wish.objects.wish_valid(request):

        return redirect('wishes/new')

    user = User.objects.get(id=uid)
        
    wish = Wish.objects.create(wish=request.POST['wish'],description=request.POST['description'],isGranted=False,wisher=user)

    return redirect('/wishes')

def edit(request, wish_id):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    info ={
        'user': User.objects.get(id=uid),
        'wish': Wish.objects.get(id=wish_id),
    }
    return render(request,'wish_app/edit.html', info)

def editing(request, wish_id):
        

    if not NewWish.objects.new_wish_valid(request):
        
        return redirect('/wishes/edit/'+ wish_id)

    edit_wish = Wish.objects.get(id=wish_id)
    edit_wish.wish=request.POST['new_wish']
    edit_wish.save()

    edit_wish = Wish.objects.get(id=wish_id)
    edit_wish.description = request.POST['new_description']
    edit_wish.save()

    return redirect('/wishes') 


def grant_wish(request,wish_id):
    wish = Wish.objects.get(id = wish_id)
    wish.isGranted = True
    wish.save()

    return redirect('/wishes')



def remove(request, wish_id):
    del_wish = Wish.objects.get(id=wish_id)
    del_wish.delete()

    return redirect('/wishes')

def stats(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    # print(Wish.objects.filter(isGranted=True).filter(id=uid))
    context={
        'user': User.objects.get(id=uid),
        'granted': Wish.objects.filter(isGranted=True),
        'ur_granted': Wish.objects.filter(isGranted=True).filter(wisher=uid),
        'ur_ungranted': Wish.objects.all().filter(isGranted=False).filter(wisher=uid),
    }

    return render(request, 'wish_app/stats.html',context)


def like(request,wish_id):
    uid = request.session.get('uid')

    if not uid:
        return redirect('/')

    user = User.objects.get(id=uid)
    wish = Wish.objects.get(id=wish_id)

    user.liked_wishes.add(wish)
    # wish.likers.add(user)
    
    print(user.liked_wishes.all())

    return redirect('/wishes')


# def like(request,wish_id):
#     uid = request.session.get('uid')

#     if not uid:
#         return redirect('/')

#     user = User.objects.get(id=uid)
#     wish = Wish.object.filter(id=wish_id).first()

#     if wish is not None:

#         if user in wish.likers.all():
#             wish.likers.remove(user)
#         else:
#             wish.likers.add(user)
#     return redirect('/wishes')




