
from cProfile import label
from datetime import datetime, timedelta, date
from django.utils.dateparse import parse_date
from turtle import width
from django.db import models
# from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Bordereau, BordereauDetail, Compte, Journee, Nature, PartiVersante, Quitance, SousStructure, get_dr_next_num, get_next_num

from crispy_forms_foundation.layout import Layout, Fieldset, Field, SplitDateTimeField, Row, Column, ButtonHolder, Submit, Hidden
from crispy_forms.bootstrap import Tab, TabHolder, StrictButton
from crispy_forms.helper import FormHelper

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Button, HTML

import os

class PartieVersanteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.request = kwargs.pop("request", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Hidden('form', "versante_form"),
                Column(FloatingField('type_versante'), css_class='form-group col-md-6'),
                Column(FloatingField('reference', autocomplete="off"), css_class='form-group col-md-6'),
                Column(FloatingField('nom_prenom', id="nom_prenom_versante", autocomplete="off"), css_class='form-group col-md-6'),
                Column(FloatingField('telephone', autocomplete="off"), css_class='form-group col-md-6'),
                Column(FloatingField('adresse', autocomplete="off"), css_class='form-group col-md-6'),
                Column(FloatingField('mail', autocomplete="off"), css_class='form-group col-md-6')
            ),
            ButtonHolder(HTML('<button type="submit" class="btn btn-success px-5 my-3">Enregistrer</button>'), css_class="text-center")
        )

        super().__init__(*args, **kwargs)

    class Meta:
        model = PartiVersante
        exclude = ("created_by", )


    def save(self, commit=True):
        partie_versante = super(PartieVersanteForm, self).save(commit=False)
        if commit:
            partie_versante.created_by = self.request.user
            partie_versante.save()
        return partie_versante

class QuitanceForm(forms.ModelForm):
    versante = forms.CharField(required=False)
    nom_partie_versante = forms.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.request = kwargs.pop("request", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Hidden('form', "quitance_form"),
                Column(FloatingField('versante'), css_class='form-group col-md-3'),),
            Row(
                Column(FloatingField('nature'), css_class='form-group col-md-3'),
                Column(FloatingField('montant'), css_class='form-group col-md-2'),
                Column(FloatingField('nom_prenom', autocomplete="off", label="Partie Versante"), css_class='form-group col-md-3'),
                Column(FloatingField('nom_partie_versante', autocomplete="off"), css_class='form-group col-md-3'),
                
            Column(HTML('<button type="submit" class="btn btn-success">Enregistrer</button>'), css_class='form-group col-md-1 mt-1')
            ),
            #ButtonHolder(HTML('<button type="submit" class="btn btn-success px-5 my-3">Enregistrer</button>'), css_class="text-center")
        )

        super().__init__(*args, **kwargs)
        # self.fields["partie_versante"].queryset = PartiVersante.objects.all()[:1]

    class Meta:
        model = Quitance
        exclude = ("created_by", 'journee')


    def save(self, commit=True):
        quitance = super(QuitanceForm, self).save(commit=False)
        if commit:
            try:
                versante = int(self.cleaned_data['versante'])
                quitance.partie_versante = PartiVersante.objects.get(pk=versante)
                quitance.nom_partie_versante = quitance.partie_versante.nom_prenom
            except:
                pass
            
            quitance.journee = self.request.user.actived_journee
            quitance.numero = get_next_num()
            print(quitance.numero)
            print(get_next_num())
            quitance.created_by = self.request.user
            
            print(quitance.nom_partie_versante)
            quitance.save()
        return quitance
    

class BordereauForm(forms.ModelForm):
    poste_comptable = forms.CharField(required=True)
    data = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.type_op = kwargs.pop("type_op", None)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Row(
                Hidden('form', "bordereau_form"),
                Hidden('data', ""),
                Column(FloatingField('numero'), css_class='form-group col-md-6'),
                Column(FloatingField('date'), css_class='form-group col-md-6'),
                Column(FloatingField('poste_comptable'), css_class='form-group col-md-12'),
                Column(FloatingField('nom_prenom', id='id_deposant'), css_class='form-group col-md-6'),
                Column(FloatingField('date_reception'), css_class='form-group col-md-6'),
            ),
        
        )

        super().__init__(*args, **kwargs)
        # self.fields["grade"].queryset = Grade.objects.all().order

    class Meta:
        model = Bordereau
        exclude = ("created_by", 'type_operation', 'journee')

    def clean_poste_comptable(self):
        try:
            poste_comptable = int(self.cleaned_data.get('poste_comptable'))
            return SousStructure.objects.get(pk=poste_comptable)
        except:
            raise forms.ValidationError(_("Ce champ est obligatoire "), code='required')
        
        
    def save(self, commit=True):
        bordereauForm = super(BordereauForm, self).save(commit=False)
        if commit:
            bordereauForm.created_by = self.request.user
            bordereauForm.type_operation = self.type_op
            bordereauForm.journee = Journee.objects.filter(created_by=self.request.user, actived=True).order_by('-id')[0]
            
            bordereauForm.save()
            
            datas = [d.split(',') for d in self.cleaned_data['data'].split(';')]
            ischeque = False if self.type_op == 1 else True
            
            if len(datas[0]) > 3:
                print(datas)
                print(datas[0][5])
                details = [BordereauDetail(bordereau=bordereauForm, ischeque=ischeque, created_by=self.request.user, nature=Nature.objects.get(pk=d[0]), compte=Compte.objects.get(pk=d[1]), montant=d[2], num_cheque=d[3], banque=d[4], date_cheque=parse_date(d[5]), titulaire=d[6]) for d in datas]
            elif len(datas[0]) == 3:
                details = [BordereauDetail(bordereau=bordereauForm, ischeque=ischeque, created_by=self.request.user, nature=Nature.objects.get(pk=d[0]), compte=Compte.objects.get(pk=d[1]), montant=d[2]) for d in datas]
            else:
                details = None
                
            if details != None:
                BordereauDetail.objects.bulk_create(details)
                print(get_next_num())
                print(get_dr_next_num())
                if self.type_op == 1:
                    Quitance.objects.create(numero=get_next_num(), bordereau=bordereauForm, montant=bordereauForm.montant, nature=bordereauForm.nature, nom_prenom=bordereauForm.nom_prenom, created_by=self.request.user, journee=self.request.user.actived_journee)
                elif self.type_op == 2:
                    Quitance.objects.create(numero_dr=get_dr_next_num(), bordereau=bordereauForm, montant=bordereauForm.montant, nature=bordereauForm.nature, nom_prenom=bordereauForm.nom_prenom, created_by=self.request.user, journee=self.request.user.actived_journee)
                    
            print(datas)
            print(details)
            
        return bordereauForm
    
    
class BordereauDetailForm(forms.ModelForm):
    compte = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.request = kwargs.pop("request", None)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Row(
                Hidden('form', "bordereau_detail_form"),
                Column(FloatingField('nature', id='nature_cheque', autocomplete="off"), css_class='form-group col-md-12'),
                Column(FloatingField('compte', autocomplete="off"), css_class='form-group col-md-12'),
                Column(FloatingField('montant', id="montant_cheque", autocomplete="off"),  css_class='form-group col-md-12'),
                Column(FloatingField('num_cheque', autocomplete="off"), css_class='form-group col-md-12'),
                Column(FloatingField('banque'), css_class='form-group col-md-12'),
                Column(FloatingField('date_cheque', autocomplete="off"), css_class='form-group col-md-12'),
                Column(FloatingField('titulaire', autocomplete="off"), css_class='form-group col-md-12'),
            )
        )

        super().__init__(*args, **kwargs)
        # self.fields["grade"].queryset = Grade.objects.all().order

    class Meta:
        model = BordereauDetail
        exclude = ("created_by", )


    def save(self, commit=True):
        bordereauForm = super(BordereauDetailForm, self).save(commit=False)
        if commit:
            bordereauForm.created_by = self.request.user
            bordereauForm.save()
        return bordereauForm
    
    