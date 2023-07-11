from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clienti/', views.clienti, name='clienti'),
    path('carti/', views.carti, name='carti'),
    path('edituri/', views.edituri, name='edituri'),
    path('inchirieri/', views.inchirieri, name='inchirieri'),
    path('inchirieri/carte/<int:id_carte>', views.carte, name='carte'),
    path('inchirieri/client/<int:nr_card>', views.client, name='client'),
    path('clienti/detalii/<int:id_cnp>', views.detalii, name='detalii'),
    path('inchirieri/stergereInchiriere/<int:id_inchiriere>', views.stergereInchiriere, name='stergereInchiriere'),
    path('clienti/stergereClient/<int:nr_card>', views.stergereClient, name='stergereClient'),
    path('carti/stergereCarte/<int:id_carte>', views.stergereCarte, name='stergereCarte'),
    path('edituri/stergereEditura/<str:id_editura>', views.stergereEditura, name='stergereEditura'),
    path('clienti/editareClient/<int:nr_card>', views.editareClient, name='editareClient'),
    path('carti/editareCarte/<int:id_carte>', views.editareCarte, name='editareCarte'),
    path('inchirieri/editareInchiriere/<int:id_inchiriere>', views.editareInchiriere, name='editareInchiriere'),
    path('edituri/editareEditura/<str:id_editura>', views.editareEditura, name='editareEditura'),
    path('clienti/adaugareClient/', views.adaugareClient, name='adaugareClient'),
    path('edituri/adaugareEditura/', views.adaugareEditura, name='adaugareEditura'),
    path('carti/adaugareCarte/', views.adaugareCarte, name='adaugareCarte'),
    path('inchirieri/adaugareInchiriere/', views.adaugareInchiriere, name='adaugareInchiriere'),
]
