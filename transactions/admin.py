from django.contrib import admin
from transactions.models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass
