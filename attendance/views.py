from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance
from .forms import StudentForm, AttendanceForm

# --- Authentication ---
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('student_list')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


# --- Student CRUD ---
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


# --- Attendance ---
@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('attendance_list')
    return render(request, 'attendance_list.html', {'records': records, 'form': form})
