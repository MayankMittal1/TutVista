from .models import Student,Teacher,Question,Answer
from django import forms

dept_choice=["Physics","Chemistry","Mathematics","Computers"]
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'password', 'first_name','last_name','email']
        widgets = {'password': forms.PasswordInput()}
class Register_tForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'password','first_name','last_name', 'email','department']
        widgets = {'password': forms.PasswordInput()}
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class Login_tForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class QuestonForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','question_dept','question_image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text','answer_image','comment']

class ForgetPass_s(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()

