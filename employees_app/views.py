from .models import Employee
from django.views import View
from django.db.models import Q 
from .forms import EmployeeForm
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# checking here user permission
    # res = request.user.has_perm('employees_app.change_employee')
    # print(f'\n {res} \n')

# add employee
def homepage(request):
    
    all_emp = Employee.objects.all()

    paginator = Paginator(all_emp, 5, orphans=1) # paginator obj created
    page_number = request.GET.get('page')        
    page_obj    = paginator.get_page(page_number)

    
    return render(request, 'emp_app/home.html', {'page_obj': page_obj})

def not_found_page(request, *args, **kwargs):
    return HttpResponse({'Error': 'Having Some Error or Invalid Request'})

class AddEmployeeView(LoginRequiredMixin, View):

    def get(self, request):
        form = EmployeeForm()
        return render(request, 'emp_app/add_employee.html', {'form': form})
    
    def post(self, request):
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # fetching all validdated data from form
            ename = form.cleaned_data['name']
            email = form.cleaned_data['email']
            dept  = form.cleaned_data['dept']
            salary = form.cleaned_data['salary']
            epic   = form.cleaned_data['image']
            user = request.user
            # creating employee obj here
            employee_obj = Employee(name = ename, email=email, dept = dept, salary = salary, image = epic, user = user)

            employee_obj.save() # saving data into database

            cache.clear()
            
            messages.success(request, 'Congrats New Employee Successfuly Created!')
            return redirect('homepage') # redirecting at home page

        return render(request, 'emp_app/add_employee.html', {'form': form})

class UpdateeEmployee(LoginRequiredMixin, View):
    def get(self, request,id=None):
                if id is not None and type(id) == int:
                    try:
                        emp  = Employee.objects.get(pk=id)
                    except Employee.DoesNotExist:
                        return redirect('page_not_found')
                    else:
                        if request.user  == emp.user:
                            form = EmployeeForm(instance=emp)
                            return render(request, 'emp_app/update_employee.html',{'form': form})
                        else:
                            messages.success(request, " Sorry! you don't have permission to update this employee data you can Only Update Your Data Only That Your Have Inserted Ok! ")
                            return redirect('homepage')
                             
                else:
                    return redirect('page_not_found')
            
    def post(self, request, id=None):
            if id is not None and type(id) == int:

                try:
                     emp = Employee.objects.get(pk = id)
                except Employee.DoesNotExist:
                     return redirect('page_not_found')
                else:
                    if request.user == emp.user:
                        form  = EmployeeForm(request.POST, request.FILES, instance=emp)

                        if form.is_valid():
                            form.save()
                            cache.clear()

                            messages.success(request, 'Employee Data Succeddfuly Updated!')
                            return redirect('homepage')
                        return render(request, 'emp_app/update_employee.html',{'form': form})
                    else:
                            messages.success(request, " Sorry! you don't have permission to update this employee data you can Only Update Your Data Only That Your Have Inserted Ok! ")
                            return redirect('homepage')
                             
                    
            else:
                return redirect('page_not_found')
        
class DeleteEmployee(LoginRequiredMixin, View):
     def get(self, request, id=None):
        if request.user.is_superuser:
        
            if id is not None and type(id) == int:
                try:
                    emp = Employee.objects.get(pk = id)
                except Employee.DoesNotExist:
                     return redirect('page_not_found')
                else:
                    emp.delete()
                    cache.clear()

                    messages.success(request, 'Employee Data Successfuly Deleted!')
                    return redirect('homepage')
            else:
                return redirect('page_not_found')
        else:
            messages.success(request, "Sorry! You Don't have permissions to delete employees  data! Only Admin(Krishna) Can Delete Data! Thank You!")
            return redirect('homepage')
            

def search_employees(request,by=None, *args, **kwargs):

    search  = request.POST['filters']        # getting keywords to search the data
    
    result = Employee.objects.filter(
        Q(name__icontains = search)|       # name contains
        Q(email__icontains=search) |       # email icontains
        Q(salary__icontains = search)|     # salary icontains       
        Q(dept__name__icontains = search)| # dept name icontains
        Q(join_date__icontains = search))  # joining date icontains
    if result.count() <1:                  # checking result is must greater than or equal 1
        result = Employee.objects.all()    # if no object is found than return all obj

    p = Paginator(result, 5, orphans=1)
    page_number = 1
    page_obj = p.get_page(page_number)

         
    return render(request, 'emp_app/search.html', {'page_obj': page_obj })

def dynamic(request, nm=None):
    # defualt return all 
    emp = Employee.objects.all()
   
    if 'recent' in nm:
        emp  = Employee.objects.all().order_by('-id')
    
    elif 'max' in nm:
        # emp = Employee.objects.get(pk=1)
        # return render(request, 'emp_app/home.html', {'all_emp': emp})

        all = Employee.objects.all()
        max = 0
        for emps in all:
            if emps.salary>max:
                max = emps.salary
        print(f'\n Maximui salary is: {max} ')
        emp  = Employee.objects.filter(salary__gte = max)
   
    elif 'min' in nm:
        all = Employee.objects.all()
        salary = all[0].salary # assuming first object has minimium salary
        for em in all:
            if em.salary<salary:
                salary = em.salary
        
        emp   = Employee.objects.filter(salary__lte=salary)
   
    elif nm is not None:
        emp = Employee.objects.filter(dept__name__icontains=nm)

    if emp.count() < 1:
        emp  = Employee.objects.all()
    
    # creating paginatonation using Paginator class
    p = Paginator(emp, 5, orphans=1)
    page_number  = request.GET.get('page')
    page_obj     = p.get_page(page_number)
    

    return render(request, 'emp_app/home.html', {'page_obj': page_obj})


