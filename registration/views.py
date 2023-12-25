from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from App1.models import Pasajero, Empleado
from forms import LoginForm

# Create your views here.
class Login(CreateView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

            # Comprueba si el usuario es empleado o pasajero
            if Empleado.objects.filter(persona__user=user).exists():
                return redirect('HomeEmp')  # URL para el home de empleados
            elif Pasajero.objects.filter(persona__user=user).exists():
                return redirect('HomePas')  # URL para el home de pasajeros
            else:
                # Redirecciona a una página por defecto si no es ni empleado ni pasajero
                return redirect('HabForm')

        else:
            messages.error(self.request, 'Usuario o contraseña incorrectos.')
            return self.form_invalid(form)