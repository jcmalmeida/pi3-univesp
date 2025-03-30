from django.db import models
from django.contrib.auth.models import User
from usuarios.models import *
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
from .validators import validar_cnpj  # Importe a função de validação de CNPJ
class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    nome = models.CharField(max_length=255, verbose_name="Nome da empresa")

    def __str__(self):
        return f"{self.nome} ({self.cnpj})"

    def clean(self):
        # Validação customizada para o campo CNPJ no modelo
        if not validar_cnpj(self.cnpj):
            raise ValidationError("CNPJ inválido.")

class Vaga(models.Model):
    nome = models.CharField(max_length=255)
    descricao=CKEditor5Field('Text', config_name='extends')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    link = models.URLField(blank=True)
    inativa = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

