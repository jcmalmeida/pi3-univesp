from django import forms

class ProfileTypeForm2(forms.Form):
    profile_type = forms.ChoiceField(
        choices=[('aluno', 'Aluno'), ('anunciante', 'Anunciante')],
        label='',
        required=True
    )


