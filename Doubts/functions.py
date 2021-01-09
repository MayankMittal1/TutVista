from django.db import connection
def return_id(a):
    if a=="Q":
        with connection.cursor() as cursor:
            cursor.execute("select id from Doubts_Question order by id desc")
            b=cursor.fetchone()
            if b is None:
                return 0
            else:
                return b[0]+1
    elif a=="A":
        with connection.cursor() as cursor:
            cursor.execute("select id from Doubts_Answer order by id desc")
            b=cursor.fetchone()
            if b is None:
                return 0
            else:
                return b[0]+1
    elif a=="comment_q":
        with connection.cursor() as cursor:
            cursor.execute("select id from Doubts_Comment_question order by id desc")
            b=cursor.fetchone()
            if b is None:
                return 0
            else:
                return b[0]+1
