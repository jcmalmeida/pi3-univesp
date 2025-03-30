from django import forms
from .models import Vaga, Empresa
from django import forms
from .models import Vaga, Empresa
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import ValidationError
from .models import Empresa
from .validators import validar_cnpj  # Importa o validador


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['nome', 'descricao', 'empresa', 'link', 'inativa']
        widgets = {
            'descricao': CKEditor5Widget(config_name='default'),  # Configura o CKEditor para o campo descrição
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Preenchendo o campo empresa com empresas já cadastradas
        empresas = Empresa.objects.all()
        empresa_choices = [(empresa.id, empresa.nome) for empresa in empresas]
        empresa_choices.insert(0, ('', 'Selecione uma empresa'))
        self.fields['empresa'].choices = empresa_choices

        # Adicionando placeholders e removendo labels
        self.fields['nome'].widget.attrs.update({'placeholder': 'Título da Vaga'})
        self.fields['empresa'].widget.attrs.update({'placeholder': 'Selecione uma empresa'})
        self.fields['link'].widget.attrs.update({'placeholder': 'Link para a Vaga (opcional)'})

        # Configurando o campo 'inativa' como uma escolha entre "Ativa" e "Inativa"
        self.fields['inativa'] = forms.ChoiceField(
            choices=[(False, 'Ativa'), (True, 'Inativa')],
            widget=forms.Select(),
            label='Status da Vaga'
        )

        # Remover os labels
        for field in self.fields:
            self.fields[field].label = ''

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')

        # Verifica se uma empresa foi selecionada
        if not empresa:
            raise forms.ValidationError("Você deve selecionar uma empresa.")

        return cleaned_data


#class EmpresaForm(forms.ModelForm):
#    class Meta:
#        model = Empresa
#        fields = ['nome', 'cnpj']
#        widgets = {
#            'nome': forms.TextInput(attrs={'placeholder': 'Nome da Empresa'}),
#            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ (XX.XXX.XXX/XXXX-XX)'}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        # Remover labels dos campos
#        self.fields['nome'].label = ''
#        self.fields['cnpj'].label = ''
#
#
#    def clean_cnpj(self):
#        cnpj = self.cleaned_data.get('cnpj')
#        if not validar_cnpj(cnpj):
#            raise ValidationError("CNPJ inválido.")
#        return cnpj



class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['cnpj', 'nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da Empresa', 'readonly': 'readonly'}),
            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ (XX.XXX.XXX/XXXX-XX)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = ''
        self.fields['cnpj'].label = ''
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        
        # Verifica se o CNPJ já existe, ignorando a instância atual em caso de edição
        if Empresa.objects.filter(cnpj=cnpj).exists():
            raise ValidationError("Este CNPJ já está cadastrado. Por favor, insira um CNPJ diferente.")
        
        return cnpj
