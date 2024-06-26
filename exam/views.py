from django.shortcuts import render ,redirect
from .models import Users , ReShows ,CommendsUser
import bcrypt
from django.contrib import messages

def loginPage(request):
    return render(request,'login.html')


def login(request):
    email = request.POST['emailLog']
    password = request.POST['pass']
    user = Users.objects.filter(email=email)
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("TVshows")
        else:
            messages.error(request, 'Incorrect User name or Password')
    else:
        messages.error(request, 'Incorrect User name or Password')
    return redirect('loginPage')


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        messages.error(request, 'Registration failed.')
        return render(request,'login.html', {'errors': errors})
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        messages.success(request, 'Registration successful. You can now log in.')
        return render(request ,"login.html")

def TVshows(request):
    user = Users.objects.get(id = request.session['userid'])
    show = ReShows.objects.all()
    return render(request,'shows.html',{'user':user,'shows':show})

def logout(request):
    if 'userid' in request.session:
        del request.session['userid'] 
    return redirect('loginPage')

def newShow(request):
    user = Users.objects.get(id = request.session['userid'])
    return render(request,'newShow.html',{'user':user})

def addShow(request):
    showsb = ReShows.objects.all
    errors = ReShows.objects.basic_validator(request.POST, is_edit=False)
    if len(errors) > 0:
        return render(request,'newShow.html', {'errors': errors})
    else:
        
        if ReShows.objects.filter(title=request.POST['title']).exists():
            messages.error(request, 'Title must be unique.')
            return render(request,'newShow.html')
        else:
            title = request.POST['title']

        network = request.POST['network']
        releaseDate = request.POST['releaseDate']
        comments = request.POST['comments']
        user = Users.objects.get(id = request.session['userid'])
        tvShow = ReShows.objects.create(title = title , network = network,releaseDate=releaseDate,comments=comments,user=user)
    return redirect('TVshows')

def details(request,Sid):
    user = Users.objects.get(id = request.session['userid'])
    show = ReShows.objects.get(id = Sid)
    com = CommendsUser.objects.all()
    return render(request,'details.html',{'user':user,'show':show,'coms':com})

def addCom(request,Sid):
    user = Users.objects.get(id = request.session['userid'])
    show = ReShows.objects.get(id = Sid)
    com = request.POST['PostcomName']
    CommendsUser.objects.create(user = user , reshow = show,text=com)
    return redirect('details',Sid)

def delCom(request,Cid,Sid):
    com = CommendsUser.objects.get(id = Cid)
    com.delete()
    return redirect('details',Sid)


def edit(request,Sid):
    user = Users.objects.get(id = request.session['userid'])
    show = ReShows.objects.get(id = Sid)
    return render(request,'editShow.html',{'user':user,'show':show})

def editShow(request,Sid):
    show = ReShows.objects.get(id = Sid)
    user = Users.objects.get(id = request.session['userid'])
    if request.method == "POST":
        errors = ReShows.objects.basic_validator(request.POST, is_edit=True)
        if len(errors) > 0:
            return render(request,'editShow.html', {'errors': errors,'show':show})
        else:

            if ReShows.objects.filter(title=request.POST['Etitle']).exists():
                messages.error(request, 'Title must be unique.')
                return render(request,'editShow.html',{'user':user,'show':show})
            else:
                title = request.POST['Etitle']
        
            # title = request.POST['Etitle']
            network = request.POST['Enetwork']
            releaseDate = request.POST['EreleaseDate']
            comments = request.POST['Ecomments']
            
            show.title = title
            show.network = network
            show.releaseDate = releaseDate
            show.comments = comments
            show.save()
            return redirect('TVshows')
    else:
        return redirect('edit',Sid)
    
def delete(request,Sid):
    show = ReShows.objects.get(id = Sid)
    show.delete()
    return redirect('TVshows')