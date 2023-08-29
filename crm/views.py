# crm/views.py
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .models import Customer
from .models import QuizQuestion
from .models import Certificate
from .models import Document
from .forms import DocumentForm
from django.contrib import messages #import messages
from datetime import datetime
import json

def home(request):
    return render(request, 'crm/home.html')

def faq(request):
    return render(request, 'crm/FAQ.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'crm/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'crm/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def customer_list(request):
    customers = Customer.objects.filter(user=request.user)
    invoices = {}
    for customer in customers:
        html_content = render(request, 'crm/customer_invoice.html', {'customer': customer,'inv_no':"%06d" % customer.id, 'currentDate': datetime.today().strftime('%d-%m-%Y')}).content
        base64_content = base64.b64encode(html_content).decode('utf-8')
        invoices[customer.id] = base64_content
    invoices = json.dumps(invoices)
    return render(request, 'crm/customer_list.html', {'customers': customers, 'invoices': invoices})

def add_customer(request):
    if request.method == 'POST':
        # Process the form data and save the new customer record
        # For simplicity, assume the form has fields: name, email, phone, address, etc.
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        user = request.user 
        customer = Customer.objects.create(name=name, email=email, phone=phone, address=address, user=user)
        return redirect('customer_list')
    return render(request, 'crm/add_customer.html')

def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        # Process the form data and update the existing customer record
        # For simplicity, assume the form has fields: name, email, phone, address, etc.
        customer.name = request.POST['name']
        customer.email = request.POST['email']
        customer.phone = request.POST['phone']
        customer.address = request.POST['address']
        customer.save()
        return redirect('customer_list')
    return render(request, 'crm/edit_customer.html', {'customer': customer})

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'crm/delete_customer.html', {'customer': customer})

def about(request):
    if request.method == 'POST':
        score = 0
        # Get the submitted answers and calculate the score
        for question in QuizQuestion.objects.all():
            submitted_answer = request.POST.get(f'question_{question.id}')
            print(question.get_correct_answer())
            if submitted_answer == question.get_correct_answer():
                score += 1
        # Check if the user achieved the required score for the certificate
        required_score = 8  # 80% score required for the certificate
        if (score / QuizQuestion.objects.count()) * 10 >= required_score:
            # Create and save the certificate for the user
            messages.success(request, "Congratulations! You Have Earned The Certificate.")
            # You can also generate and save a PDF certificate here if needed
        else:
            messages.error(request, "No Certificates Have Been Earned Please Try Again.")
        certificate = Certificate.objects.update_or_create(user=request.user,defaults={'score':score,'date_issued':datetime.now()})
        return redirect('about')
    else:
        # Get all the quiz questions and display them on the about page
        quiz_questions = QuizQuestion.objects.all()
        certificate = Certificate.objects.filter(user= request.user.id).first()
        return render(request, 'crm/about.html', {'quiz_questions': quiz_questions, 'certificate': certificate})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'crm/upload_document.html', {'form': form})

def document_list(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'crm/document_list.html', {'documents': documents})

def delete_document(request, document_id):
    # Get the document object based on the document_id
    document = get_object_or_404(Document, id=document_id)

    if request.method == 'POST':
        # Delete the document and redirect to the document list page
        document.delete()
        return redirect('document_list')

    return render(request, 'crm/delete_document.html', {'document': document})