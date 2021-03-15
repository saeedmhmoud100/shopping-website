from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Customer, Product, Card, OrderPlaced
from .forms import CustomerRegisterationForm, CustomerProfileForm


class ProductView(View):
  def get(self, request):
    topwears = Product.objects.filter(category='TW')
    bottomwears = Product.objects.filter(category='BW')
    mobiles = Product.objects.filter(category='M')
    context = {
        'topwears': topwears,
        'bottomwears': bottomwears,
        'mobiles': mobiles
    }
    return render(request, 'app/home.html', context)


class ProductDetailView(View):
  def get(self, request, pk):
    product = Product.objects.get(pk=pk)
    item_already_in_card = False
    if request.user.is_authenticated:
      item_already_in_card = Card.objects.filter(Q(product=product.id), Q(user=request.user)).exists()
    print(item_already_in_card)
    context = {
        'product': product,
        'item_already_in_card':item_already_in_card
    }
    return render(request, 'app/productdetail.html', context)

@login_required
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  Card(user=user, product=product).save()
  return redirect('/card')

@login_required
def show_card(request):
  if request.user.is_authenticated:
    user = request.user
    card = Card.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    card_product = [p for p in Card.objects.all() if p.user == user]
    # print(card_product)
    if card_product:
        for p in card_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'cards': card, 'totalamount': totalamount, 'amount': amount})
    else:
        return render(request, 'app/emptycard.html')

@login_required
def plus_card(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Card.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity += 1
    c.save()

    amount = 0.0
    shipping_amount = 70.0
    card_product = [p for p in Card.objects.all() if p.user ==
                    request.user]
    for p in card_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)

@login_required
def minus_card(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Card.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()

    amount = 0.0
    shipping_amount = 70.0
    card_product = [p for p in Card.objects.all() if p.user ==request.user]
    for p in card_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)

@login_required
def remove_card(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Card.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()

    amount = 0.0
    shipping_amount = 70.0
    card_product = [p for p in Card.objects.all() if p.user ==
                    request.user]
    for p in card_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)


def buy_now(request):
  return render(request, 'app/buynow.html')

@login_required
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  print(request.user.customer)
  return render(request, 'app/orders.html',{'order_placed':op})


def mobile(request, data=None):
  if data == None:
      mobiles = Product.objects.filter(category='M')
  elif data == 'Redmi' or data == 'Samsung':
      mobiles = Product.objects.filter(category='M').filter(brand=data)
  return render(request, 'app/mobile.html', {'mobiles': mobiles})


class CustomerRegistrationView(View):
  def get(self, request):
    form = CustomerRegisterationForm()
    context = {
        'form': form
    }
    return render(request, 'app/customerregistration.html', context)

  def post(self, request):
    form = CustomerRegisterationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'registered successfully!')
        return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'app/customerregistration.html', context)

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  card_items = Card.objects.filter(user=user)
  amount=0.0
  shipping_amount=70.0
  totalamount=0.0
  card_product = [p for p in Card.objects.all() if p.user ==request.user]
  if card_product:
    for p in card_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount= amount + shipping_amount
  return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'card_items':card_items})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  print(custid)
  customer = Customer.objects.get(id=custid)
  card = Card.objects.filter(user=user)
  for c in card:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect('orders')
  
  
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    context = {
        'form': form,
        'active': 'btn-primary'
    }
    return render(request, 'app/profile.html', context)
  


def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
      user = request.user
      name = form.cleaned_data['name']
      localty = form.cleaned_data['localty']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']

      reg = Customer(user=user, name=name, localty=localty,
                     city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(
          request, 'Congratulation! Profile Updated Successfully!..')
      context = {
          'form': form,
          'active': 'btn-primary'
      }
      return render(request, 'app/profile.html', context)
