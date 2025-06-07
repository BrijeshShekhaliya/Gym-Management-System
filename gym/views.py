from contextlib import redirect_stderr
from dbm import error

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VideoUploadForm
from .models import VideoUpload
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Plan, Member
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VideoUpload
from .forms import VideoUploadForm
# Create your views here.


def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')


def Index(request):
    if not request.user.is_staff:
        return redirect('admin_login')  # Redirect non-staff users to the login page

    # Get the total counts for members, enquiries, equipment, and enquiry logins
    total_members = Member.objects.count()
    total_enquiries = Enquiry.objects.count()
    total_equipment = Equipment.objects.count()
    total_enquiry_logins = Enquiry_Login.objects.count()

    # Get the latest member (most recently added member)
    latest_member = Member.objects.latest('joindate') if Member.objects.exists() else None

    # Get the latest enquiry (most recent enquiry)
    latest_enquiry = Enquiry.objects.latest('id') if Enquiry.objects.exists() else None

    # Get the latest Enquiry Login User
    latest_enquiry_login = Enquiry_Login.objects.latest('id') if Enquiry_Login.objects.exists() else None

    # Render the admin dashboard template with the context
    return render(request, 'index.html', {
        'total_members': total_members,
        'total_enquiries': total_enquiries,
        'total_equipment': total_equipment,
        'total_enquiry_logins': total_enquiry_logins,
        'latest_member': latest_member,
        'latest_enquiry': latest_enquiry,
        'latest_enquiry_login': latest_enquiry_login,
        'user': request.user,  # Pass the logged-in user
    })

def Admin_Login(request):
    if not request.user.is_authenticated:
        error = None
        if request.method == 'POST':
            u = request.POST['uname']
            p = request.POST['pwd']
            user = authenticate(username=u, password=p)
            try:
                if user.is_staff:
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        d = {'error': error}
        return render(request, 'login.html', d)
    else:
        if request.user.is_staff:
            return redirect('home')
        else:
            return redirect('user_home')


def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    logout(request)
    return redirect('admin_login')


def Add_Equipment(request):
    error=""
    if not  request.user.is_staff:
        return redirect('admin_login')
    if request.method=="POST":
        n = request.POST['name']
        p = request.POST['price']
        u = request.POST['unit']
        d = request.POST['date']
        de = request.POST['description']
        try:
            Equipment.objects.create(name=n,price=p,unit=u,date=d,description=de)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request , 'add_equipment.html' , d)


def View_Equipment(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    equipment = Equipment.objects.all()
    d = {'equipment':equipment}
    return render(request , 'view_equipment.html' , d)

def Delete_Equipment(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    equipment = Equipment.objects.get(id=pid)
    equipment.delete()
    return redirect('view_equipment')



def Add_Plan(request):
    error=""
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method=="POST":
        n = request.POST['name']
        a = request.POST['amount']
        d = request.POST['duration']
        try:
            Plan.objects.create(name=n,amount=a,duration=d)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request , 'add_plan.html' , d)


def View_Plan(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    plan = Plan.objects.all()
    d = {'plan':plan}
    return render(request , 'view_plan.html' , d)

def Delete_Plan(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    plan = Plan.objects.get(id=pid)
    plan.delete()
    return redirect('view_plan')


@login_required(login_url='user_login')  # Redirect to login page if not authenticated
def Add_Member(request):
    error = ""
    plan1 = Plan.objects.all()

    # Check if the user is not an admin (non-staff)
    if not request.user.is_staff:
        # Check if the user has submitted within the last 60 days
        last_submission = Member.objects.filter(user=request.user).order_by('-submission_date').first()

        if last_submission and last_submission.submission_date >= timezone.now() - timedelta(days=60):
            # If within 60 days, set error message and prevent form submission
            error = "You can only submit the form once every 60 days."

    # Proceed with form processing if no restriction applies (either admin or 60 days limit not reached)
    if request.method == "POST" and error == "":
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        p = request.POST['plan']
        j = request.POST['joindate']
        ex = request.POST['expiredate']
        i = request.POST['initialamount']

        plan = Plan.objects.filter(name=p).first()
        try:
            # Save the new member record with the current user and submission date
            Member.objects.create(
                user=request.user,  # Associate the member with the current user
                name=n,
                contact=c,
                emailid=e,
                age=a,
                gender=g,
                plan=plan,
                joindate=j,
                expiredate=ex,
                initialamount=i,
                submission_date=timezone.now()  # Set the submission date to now
            )
            error = "no"
        except:
            error = "yes"

    context = {'error': error, 'plan': plan1}
    return render(request, 'add_member.html', context)

def View_Member(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    member = Member.objects.all()
    d = {'member':member}
    return render(request , 'view_member.html' , d)

def Delete_Member(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    member= Member.objects.get(id=pid)
    member.delete()
    return redirect('view_member')

def Add_Request(request):
    error=""
    if request.method=="POST":
        n = request.POST['name']
        g = request.POST['gender']
        a = request.POST['age']
        m = request.POST['mobileno']
        e = request.POST['emailid']
        try:
            Enquiry_Login.objects.create(name=n,gender=g,age=a,mobileno=m,emailid=e)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request , 'add_request.html' , d)

def View_Request(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    r= Enquiry_Login.objects.all()
    d = {'r':r}
    return render(request, 'view_request.html', d)

def Delete_Request(request,pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    request= Enquiry_Login.objects.get(id=pid)
    request.delete()
    return redirect('view_request')


@login_required(login_url='user_login')  # Ensure user is logged in
def view_member_details(request):
    user = request.user
    if user.is_staff:
        members = Member.objects.all()  # Admin can see all members
    else:
        members = Member.objects.filter(user=user)  # Regular users see only their details
    return render(request, 'member_detail.html', {'members': members})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user  # Associate the video with the logged-in user
            video.save()
            return redirect('view_videos')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

@login_required
def view_videos(request):
    videos = VideoUpload.objects.filter(user=request.user)
    return render(request, 'view_videos.html', {'videos': videos})




