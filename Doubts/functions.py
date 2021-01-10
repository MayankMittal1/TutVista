from django.db import connection
from django.db.models.query import QuerySet
from .models import Student, Question, Teacher, Answer, get_info
def return_id(a):
    if a=="Q":
        b=Question.objects.order_by('id')
        if not b:
            return 0
        else:
            return b[len(b)-1].id+1
    elif a=="A":
        b=Answer.objects.order_by('id')
        if not b:
            return 0
        else:
            return b[len(b)-1].id+1