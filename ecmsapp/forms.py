from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class update_form(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['shop','shop_owner']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields='__all__'
        exclude = ['customer']

class UpdateCustomer(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
