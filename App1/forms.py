from django import forms
from .models import (Habitacion, Reserva, Pasajero, Persona,Servicio, Empleado)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

class PerForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['rut']
        widgets = {
            "rut": forms.TextInput(attrs={"class": "form-control"}),
        }


class HabForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["numero" , "capacidad" , "orientacion"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "capacidad": forms.NumberInput(attrs={"class": "form-control"}),
            "orientacion": forms.TextInput(attrs={"class": "form-control"}),
        }



class ResForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["habitacion", "fecha_reserva", "cantidad_dias"]  
        widgets = {
            "habitacion": forms.Select(attrs={"class": "form-control"}),
            "fecha_reserva": forms.DateInput(attrs={"class": "form-control"}),
            "cantidad_dias": forms.NumberInput(attrs={"class": "form-control"}),
        }

class PasForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['reservas','responsable']
        widgets = {
            "reservas": forms.Select(attrs={"class": "form-control"}),
            "responsable": forms.CheckboxInput(attrs={"class": "form-control"}),
        }
    
    
class ServForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["responsable", "checkIn", "checkOut"]  
        widgets = {
            "responsable": forms.Select(attrs={"class": "form-control"}),
            "checkIn": forms.DateInput(attrs={"class": "form-control"}),
            "checkOut": forms.DateInput(attrs={"class": "form-control"}),
        }

class EmpForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['perfil', 'fecha_contratacion']
        widgets = {
            "perfil": forms.Select(attrs={"class": "form-control"}),
            "fecha_contratacion": forms.DateInput(attrs={"class": "form-control"}),
        }