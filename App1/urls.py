from django.urls import path
from .views import (Home, Contacto, HabListView, PasListView, HabCreateView, ResListView, EmpDeleteView, HabDeleteView, PasDeleteView, ResDeleteView,
                    ResCreateView, EmpCreateView, EmpListView, PasCreateView, ServListView, ServCreateView,FinalizarServicioView )

urlpatterns = [
    path("", Home.as_view(), name="Home"),
    path("contacto/", Contacto.as_view(), name="Contacto"),
    path("hab_list/", HabListView.as_view(), name="HabList"),
    path("hab_list/delete/<int:pk>",HabDeleteView.as_view(), name="HabDel"),
    path("hab_form/", HabCreateView.as_view(), name="HabForm"),
    path("pasajeros_list/", PasListView.as_view(), name="PasList"),
    path("pasajeros_list/delete/<int:pk>",PasDeleteView.as_view(), name="PasDel"),
    path("pas_form/", PasCreateView.as_view(), name="PasForm"),
    path("res_list/", ResListView.as_view(), name="ResList"),
    path("res_list/delete/<int:pk>",ResDeleteView.as_view(), name="ResDel"),
    path("res_form/", ResCreateView.as_view(), name="ResForm"),
    path("serv_list/", ServListView.as_view(), name="ServList"),
    path("serv_form/", ServCreateView.as_view(), name="ServForm"),
    path("emp_list/", EmpListView.as_view(), name="EmpList"),
    path("emp_form/", EmpCreateView.as_view(), name="EmpForm"),
    path("emp_list/delete/<int:pk>", EmpDeleteView.as_view(), name="EmpDel"),
    path('serv_fin/<int:pk>/', FinalizarServicioView.as_view(), name='ServFin'),
]