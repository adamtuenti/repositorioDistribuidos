from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    privilegios = serializers.ReadOnlyField(source="get_privilegios")

    def create(self, validated_data):
        usuario = Usuario.objects.create(
            cedula = validated_data['cedula'],
            username=validated_data['username'],
            email = validated_data['email'],
            telefono = validated_data['telefono'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        usuario.set_password(validated_data['password'])
        usuario.save()
        # idUsuario = Usuario.objects.order_by('-id')[0]
        # assign_role(idUsuario, 'cliente')
        return usuario  

    class Meta:
        fields = (
            'id',
            'cedula',
            'username',
            'imagen',
            'email',
            'first_name',
            'last_name',
            'password',
            'telefono',
            'is_active',
            'privilegios'
        )
        model = Usuario

