from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.is_active = True
        obj.set_password(obj.password)
        obj.save()


    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
    ]

    fields = [
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'groups',
        'user_permissions'
    ]


class GiornoChiusuraAdmin(admin.ModelAdmin):
    list_display = [
        'data'
    ]
    fields = [
        'data'
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
        'fatto',
        'controlli_extra'
    ]

    list_display = [
        'n_matricola',
        'cognome',
        'nome',
        'fatto',
        'impiego',
    ]



class PrepostoAdmin(admin.ModelAdmin):
    fields = [
        'n_matr',

        'nome',
        'cognome',
        'superiore',

    ]
    list_display = [
        'n_matr',
        'nome',
        'cognome',
    ]



class ImpiegoAdmin(admin.ModelAdmin):
    list_display = [
        'impiego',
    ]
    fields = [
        'impiego',
        'controlli',
    ]


class ResponsabileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.is_active = True
        obj.set_password(obj.password)

        try:
            print Group.objects.all()[0]
            obj.groups.add(Group.objects.all()[0])
        except:
            print "Errore assegnamento gruppo"

        obj.save()
    fields = [
        'username',
        'passw',
        'first_name',
        'last_name',

        'email',

        'groups',
        'is_staff',

    ]
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
    ]

class ImpostazioneAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Generali', {
            'fields': (
                'titolo',
                'data_inizio',
                'attiva',
            )
        }),
        ('Parametri email', {
            #'classes': ('collapse',),
            'fields': (
                'messaggio',
            )
        }),
        ('Parametri riguardanti i controlli', {
            #'classes': ('collapse',),
            'fields': (
                'sogliaControllo_ore',
                'sogliaControllo_minuti',
            )
        }),
        ('Giorni di lavoro', {
            'classes': ('collapse',),
            'fields': (
                'lunedi',
                'martedi',
                'mercoledi',
                'giovedi',
                'venerdi',
                'sabato',
                'domenica',
            )
        }),
    )

    list_display = [

        'titolo',
        'is_today',
        'attiva',
        'creazione',
        'data_inizio',
    ]


class OrarioAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'orario'
    ]
    ordering = [
        'orario'
    ]
'''
class UtenteAdmin(admin.ModelAdmin):
    fields = [

        'username',
        'password',

        'nome',
        'cognome',

        'n_matr',
        #'superiore',

    ]
    list_display = [

        'username',
        'n_matr',
        'nome',
        'cognome',
    ]
'''
#admin.site.register(Utente, UtenteAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Responsabile, ResponsabileAdmin)
admin.site.register(Preposto, PrepostoAdmin)
admin.site.register(Dipendente, DipendenteAdmin)
admin.site.register(Controllo, ControlloAdmin)
admin.site.register(ControlloAggiuntivo, ControlloAdmin)
admin.site.register(Impiego, ImpiegoAdmin)
admin.site.register(Orario, OrarioAdmin)
admin.site.register(Impostazione, ImpostazioneAdmin)
admin.site.register(GiornoChiusura, GiornoChiusuraAdmin)
