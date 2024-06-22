from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Loan
from django.db.models import Q


# Create your views here.
@login_required
def loans(request):
    loans = Loan.objects.filter(Q(borrower=request.user) & Q(return_date__isnull=True))
    past_loans = Loan.objects.filter(
        Q(borrower=request.user) & Q(return_date__isnull=False)
    )
    context = {"loans": loans, "past_loans": past_loans}
    return render(request, "loans/loans.html", context=context)
