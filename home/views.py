import datetime
import random
from django.shortcuts import render, redirect

from django.http import HttpResponse
from home.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
import smtplib
from .utils import *
from django.conf import settings

#from django.contrib.auth import get_user_model

#User = get_user_model()

def send_email(request):
    #send_email_client(subject, message, fromEmail, to_list)
    """ subject="TEST EMAIL"
    message="Test EMAIL"
    fromEmail = settings.EMAIL_HOST_USER
    to_list = ['anoopmonu02@gmail.com'] """

    #if file_path located inside the App directory then
    #file_path = f"{settings.BASE_DIR}/concatinated_path_of_file"
    send_email_with_attachment("TEST EMAIL SEND FROM DJANGO", "Mail received using django with attachment",['anoopmonu02@gmail.com'],'C:\\Softwares\\app.py')
    return redirect('/')

@login_required(login_url="/login/")
def home(request):

    Car.objects.create(
        car_name = f"Tata-{random.randint(0,100)}",
        m_year = 2023
        )

    peoples = [
        {'name':'Anoop Kr Chaudhary', 'age':40},
        {'name':'MJ','age':35},
        {'name':'Daksh Chaudhary','age':6},
        {'name':'Kalpana Verma','age':30},
        {'name':'Tanush','age':1}
    ]    
    return render(request, "home/index.html", context={'page':'Django 2023','peoples':peoples})

@login_required
def about(request):
    context = {'page':'About Page'}
    return render(request, "home/about.html", context)

@login_required(login_url="/login/")
def contact(request):    
    Categories = Category.objects.all()
    print(Categories)
    
    context = {'page':'Contact Page','Categories':Categories}
    if request.method == 'POST':
        data = request.POST
        print(data)
        categoryId = data.get('category')
        print(categoryId)
        print("----------------------------------")
        categories = Category.objects.get(id=categoryId)
        anniversary_data = data.get('anniversary')
        aniDate = None
        if anniversary_data:
            try:
                aniDate = datetime.strptime(anniversary_data, '%Y-%m-%d').date()                
            except ValueError:
                # Handle the case where the date format is invalid
                # You might want to log an error or handle it in a way that makes sense for your application
                pass
        else:
            aniDate = None
        print(categories)
        print(aniDate)
        PhoneBook.objects.create(
            name = data.get('name'),
            age = data.get('age'),
            dob = data.get('dob'),
            email = data.get('email'),
            mobile = data.get('mobile'),
            category = categories,
            anniversary = aniDate
        )
        return redirect("/contact/", context)
    
    
    return render(request, "home/contact.html", context)

def addContact(request):
    print("Saving values")
    if request.method == 'POST':
        data = request.POST
        print(data)
        categories = Category.get(data.get('category'))
        print(categories)
        PhoneBook.objects.create(
            name = data.get('name'),
            age = data.get('age'),
            dob = data.get('dob'),
            email = data.get('email'),
            mobile = data.get('mobile'),
            category = data.get('category'),
            anniversary = data.get('anniversary')
        )
    return render(request, "home/contact.html")
    #return render(request, "contact_list.html")

@login_required
def contacts(request):
    contacts = PhoneBook.objects.all()
    if request.GET.get('search_name'):
        contacts = contacts.filter(name__icontains=request.GET.get('search_name'))
    context = {'page':'Contact List Page','contacts':contacts}
    print(contacts)
    return render(request, "home/contact_list.html", context)

@login_required
def delete_contact(request, id):
    delContactObj = PhoneBook.objects.get(id=id)
    delContactObj.delete()
    return redirect("/contact/")

@login_required
def update_contact(request, id):
    updateContactObj = PhoneBook.objects.get(id=id)
    Categories = Category.objects.all()
    print(request.method)
    if request.method == "POST":
        data = request.POST
        categoryId = data.get('category')
        categories = Category.objects.get(id=categoryId)
        print(categoryId)
        print("----------------------------",categories," PhoneBook OBject ",updateContactObj)
        updateContactObj.name = data.get('name')
        updateContactObj.age = data.get('age')
        updateContactObj.dob = data.get('dob')
        updateContactObj.email = data.get('email')
        updateContactObj.mobile = data.get('mobile')
        updateContactObj.category = categories
        updateContactObj.anniversary = data.get('anniversary')
        updateContactObj.save()

        phoneBooks = PhoneBook.objects.all()
        context={'phoneBooks':phoneBooks}
        return redirect("/contacts/")
    context={'phoneBook':updateContactObj, 'Categories':Categories}    
    return render(request, "home/update_contacts.html", context)

@login_required
def search(request, search_text):
    phoneBooks = PhoneBook.objects.all()
    context={'phoneBooks':phoneBooks}
    return redirect('home/contact_list.html',context)

def login_page(request):
    if request.method == "POST":
        data = request.POST
        print("Data: ",data)
        username = data.get('username')        
        password = data.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            print("User Found")
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Invalid credential!")
                return redirect("/login/")
            else:
                login(request, user)
                return redirect('/contacts/')
        else:
            messages.error(request, "Invalid username!")
            return redirect("/login/")
        
    return render(request, "login.html")

@login_required
def logout_page(request):
    print("Request: ", request)
    logout(request)
    return redirect("/login/")


def register(request):
    if request.method == "POST":
        data = request.POST
        print("Data: ",data)
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        user = User.objects.filter(username=username)
        print("user found:",user)
        if user.exists():
            messages.warning(request, "Username already taken.")
            return redirect('/register/')
        
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name
            )
        user.set_password(password)
        user.save()
        print("User Saved")
        messages.success(request, "Username successfully created.")
        return redirect('/register/')
    return render(request, "register.html")

def get_student_data(request):
    qs = Student.objects.all()

    if request.GET.get('search'):
        skey = request.GET.get('search')
        qs = qs.filter(
        Q(student_name__icontains=skey)|
        Q(student_age__icontains=skey)|
        Q(student_id__student_id__icontains=skey)|
        Q(department__department_name__icontains=skey)
        )

    p = Paginator(qs, 15)
    page_number = request.GET.get("page",1)
    page_obj = p.get_page(page_number)
    return render(request, 'report/students.html', {'qs':page_obj})

from .fakedata import generate_reprt_card
def see_marks(request, student_id):
    #generate_reprt_card()
    print(f"Student: {student_id}--")
    qs = SubjectMarks.objects.filter(student__student_id__student_id__exact=f"{student_id}")
    print(len(qs))
    total_marks = qs.aggregate(total_marks = Sum('marks'))
    

    return render(request, "report/see_marks.html", {"qs":qs,"total_marks":total_marks})


def ormMethodSample(request):
    data = Student.objects.all()
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)
    
    return render(request, "home/query.html",{"data":data})

# OR Qry Example using Q
def ormMethodSample1(request):
    data = Student.objects.filter(
        Q(student_name__startswith="Alex") | ~Q(student_age__gt=30)
        )
     
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    # OR Qry Example using Q
    return render(request, "home/query.html",{"data":data})

# And Qry Example using Q
def ormMethodSample2(request):
    #And operation
    data = Student.objects.filter(student_name__startswith="Alex") & Student.objects.filter(student_age=22)
    #And operation using Q
    data = Student.objects.filter(Q(student_name__startswith="Alex") & Q(student_age__gt=22))
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})

# Union Qry Example
def ormMethodSample3(request):
    data = Subject.objects.all().values_list("subject_name").union(Car.objects.all().values_list("car_name"))
    
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})

# Not Qry Example
def ormMethodSample4(request):
    #Not operation may handle via exclude or filter ~Q
    data = Student.objects.filter(~Q(student_name__icontains="alex"))
    
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})


# Simple Qry Field Selection Example
def ormMethodSample5(request):
    data = Student.objects.filter(student_age__gte=25).only('student_name','student_age')
    
    print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})


# Simple raw Qry Example
def ormMethodSample6(request):
    qry = "SELECT * FROM home_student WHERE student_age>=35"
    data = Student.objects.raw(qry)[:5]
    
    #print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})

# Bypass ORM Example
def ormMethodSample7(request):
    cursor = connection.cursor()
    qry = "SELECT count(*) FROM home_student"
    #data = Student.objects.raw(qry)[:5]
    cursor.execute(qry)
    data = cursor.fetchone()
    #print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})

def dictFetchAll(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

# Bypass ORM Example fetchAll 
def ormMethodSample8(request):
    cursor = connection.cursor()
    qry = "SELECT * FROM home_student WHERE student_age>=35 and department_id=3"
    cursor.execute(qry)
    #data = cursor.fetchall()
    data  = dictFetchAll(cursor)
    #print(data.query) # to return sql query
    print(f"---------------------------------{data}")
    #It Will return qry details like time execution time, query etc.
    print(connection.queries)

    return render(request, "home/query.html",{"data":data})