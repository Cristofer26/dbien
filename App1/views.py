from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Habitacion, Pasajero, Reserva, Servicio, Empleado,RegistroAlojamiento
from django.views.generic.base import TemplateView
from .forms import HabForm, ResForm, PasForm, ServForm, EmpForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, PerForm, EmpForm, RegistroAlojamientoFormset
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
# Create your views here.
        
@method_decorator(login_required, name='dispatch')
class Contacto(TemplateView):
    template_name = "App1/contacto.html"

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

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Habitacion.objects.all()

        if query:
            object_list = object_list.filter(
                Q(numero__icontains=query) |
                Q(capacidad__icontains=query) |
                Q(orientacion__icontains=query) |
                Q(precio__icontains=query) 
            )

        return object_list

@method_decorator(login_required, name='dispatch')
class PasListView(ListView):
    model = Pasajero
    template_name = "App1/pasajeros_list.html"
    context_object_name = "pasajeros"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = self.model.objects.all()

        if query:
            object_list = object_list.filter(
                Q(persona__rut__icontains=query) |
                Q(persona__user__first_name__icontains=query) |
                Q(persona__user__last_name__icontains=query)
            )

        return object_list

@method_decorator(login_required, name='dispatch')
class ResListView(ListView):
    model = Reserva
    template_name = "App1/reservas_list.html"
    context_object_name = "reservas"

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q')

        try:
            # Intenta obtener el objeto Pasajero asociado al usuario.
            pasajero = get_object_or_404(Pasajero, persona__user=user)
            object_list = Reserva.objects.filter(pasajero=pasajero)
        except Http404:
            # Si el usuario no es un pasajero, muestra todas las reservas.
            object_list = Reserva.objects.all()

        # Aplica un filtro de búsqueda si se proporciona un término de búsqueda.
        if query:
            object_list = object_list.filter(
                Q(habitacion__numero__icontains=query) |
                Q(fecha_reserva__icontains=query)
            )

        return object_list

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pas_form' not in context:
            context['pas_form'] = PasForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        pas_form = PasForm(request.POST)
        if form.is_valid() and pas_form.is_valid():
            return self.form_valid(form, pas_form)
        else:
            return self.form_invalid(form, pas_form)

    def form_valid(self, form, pas_form):
        # Si se envía el PasForm, crea un nuevo pasajero
        nuevo_pasajero = pas_form.save()
        reserva = form.save(commit=False)
        reserva.pasajero = nuevo_pasajero
        reserva.save()
        return super(ResCreateView, self).form_valid(form)

    def form_invalid(self, form, pas_form):
        return self.render_to_response(self.get_context_data(form=form, pas_form=pas_form))

@method_decorator(login_required, name='dispatch')
class PasCreateView(CreateView):
    model = Pasajero
    form_class = PasForm
    template_name = "App1/pas_form.html"
    success_url = reverse_lazy("PasList")

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')    
class ServListView(ListView):
    model = Servicio
    template_name = "App1/serv_list.html"
    context_object_name = "servicios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios_con_habitaciones = []
        for servicio in context['servicios']:
            habitaciones_unicas = set()
            for registro in servicio.registros.all():
                habitaciones_unicas.add(registro.habitacion.numero)
            servicios_con_habitaciones.append({
                'servicio': servicio,
                'habitaciones': habitaciones_unicas
            })
        context['servicios_con_habitaciones'] = servicios_con_habitaciones
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = self.model.objects.all()

        if query:
            object_list = object_list.filter(
                Q(es_responsable__persona__user__first_name__icontains=query) |
                Q(registros__habitacion__numero__icontains=query)
            )

        return object_list

@method_decorator(login_required, name='dispatch')
class ServCreateView(CreateView):
    model = Servicio
    form_class = ServForm
    template_name = "App1/serv_form.html"
    success_url = reverse_lazy("ServList")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['pasajero_formset'] = formset_factory(PasForm, extra=1)(self.request.POST, prefix='pasajeros')
            context['registro_formset'] = RegistroAlojamientoFormset(self.request.POST, prefix='registros')
        else:
            context['pasajero_formset'] = formset_factory(PasForm, extra=1)(prefix='pasajeros')
            context['registro_formset'] = RegistroAlojamientoFormset(prefix='registros')

        # Actualizar queryset de pasajero en cada formulario de registro
        if 'pasajeros_creados_ids' in self.request.session:
            pasajeros_creados_ids = self.request.session['pasajeros_creados_ids']
            for form in context['registro_formset']:
                form.fields['pasajero'].queryset = Pasajero.objects.filter(id__in=pasajeros_creados_ids)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        pasajero_formset = context['pasajero_formset']
        registro_formset = context['registro_formset']

        if not (form.is_valid() and pasajero_formset.is_valid() and registro_formset.is_valid()):
            return self.form_invalid(form)

        # Guardar los pasajeros y determinar el responsable
        pasajeros = []
        for pasajero_form in pasajero_formset:
            if pasajero_form.cleaned_data:
                pasajero = pasajero_form.save()
                pasajeros.append(pasajero)

        # El primer pasajero es el responsable
        if pasajeros:
            responsable_id = pasajeros[0].id
        else:
            # Manejo del caso en que no hay pasajeros
            responsable_id = None

        # Guardar el servicio con la información del responsable
        servicio = form.save(commit=False)
        servicio.es_responsable_id = responsable_id
        servicio.save()
        form.save_m2m()

        # Asumiendo que solo hay una habitación en el registro_formset
        habitacion_seleccionada = None
        for registro_form in registro_formset:
            if registro_form.cleaned_data:
                habitacion_seleccionada = registro_form.cleaned_data['habitacion']

        # Guardar registros de alojamiento para cada pasajero con la misma habitación
        for pasajero in pasajeros:
            RegistroAlojamiento.objects.create(
                servicio=servicio, 
                habitacion=habitacion_seleccionada, 
                pasajero=pasajero
            )

        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')    
class EmpListView(ListView):
    model = Empleado
    template_name = "App1/emp_list.html"
    context_object_name = "empleados"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = self.model.objects.all()

        if query:
            object_list = object_list.filter(
                Q(persona__rut__icontains=query) |
                Q(persona__user__first_name__icontains=query) |
                Q(persona__user__last_name__icontains=query)
            )

        return object_list


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
        
class FinalizarServicioView(UpdateView):
    model = Servicio
    fields = []
    template_name = 'App1/serv_fin.html'

    def form_valid(self, form):
        servicio = form.save(commit=False)
        servicio.finalizar_servicio()
        return redirect('ServList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.object
        habitaciones_unicas = {registro.habitacion.numero for registro in RegistroAlojamiento.objects.filter(servicio=servicio)}
        context['habitaciones'] = habitaciones_unicas
        return context
    
@method_decorator(login_required, name='dispatch')
class EmpDeleteView(DeleteView):
    model = Empleado
    template_name = "App1/emp_del.html"
    success_url = reverse_lazy("EmpList")

@method_decorator(login_required, name='dispatch')
class HabDeleteView(DeleteView):
    model = Habitacion
    template_name = "App1/hab_del.html"
    success_url = reverse_lazy("HabList")

@method_decorator(login_required, name='dispatch')
class PasDeleteView(DeleteView):
    model = Pasajero
    template_name = "App1/pas_del.html"
    success_url = reverse_lazy("PasList")

@method_decorator(login_required, name='dispatch')
class ResDeleteView(DeleteView):
    model = Reserva
    template_name = "App1/res_del.html"
    success_url = reverse_lazy("ResList")