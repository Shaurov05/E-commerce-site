from django.shortcuts import render
from . models import *
from accounts.models import Customer
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
# Create your views here.


class CategoryList(ListView):
    model = Category

    def get(self, request,  *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        category_list = Category.objects.all()

        print('CartItems', cartItems)
        return render(request, template_name = 'store/category_list.html',
                    context={'category_list':category_list , 'cartItems':cartItems})



class CategoryDetail(DetailView):
    model = Category

    def get(self, request,  *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        category_list = Category.objects.all()

        pk = self.kwargs['pk']
        products = Product.objects.all().filter(category__id=pk)
        category_name = Category.objects.get(pk=pk).name

        print('CartItems', cartItems)
        return render(request, template_name = 'store/category_detail.html',
                    context={'category_name':category_name, 'products':products , 'cartItems':cartItems, 'pk':pk})


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    print("Cartitem",cartItems)
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # for item in items:
    #     print(item.product.image.url)

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      context = {'items':items, 'order':order,'cartItems':cartItems}
      return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId %s and Action %s' % (productId, action))

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    print("Data: ", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)



@login_required
def UserLogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('store'))




#
