from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Result
from .forms import ResultForm
from students.models import Student


# ---------------------------------------------------------
# ADMIN: Result List (simple list - NOT search page)
# ---------------------------------------------------------
def result_list(request):
    results = Result.objects.all()
    return render(request, "results/result_list.html", {"results": results})


# ---------------------------------------------------------
# ADMIN: Create Result
# ---------------------------------------------------------
def create_result(request):
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("result_list")
    else:
        form = ResultForm()

    return render(request, "results/result_form.html", {"form": form})


# ---------------------------------------------------------
# ADMIN: Edit Result
# ---------------------------------------------------------
def edit_result(request, pk):
    result = get_object_or_404(Result, pk=pk)

    if request.method == "POST":
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect("result_list")
    else:
        form = ResultForm(instance=result)

    return render(request, "results/result_form.html", {"form": form})


# ---------------------------------------------------------
# ADMIN: Delete Result
# ---------------------------------------------------------
def delete_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    result.delete()
    return redirect("result_list")


# =========================================================
# PUBLIC RESULT SEARCH (HOME PAGE)
# =========================================================
def student_result_view(request):
    name = request.GET.get("name")
    roll_no = request.GET.get("roll_no")

    if name and roll_no:
        try:
            student = Student.objects.get(name=name, roll_no=roll_no)
            results = Result.objects.filter(student=student)

            return render(request, "results/student_result.html", {
                "student": student,
                "results": results,
                "error": None
            })

        except Student.DoesNotExist:
            return render(request, "results/student_result.html", {
                "error": "No student found with the provided details.",
                "student": None,
                "results": None
            })

    return render(request, "results/student_result.html", {
        "student": None,
        "results": None,
        "error": None
    })


# =========================================================
# ADMIN: All Results → Search + Pagination Page
# URL: /results/all/
# Template: templates/results/all_results.html
# =========================================================
def all_results(request):
    query = request.GET.get('q', '').strip()

    qs = Result.objects.select_related('student').all().order_by('student__name')

    if query:
        qs = qs.filter(
            Q(student__name__icontains=query) |
            Q(subject__icontains=query) |
            Q(marks__icontains=query)
        )

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "results/result_list.html", {
        "query": query,
        "page_obj": page_obj,
    })