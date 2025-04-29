from django.contrib import admin


from .models import Empresa, Vaga, Curso


admin.site.register(Empresa)
admin.site.register(Vaga)
admin.site.register(Curso)

# Register your models here.
