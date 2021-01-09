from django.forms.utils import ErrorDict
from django.shortcuts import render, redirect,get_object_or_404
from .forms import QuestonForm, RegisterForm, LoginForm, Register_tForm, Login_tForm, AnswerForm, ForgetPass_s
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, Question, Teacher, Answer, get_info
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db import connection
from django.conf import settings 
from django.core.mail import send_mail
from Doubts import functions
import random
import string
# Create your views here.
def rand_pass(size=6):  
    generate_pass = ''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)  
                                            for n in range(size)])
    return generate_pass

def home_r(request):
    return redirect('/home')

def home(request):
    if request.method == 'POST':
        subject = 'Welcome To Tut Vista'
        message = "Hi {}, thank you for contacting TutVista".format(request.POST.get('name').upper())
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [request.POST.get('email'), ] 
        send_mail( subject, message, email_from, recipient_list )
        get_info.objects.create(name=request.POST.get('name'),email=request.POST.get('email'),phone=request.POST.get('phone'),comment=request.POST.get('comment'))
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')

    
def teacher_home(request):
    if request.session.has_key('t'):
        ur=request.session['t']
        teacher = get_object_or_404(Teacher, user=ur)
        ans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=1)
        uans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=0)
        return render(request, 'teacher_home.html', {'ur': ur, 'teacher': teacher,'ans_ques':ans_ques,'uans_ques':uans_ques})
    else:
        return redirect('/login_t', {'error':"Please login to continue"})

def student_home(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        student = get_object_or_404(Student, user=ur)
        ques = Question.objects.all().filter(user_id=ur)
        return render(request, 'student_home.html', {'ur': ur, 'student': student,'ques':ques})
    else:
        return redirect('/login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            try:
                subject = 'Welcome To Tut Vista'
                message = "Hi {}, thank you for registering in TutVista".format(request.POST.get('first_name').upper())
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [request.POST.get('email'), ] 
                send_mail( subject, message, email_from, recipient_list )
            except:
                pass
            messages.success(request, "Successfully saved")
            return  redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'reg_form.html', {'form': form})

def register_t(request):
    if request.method == 'POST':
        form = Register_tForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully saved")
            return  redirect('/login_t')
    else:
        form = Register_tForm()
    return render(request, 'reg_form.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            ur = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            dbuser = Student.objects.filter(user=ur, password=pd)
            if not dbuser:
                return render(request, 'signin.html', {'form': form, 'error':"Invalid Details"})
            else:
                request.session['s'] = ur
                return redirect('/student_home')
    else:
        form = LoginForm()
        return render(request, 'signin.html', {'form': form})


def new_question(request):
    if request.method=='POST' and request.session.has_key('s'):
        ur = request.session['s']
        student = get_object_or_404(Student, user=ur)
        tut="a"
        form = QuestonForm(request.POST, request.FILES)
        if form.is_valid():
            id=functions.return_id("Q")
            with connection.cursor() as cursor:
                cursor.execute("select * from Doubts_Teacher where department=%s order by assigned_count", [request.POST.get('question_dept')])
                a=cursor.fetchone()
                ass=a[6].split(",")
                ass.append(str(id))
                b=",".join(ass)
                cursor.execute("update Doubts_Teacher set assigned_count={}, assigned='{}' where user='{}'".format(int(a[5])+1,b,a[0]))
            question_image=request.FILES.get('question_image')
            
            Question.objects.create(id=id,user_id=student,question_text=request.POST.get('question_text'),question_dept=request.POST.get('question_dept'),question_image=request.FILES.get('question_image'),assigned_teacher=a[0])
        ques = Question.objects.all().filter(user_id=ur)
        return redirect('/student_home')
    elif request.method!='POST':
        ur = request.session['s']
        form = QuestonForm()
        student = get_object_or_404(Student, user=ur)
        return render(request, 'new_question.html', {'ur': ur,'form':form,'student':student})
    else:
        return redirect('/register')


def login_t(request):
    if request.method == 'POST':
        form = Login_tForm(request.POST)
        if form.is_valid():
            ur = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            dbuser = Teacher.objects.filter(user=ur, password=pd)
            if not dbuser:
                return render(request,'signin.html',{'form':form,'error':"Invalid Details"})
            else:
                request.session['t'] = ur
                return redirect('/teacher_home')
    else:
        form = Login_tForm()
        return render(request, 'signin.html', {'form': form})

def answer(request):
    if request.method=='POST' and request.session.has_key('t'):
        q_id=request.GET.get("q_id")
        ur = request.session['t']
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            qq = Answer.objects.filter(question_id=q_id)
            if not qq:
                id=functions.return_id("A")
                Answer.objects.create(question_id=q_id,id=id,answer_text=request.POST.get('answer_text'),answer_image=request.FILES.get('answer_image'))
                with connection.cursor() as cursor:
                    cursor.execute("update Doubts_Question set ans_id='{}', answered = 1 where id='{}'".format(id,q_id))
            else:
                Answer.objects.filter(question_id=q_id).delete()
                id=functions.return_id("A")
                Answer.objects.create(question_id=q_id,id=id,answer_text=request.POST.get('answer_text'),answer_image=request.FILES.get('answer_image'))
                with connection.cursor() as cursor:
                    cursor.execute("update Doubts_Question set ans_id='{}', answered = 1 where id='{}'".format(id,q_id))
        instance = get_object_or_404(Teacher, user=ur)
        ans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=1)
        uans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=0)
        return redirect('/teacher_home')
    elif request.method!='POST'and request.session.has_key('t'):
        ur = request.session['z']
        form = AnswerForm()
        return render(request, 'answer.html', {'ur':ur, 'form': form})
    else:
        return redirect('/login')

def view_answer(request):
    if request.session.has_key('t'):
        ur = request.session['t']
        ans_id=request.GET.get("aid")
        q_id=request.GET.get("qid")
        answer=Answer.objects.filter(id=ans_id)[0]
        question=Question.objects.filter(id=q_id)[0]
        instance=Teacher.objects.filter(user=ur)[0]
        return render(request,"view_answer.html",{'answer':answer, 'instance':instance})

    elif request.session.has_key('s'):
        ur = request.session['s']
        ans_id=request.GET.get("aid")
        q_id=request.GET.get("qid")
        answer=Answer.objects.filter(id=ans_id)[0]
        question=Question.objects.filter(id=q_id)[0]
        instance=Student.objects.filter(user=ur)[0]
        return render(request,"view_answer_s.html",{'answer':answer, 'instance':instance})
    else:
        return redirect('/login')

def profile(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        student=Student.objects.filter(user=ur)[0]
        return render(request,'updateprofile_s.html',{'student':student})
    else:
        return redirect('/login')

def profile_t(request):
    if request.session.has_key('t'):
        ur=request.session['t']
        teacher=Teacher.objects.filter(user=ur)[0]
        return render(request,'updateprofile_t.html',{'teacher':teacher})
    else:
        return redirect('/login_t')

def update_img(request):
    if request.method=='POST'and request.session.has_key('s'):
        image=request.FILES.get('image')
        ur=request.session['s']
        student=Student.objects.get(user=ur)
        student.image=image
        student.save()
        return redirect('/profile')

    elif request.method=='POST'and request.session.has_key('t'):
        image=request.FILES.get('image')
        ur=request.session['t']
        teacher=Teacher.objects.get(user=ur)
        teacher.image=image
        teacher.save()
        return redirect('/profile_t')
    else:
        return redirect('/home')

def all_questions(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        student=Student.objects.filter(user=ur)[0]
        phy_ques = Question.objects.all().filter(question_dept='Physics')
        chem_ques = Question.objects.all().filter(question_dept='Chemistry')
        math_ques = Question.objects.all().filter(question_dept='Maths')
        return render(request,'all_questions.html',{'student':student,'phy_ques':phy_ques,'chem_ques':chem_ques,'math_ques':math_ques})
    else:
        return redirect('/login')

def logout(request):
    if request.session.has_key('s'):
        request.session.pop('s')
        return redirect('/home')

    elif request.session.has_key('t'):
        request.session.pop('t')
        return redirect('/home')
    else:
        return redirect('/home')

def update_info(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        phone=request.POST.get('phone')
        student=get_object_or_404(Student,user=ur)
        student.first_name=first_name
        student.last_name=last_name
        student.phone=phone
        student.save()
        return redirect('/profile')

    elif request.session.has_key('t'):
        ur=request.session['t']
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        phone=request.POST.get('phone')
        teacher=get_object_or_404(Teacher,user=ur)
        teacher.first_name=first_name
        teacher.last_name=last_name
        teacher.phone=phone
        teacher.save()
        return redirect('/profile_t')
    else:
        return redirect('/home')

def forget_pass(request):
    if request.method == 'POST':
        form = ForgetPass_s(request.POST)
        if form.is_valid():
            ur = form.cleaned_data['username']
            em = form.cleaned_data['email']
            dbuser = Student.objects.filter(user=ur, email=em)[0]
            if not dbuser:
                dbuser = Teacher.objects.filter(user=ur, email=em)[0]
                if not dbuser:
                    return render(request,'signin.html',{'form':form,'error':"No such user Exists"})
                else:
                    ran_pass=rand_pass()
                    subject = 'Reset Password'
                    message = "Hi {}, thank you for contacting TutVista\nYour temporary password is {}.\nGo to profile section to update your password.".format(dbuser.first_name,ran_pass)
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [dbuser.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    user = get_object_or_404(Teacher, user=ur, email=em)
                    user.password=ran_pass
                    user.save()
                    return render(request,'signin.html',{'form':form,'error':"An email has been sent "+ran_pass})
            else:
                ran_pass=rand_pass()
                subject = 'Reset Password'
                message = "Hi {}, thank you for contacting TutVista\nYour temporary password is {}.\n Go to profile section to update your password.".format(dbuser.first_name,ran_pass)
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [dbuser.email, ]
                send_mail( subject, message, email_from, recipient_list )
                user = get_object_or_404(Student, user=ur, email=em)
                user.password=ran_pass
                user.save()
                return render(request,'signin.html',{'form':form,'error':"An email has been sent "+ran_pass})
    else:
        form = ForgetPass_s()
        return render(request, 'signin.html', {'form': form})

def update_pass(request):
    if request.session.has_key('t'):
        ur=request.session['t']
        user = get_object_or_404(Teacher, user=ur)
        user.password=request.POST.get('new_pass')
        user.save()
        return redirect('/profile_t')
    elif request.session.has_key('s'):
        ur=request.session['s']
        user = get_object_or_404(Student, user=ur)
        user.password=request.POST.get('new_pass')
        user.save()
        return redirect('/profile')
