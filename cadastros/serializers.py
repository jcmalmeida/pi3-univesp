# seu_app/serializers.py
from rest_framework import serializers

class UploadArquivoSerializer(serializers.Serializer):
    arquivo = serializers.FileField()
