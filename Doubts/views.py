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
a=''
register_mail="Welcome to the TutVista family. Thank you for registering yourself with us.\nBefore you begin with your journey here, do update your profile by filling up the required credentials. We at TutVista are building an engaged community of teacher-student so that the doubts of every student do not remain unanswered and they could be more confident in applying their concepts.\nNow that you are here, try out by asking a sample doubt from one of our tutors so that you might get comfortable with the interface. Be respectful in your language while you ask your doubts from your tutors. In case you have any doubts regarding the functionality of the doubt portal, do not hesitate to get in touch with us.\nHappy Doubt-Solving\nTutVista Team"
get_info_t="Hi {}, thank you for contacting TutVista.\nTutVista is a free online doubt-clearing platform created by Hypertext Assassins, a development and coding group from IIT Roorkee. We at TutVista aspire to help each and every student who is facing problems during this ongoing pandemic. Many students have complained about difficulties in studying as they are not being able to clear their doubts on a particular topic due to the lack of face-to-face interaction with their teachers. This is where platforms like TutVista can help a student by a lot. Any student between the classes of 9 to 12 can ask any doubt from Physics, Chemistry or Mathematics and we can guarantee a reply within 24 hours by anyone of our many competent tutors.\nA student can register/login by clicking on the “Student Portal” option on the top right of the home screen and then filling the necessary details. Then, after logging in, on his dashboard there would be a blue button called “Add Question”, clicking on which would allow the student to ask any doubt he/she has. There is also an option for “All Questions”. By this the student would be able to view all the questions asked by all the students throughout the country which has been answered by our tutors.\nFor further information you can contact us by sending an email to tutvista@gmail.com. Till then, keep your curiosity flowing and never stop asking questions!\nHappy Doubt-Solving,\nTutVista Team."
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
        message = get_info_t.format(request.POST.get('name').upper())
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
        teacher = get_object_or_404(Teacher, username=ur)
        ans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=1)
        uans_ques = Question.objects.all().filter(assigned_teacher=ur, answered=0)
        return render(request, 'teacher_home.html', {'ur': ur, 'teacher': teacher,'ans_ques':ans_ques,'uans_ques':uans_ques})
    else:
        return redirect('/login_t', {'error':"Please login to continue"})

def student_home(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        student = get_object_or_404(Student, username=ur)
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
                message = "Hi {},\n".format(request.POST.get('first_name').upper())
                message=message+register_mail
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
            dbuser = Student.objects.filter(username=ur, password=pd)
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
        student = get_object_or_404(Student, username=ur)
        tut="a"
        form = QuestonForm(request.POST, request.FILES)
        if form.is_valid():
            id=functions.return_id("Q")
            teachers=Teacher.objects.filter(department=request.POST.get('question_dept')).order_by('assigned_count')
            teacher=teachers[0]
            ass=teacher.assigned.split(",")
            ass.append(str(id))
            b=",".join(ass)
            teacher.assigned_count=teacher.assigned_count+1
            teacher.assigned=b
            Question.objects.create(id=id,user_id=student,question_text=request.POST.get('question_text'),question_dept=request.POST.get('question_dept'),question_image=request.FILES.get('question_image'),assigned_teacher=teacher.username)
            teacher.save()
            question_image=request.FILES.get('question_image')
        ques = Question.objects.all().filter(user_id=ur)
        return redirect('/student_home')
    elif request.method!='POST':
        ur = request.session['s']
        form = QuestonForm()
        student = get_object_or_404(Student, username=ur)
        return render(request, 'new_question.html', {'ur': ur,'form':form,'student':student})
    else:
        return redirect('/register')


def login_t(request):
    if request.method == 'POST':
        form = Login_tForm(request.POST)
        if form.is_valid():
            ur = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            dbuser = Teacher.objects.filter(username=ur, password=pd)
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
                question=get_object_or_404(Question,id=q_id)
                question.ans_id=id
                question.answered=1
                question.save()
            else:
                return redirect('/teacher_home')
        return redirect('/teacher_home')
    elif request.method!='POST'and request.session.has_key('t'):
        ur = request.session['t']
        form = AnswerForm()
        return render(request, 'answer.html', {'ur':ur, 'form': form})
    else:
        return redirect('/login')

def view_answer(request):
    if request.session.has_key('t'):
        ur = request.session['t']
        ans_id=request.GET.get("aid")
        q_id=request.GET.get("qid")
        answer=get_object_or_404(Answer,id=ans_id)
        instance=get_object_or_404(Teacher,username=ur)
        return render(request,"view_answer.html",{'answer':answer, 'instance':instance})

    elif request.session.has_key('s'):
        ur = request.session['s']
        ans_id=request.GET.get("aid")
        q_id=request.GET.get("qid")
        answer=get_object_or_404(Answer,id=ans_id)
        instance=get_object_or_404(Student,username=ur)
        return render(request,"view_answer_s.html",{'answer':answer, 'instance':instance})
    else:
        return redirect('/login')

# def comment_ques(request):
#     q_id=request.GET.get("qid")
#     if request.method=='POST' and request.session.has_key('z'):
#         ur = request.session['z']
#         form = Comment_qForm(request.POST)
#         if form.is_valid():
#             Comment_question.objects.create(question_id=q_id, id=functions.return_id("comment_q"),comment_text=request.POST.get("comment_text"))
#         comments=Comment_question.objects.filter(question_id=q_id)
#         return render(request,'comment.html', {'ur':ur, 'form': form,'comments':comments})
#     elif request.method!='POST':
#         ur = request.session['z']
#         form = Comment_qForm()
#         comments=Comment_question.objects.filter(question_id=q_id)
#         return render(request,'comment.html', {'ur':ur, 'form': form,'comments':comments})


# def comment_ans(request):
#     a_id=request.GET.get("aid")
#     if request.method=='POST' and request.session.has_key('z'):
#         ur = request.session['z']
#         form = Comment_aForm(request.POST)
#         if form.is_valid():
#             Comment_answer.objects.create(answer_id=a_id, id=functions.return_id("comment_a"),comment_text=request.POST.get("comment_text"))
#         comments=Comment_answer.objects.filter(answer_id=a_id)
#         return render(request,'comment.html', {'ur':ur, 'form': form,'comments':comments})
#     elif request.method!='POST':
#         ur = request.session['z']
#         form = Comment_aForm()
#         comments=Comment_answer.objects.filter(answer_id=a_id)
#         return render(request,'comment.html', {'ur':ur, 'form': form,'comments':comments})
def profile(request):
    global a
    if request.session.has_key('s'):
        error=""
        if a=="error":
            error="Old password is incorrect"
        if a=="success":
            error="Password has been updated to new one"
        ur=request.session['s']
        student=Student.objects.filter(username=ur)[0]
        a = ""
        return render(request,'updateprofile_s.html',{'student':student, 'error':error})
    else:
        return redirect('/login')

def profile_t(request):
    global a
    if request.session.has_key('t'):
        error=""
        if a=="error":
            error="Old password is incorrect"
        if a=="success":
            error="Password has been updated to new one"
        ur=request.session['t']
        teacher=Teacher.objects.filter(username=ur)[0]
        a=""
        return render(request,'updateprofile_t.html',{'teacher':teacher, 'error':error})
    else:
        return redirect('/login_t')

def update_img(request):
    if request.method=='POST'and request.session.has_key('s'):
        image=request.FILES.get('image')
        ur=request.session['s']
        student=Student.objects.get(username=ur)
        student.image=image
        student.save()
        return redirect('/profile')

    elif request.method=='POST'and request.session.has_key('t'):
        image=request.FILES.get('image')
        ur=request.session['t']
        teacher=Teacher.objects.get(username=ur)
        teacher.image=image
        teacher.save()
        return redirect('/profile_t')
    else:
        return redirect('/home')

def all_questions(request):
    if request.session.has_key('s'):
        ur=request.session['s']
        student=Student.objects.filter(username=ur)[0]
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
        student=get_object_or_404(Student,username=ur)
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
        teacher=get_object_or_404(Teacher,username=ur)
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
            dbuser = Student.objects.filter(username=ur, email=em)
            if not dbuser:
                dbuser = Teacher.objects.filter(username=ur, email=em)
                if not dbuser:
                    return render(request,'signin.html',{'form':form,'error':"No such user Exists"})
                else:
                    dbuser=dbuser[0]
                    ran_pass=rand_pass()
                    subject = 'Reset Password'
                    message = "Hi {}, thank you for contacting TutVista\nYour temporary password is {}.\nGo to profile section to update your password.".format(dbuser.first_name,ran_pass)
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [dbuser.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    user = get_object_or_404(Teacher, username=ur, email=em)
                    user.password=ran_pass
                    user.save()
                    return render(request,'signin.html',{'form':form,'error':"An email has been sent "})
            else:
                dbuser=dbuser[0]
                ran_pass=rand_pass()
                subject = 'Reset Password'
                message = "Hi {}, thank you for contacting TutVista.\nYour temporary password is {}.\n Go to profile section to update your password.".format(dbuser.first_name,ran_pass)
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [dbuser.email, ]
                send_mail( subject, message, email_from, recipient_list )
                user = get_object_or_404(Student, username=ur, email=em)
                user.password=ran_pass
                user.save()
                return render(request,'signin.html',{'form':form,'error':"An email has been sent "+ran_pass})
    else:
        form = ForgetPass_s()
        return render(request, 'signin.html', {'form': form})

def update_pass(request):
    global a
    if request.session.has_key('t'):
        ur=request.session['t']
        user = get_object_or_404(Teacher, username=ur)
        if user.password==request.POST.get('old_pass'):
            user.password=request.POST.get('new_pass')
            user.save()
            a="success"
            return redirect('/profile_t')
        else:
            a="error"
            return redirect('/profile_t')

    elif request.session.has_key('s'):
        ur=request.session['s']
        user = get_object_or_404(Student, username=ur)
        if user.password==request.POST.get('old_pass'):
            user.password=request.POST.get('new_pass')
            user.save()
            a="success"
            return redirect('/profile')
        else:
            a="error"
            return redirect('/profile')
    else:
        return redirect('/home')
def error_404(request,exception):
    return render(request, "error.html")
def error_400(request,exception):
    return render(request, "error.html")
def error_500(request):
    return render(request, "error.html")
def error_403(request,exception):
    return render(request, "error.html")
def about_us(request):
    return render(request,"aboutus.html")