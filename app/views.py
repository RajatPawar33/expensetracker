from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            Q(email = email) |  Q(username = username)
            )

        if user_obj.exists():
            messages.error(request, 'Error: Username or Email already exists')
            return redirect('/registration/')
        
        user_obj = User.objects.create(
           first_name = first_name,
            last_name = last_name,
            username = username,
            email = email    
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.error(request, 'Success : Account created')
        return redirect('/registration/')

    return render(request , 'registration.html')


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(
          username = username
            )
        if not user_obj.exists():
            messages.error(request, 'Error: Username does not exist')
            return redirect('/')

       
        user_obj = authenticate(username = username , password = password)

        if not user_obj:
            messages.error(request, 'Error: Invalid credentials')
            return redirect('/')
        
        login(request, user_obj)
        return redirect('index/')
        

    return render(request , 'login.html')

def logout_page(request):
    logout(request)
    messages.error(request, 'Logged out successfull...')
    return redirect('login_page')


@login_required(login_url='/login/')
def index(request):
    # Initialize the context variables
    transactions = Transaction.objects.filter(created_by=request.user)
    income = transactions.filter(transtype='Credit').aggregate(total_income=Sum('amount'))['total_income'] or 0.0
    expense = transactions.filter(transtype='Debit').aggregate(total_expense=Sum('amount'))['total_expense'] or 0.0
    balance = income - expense

    if request.method == "POST":
        # Handle POST request to add a new transaction
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        transtype = request.POST.get('transtype')

        if not description or not transtype:
            messages.error(request, "Description and transaction type are required.")
            return render(request, 'index.html', {
                'transactions': transactions,
                'balance': balance,
                'income': income,
                'expense': expense,
            })  # Re-render the page with the current state

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "Amount must be a valid number.")
            return render(request, 'index.html', {
                'transactions': transactions,
                'balance': balance,
                'income': income,
                'expense': expense,
            })  # Re-render the page with the current state

        # Create the transaction
        Transaction.objects.create(
            description=description,
            amount=amount,
            transtype=transtype,
            created_by=request.user
        )

        # Recalculate income, expense, and balance after adding the transaction
        transactions = Transaction.objects.filter(created_by=request.user)
        income = transactions.filter(transtype='Credit').aggregate(total_income=Sum('amount'))['total_income'] or 0.0
        expense = transactions.filter(transtype='Debit').aggregate(total_expense=Sum('amount'))['total_expense'] or 0.0
        balance = income - expense

        # Provide feedback to the user
        messages.success(request, "Transaction added successfully.")

    # Render the page with updated context after handling POST or GET
    return render(request, 'index.html', {
        'transactions': transactions,
        'balance': balance,
        'income': income,
        'expense': expense,
    })



@login_required(login_url='/login/')
def deleteTransaction(request,uuid):
    
    Transaction.objects.get(uuid = uuid).delete()
    messages.success(request,"Transaction deleted successfully")
    return redirect('index')



















 # if request.method == "POST":
    #     description = request.POST.get('description')
    #     amount = request.POST.get('amount')
    #     transtype = request.POST.get('transtype')
        

    #     if description is None:
    #         messages.info(request, "Description Cannot be blank")
    #         return redirect('index')
        

    #     try:
    #         amount = float(amount)
    #     except Exception as e:
    #         messages.info(request, "Should be a Number")
    #         return redirect('index')
        
    #     Transaction.objects.create(
    #         description = description,
    #         transtype = transtype
    #         amount = amount,
    #         created_by = request.user
    #     )

    #     # if transtype == 'Debit':
    #     #     expense+=amount
    #     #     balance-=amount
    #     # elif transtype == 'Credit':
    #     #     balance+=amount
    #     #     income+=amount

    #     return redirect('index')


    # context = {
    #     'transactions' : Transaction.objects.filter(created_by = request.user),
    #            'balance' : Transaction.objects.filter(created_by = request.user).aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
    #            'income' : Transaction.objects.filter(created_by = request.user,amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
    #            'expense' : Transaction.objects.filter(created_by = request.user,amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,
    #             #  'balance':balance,
    #             #  'income':income,
    #             #  'expense':expense,

    #            }
    
    # return render(request, 'index.html', context)