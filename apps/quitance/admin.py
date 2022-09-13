from django.contrib import admin
from .models import Agent, Config, EcritureBrouillard, Journee, Nature, PartiVersante, PrintedQuitance, Quitance, Structure, Compte, Bordereau, BordereauDetail, SousStructure, TypePartiVersante
from django.contrib.auth.admin import UserAdmin



@admin.register(EcritureBrouillard)
class EcritureBrouillardAdmin(admin.ModelAdmin):
    list_display = ('id', 'montant_credit', 'montant_debit')
    
    
@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('libele', 'value')
    
    
@admin.register(Agent)
class StructureAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'cgib')
    exclude = ('password',)
    
@admin.register(PrintedQuitance)
class PrintedQuitanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'quitance', 'created_by', 'created_at')
    
    
@admin.register(TypePartiVersante)
class TypePartiVersanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'libele')
    

@admin.register(PartiVersante)
class PartiVersanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_prenom', 'type_versante', 'reference')
    
    
@admin.register(Quitance)
class QuitanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'montant', 'numero', 'numero_dr', 'nature', 'partie_versante')
    
@admin.register(Journee)
class JourneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'actived', 'created_by', 'created_at', 'updated_at')
       
@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ('id', 'libele', 'code')
    
@admin.register(SousStructure)
class SousStructureAdmin(admin.ModelAdmin):
    list_display = ('id', 'structure', 'libele', 'numero')
    
@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpt', 'libele')

@admin.register(Bordereau)
class BordereauAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'type_operation', 'poste_comptable', 'date')

@admin.register(BordereauDetail)
class BordereauDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'bordereau', 'montant', 'nature', 'compte', 'ischeque', 'num_cheque', 'banque', 'date_cheque')
    

@admin.register(Nature)
class NatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'libele')