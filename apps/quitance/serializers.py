from rest_framework import serializers
from .models import PartiVersante, TypePartiVersante

class TypePartiVersanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePartiVersante
        fields = "__all__"


class PartiVersanteSerializer(serializers.ModelSerializer):
    type_versante = TypePartiVersanteSerializer(many=False)
    class Meta:
        model = PartiVersante
        fields = "__all__"

    def to_representation(self, instance):
        result = super(PartiVersanteSerializer, self).to_representation(instance)
        result['text'] = "%s: %s" % (instance.nom_prenom, instance.reference) 
        
        return result