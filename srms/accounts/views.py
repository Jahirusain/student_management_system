from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from students.models import Student
from results.models import Result
from django.db.models import Q



# ------------------------
# LOGIN VIEW
# ------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, "accounts/login.html")


# ------------------------
# LOGOUT VIEW
# ------------------------
def logout_view(request):
    logout(request)
    return redirect("home")  # Redirects to login page



# ------------------------
# CREATE ADMIN (missing function)
# ------------------------
def create_admin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        User.objects.create(
            username=username,
            password=make_password(password),
            is_staff=True,
            is_superuser=True
        )
        return redirect("login")

    return render(request, "accounts/create_admin.html")


from django.shortcuts import render
from django.core.paginator import Paginator
from students.models import Student
from results.models import Result

def admin_dashboard(request):
    # --- STUDENT SEARCH ---
    student_search = request.GET.get('student_search', '')
    students = Student.objects.all()

    if student_search:
        students = students.filter(name__icontains=student_search) | students.filter(roll_no__icontains=student_search)

    # --- STUDENT PAGINATION ---
    student_paginator = Paginator(students, 5)  # 5 rows per page
    student_page_number = request.GET.get('student_page')
    student_page = student_paginator.get_page(student_page_number)

    # --- RESULT SEARCH ---
    result_search = request.GET.get('result_search', '')
    results = Result.objects.select_related('student').all()

    if result_search:
        results = results.filter(student__name__icontains=result_search) | results.filter(subject__icontains=result_search)

    # --- RESULT PAGINATION ---
    result_paginator = Paginator(results, 5)
    result_page_number = request.GET.get('result_page')
    result_page = result_paginator.get_page(result_page_number)

    context = {
        "students": student_page,
        "results": result_page,
        "student_search": student_search,
        "result_search": result_search,
        "student_count": Student.objects.count(),
        "result_count": Result.objects.count(),
    }

    return render(request, "admin_dashboard.html", context)
