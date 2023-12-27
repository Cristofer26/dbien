from django import forms
from .models import (Habitacion, Reserva, Pasajero, Persona,Servicio, Empleado, RegistroAlojamiento)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import random
from django.forms import modelformset_factory, inlineformset_factory

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

class SimpleUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

class PerForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['rut']
        widgets = {
            "rut": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        if not validar_rut(rut):
            raise ValidationError('El RUT ingresado no es válido.')
        
        return rut

def validar_rut(rut):
    rut = rut.replace('.', '').replace('-', '')
    if not rut[:-1].isdigit() or not (rut[-1].isdigit() or rut[-1].upper() == 'K'):
        return False
    cuerpo, dv = rut[:-1], rut[-1].upper()
    reversed_digits = map(int, reversed(cuerpo))

    s = sum(d * (i % 6 + 2) for i, d in enumerate(reversed_digits))
    dv_esperado = (11 - s % 11)

    if dv_esperado == 11:
        dv_esperado = '0'
    elif dv_esperado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_esperado)

    return dv == dv_esperado



class HabForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["numero" , "capacidad" , "orientacion", "precio"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "capacidad": forms.NumberInput(attrs={"class": "form-control"}),
            "orientacion": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(attrs={"class": "form-control"}),
        }



class ResForm(forms.ModelForm):
    pasajero = forms.ModelChoiceField(
    queryset=Pasajero.objects.all(),
    required=False,
    widget=forms.Select(attrs={"class": "form-control"}))
    
    class Meta:
        model = Reserva
        fields = ["habitacion", "fecha_reserva", "cantidad_dias"]  
        widgets = {
            "habitacion": forms.Select(attrs={"class": "form-control"}),
            "fecha_reserva": forms.DateInput(attrs={"class": "form-control"}),
            "cantidad_dias": forms.NumberInput(attrs={"class": "form-control"}),
        }

class PasForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    rut = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Pasajero
        fields = []

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not validar_rut(rut):
            raise forms.ValidationError('El RUT ingresado no es válido.')
        return rut

    def save(self, commit=True):
        # Obtiene las dos primeras letras del nombre y el apellido completo
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username_base = f"{first_name[:2].lower()}{last_name.lower()}"
        username = username_base
        max_attempts = 10
        attempts = 0

        # Intenta encontrar un nombre de usuario único
        while User.objects.filter(username=username).exists() and attempts < max_attempts:
            attempts += 1
            # Añade un número aleatorio para intentar hacerlo único
            username = f"{username_base}{random.randint(1, 100)}"

        if attempts == max_attempts:
            raise forms.ValidationError("No se pudo generar un nombre de usuario único.")


        rut_clean = self.cleaned_data['rut'].replace('.', '').replace('-', '')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=rut_clean 
        )

        # Asocia el usuario con la persona y el pasajero
        persona = Persona.objects.create(user=user, rut=self.cleaned_data['rut'])
        pasajero = super().save(commit=False)
        pasajero.persona = persona

        if commit:
            pasajero.save()

        return pasajero

PasajeroFormSet = modelformset_factory(Pasajero, form=PasForm, extra=1, can_delete=True)
    
class ServForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = []  
    
    def form_valid(self, form):
        context = self.get_context_data()
        pasajero_forms = context['pasajero_forms']
        if all([pf.is_valid() for pf in pasajero_forms]):
            response = super().form_valid(form)
            servicio = self.object

            # ID del pasajero responsable
            responsable_id = self.request.POST.get('responsable')

            for pf in pasajero_forms:
                pasajero = pf.save(commit=False)
                # Aquí creas un registro de alojamiento para cada pasajero
                registro = RegistroAlojamiento.objects.create(
                    pasajero=pasajero, 
                    servicio=servicio
                )

                # Comprobar si este pasajero es el responsable
                if str(pasajero.id) == responsable_id:
                    servicio.es_responsable = pasajero
                    servicio.save()

            return response
        else:
            return self.form_invalid(form)

class EmpForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['perfil', 'fecha_contratacion']
        widgets = {
            "perfil": forms.Select(attrs={"class": "form-control"}),
            "fecha_contratacion": forms.DateInput(attrs={"class": "form-control"}),
        }

class RegistroAlojamientoForm(forms.ModelForm):
    class Meta:
        model = RegistroAlojamiento
        fields = ('habitacion', 'pasajero')
        widgets = {
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'pasajero': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistroAlojamientoForm, self).__init__(*args, **kwargs)
        habitaciones_disponibles = Habitacion.objects.filter(
            id__in=[h.id for h in Habitacion.objects.all() if h.esta_disponible()]
        )
        self.fields['habitacion'].queryset = habitaciones_disponibles

RegistroAlojamientoFormset = forms.inlineformset_factory(
    Servicio, RegistroAlojamiento, 
    form=RegistroAlojamientoForm,
    fields=('habitacion',),  # Solo incluir 'habitacion'
    extra=1,
    can_delete=False
)
