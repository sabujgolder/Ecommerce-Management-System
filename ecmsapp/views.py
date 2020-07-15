from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .models import *
from django.forms import inlineformset_factory

from .filters import ProductFilter,OrderFilter
from .forms import *
from .decorators import *

from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@unauthenticated_user
def login_view(request):
    if request.method =='POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Does not exist')

    return render(request,'ecmsapp/login.html')


@unauthenticated_user
def registerPage(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            user_status = form.cleaned_data.get('user_status').lower()
            if user_status == 'customer':
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    name=user.username,)
            elif user_status =='shop owner':
                group = Group.objects.get(name='shop owner')
                user.groups.add(group)
                Shop_Owner.objects.create(
                    user=user,
                    name=user.username,)
            return redirect('login')

    context = {'form':form}
    return render(request, 'ecmsapp/register.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@admin_only
def home(request):
    Posts = Customer_Post.objects.all()[:3]
    Shop_Owner_Posts = Shop_Owner_Post.objects.all()[:3]
    return render(request,'ecmsapp/home.html',{'Posts':Posts,'Shop_Owner_Posts':Shop_Owner_Posts})

@login_required(login_url='login')
def customer_forum(request):
    Posts = Customer_Post.objects.all()
    return render(request,'ecmsapp/customer_forum.html',{'Posts':Posts})

@login_required(login_url='login')
def shop_owners_forum(request):
    Shop_Owner_Posts = Shop_Owner_Post.objects.all()
    return render(request,'ecmsapp/shop_owners_forum.html',{'Shop_Owner_Posts':Shop_Owner_Posts})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def customer(request,pk):
    customer_data = Customer.objects.get(id=pk)
    orders = customer_data.order_set.all()
    total = orders.count()
    SearchFilter = OrderFilter(request.GET , queryset = orders)
    orders = SearchFilter.qs
    return render(request,'ecmsapp/customer_temp.html',{'customer_data':customer_data,'orders':orders,'SearchFilter':SearchFilter,'total':total})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def shop_owner(request,pk):
    shop_owner_data = Shop_Owner.objects.get(id=pk)
    total_product = shop_owner_data.product_set.all().count()
    shops = shop_owner_data.shop_set.all()
    return render(request,'ecmsapp/shop_owner_temp.html',{'shop_owner_data':shop_owner_data,'shops':shops,'total_product':total_product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def shop(request,pk):
    shop_owner_data = Shop_Owner.objects.get(id=pk)
    products = shop_owner_data.product_set.all()


    # Get Order numbers for each product
    l=[]
    delivered = 0
    pending = 0
    for product in products:
        item = Product.objects.get(id=product.id)
        orderset = item.order_set.all()

        # get total delivered orders
        delivered = delivered+orderset.filter(status='Delivered').count()

        # get total pending orders
        pending = pending+orderset.filter(status='Pending').count()



        l.append(orderset)

    order_list=[]
    for product in products:
        item = Product.objects.get(id=product.id)
        orders = item.order_set.all().count()
        order_list.append(orders)

    total_orders = 0
    for i in range(len(order_list)):
        total_orders = total_orders + order_list[i]


    shops = shop_owner_data.shop_set.all()
    return render(request,'ecmsapp/shop.html',{'shops':shops,'shop_owner_data':shop_owner_data,
                                                'products':products,'order_list':order_list,
                                                'delivered':delivered,'pending':pending,
                                                'total_orders':total_orders,'l':l})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner','Customer'])
def shop_owner_data(request,pk):
    shop_owner_data = Shop_Owner.objects.get(id=pk)
    shops = shop_owner_data.shop_set.all()
    return render(request,'ecmsapp/shop_owner_data.html',{'shop_owner_data':shop_owner_data,'shops':shops})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def add_products(request,pk):
    order_form = inlineformset_factory(Shop_Owner,Product,fields=('name','price','product_pic'),extra=5)
    shop = Shop_Owner.objects.get(id=pk)
    print(shop_owner)
    if request.method == 'POST':
        form = order_form(request.POST,instance=shop)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'ecmsapp/products.html',{'formset':order_form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def products(request,pk):
    shop_owner_data = Shop_Owner.objects.get(id=pk)
    products = shop_owner_data.product_set.all()

    SearchFilter = ProductFilter(request.GET , queryset = products)
    products = SearchFilter.qs

    return render(request,'ecmsapp/shop_products.html',{'products':products,'SearchFilter':SearchFilter,'shop_owner_data':shop_owner_data})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def update_product(request,pk):
    product = Product.objects.get(id=pk)
    form = update_form(instance=product)
    if request.method =='POST':
        form = update_form(request.POST,instance = product)
        if form.is_valid:
            form.save()
            return redirect('/')
    return render(request,'ecmsapp/update_product.html',{'form':form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def bulk_product_update(request,pk):
    shop_owner = Shop_Owner.objects.get(id=pk)
    update_order_formset = inlineformset_factory(Shop_Owner,Product,fields=('name','price'),extra=0)
    formset = update_order_formset(instance=shop_owner)
    if request.method =='POST':
        form = update_order_formset(request.POST,instance = shop_owner)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'ecmsapp/bulk_product_update.html',{'form':formset})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','shop owner'])
def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    order = product.order_set.all().count()
    if order > 0 :
        return HttpResponse('Customers have order for this Product.Can not be deleted unless the order is completed')
    else:
        product.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def data_chart(request):
    return render(request,'ecmsapp/data_chart.html')


def customers(request):
    all_customers = Customer.objects.all()
    return render(request,'ecmsapp/customer_data.html',{'all_customers':all_customers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def create_order(request,pk):
    customer = Customer.objects.get(id=pk)
    formset = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    if request.method =='POST':
        form = formset(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context={'formset':formset,'customer':customer}
    return render(request,'ecmsapp/create_order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def Update_Order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return HttpResponse('Order Updated')

	context = {'form':form}
	return render(request, 'ecmsapp/order_update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def Delete_Order(request, pk):
	order = Order.objects.get(id=pk)
	order.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def Update_Customer(request, pk):
	customer = Customer.objects.get(id=pk)
	form = UpdateCustomer(instance=customer)
	if request.method == 'POST':
		form = UpdateCustomer(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return HttpResponse('Update SuccessFully')

	context = {'form':form}
	return render(request, 'ecmsapp/customer_update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def order_search(request,pk):
    customer_data = Customer.objects.get(id=pk)
    orders = customer_data.order_set.all()

    SearchFilter = ProductFilter(request.GET , queryset = orders)
    orders = SearchFilter.qs
    return render(request,'ecmsapp/customer_temp.html',{'orders':orders,'SearchFilter':SearchFilter,'customer_data':customer_data})

@login_required(login_url='login')
def customer_post_detail(request,pk):
    post = Customer_Post.objects.get(id=pk)
    return render(request,'ecmsapp/customer_post_detail.html',{'Post':post})

@login_required(login_url='login')
def shop_owner_post_detail(request,pk):
    post = Shop_Owner_Post.objects.get(id=pk)
    return render(request,'ecmsapp/shop_owner_post_detail.html',{'Post':post})


@login_required(login_url='login')
@admin_only
def all_shops(request):
    shops = Shop.objects.all()
    return render(request,'ecmsapp/all_shops.html',{'shops':shops})
