from django.contrib import admin
from .models import *


class SettimanaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Generali', {
            'fields': (
                'cod_preposto',
                'area',
                'data_inizio',
            )
        }),
        ('Orari', {

            'fields': (
                'lun',
                'mar',
                'mer',
                'gio',
                'ven',
            ),
            },
         ),
        ('Selezione giorni chiusura', {
            'classes': ('collapse',),
            'fields': (
                'lun_festivo',
                'mar_festivo',
                'mer_festivo',
                'gio_festivo',
                'ven_festivo',
            ),
        }),
        ('Debug',{
            'fields': (
                'lun_fatto',
                'lun_check',
                'mar_fatto',
                'mar_check',
                'mer_fatto',
                'mer_check',
                'gio_fatto',
                'gio_check',
                'ven_fatto',
                'ven_check',
                )
        }
    ))

    list_display = [
        'id',
        'completato',
        'cod_preposto',
        'area',
        'data_inizio',
	    'lun_fatto',
	    'lun_check',
        'mar_fatto',
        'mar_check',
        'mer_fatto',
        'mer_check',
        'gio_fatto',
        'gio_check',
        'ven_fatto',
        'ven_check',
    ]

class SegnalazioneAdmin(admin.ModelAdmin):
    fields =[
        'matricola',
        'dettaglio'
    ]

    list_display = [
        'id',
        'matricola',
        'data'
    ]
    readonly_fields = ('data',)

class SegnalazionePrepAdmin(admin.ModelAdmin):
    fields =[
        'matricola',
        'dettaglio'
    ]

    list_display = [
        'id',
        'matricola',
        'data'
    ]
    readonly_fields = ('data',)

admin.site.register(Settimana, SettimanaAdmin)
admin.site.register(Segnalazione, SegnalazioneAdmin)
admin.site.register(SegnalazionePrep, SegnalazionePrepAdmin)