from django import forms
from .models import Restaurant
from .models import userreg

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"

class loginForm(forms.ModelForm):
    class Meta:
        model = userreg
        fields = "__all__"
