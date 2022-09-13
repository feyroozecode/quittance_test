from datetime import datetime
from django.utils.dateparse import parse_date
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponse
from quitance.models import BordereauDetail
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import requests
from django.db.models import Q

from .forms import BordereauDetailForm, BordereauForm, QuitanceForm, PartieVersanteForm
from .models import Compte, Journee, PartiVersante, Quitance, PrintedQuitance, SousStructure, get_dr_next_num, get_next_num
from .serializers import PartiVersanteSerializer
# Create your views here.
class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        

class PrintQuitancePageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/print_quitance_page.html"
    
    def get(self, request, pk, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['close'] = False
        
        quitance = Quitance.objects.get(pk=pk)
        printedQuitance = PrintedQuitance.objects.filter(quitance=quitance, created_by=request.user)
        if printedQuitance.count() == 0 or 'quitance.reprint_quitance' in request.user.get_all_permissions():
            PrintedQuitance.objects.create(quitance=quitance, created_by=request.user)
            context['quitance'] = quitance
        else:
            context['close'] = True
            
        return self.render_to_response(context)
    
class AjaxHtmxPageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/ajax.html"
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
       
        last_quitances = None
        
        if request.htmx and request.GET.get('last_quitances', None) != None:
            if request.GET.get('last_quitances', None) == 'bdrs':
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau__type_operation=1, journee=request.user.actived_journee).exclude(bordereau=None).order_by('-id')[:10]
            elif request.GET.get('last_quitances', None) == 'tiers':
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau=None, journee=request.user.actived_journee).order_by('-id')[:10]
            elif request.GET.get('last_quitances', None) == 'cheques':
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau__type_operation=2, journee=request.user.actived_journee).order_by('-id')[:10]
                
            return render(request, 'quitance/partials/quitance_list.html', context={'last_quitances': last_quitances})
        
        if len(self.request.GET.get('search_versante', '')) > 0:
            txt = self.request.GET.get('search_versante', '')
            q = (Q(**{'nom_prenom__icontains': txt}) | Q(**{'reference__icontains': txt}))
            search = PartiVersante.objects.filter(q)
            
            return JSONResponse([{'id': p.id, 'text': '%s: %s' % (p.reference, p.nom_prenom)} for p in search], status=200)
        
        if len(self.request.GET.get('search_comptable', '')) > 0:
            txt = self.request.GET.get('search_comptable', '')
            q = (Q(**{'numero__icontains': txt}) | Q(**{'libele__icontains': txt}) | Q(**{'structure__libele__icontains': txt}))
            search = SousStructure.objects.filter(q)
            
            return JSONResponse([{'id': p.id, 'text': '%s: %s' % (p.numero, p.libele)} for p in search], status=200)
        
        if len(self.request.GET.get('search_compte', '')) > 0:
            txt = self.request.GET.get('search_compte', '')
            q = (Q(**{'cpt__icontains': txt}) | Q(**{'libele__icontains': txt}))
            search = Compte.objects.filter(q)
            
            return JSONResponse([{'id': p.id, 'text': '%s: %s' % (p.cpt, p.libele)} for p in search], status=200)
        
        return self.render_to_response(context)
    
class NumerairePageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/numeraire_page.html"
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)        
        if 'quitance.versement_numeraire' not in request.user.get_all_permissions():
            if 'quitance.depot_cheque' in request.user.get_all_permissions():
                return redirect('op_cheques')
            else:
                return redirect('login')
        print(datetime.today().date())
        journee, isnew = Journee.objects.get_or_create(date=datetime.today().date(), created_by=self.request.user)
        if not isnew and journee.actived == False:
            journee.actived = True
            journee.save()
            
        context['versante_form'] = PartieVersanteForm(data = self.request.POST or None, request = self.request)
        context['quitance_form'] = QuitanceForm(data = self.request.POST or None, request = self.request)
        context['bordereau_detail_form'] = BordereauDetailForm(data = self.request.POST or None, request = self.request)
        context['bordereau_form'] = BordereauForm(data = self.request.POST or None, request = self.request, type_op=1)
        return self.render_to_response(context)
    
    
    def post(self, request, *args, **kwargs):
        context = {}
        if self.request.method == "POST" and self.request.POST.get('form') == 'quitance_form' and self.request.is_ajax():
            form = QuitanceForm(self.request.POST, request = self.request)
            if form.is_valid():
                quitance = form.save()
                context = {"success": True, "data": {'id': quitance.id}}
                return JSONResponse(context, status=200)

            return JsonResponse({"success":False, "form": form.errors}, status=400)
        
        if self.request.method == "POST" and self.request.POST.get('form') == 'versante_form' and self.request.is_ajax():
            form = PartieVersanteForm(self.request.POST, request = self.request)
            if form.is_valid():
                versante = form.save()
                context = {"success": True, "data": PartiVersanteSerializer(versante).data}
                return JSONResponse(context, status=200)

            return JsonResponse({"success":False, "form": form.errors}, status=400)
        
        if self.request.method == "POST" and self.request.POST.get('form') == 'bordereau_form' and self.request.is_ajax():
            form = BordereauForm(self.request.POST, request = self.request, type_op=1)
            if form.is_valid():
                bordereau = form.save()
                context = {"success": True, "data": {'id': bordereau.id, 'quitance': bordereau.quitance.id}}
                return JSONResponse(context, status=200)

            return JsonResponse({"success":False, "form": form.errors}, status=400)
        
        
        context['versante_form'] = PartieVersanteForm(data = self.request.POST or None, request = self.request)
        context['quitance_form'] = QuitanceForm(data = self.request.POST or None, request = self.request)
        context['bordereau_detail_form'] = BordereauDetailForm(data = self.request.POST or None, request = self.request)
        context['bordereau_form'] = BordereauForm(data = self.request.POST or None, request = self.request, type_op=1)
        return self.render_to_response(context)


class ChoisirJourneePageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/includes/journnee.html"
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        
        if self.request.method == "POST" and self.request.POST.get('form') == 'active_journee':
            journee, isnew = Journee.objects.get_or_create(date=parse_date(self.request.POST['journee']), created_by=self.request.user)
            print(journee)
            if journee.actived == False:
                journee.actived = True
                journee.save()
                
            return redirect('op_cheques')
class ChequePageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/cheque_page.html"
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if request.user.actived_journee == None:
            return  redirect('select_journee')
        
        if 'quitance.depot_cheque' not in request.user.get_all_permissions():
            if 'quitance.versement_numeraire' in request.user.get_all_permissions():
                return redirect('op_numeraires')
            else:
                return  redirect('login')

        context['bordereau_detail_form'] = BordereauDetailForm(data = self.request.POST or None, request = self.request)
        context['bordereau_form'] = BordereauForm(data = self.request.POST or None, request = self.request, type_op=2)
        return self.render_to_response(context)
    
    
    def post(self, request, *args, **kwargs):
        context = {}
        if 'quitance.depot_cheque' not in request.user.get_all_permissions():
            if 'quitance.versement_numeraire' in request.user.get_all_permissions():
                return redirect('op_numeraires')
            else:
                return redirect('login')
            
        if self.request.method == "POST" and self.request.POST.get('form') == 'bordereau_form' and self.request.is_ajax():
            form = BordereauForm(self.request.POST, request = self.request, type_op=2)
            if form.is_valid():
                bordereau = form.save()
                context = {"success": True, "data": {'id': bordereau.id, 'quitance': bordereau.quitance.id}}
                return JSONResponse(context, status=200)

            return JsonResponse({"success":False, "form": form.errors}, status=400)
        
        context['bordereau_detail_form'] = BordereauDetailForm(data = self.request.POST or None, request = self.request)
        context['bordereau_form'] = BordereauForm(data = self.request.POST or None, request = self.request, type_op=2)
        return self.render_to_response(context)
    
    
class EtatJournalierPageView(LoginRequiredMixin, TemplateView):
    
    template_name = "quitance/etat_journalier.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        last_quitances = None
    
        # for row in c:
        #     print (row[0], '-', row[1]) # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.
        #conn.close()
        if request.GET.get('type', None) != None:
            if request.GET.get('type', None) == 'bdrs' and 'quitance.versement_numeraire' in request.user.get_all_permissions():
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau__type_operation=1).exclude(bordereau=None)
            elif request.GET.get('type', None) == 'tiers' and 'quitance.versement_numeraire' in request.user.get_all_permissions():
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau=None)
            elif request.GET.get('type', None) == 'cheques' and 'quitance.depot_cheque' in request.user.get_all_permissions():
                last_quitances = Quitance.objects.filter(created_by=request.user, bordereau__type_operation=2)
            if last_quitances != None:
                context['last_quitances'] = last_quitances.filter(journee=request.user.actived_journee).order_by('-id')
        
        return self.render_to_response(context) 
    
    