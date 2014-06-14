import os
import array
from datetime import datetime, timedelta
from django.core.context_processors import request
from django.db.utils import ConnectionDoesNotExist
import decimal
from main import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import loader, RequestContext
from main.models import Category, Project, Comment, User, Perk, Atachment, Donation, Message, ObservedProject, Rating,DailyVisit
from main.forms import UserUpdateForm, UserCommentForm, UserCategoryForm, UserForm,MessageForm
from django.db.models import Q, Count
from pp.settings import STATIC_ROOT,STATIC_URL


def index(request):
    template = loader.get_template('index.html')
    now = datetime.now().date()
    deadline_project_list = Project.objects.filter(deadline__gte=now).order_by('deadline')[:3]

    popular_project_list = Project.objects.filter(deadline__gte=now).order_by('-visit_counter')[:3]
    popular_project=list()
    deadline_project=list()
    #wyswietla tylko prjekty niezakonczone, posortowane wzgledem licznika odwiedzin malejąco
    for p in deadline_project_list:
        deadline_project_dictionary={}
        perc = (p.money_raised / p.funding_goal) * 100
        percentage = int(perc)
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
        setattr(p, 'percentage', percentage)
        atachments=Atachment.objects.filter(project=p)
        hasatachment=False
        for a in atachments:
            if "jpg" in a.url or 'png' in a.url or 'gif' in a.url:
                deadline_project_dictionary['Atachment']=a
                hasatachment=True
                break;
        if not hasatachment:
            at=Atachment()
            at.url='project.jpg'
            at.project=p
            deadline_project_dictionary['Atachment']=at
        deadline_project_dictionary['Project']=p
        deadline_project.append(deadline_project_dictionary)
    for p in popular_project_list:
        popular_project_dictionary={}
        perc = (p.money_raised / p.funding_goal) * 100
        percentage = int(perc)
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
        setattr(p, 'percentage', percentage)
        atachments=Atachment.objects.filter(project=p)
        hasatachment=False
        for a in atachments:
            if "jpg" in a.url or 'png' in a.url or 'gif' in a.url:
                popular_project_dictionary['Atachment']=a
                hasatachment=True
                break;
        if not hasatachment:
            popular_project_dictionary['Atachment']=Atachment('project.jpg',p)
        popular_project_dictionary['Project']=p
        popular_project.append(popular_project_dictionary)
    context = RequestContext(request, {
        'deadline_project_list': deadline_project,
        'popular_project_list': popular_project,
    })
    return HttpResponse(template.render(context))

def projects(request):
    order_by = request.GET.get('order_by', '-visit_counter')
    key = request.GET.get('key', '')
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(
        order_by)
    now = datetime.now().date()
    for p in projects_list:
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
        ratinglist=Rating.objects.filter(project=p)
        ratingsum=0
        for r in ratinglist:
            ratingsum+=r.rating
        setattr(p,'overalrating',ratingsum/ratinglist.count())
    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects_list': projects_list,
        'key': key,
    })
    return HttpResponse(template.render(context))


def adminUsers(request):
    typ = 2
    try:
        typ = request.session['type']
    except KeyError:
        pass
    if(typ in {0, 1}):
        template = loader.get_template('admin_users.html')
        user_list = User.objects.all()
        context = RequestContext(request, {'usrs' : user_list, })
        return HttpResponse(template.render(context))
    else:
        return redirect('/')

def adminProjects(request):
    typ = 2
    try:
        typ = request.session['type']
    except KeyError:
        pass
    if(typ in {0, 1}):
        template = loader.get_template('admin_projects.html')
        pro_list = Project.objects.all()
        context = RequestContext(request, {'pros' : pro_list, })
        return HttpResponse(template.render(context))
    else:
        return redirect('/')

def adminComments(request):
    typ = 2
    try:
        typ = request.session['type']
    except KeyError:
        pass
    if(typ in {0, 1}):
        template = loader.get_template('admin_comments.html')
        com_list = Comment.objects.all()
        context = RequestContext(request, {'coms' : com_list, })
        return HttpResponse(template.render(context))
    else:
        return redirect('/')


def adminCategories(request):
    typ = 2
    try:
        typ = request.session['type']
    except KeyError:
        pass
    if(typ == 0):
        template = loader.get_template('admin_categories.html')
        cat_list = Category.objects.all()
        context = RequestContext(request, {'cats' : cat_list, })
        return HttpResponse(template.render(context))
    else:
        return redirect('/')


def moderator(request):
    template = loader.get_template('moderator.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def categories(request):
    order_by = request.GET.get('order_by', 'name')
    cat_list = Category.objects.annotate(count=Count('project__id')).order_by(order_by)

    template = loader.get_template('categories.html')
    context = RequestContext(request, {
        'cat_list': cat_list,
    })
    return HttpResponse(template.render(context))


def projects(request, cat_id="0"):
    order_by = request.GET.get('order_by', '-visit_counter')
    key = request.GET.get('key', '')
    projects_list = Project.objects.filter(Q(title__contains=key) | Q(full_description__contains=key)).order_by(
        order_by)
    catId = int(cat_id)
    if catId > 0:
        projects_list = Project.objects.filter(category__id=catId).order_by(order_by)
    now = datetime.now().date()
    for p in projects_list:
        diff = p.deadline - now
        daysLeft = diff.days
        if daysLeft < 0:
            daysLeft = 0
        setattr(p, 'toEnd', daysLeft)
    template = loader.get_template('projects.html')
    context = RequestContext(request, {
        'projects_list': projects_list,
        'key': key,
    })
    return HttpResponse(template.render(context))


def project(request, pro_id):
    template = loader.get_template('project.html')
    pro = Project.objects.get(id=int(pro_id))
    obs = False
    obsId = 0
    atachments=Atachment.objects.filter(project=pro)
    perks=Perk.objects.filter(project=pro).order_by('amount')
    rating=0
    login=False
    try:
        login=request.session['login']
    except:
        login=False
        pass
    if login:
        user = User.objects.get(login=request.session['login'])
        try:
            o = ObservedProject.objects.get(user=user, project=pro)
            obsId = o.id
            obs = True
        except:
            pass
        try:
            userrate = Rating.objects.get(Q(project__id=pro.id) & Q(user__id=user.id))
        except Rating.DoesNotExist:
            userrate = None
        try:
            rates=Rating.objects.filter(Q(project__id=int(pro.id)))
        except:
            rates=None
        i=int(rates.__len__())
        rating=0
        for rate in rates:
            rating+=rate.rating
        if i!=0:
            rating = rating/i
            rating = int(rating)
    else:
        userrate=False
    coms = Comment.objects.filter(project=pro).order_by('-date_created')
    context = RequestContext(request, {'coms': coms, 'proid': str(pro_id),'project': pro,'atachments': atachments,
                                       'perks': perks, 'obs' : obs, 'obsid' : obsId,'userrate': userrate,'rating':rating})
    return HttpResponse(template.render(context))


def UserRegister(request):
    f = forms.UserRegisterForm()
    context = RequestContext(request, {'formset': f})
    if request.method == 'POST':
        f = forms.UserRegisterForm(request.POST)
        if f.is_valid():
            login = f.cleaned_data.get("login")
            email=f.cleaned_data.get("email")
            password = f.cleaned_data.get("password")
            confirmpassword=f.cleaned_data.get("confirmpassword")
            if password == confirmpassword:
                try:
                    us = User.objects.get(login=f.data['login'])
                except:
                    f.save()
                    return redirect('/', request)
                return redirect('/rejestracja')
                return redirect('/', request)
            else:
                return redirect('/rejestracja')
    else:
        return render_to_response('register.html', context)

def AddNewProject(request):

    if 'login' in request.session:
            user=User.objects.get(login=request.session['login'])
            f = forms.ProjectRegisterForm(prefix='project')
            fr = forms.ProjectPerks(prefix='perk')
            context = RequestContext(request, {'formset': f, 'form1': fr})
            if request.method == 'POST':
                f = forms.ProjectRegisterForm(request.POST, prefix='project')
                p = Project()
                if(f.is_valid()):
                    p.title = f.cleaned_data['title']
                    p.short_description = f.cleaned_data['short_description']
                    p.funding_goal = f.cleaned_data['funding_goal']
                    p.full_description = f.cleaned_data['description']
                    p.category = f.cleaned_data['category']
                    p.user =user
                    p.deadline=datetime.strptime(request.POST['date'],"%d/%m/%Y")
                    Project.save(p)
                    if (request.FILES.getlist('file')!=""):
                        if(not os.path.exists('main'+'\\'+STATIC_ROOT+str(p.id)+'\\'+p.title)):
                             os.mkdir('main'+'\\'+STATIC_ROOT+str(p.id))
                        for file in request.FILES.getlist('file'):
                            l = open('main'+'\\'+STATIC_ROOT+str(p.id)+'\\'+file.name, 'wb+')
                            for chunk in file.chunks():
                                l.write(chunk)
                            l.close()
                            atachment=Atachment()
                            atachment.url=str(p.id)+'/'+file.name
                            atachment.project=p
                            Atachment.save(atachment)
                    for urlfile in request.POST.getlist('urlfile'):
                        atachment=Atachment()
                        atachment.url=urlfile
                        atachment.project=p
                        Atachment.save(atachment)
                    j=0
                    perkvalue=Perk()
                    for perk in request.POST.getlist('perk'):

                        if j==0:
                            perkvalue.project=p
                            perkvalue.title= perk
                            j+=1
                        elif j==1:
                            perkvalue.description=perk
                            j+=1
                        elif j==2:
                            j+=1
                            perkvalue.amount= int(perk)
                        else:
                            j=0
                            try:
                                if not '-' in perk:
                                    perkvalue.number_available=int(perk)
                            except:
                                pass
                            perkvalue.save()
                            perkvalue=Perk()
                return redirect('/', request)
            else:
                return render_to_response('AddNewProject.html', context)
    else:
        return redirect('/logowanie', request)

def EditProject(request, project_id):

    proj=Project.objects.get(id=int(project_id))
    f = forms.ProjectRegisterForm(prefix='project',initial={'title':proj.title,'category':proj.category,'description':proj.full_description,'short_description':proj.short_description,'funding_goal':proj.funding_goal })
    fr = forms.ProjectPerks(prefix='perk')
    atachments=Atachment.objects.filter(project=proj)
    perks=Perk.objects.filter(project=proj).order_by('amount')
    day=proj.deadline.strftime("%d")
    month=proj.deadline.strftime("%m")
    year=proj.deadline.strftime("%Y")
    print(year)
    context = RequestContext(request, {'formset': f, 'form1': fr,'atachments':atachments,'perks':perks,'projectid':proj.id,'day': day,'month':month,'year':year})
    if request.method == 'POST':
        return redirect('/', request)
    return render_to_response('EditProject.html',context)
def saveeditedproject(request,project_id):
    if 'login' in request.session:
        if request.method == 'POST':
            user=User.objects.get(login=request.session['login'])
            f = forms.ProjectRegisterForm(request.POST, prefix='project')
            p = Project.objects.get(id=project_id)
            if(f.is_valid()):
                p.title = f.cleaned_data['title']
                p.short_description = f.cleaned_data['short_description']
                p.funding_goal = f.cleaned_data['funding_goal']
                p.full_description = f.cleaned_data['description']
                p.category = f.cleaned_data['category']
                p.user =user
                p.deadline=p.deadline=datetime.strptime(request.POST['date'],"%d/%m/%Y")
                p.save()
                for removedperk in request.POST.getlist('removedperk'):
                    Perk.objects.get(id=int(removedperk))
                for removedatachment in request.POST.getlist('removedatachment'):
                    atachment=Atachment.objects.get(id=int(removedatachment))
                    if atachment.url.startswith('http') or atachment.url.__contains__('www'):
                        atachment.delete()
                    else:
                        os.remove(STATIC_ROOT+atachment.url)
                        atachment.delete()
                if (request.FILES.getlist('file')!=""):
                    if(not os.path.exists('main'+'\\'+STATIC_ROOT+str(p.id))):
                        os.mkdir(p.title)
                    for file in request.FILES.getlist('file'):
                        l = open('main'+'\\'+STATIC_ROOT+str(p.id)+'\\'+file.name, 'wb+')
                        for chunk in file.chunks():
                            l.write(chunk)
                        l.close()
                        atachment=Atachment()
                        atachment.url=p.id+'\\'+file.name
                        atachment.project=p
                        Atachment.save(atachment)
                for urlfile in request.POST.getlist('urlfile'):
                    atachment=Atachment()
                    atachment.url=urlfile
                    atachment.project=p
                    Atachment.save(atachment)
                j=0
                perkvalue=Perk()
                for perk in request.POST.getlist('perk'):
                    if j==0:
                        perkvalue.project=p
                        perkvalue.title= perk
                        j+=1
                    elif j==1:
                        perkvalue.description=perk
                        j+=1
                    elif j==2:
                        j+=1
                        perkvalue.amount= int(perk)
                    else:
                        j=0
                        if int(perk)>0:
                            perkvalue.number_available=int(perk)
                        perkvalue.save()
                        perkvalue=Perk()
                return redirect('/', request)
            else:
                return redirect('/editproject/'+str(project_id)+'/',request)
        else:
            return redirect('/', request)
    else:
        return redirect('/logowanie', request)
def Signin(request):
    if request.method == 'POST':
        c = forms.Signin(request.POST)
        try:
            us = User.objects.get(login=c.data['login'],password=c.data['password'])
        except:
            return redirect('/logowanie')
        request.session['user'] = us.id
        request.session['login'] = us.login
        request.session['type'] = us.type
        return redirect('/')
    else:
        f = forms.Signin
        return render_to_response('signin.html', RequestContext(request, {'formset': f}))


def addcoment(request, pro_id):
    if request.method == 'POST':
        c = forms.ComentForm(request.POST)
        coment = Comment()
        coment.project = Project.objects.get(id=int(pro_id))
        coment.content = c.data['content']
        coment.user = User.objects.get(id=1)
        coment.save()
        return redirect('/project/' + str(pro_id))
    else:
        f = forms.ComentForm
        return render_to_response('comment.html', RequestContext(request, {'formset': f}))

def Support(request,pro_id):
    template = loader.get_template('support.html')
    projekt = Project.objects.get(id=int(pro_id))
    perk_list = Perk.objects.filter(project=projekt).order_by('amount')
    if perk_list.count()>0:
        zmienna=perk_list[0].amount
    choice_perk_list=Perk.objects.filter(project=projekt).order_by('amount')
    context = RequestContext(request, {
            'perk_list': perk_list,
            'choice_perk_list': choice_perk_list,
            'projekt': projekt,
            'proid': str(pro_id)
            })
    if request.method == 'POST':
        f = forms.SupportForm(request.POST)
        if f.data['amount']:
            if f.is_valid:
               amount=int(f.data['amount'])
               user = request.session['user']
               if amount<zmienna:
                   f = forms.SupportForm
                   return render_to_response('support.html', RequestContext(request, {'formset': f}),context)
               else:
                   for perk in perk_list:
                    if perk.amount<=amount:
                        kwota=perk.amount
                        id=perk.id
                        donation = Donation()
                        donation.amount=decimal.Decimal(f.data['amount'])
                        donation.date=datetime.now().date()
                        donation.user= User.objects.get(id=user)
                        donation.project=Project.objects.get(id=pro_id)
                        donation.perk=Perk.objects.get(id=id)
                        donation.save()
            return redirect('/',request)
        else:
            f = forms.SupportForm
            return render_to_response('support.html', RequestContext(request, {'formset': f}),context)
    else:
        f = forms.SupportForm
        return render_to_response('support.html', RequestContext(request, {'formset': f}),context)


def messages(request):
    try:
        login = request.session['login']
        user = User.objects.get(login=login)
        mes_id = request.GET.get('id', '0')
        mesID = int(mes_id)
        if mesID > 0:
            try:
                userTo = User.objects.get(login=login)
                mes = Message.objects.get(Q(id = mesID) & Q(user_to = userTo))
                mes.delete()
            except:
                bla = "bla"
        messages_list = Message.objects.filter(user_to = user)
        template = loader.get_template('messages.html')
        context = RequestContext(request, {
        'messages_list': messages_list,
        })
        return HttpResponse(template.render(context))
    except:
        return redirect('/')

def newMessage(request, user_id="0"):
    if request.method == 'POST':
        f = forms.MessageForm(request.POST)
        if f.is_valid():
            message = Message()
            message.subject = f.cleaned_data['subject']
            message.content = f.cleaned_data['content']
            message.date_created = datetime.now()
            message.user_to = User.objects.get(login=f.cleaned_data['user_to'])
            try:
                message.user_from = User.objects.get(login=request.session['login'])
            except:
                return redirect('/')
            message.save()
        return redirect('/')
    else:
        f = forms.MessageForm
        userID = int(user_id)
        if userID > 0:
            user = User.objects.get(id=userID)
            f = forms.MessageForm(initial={'user_to' : user.login})
        return render_to_response('new_message.html', RequestContext(request, {'formset': f}))

def message(request, mes_id="0"):
    try:
        login = request.session['login']
        user = User.objects.get(login=login)
        mesID = int(mes_id)
        if mesID > 0:
            try:
                userTo = User.objects.get(login=login)
                mes = Message.objects.get(id = mesID, user_to = userTo)
                template = loader.get_template('message.html')
                context = RequestContext(request, {
                'message': mes,
                })
                return HttpResponse(template.render(context))
            except:
                return redirect('/')
    except:
        return redirect('/')

def UserUpdate(request, uid=-1):
    us = User.objects.get(id=int(uid))
    form = UserUpdateForm(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        return render_to_response('updateCat.html', RequestContext(request, {'formset': form}))

def CommentUpdate(request, uid=-1):
    us = Comment.objects.get(id=int(uid))
    form = UserCommentForm(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        return render_to_response('updateCat.html', RequestContext(request, {'formset': form}))

def CatUpdate(request, uid=-1):
    us = None
    if uid != -1:
      us = Category.objects.get(id=int(uid))
    form = UserCategoryForm(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        return render_to_response('updateCat.html', RequestContext(request, {'formset': form}))

def delUser(request, uid):
    User.objects.get(id=int(uid)).delete()
    return redirect('/')

def delCat(request, uid):
    Category.objects.get(id=int(uid)).delete()
    return redirect('/')

def delCom(request, uid):
    Comment.objects.get(id=int(uid)).delete()
    return redirect('/')

def delPro(request, uid):
    Project.objects.get(id=int(uid)).delete()
    return redirect('/')


def visitors(request,project_id):
    p=Project.objects.get(id=project_id)
    p.visit_counter=p.visit_counter+1
    today = datetime.today()
    p.save()
    try:
        TodayVisitors = DailyVisit.objects.get(project=p, day=today)
        TodayVisitors.visitors=TodayVisitors.visitors+1
        TodayVisitors.save()
    except:
        TodayVisitors = DailyVisit(project=p, day=today)
        TodayVisitors.visitors=1
        TodayVisitors.save()
    return HttpResponse('')


def rate(request, project_id, rate):
    p=Project.objects.get(id=project_id)
    user=User.objects.get(login=request.session['login'])
    r=Rating()
    r.rating=rate
    r.user=user
    r.project=p
    r.save()
    try:
            rates=Rating.objects.filter(Q(project__id=int(p.id)))
    except:
            rates=None
    j=int(rates.__len__())
    rating=0
    for rate in rates:
        rating+=rate.rating
    if j!=0:
        rating = rating/j
    rating = int(rating)

    html='Ocena:<nobr>'
    for i in range(1,6):
        if i>int(rating):
            print(i)
            html += '<img width=\"20\" height=\"20\" src=\"/static/emptystarr.png\" >'
        else:
            print(i)
            html += '<img width=\"20\" height=\"20\" src=\"/static/fillstar.jpg\"  >'
    html+='</nobr><br>'
    print(html)
    return HttpResponse(html)

def logout(request):
    del request.session["user"]
    del request.session["login"]
    del request.session["type"]
    request.session.modified = True
    return redirect('/')

def notices(request):
    try:
        userID = int(request.session['user'])
        user = User.objects.get(id=userID)
        now = datetime.now().date()
        zakonczone = Project.objects.filter(Q(deadline__lte=now) & Q(user=user)).order_by('deadline')
        for zakonczony in zakonczone:
            wplaty = Donation.objects.filter(project=zakonczony)
            setattr(zakonczony, 'liczbaWplat', wplaty.count())
        last_week = datetime.today() - timedelta(days=7)
        komentarze = Comment.objects.filter(Q(project__user=user) & Q(date_created__gte=last_week)).order_by('date_created')[:10]
        zakonczoneObs = ObservedProject.objects.filter(Q(user=user) & Q(project__deadline__lte=now)).order_by('project__deadline')
        komentarzeObs = list()
        obserwowane = ObservedProject.objects.filter(user=user)
        for obserwowany in obserwowane:
            kom = Comment.objects.filter(Q(project=obserwowany.project) & Q(date_created__gte=last_week))[:3]
            komentarzeObs.extend(kom)
        wsparte = Donation.objects.filter(Q(user=user) & Q(project__deadline__lte=now))
        wplaty = Donation.objects.filter(Q(project__user=user) & Q(date__gte=last_week))
    except:
        return redirect('/')
    return render_to_response('notices.html', RequestContext(request, {'zakonczone': zakonczone, 'komentarze':komentarze, 'zakonczoneObs':zakonczoneObs, 'komentarzeObs':komentarzeObs,
                                                                       'wsparte': wsparte, 'wplaty':wplaty}))

def observed(request):
    userID = int(request.session['user'])
    user = User.objects.get(id=userID)
    observedList = ObservedProject.objects.filter(user=user)
    return render_to_response('observed.html', RequestContext(request, {'pros' : observedList}))

def addobserved(request, proid):
    ob = ObservedProject()
    userID = int(request.session['user'])
    user = User.objects.get(id=userID)
    ob.user = user
    pro = Project.objects.get(id=int(proid))
    ob.project = pro
    ob.save()
    return redirect('/project/' + proid)

def delobserved(request, id):
    ObservedProject.objects.get(id=int(id)).delete()
    return redirect('/observed/')

def delobservedp(request, proid):
    userID = int(request.session['user'])
    user = User.objects.get(id=userID)
    pro = Project.objects.get(id=int(proid))
    ObservedProject.objects.get(user=user, project=pro).delete()
    return redirect('/project/' + proid)

def editUser(request):
    us = None
    user_id = request.session['user']
    if user_id != -1:
        us = User.objects.get(id=user_id)
        form = UserForm(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        return render_to_response('user.html', RequestContext(request, {'formset': form}))

def stats(request, pro_id):
    last_month = datetime.today() - timedelta(days=30)
    now = datetime.today()
    projectID = int(pro_id)
    project = Project.objects.get(id=projectID)
    liczbaWplatLista = array.array('i',(0 for i in range(0,31)))
    liczbaWplatMax = int(0)
    for x in range(0, 31):
        data=last_month + timedelta(days=x)
        liczbaWplatWDniu = Donation.objects.filter(Q(project=project) & Q(date__gte=data) & Q(date__lt=data + timedelta(days=1)))
        liczbaWplatLista[x] = liczbaWplatWDniu.count()
        if liczbaWplatWDniu.count() > liczbaWplatMax:
            liczbaWplatMax = liczbaWplatWDniu.count()
    liczbaWplatLabel = str()
    liczbaWplatLabel += str(last_month.day) + '-' + str(last_month.month) + '-' + str(last_month.year)
    for x in range(0, 30):
        liczbaWplatLabel += "|"
    liczbaWplatLabel += str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    liczbaWplatDane = str()
    for liczba in liczbaWplatLista:
        liczbaWplatDane += str(liczba) + ","
    liczbaWplatDane = liczbaWplatDane[:-1]

    kwotaWplatLista = array.array('i',(0 for i in range(0,31)))
    kwotaWplatMax = int(0)
    for x in range(0, 31):
        kwotaWplatLista[x] = int(0)
        data=last_month + timedelta(days=x)
        kwotaWplatWDniu = Donation.objects.filter(Q(project=project) & Q(date__gte=data) & Q(date__lt=data + timedelta(days=1)))
        for wparcie in kwotaWplatWDniu:
            kwotaWplatLista[x] = kwotaWplatLista[x] + wparcie.amount
        if kwotaWplatLista[x] > kwotaWplatMax:
            kwotaWplatMax = kwotaWplatLista[x]
    kwotaWplatLabel = str()
    kwotaWplatLabel += str(last_month.day) + '-' + str(last_month.month) + '-' + str(last_month.year)
    for x in range(0, 30):
        kwotaWplatLabel += "|"
    kwotaWplatLabel += str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    kwotaWplatDane = str()
    for kwota in kwotaWplatLista:
        kwotaWplatDane += str(kwota) + ","
    kwotaWplatDane = kwotaWplatDane[:-1]

    wizytyLista = array.array('i',(0 for i in range(0,31)))
    wizytyMax = int(0)
    for x in range(0, 31):
        wizytyLista[x] = int(0)
        data=last_month + timedelta(days=x)
        if DailyVisit.objects.filter(Q(project=project) & Q(day=data)).count() > 0:
            wizytyWDniu = DailyVisit.objects.get(Q(project=project) & Q(day=data))
            wizytyLista[x] = wizytyWDniu.visitors
            if wizytyLista[x] > wizytyMax:
               wizytyMax = wizytyLista[x]
    wizytyLabel = str()
    wizytyLabel += str(last_month.day) + '-' + str(last_month.month) + '-' + str(last_month.year)
    for x in range(0, 30):
        wizytyLabel += "|"
    wizytyLabel += str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    wizytyDane = str()
    for wizyty in wizytyLista:
        wizytyDane += str(wizyty) + ","
    wizytyDane = wizytyDane[:-1]
    return render_to_response('stats.html', RequestContext(request, {'liczbaWplatLabel': liczbaWplatLabel, 'liczbaWplatDane':liczbaWplatDane, 'liczbaWplatMax': liczbaWplatMax,
                                                                     'kwotaWplatLabel': kwotaWplatLabel, 'kwotaWplatDane':kwotaWplatDane, 'kwotaWplatMax': kwotaWplatMax,
                                                                     'wizytyLabel': wizytyLabel, 'wizytyDane':wizytyDane, 'wizytyMax': wizytyMax}))