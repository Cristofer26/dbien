from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Habitacion, Pasajero, Reserva, Servicio, Empleado
from django.contrib import messages
from django.views.generic.base import TemplateView
from .forms import HabForm, ResForm, PasForm, ServForm, EmpForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, PerForm, EmpForm

# Create your views here.
        
@method_decorator(login_required, name='dispatch')
class HomeEmp(TemplateView):
    template_name = "App1/home_emp.html"

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = "App1/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['es_pasajero'] = Pasajero.objects.filter(persona__user=user).exists()
        return context

@method_decorator(login_required, name='dispatch')    
class HabListView(ListView):
    model = Habitacion
    template_name = "App1/hab_list.html"
    context_object_name = "habitaciones"

@method_decorator(login_required, name='dispatch')
class PasListView(ListView):
    model = Pasajero
    template_name = "App1/pasajeros_list.html"
    context_object_name = "pasajeros"

@method_decorator(login_required, name='dispatch')
class ResListView(ListView):
    model = Reserva
    template_name = "App1/reservas_list.html"
    context_object_name = "reservas"

@method_decorator(login_required, name='dispatch')
class HabCreateView(CreateView):
    model = Habitacion
    form_class = HabForm
    template_name = "App1/hab_form.html"
    success_url = reverse_lazy("HabList")

@method_decorator(login_required, name='dispatch')
class ResCreateView(CreateView):
    model = Reserva
    form_class = ResForm
    template_name = "App1/res_form.html"
    success_url = reverse_lazy("ResList")


@method_decorator(login_required, name='dispatch')
class PasCreateView(CreateView):
    model = Pasajero
    form_class = PasForm
    second_form_class = UserForm
    third_form_class = PerForm
    template_name = "App1/pas_form.html"
    success_url = reverse_lazy("PasList")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        form2 = self.second_form_class(self.request.POST)
        form3 = self.third_form_class(self.request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form2.save()
            persona = form3.save(commit=False)
            persona.user = user
            persona.save()
            empleado = form.save(commit=False)
            empleado.persona = persona
            empleado.save()
            return super(PasCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')    
class ServListView(ListView):
    model = Servicio
    template_name = "App1/serv_list.html"
    context_object_name = "servicios"


@method_decorator(login_required, name='dispatch')
class ServCreateView(CreateView):
    model = Servicio
    form_class = ServForm
    template_name = "App1/serv_form.html"
    success_url = reverse_lazy("ServList")

@method_decorator(login_required, name='dispatch')    
class EmpListView(ListView):
    model = Empleado
    template_name = "App1/emp_list.html"
    context_object_name = "empleados"


@method_decorator(login_required, name='dispatch')
class EmpCreateView(CreateView):
    model = Empleado
    form_class = EmpForm
    second_form_class = UserForm
    third_form_class = PerForm
    template_name = "App1/emp_form.html"
    success_url = reverse_lazy("EmpList")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        form2 = self.second_form_class(self.request.POST)
        form3 = self.third_form_class(self.request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form2.save()
            persona = form3.save(commit=False)
            persona.user = user
            persona.save()
            empleado = form.save(commit=False)
            empleado.persona = persona
            empleado.save()
            return super(EmpCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)