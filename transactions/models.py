from datetime import timedelta
from django.utils import timezone
from django.db import models
from user.models import OurBookUser
from book.models import BookCopy


# Create your models here.
class Loan(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    expected_return_date = models.DateField(default=timezone.now() + timedelta(days=15))
    return_date = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(OurBookUser, on_delete=models.SET_NULL, null=True)


class Renovation(models.Model):
    loan = models.ForeignKey(Loan, related_name='renovations', on_delete=models.CASCADE)
    renovation_date = models.DateField(auto_now_add=True)
