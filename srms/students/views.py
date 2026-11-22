from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm

def student_list(request):
    query = request.GET.get('q', '')  # search key

    # filter by name or roll no
    students = Student.objects.filter(name__icontains=query) | Student.objects.filter(roll_no__icontains=query)

    # pagination
    paginator = Paginator(students, 5)  # 5 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'students/student_list.html', context)



def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')
