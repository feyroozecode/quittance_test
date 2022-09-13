from datetime import datetime
import uuid
from venv import create
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateTimeField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, F, Count

# from .utils import do_ecriture_quitance


TYPE_OPERATION = (
    (1, 'VERSEMENT NUMERAIRE'),
    (2, 'DEPOT CHEQUE')
)

class Agent(AbstractUser):
    cgib = models.CharField(_("CGIB compte"), max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
        permissions = (
            ("versement_numeraire", "Peut effectuer un versement numeraire"),
            ("depot_cheque", "Peut effectuer un dépôt chèque"),
            ("reprint_quitance", "Peut reimprimer une quitance"),
        )
    
    @property
    def actived_journee(self):
        try:
            return Journee.objects.get(actived=True, created_by=self)
        except:
            return None
  
class Journee(models.Model):
    date = models.DateField(_("Journee comptable"), max_length=100)
    actived = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('date', 'created_by')
        verbose_name = _("Journee")
        verbose_name_plural = _("Journees")

    def __str__(self):
        return str(self.date)
    
    def save(self, *args, **kwargs):
        if self.actived == True:
            Journee.objects.filter(created_by=self.created_by, actived=True).update(actived=False)
        
        super(Journee, self).save(*args, **kwargs)
    
# Create your models here.
class Structure(models.Model):
    libele = models.CharField(_("Poste comptable"), max_length=100, unique=True)
    code = models.CharField(_("Code"), max_length=10, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Structure")
        verbose_name_plural = _("Structures")

    def __str__(self):
        return self.libele
    
class SousStructure(models.Model):
    libele = models.CharField(_("Poste comptable"), max_length=100)
    numero = models.CharField(_("Numéro poste"), max_length=10, unique=True)
    structure = models.ForeignKey("Structure", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('libele', 'structure')
        verbose_name = _("Sous Structure")
        verbose_name_plural = _("Sous Structures")

    def __str__(self):
        return self.libele
    
class Compte(models.Model):
    cpt = models.CharField(_("Compte"), max_length=15, unique=True)
    libele = models.CharField(_("Intitulé du compte"), max_length=100, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Compte")
        verbose_name_plural = _("Comptes")

    def __str__(self):
        return self.libele

class TypePartiVersante(models.Model):
    libele = models.CharField(_("Libele"), max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.libele
    
class PartiVersante(models.Model):
    nom_prenom = models.CharField(_("Nom et Prénom"), max_length=200)
    type_versante = models.ForeignKey("TypePartiVersante", on_delete=models.CASCADE)
    reference = models.CharField(_("Nif/Matricule"), max_length=50)
    adresse = models.CharField(_("Adresse"), max_length=100, null=True, blank=True)
    telephone = models.CharField(_("Téléphone"), max_length=100, null=True, blank=True)
    mail = models.CharField(_("Mail"), max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom_prenom

class PrintedQuitance(models.Model):
    quitance = models.ForeignKey("Quitance", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s by %s at %s" % (self.quitance, self.created_by, self.created_at)

def get_next_num():
    year = datetime.today().date().year
    format = 'Q-%s' % str(year)[2:]
    l = [int(q.numero[6:]) for q in Quitance.objects.exclude(numero__isnull=True) if q.numero[:4] == format]
    if l:
        next = max(l)+1
    else:
        next = 1
        
    return u"%s%06d" % (format, next)

def get_dr_next_num():
    year = datetime.today().date().year
    format = 'DR-%s' % str(year)[2:]
    l = [int(q.numero_dr[6:]) for q in Quitance.objects.exclude(numero_dr__isnull=True) if q.numero_dr[:5] == format]
    if l:
        next = max(l)+1
    else:
        next = 1
        
    return u"%s%06d" % (format, next)

def debit_credit_brouillard(quitance, sens_ecriture, compte, lien, num_fiche):
    br = EcritureBrouillard()
    br.JOURNAL = 'BT-14'
    br.NUM_PIECE = quitance.get_numero
    br.CODE_PIECE = 'QUITCE'
    br.ORDONNATEUR = 0
    br.MONTANT_ECRITURE = quitance.montant
    br.ECRITURE_LIBELLE = quitance.libele
    br.ORIGINE = 'CAISSE'
    br.ORIGINE_KEY = 'QTTCE-JN'
    br.DATE_CREATION = datetime.today()
    br.UTILISATEUR_CREATION = 'USERNAME'
    br.DATE_MODIFICATION = datetime.today()
    br.UTILISATEUR_MODIFICATION = 'USERNAME'
    br.date_echeance = datetime.today()
    br.when_done = datetime.today()
    br.statut_ecriture = 'VALIDE'
    br.cloture = 'P'
    br.devise = 'CFA'
    br.model_line = '0'
    br.REFERENCE_2 = 'MAJ'
    br.DATE_ECRITURE =  quitance.journee
    
    br.POSTE_COMPTABLE = Config.objects.get(code='poste_comptable').value
    br.annee_budgetaire = quitance.journee.date.year
    br.num_ecriture = lien 
    br.num_fiche = num_fiche
    
    # br.expediteur = 
    # br.destinataire =
    # br.lien_ecriture = 
    # br.who_done = 
    # br.comptable = 
    # br.SPECIFICATION_SECONDAIRE = 
    # br.observations =
    
    br.COMPTE = compte
    br.SENS_ECRITURE = sens_ecriture
    
    if sens_ecriture == 'D':
        br.montant_debit = quitance.montant
        br.montant_credit = 0
    else:
        br.montant_debit = 0
        br.montant_credit = quitance.montant
        
    br.save()

class Quitance(models.Model):
    bordereau = models.ForeignKey("Bordereau", on_delete=models.CASCADE, null=True, blank=True)
    numero = models.CharField("Numero Quittance", max_length=15, null=True, blank=True)
    numero_dr = models.CharField("Numero Declaration recette", max_length=15, null=True, blank=True)
    montant = models.BigIntegerField(_("Montant"))
    nature = models.CharField(_("Nature"), max_length=200)
    nom_prenom = models.CharField(_("Nom et Prénom"), max_length=100, null=True, blank=True)
    nom_partie_versante = models.CharField(_("Nom Parti Versante"), max_length=100, null=True, blank=True)
    partie_versante = models.ForeignKey("PartiVersante", on_delete=models.CASCADE, null=True, blank=True)
    journee = models.ForeignKey("Journee", on_delete=models.CASCADE)
    
    sent_cgib = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    @property
    def get_numero(self):
        return self.numero if self.numero != None else self.numero_dr
    
    @property
    def is_dr(self):
        return True if self.numero == None and self.numero_dr != None else False
    
    def __str__(self):
        return str(self.get_numero)
    
    
    @property
    def libele(self):
        return "libele de la quittance"
     # this is not needed if small_image is created at set_image
    # def save(self, *args, **kwargs):
    #     if self.pk is None or (self.pk is not None and self.sent_cgib == None):
    #         # try:
    #             if not self.is_dr:
    #                 do_ecriture_quitance(
    #                     post_comptable=Config.objects.get(code='poste_comptable').value, 
    #                     annee_budgetaire=self.created_by.actived_journee.date.year, 
    #                     compte_debit=Config.objects.get(code='compte_debit').value, 
    #                     compte_credit=Config.objects.get(code='compte_credit').value, 
    #                     num_quitance=self.get_numero,
    #                     montant=self.montant, 
    #                     libele=self.libele, 
    #                     journee=str(self.created_by.actived_journee), 
    #                     agent=self.created_by.cgib
    #                 )
    #                 self.sent_cgib = datetime.now()
    #         # except:
    #         #     pass
            
    #     super(Quitance, self).save(*args, **kwargs)
    
class Bordereau(models.Model):
    id = models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True)
    numero = models.CharField(_("Numero du bordereau"), max_length=10)
    type_operation = models.IntegerField(_("Type Operation"), choices=TYPE_OPERATION)
    poste_comptable = models.ForeignKey("SousStructure", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(_("Date du bordereau"))
    date_reception = models.DateField(_("Date reception"))
    nom_prenom = models.CharField(_("Nom et Prénom"), max_length=100, null=True, blank=True)
    journee = models.ForeignKey("Journee", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Bordereau")
        verbose_name_plural = _("Bordereaux")

    def __str__(self):
        return str(self.id)
    
    @property
    def montant(self):
        total = BordereauDetail.objects.filter(bordereau=self).values('montant').aggregate(total=Sum('montant'))
        return total.get('total')
    
    @property
    def nature(self):
        return "---"
    
    @property
    def quitance(self):
        return Quitance.objects.get(bordereau=self)
    
class BordereauDetail(models.Model):
    bordereau = models.ForeignKey("Bordereau", on_delete=models.CASCADE, null=True, blank=True)
    ischeque = models.BooleanField(_("Is cheque"))
    montant = models.BigIntegerField(_("Montant"))
    nature = models.ForeignKey("Nature", on_delete=models.CASCADE)
    compte = models.ForeignKey("Compte", on_delete=models.CASCADE)
    
    titulaire = models.CharField(_("Partie Versante"), max_length=100, null=True, blank=True)
    num_cheque = models.CharField(_("Numero du cheque"), max_length=10, null=True, blank=True)
    banque = models.CharField(_("Banque du cheque"), max_length=50, null=True, blank=True)
    date_cheque = models.DateField(_("Date du cheque"), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Détails Bordereau")
        verbose_name_plural = _("Détails Bordereaux")

    def __str__(self):
        return "%s %s" % (self.bordereau, self.montant)
    
class Nature(models.Model):
    libele = models.CharField(_("Libele"), max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.libele
    
class EcritureBrouillard(models.Model):
    POSTE_COMPTABLE = models.CharField(max_length=100, null=True, blank=True)
    annee_budgetaire = models.CharField(max_length=100, null=True, blank=True)
    JOURNAL = models.CharField(max_length=100, null=True, blank=True)
    AUXILIAIRE = models.CharField(max_length=100, null=True, blank=True)
    COMPTE = models.CharField(max_length=100, null=True, blank=True)
    NUM_PIECE = models.CharField(max_length=100, null=True, blank=True)
    CODE_PIECE = models.CharField(max_length=100, null=True, blank=True)
    ORDONNATEUR = models.CharField(max_length=100, null=True, blank=True)
    SENS_ECRITURE = models.CharField(max_length=100, null=True, blank=True)
    MONTANT_ECRITURE = models.CharField(max_length=100, null=True, blank=True)
    ECRITURE_LIBELLE = models.CharField(max_length=100, null=True, blank=True)
    DATE_ECRITURE = models.CharField(max_length=100, null=True, blank=True)
    ORIGINE = models.CharField(max_length=100, null=True, blank=True)
    ORIGINE_KEY = models.CharField(max_length=100, null=True, blank=True)
    DATE_CREATION = models.CharField(max_length=100, null=True, blank=True)
    UTILISATEUR_CREATION = models.CharField(max_length=100, null=True, blank=True)
    DATE_MODIFICATION = models.CharField(max_length=100, null=True, blank=True)
    UTILISATEUR_MODIFICATION = models.CharField(max_length=100, null=True, blank=True)
    num_ecriture = models.CharField(max_length=100, null=True, blank=True)
    num_fiche = models.CharField(max_length=100, null=True, blank=True)
    expediteur = models.CharField(max_length=100, null=True, blank=True)
    destinataire = models.CharField(max_length=100, null=True, blank=True)
    lien_ecriture = models.CharField(max_length=100, null=True, blank=True)
    date_echeance = models.CharField(max_length=100, null=True, blank=True)
    who_done = models.CharField(max_length=100, null=True, blank=True)
    when_done = models.CharField(max_length=100, null=True, blank=True)
    statut_ecriture = models.CharField(max_length=100, null=True, blank=True)
    cloture = models.CharField(max_length=100, null=True, blank=True)
    devise = models.CharField(max_length=100, null=True, blank=True)
    montant_debit = models.CharField(max_length=100, null=True, blank=True)
    montant_credit = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    model_line = models.CharField(max_length=100, null=True, blank=True)
    comptable = models.CharField(max_length=100, null=True, blank=True)
    SPECIFICATION_SECONDAIRE = models.CharField(max_length=100, null=True, blank=True)
    SPECIFICATION_PRINCIPALE = models.CharField(max_length=100, null=True, blank=True)
    REFERENCE_2 = models.CharField(max_length=100, null=True, blank=True)
    observations = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        return self.NUM_PIECE
    
class Config(models.Model):
    libele = models.CharField(_("Libele"), max_length=100, unique=True)
    value = models.CharField(_("Value"), max_length=500)
    code = models.SlugField(_("code"), max_length=20, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.libele