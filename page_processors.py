# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import WorkOrderPage, WorkOrder, Employee, EmployeesPage
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect

from django.forms import extras
from datetimewidget.widgets import DateTimeWidget
from django.forms import TextInput, Textarea

    

class NewEmployeeForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    
class NewWorkOrderForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    title = forms.CharField(required=True)
    description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False)
    completed = forms.BooleanField(required=False)
    time_date = forms.CharField(required=True)
    address = forms.CharField(required=False)
    #finish_time = forms.DateTimeField(required=False)
    price = forms.CharField(required=False)
    send_email = forms.BooleanField(required=False)
	

    

@processor_for(EmployeesPage)
def new_employee_form(request, page):
    form = NewEmployeeForm()
    if request.method == "POST":
        if 'update' in request.POST:
            employee_id = int(request.POST['employee_id'])
            emp_obj = Employee.objects.get(pk=employee_id)
            emp_obj.name = request.POST['employee'] or None
            emp_obj.email = request.POST['email'] or None
            #work_obj.completed = request.POST['work_completed'] or None
            emp_obj.phone = request.POST['phone'] or None

            emp_obj.save(update_fields=['name','email','phone'])
            return redirect('/employees')
        elif 'new_emp' in request.POST:
                form = NewEmployeeForm(request.POST)
                if form.is_valid():
                    p = Employee(name = form.cleaned_data['name'], email = form.cleaned_data['email'], phone = form.cleaned_data['phone'])
                    p.save()
                    return redirect('/employees')
            

              
        else:
            
            emp_id = int(request.POST['employee_id'])
            emp_obj = Employee.objects.get(pk=emp_id)
            emp_obj.delete()
            return redirect('/employees')
    

        
    return {"form": form}



    

            
          
    
    
        
			
    

@processor_for(WorkOrderPage)
def newworkorder_form(request, page):
    form = NewWorkOrderForm()
    form = NewWorkOrderForm(empty_permitted=True)
    if request.method == "POST":
        if 'delete' in request.POST:
            work_id = int(request.POST['work_id'])
            work_obj = WorkOrder.objects.get(pk=work_id)
            work_obj.delete()
            return redirect('/work-orders')
        elif 'update' in request.POST:
            work_id = int(request.POST['work_id'])
            work_obj = WorkOrder.objects.get(pk=work_id)
            work_obj.title = request.POST['title'] or None
            work_obj.description = request.POST['description'] or None
            #work_obj.completed = request.POST['work_completed'] or None
            work_obj.time_date = request.POST['time_date'] or None
            work_obj.address = request.POST['address'] or None
            #work_obj.finish_time = request.POST['finish_time'] or None
            work_obj.price = request.POST['price'] or None
            work_obj.save(update_fields=['title','description','price','time_date','address'])
            return redirect('/work-orders')
        elif 'sendemail' in request.POST:
            from django.core.mail import send_mail
            from django.core.mail import EmailMultiAlternatives
            
            work_id = int(request.POST['work_id'])
            work_obj = WorkOrder.objects.get(pk=work_id)
            work_obj.email_sent = True
            work_obj.save(update_fields=['email_sent'])
            
            emp_name = request.POST['employee']
            emp_obj = Employee.objects.get(name=emp_name)
            email = emp_obj.email
             
            title = request.POST['title'] or None
            description = request.POST['description'] or None
            completed = request.POST['work_completed'] or None
            time_date = request.POST['time_date'] or None
            address = request.POST['address'] or None
            price = request.POST['price'] or None
            
            subject, from_email, to = 'Resolve Work Order', 'enquiries@resolveresidential.co.uk', email
            text_content = "%s \n Hi %s \n %s \n Address: %s \n Time and date: %s  \n Price: %s \n Resolve Residential Limited \n enquiries@resolveresidential.co.uk \n Registered Office: Star House, Star Hill, Rochester, Kent ME1 1UX" % (title, emp_name, description, address, time_date, price)
            html_content = "<html><body style='background:rgb(239, 247, 249); text-align: center;'><h1 style='color:#2FB2C7; text-align:center;'>Resolve Residential Work Order</h1><br><h2> %s </h2><br><h3>Hi <strong> %s </strong></h3><br><p> %s </p><br><p> %s </p><p> %s </p><br><p><strong>  %s</strong></p><br><address style='text-align:center;'><strong>Resolve Residential Limited</strong><br>Registered Office: Star House, Star Hill, Rochester, Kent ME1 1UX<br>Company Registration No: 9412372<br>VAT NO; 206 3534 35<br></address></body></html>" % (title, emp_name, description, address, time_date, price)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            #email_sent = request.POST['send_email'] or None
            
            
            return redirect('/work-orders')
        elif 'workcompleted' in request.POST:
            work_id = int(request.POST['work_id'])
            work_obj = WorkOrder.objects.get(pk=work_id)
            work_obj.completed = False
            work_obj.title = request.POST['title'] or None
            work_obj.description = request.POST['description'] or None
            work_obj.time_date = request.POST['time_date'] or None
            work_obj.price = request.POST['price'] or None
            work_obj.save(update_fields=['title','description','price','time_date','completed'])
            return redirect('/work-orders')
        elif 'worknotcompleted' in request.POST:
            work_id = int(request.POST['work_id'])
            work_obj = WorkOrder.objects.get(pk=work_id)
            work_obj.completed = True
            work_obj.title = request.POST['title'] or None
            work_obj.description = request.POST['description'] or None
            work_obj.time_date = request.POST['time_date'] or None
            work_obj.price = request.POST['price'] or None
            work_obj.save(update_fields=['title','description','price','time_date','completed'])
            return redirect('/work-orders')
      
        else:
            form = NewWorkOrderForm(request.POST)
            if form.is_valid():
                p = form.cleaned_data['employee']
                
                p.workorder.create(title = form.cleaned_data['title'],description = form.cleaned_data['description'],completed = form.cleaned_data['completed'],time_date = request.POST['time_date'],price = form.cleaned_data['price'],email_sent = form.cleaned_data['send_email'],address = form.cleaned_data['address'])
                p.save()
                email_send = form.cleaned_data['send_email']
                if email_send == True:
                    from django.core.mail import send_mail
                    from django.core.mail import EmailMultiAlternatives
                    
                    emp = Employee.objects.get(pk = p.id)
                    emp_name = emp.name
                    email = emp.email

                    title = request.POST['title'] or None
                    description = request.POST['description'] or None
                    
                    time_date = request.POST['time_date'] or None
                    address = request.POST['address'] or None
                    price = request.POST['price'] or None

                    subject, from_email, to = 'Resolve Work Order', 'bapp@bapp.skru.webfactional.com', 'skruproxy@gmail.com'
                    text_content = "%s \n Hi %s \n %s \n Address: %s \n Time and date: %s  \n Price: %s \n Resolve Residential Limited \n enquiries@resolveresidential.co.uk \n Registered Office: Star House, Star Hill, Rochester, Kent ME1 1UX" % (title, emp_name, description, address, time_date, price)
                    html_content = "<html><body style='background:rgb(239, 247, 249); text-align: center;'><h1 style='color:#2FB2C7; text-align:center;'>Resolve Residential Work Order</h1><br><h2> %s </h2><br><h3>Hi <strong> %s </strong></h3><br><p> %s </p><br><p> %s </p><p> %s </p><br><p><strong>  %s</strong></p><br><address style='text-align:center;'><strong>Resolve Residential Limited</strong><br>Registered Office: Star House, Star Hill, Rochester, Kent ME1 1UX<br>Company Registration No: 9412372<br>VAT NO; 206 3534 35<br></address></body></html>" % (title, emp_name, description, address, time_date, price)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    
                
                return redirect('/work-orders')
    
    return {"form": form}
