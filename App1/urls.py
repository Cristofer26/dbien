from django.urls import path
from .views import (Home, HabListView, PasListView, HabCreateView, ResListView,
                    ResCreateView, EmpCreateView, EmpListView, PasCreateView, ServListView, ServCreateView )

urlpatterns = [
    path("", Home.as_view(), name="Home"),
    path("hab_list/", HabListView.as_view(), name="HabList"),
    path("hab_form/", HabCreateView.as_view(), name="HabForm"),
    path("pasajeros_list/", PasListView.as_view(), name="PasList"),
    path("pas_form/", PasCreateView.as_view(), name="PasForm"),
    path("res_list/", ResListView.as_view(), name="ResList"),
    path("res_form/", ResCreateView.as_view(), name="ResForm"),
    path("serv_list/", ServListView.as_view(), name="ServList"),
    path("serv_form/", ServCreateView.as_view(), name="ServForm"),
    path("emp_list/", EmpListView.as_view(), name="EmpList"),
    path("emp_form/", EmpCreateView.as_view(), name="EmpForm"),
]