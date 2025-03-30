from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from .models import *

###############################################################################
###############################################################################
###############################################################################

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label=''
    )

###############################################################################
###############################################################################
###############################################################################

class CustomUserCreationForm(UserCreationForm):
    usable_password = None
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        placeholders = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirme senha',
        }

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({
                'placeholder': placeholders.get(fieldname, '')
            })
            self.fields[fieldname].label = ''

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está registrado.")
        return email
###############################################################################
###############################################################################
###############################################################################

class ProfileTypeForm(forms.Form):
    profile_type = forms.ChoiceField(
        choices=[('aluno', 'Aluno'), ('anunciante', 'Anunciante')],
        label='',
        required=True
    )

###############################################################################
###############################################################################
###############################################################################
class AlunoProfileForm(forms.ModelForm):
    class Meta:
        model = AlunoProfile
        fields = [
            'nome', 
            'instituicao', 
            'outra_instituicao', 
            'curso', 
            'outro_curso', 
            'is_formado',
            'semestre', 
            'telefone'
        ]

    def __init__(self, *args, **kwargs):
        super(AlunoProfileForm, self).__init__(*args, **kwargs)

        placeholders = {
            'nome': 'Nome completo',
            'instituicao': 'Instituição',
            'outra_instituicao': 'Digite sua instituição',
            'curso': 'Curso',
            'outro_curso': 'Digite seu curso',
            'is_formado': 'formado?',  # placeholder para formado
            'semestre': 'Semestre',
            'telefone': 'Telefone de contato',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = ''  # Remover os labels para manter o design limpo

    def clean(self):
        cleaned_data = super().clean()
        instituicao = cleaned_data.get('instituicao')

        # Se o usuário escolheu "UNIVESP", remover os dados de "Outra Instituição"
        if instituicao == 'UNIVESP':
            cleaned_data['outra_instituicao'] = None
            cleaned_data['outro_curso'] = None

        # Se o usuário escolheu "OUTRA", remover os dados de "OUTRA"
        elif instituicao == 'OUTRA':
            cleaned_data['curso'] = None

        return cleaned_data

class AnuncianteProfileForm(forms.ModelForm):
    class Meta:
        model = AnuncianteProfile
        fields = ['nome_completo', 'instituicao', 'cargo', 'telefone']

    def __init__(self, *args, **kwargs):
        super(AnuncianteProfileForm, self).__init__(*args, **kwargs)

        placeholders = {
            'nome_completo': 'Nome completo',
            'instituicao': 'Empresa',
            'cargo': 'Cargo',
            'telefone': 'Telefone de contato',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = ''

###############################################################################
###############################################################################
###############################################################################

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail'})
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['username'].help_text = None


from django import forms
from .models import AlunoProfile

class AlunoProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AlunoProfile
        fields = [
            'nome',
            'instituicao',
            'outra_instituicao',
            'curso',
            'outro_curso',
            'is_formado',
            'semestre',
            'telefone'
        ]

    def __init__(self, *args, **kwargs):
        super(AlunoProfileUpdateForm, self).__init__(*args, **kwargs)
        placeholders = {
            'nome': 'Nome completo',
            'instituicao': 'Instituição',
            'outra_instituicao': 'Digite a outra instituição',
            'curso': 'Curso',
            'outro_curso': 'Digite o outro curso',
            'is_formado': 'formado?',  # placeholder para formado
            'semestre': 'Semestre atual',
            'telefone': 'Telefone de contato',
        }

        # Definindo os placeholders para cada campo e removendo os labels
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
            self.fields[field].label = ''

    def clean(self):
        cleaned_data = super().clean()
        instituicao = cleaned_data.get('instituicao')

        # Se o usuário escolheu "UNIVESP", remover os dados de "Outra Instituição"
        if instituicao == 'UNIVESP':
            cleaned_data['outra_instituicao'] = None
            cleaned_data['outro_curso'] = None

        # Se o usuário escolheu "OUTRA", remover os dados de "OUTRA"
        elif instituicao == 'OUTRA':
            cleaned_data['curso'] = None

        return cleaned_data

class AnuncianteProfileUpdateForm(forms.ModelForm):
    usable_password = None

    class Meta:
        model = AnuncianteProfile
        fields = ['nome_completo', 'instituicao', 'cargo', 'telefone']

    def __init__(self, *args, **kwargs):
        super(AnuncianteProfileUpdateForm, self).__init__(*args, **kwargs)
        placeholders = {
            'nome_completo': 'Nome Completo',
            'instituicao': 'Instituição',
            'cargo': 'Cargo',
            'telefone': 'Telefone de contato'
        }
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = ''

###############################################################################
###############################################################################
###############################################################################



from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha antiga'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua nova senha'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua nova senha'
        })

        # Remove os textos de ajuda (help_text)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = ''
            self.fields[fieldname].label = ''














# password reset
from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}
        ),
        label=''  # Remove o label aqui
    )
from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova senha'}),
        label=''  # Remova o label
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua nova senha'}),
        label=''  # Remova o label
    )


