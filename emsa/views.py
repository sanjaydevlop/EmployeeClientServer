from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from emsa.forms import EmployeeForm
from emsa.models import Employee,MyEmployee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect


def is_staff(user):
    return user.is_authenticated and user.is_staff

# if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             return HttpResponse("Your password and confirm password are not Same!!")
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('login')
        
#     return render (request,'signup.html')

@login_required(login_url='login')
@user_passes_test(is_staff)
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            department = form.cleaned_data['department']
            is_manager = form.cleaned_data.get('is_manager', False)
            manager=form.cleaned_data['manager']
            # Generate the username and password
            username = name.lower().replace(" ", "") + str(age)
            password=form.cleaned_data['contact']
            # Create a new Employee object and set its attributes
            employee =Employee(
                name=name,
                age=age,
                email=email,
                contact=contact,
                department=department,
                is_manager=is_manager,
                manager=manager,
                username=username,
                password=password
            )
            print(employee.manager)
            employee.save()
            group=Group.objects.get(name='myEmployees')
            # employee.groups.add(group)
            # employee=form.save()
            subject = "Congratulations for getting added"
            message = "Dear {name},\n\nCongratulations! You have been added to the company.\n\nYour login credentials are:\nUsername: {username}\nPassword: {password}\n\nBest regards,\nThe Company. Please login Using this Link http://127.0.0.1:8000/elogin/".format(
                name=employee.name,
                username=name.lower().replace(" ", "") + str(age),
                password=employee.contact
            )
            my_user=User.objects.create_user(username,email,password)
            my_user.groups.add(group)
            my_user.save()
            from_email = "sanjaysurya2527@gmail.com"
            recipient_list = [employee.email]
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('show/')  
             
    else:  
        form = EmployeeForm(request.POST)  
    return render(request,'index.html',{'form':form})
@login_required(login_url='login')
@user_passes_test(is_staff)
def employee_list(request):
    employees = Employee.objects.all().order_by('-id')

    context = {'employees': employees}
    return render(request, 'employee_list.html', context)

@login_required(login_url='login')
@user_passes_test(is_staff)
def manager_list(request):
    managers = Employee.objects.filter(is_manager=True).order_by('-id')
    context = {'managers': managers}
    return render(request, 'manager_list.html', context)
@login_required(login_url='login')
@user_passes_test(is_staff)
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            new_department=form.cleaned_data['department']
            employee.department=new_department
            employee.save()
            employee.employees.update(department=new_department)
            # form.save()
            return redirect('/show')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'update_employee.html', {'form': form, 'employee': employee})
@login_required(login_url='login')
@user_passes_test(is_staff)
def delete_employee(request,pk):

    employee = Employee.objects.get(pk=pk)
    user=User.objects.get(username=employee.username)
    user.delete()
    employee.delete()
    return redirect("/show")
@login_required(login_url='login')
@user_passes_test(is_staff)
def search(request):
    query=request.GET['query']  
    employees = Employee.objects.filter(department__icontains=query)  
    return render(request,"search.html",{'employees':employees})
@login_required(login_url='login')
@user_passes_test(is_staff)
def download_page(request):
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="page.html"'
    response.write(request.META['HTTP_REFERER'])
    return response



@login_required(login_url='login')

def HomePage(request):
    employees=Employee.objects.get(username__icontains=request.user.username)
    return render (request,'home.html',{'employees':employees})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        # if(user is not None and request.user.is_staff==True):
        #     login(request,user)
        #     redirect('show')
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def EmployeeLogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    employee=authenticate(request,username=username,password=password)
    if employee is not None:
        # myEmployee=MyEmployee.objects.get(username=username)
        # print(employee.age)
        login(request,employee)
        return redirect('home')
    return render (request,'elogin.html')

    
    # if request.method=='POST':
    #     username=request.POST.get('username')
    #     password=request.POST.get('password')
        
    #     try:
    #         myEmployee=MyEmployee.objects.get(username=username)
    #         if(username==myEmployee.username and password==myEmployee.password):
    #             return HttpResponse("Successfully Logged in")
    #         elif(username!=myEmployee.username or password!=myEmployee.password):
    #             return HttpResponse("Wrong Credentials")
    #     except:
    #         return HttpResponse("Employee Does not exist")
    # return render (request,'elogin.html')
    

def TheHome(request):
    return render('ehome')


def UpdatePassword(request):
    if request.method=='POST':
        user = request.user
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        
        
        if not user.check_password(current_pass):
            return HttpResponse("Your current password is incorrect!")
        
        if new_pass != confirm_pass:
            return HttpResponse("Your new password and confirm password are not the same!")
        employees=Employee.objects.get(username__icontains=request.user.username)
        employees.password=new_pass
        user.set_password(new_pass)
        user.save()
        
        
        update_session_auth_hash(request, user)
        
        return redirect('home')
    
    return render(request, 'update_password.html')



def fun(request):
    print("I am View")
    return HttpResponse("This is Fun Page")


def excp(request):
    
    a=10//10
    return HttpResponse("This is exception Page")