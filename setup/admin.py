from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.save()

    list_display = [
        'username',
        'last_name',
        'first_name',
        'email',
        'is_staff',

    ]



class ControlloAdmin(admin.ModelAdmin):
    fields = ['titolo',
              'descrizione',
              ]



class DipendenteAdmin(admin.ModelAdmin):
    fields = [
        'nome',
        'cognome',
        'n_matricola',
        'impiego',
        'controlli_adhoc'
    ]

    list_display = [
        'n_matricola',
        'cognome',
        'nome',
        'impiego',
    ]



class PrepostoAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'password',
        'first_name',
        'last_name',

        'sottoposti',
        'superiore',
    ]
    list_display = [
        'id',
        'n_matr',
        'first_name',
        'last_name',
    ]
'''
class PrepostoAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'password',
        'last_name',
        'first_name',
        'sottoposti',
        'email',
        'groups',

    ]
    list_display = [
        'cod',
        'last_name',
        'first_name',
        'email',
    ]
'''



class ImpiegoAdmin(admin.ModelAdmin):
    list_display = [
        'impiego',
    ]


class ResponsabileAdmin(admin.ModelAdmin):

    fields = [
        'username',
        'password',
        'last_name',
        'first_name',
        'email',
        'groups',

    ]
    list_display = [
        'id',
        'last_name',
        'first_name',
        'email',
    ]

class ImpostazioneAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Generali', {
            'fields': (
                'data_inizio',
            )
        }),
        ('Parametri email', {
            'fields': (
                'smtp_server',
                'port',
                'smtp_username',
                'smtp_password',
                'messaggio',
            )
        }),
        ('Parametri riguardanti i controlli', {
            #'classes': ('collapse',),
            'fields': (
                'orari_selezione',
                'sogliaControllo_ore',
                'sogliaControllo_minuti',
            )
        }),
    )

    list_display = [
        'id',
        'nuovo',
        'creazione',
        'data_inizio',
        'smtp_server',
        'smtp_username',
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Responsabile, ResponsabileAdmin)
admin.site.register(Preposto, PrepostoAdmin)
admin.site.register(Dipendente, DipendenteAdmin)
admin.site.register(Controllo, ControlloAdmin)
admin.site.register(ControlloAggiuntivo, ControlloAdmin)
admin.site.register(Impiego, ImpiegoAdmin)
admin.site.register(Orario)
admin.site.register(Impostazione, ImpostazioneAdmin)
