from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import Student
from results.models import Result
from django.shortcuts import render

def home(request):
    """
    Public home page. No student results listed here.
    """
    return render(request, "home.html")


# Normal dashboard for logged-in users
@login_required(login_url="/accounts/login/")
def dashboard(request):
    # If the user is admin/staff, redirect to admin dashboard
    if request.user.is_staff:
        return redirect("admin_dashboard")
    
    # Regular user dashboard (e.g., students)
    return render(request, "dashboard/dashboard.html")

# Admin dashboard
@login_required(login_url="/accounts/login/")
def admin_dashboard(request):
    # Only allow staff/admin users
    if not request.user.is_staff:
        return redirect("dashboard")
    
    context = {
        "student_count": Student.objects.count(),
        "result_count": Result.objects.count(),
        "students": Student.objects.all(),
        "results": Result.objects.all(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


