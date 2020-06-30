from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,reverse
from .models import Customer
from django.contrib.auth.models import User

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			id = request.user.customer.id
			return HttpResponseRedirect(reverse('customer', args=(id,)))

		if group == 'admin' or 'admin':
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponse('you are nothing')
	return wrapper_function
