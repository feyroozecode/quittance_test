from django.urls import path, include
from . import views

urlpatterns = [
    path('ajaxhtmx', views.AjaxHtmxPageView.as_view(), name='ajax_htmx'),
    path('numeraires', views.NumerairePageView.as_view(), name='op_numeraires'),
    path('', views.NumerairePageView.as_view(), name='op_numeraires'),
    path('cheques', views.ChequePageView.as_view(), name='op_cheques'),
    path('choisir_journee', views.ChoisirJourneePageView.as_view(), name='select_journee'),
    path('print_quitance/<int:pk>', views.PrintQuitancePageView.as_view(), name='print_quitance'),
    path('etat_journalier', views.EtatJournalierPageView.as_view(), name='etat_journalier'),    
]