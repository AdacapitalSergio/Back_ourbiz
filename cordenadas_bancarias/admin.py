from django.contrib import admin
from .models import CordenadasBancarias


@admin.register(CordenadasBancarias)
class CordenadasBancariasAdmin(admin.ModelAdmin):
    list_display = ("banco", "numero_conta", "titular_conta", "iban", "numero_express", "swift_bic")
    search_fields = ("banco", "numero_conta", "titular_conta", "iban", "numero_express", "swift_bic")