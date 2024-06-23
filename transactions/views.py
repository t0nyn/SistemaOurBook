import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from book.models import Book, BookCopy
from transactions.models import Loan, Renovation
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from user.models import OurBookUser


# Create your views here.
@login_required
def loans(request):
    loans = Loan.objects.filter(Q(borrower=request.user) & Q(return_date__isnull=True))
    past_loans = Loan.objects.filter(
        Q(borrower=request.user) & Q(return_date__isnull=False)
    )
    context = {"loans": loans, "past_loans": past_loans}
    return render(request, "loans/loans.html", context=context)


def loan_item(request, id):
    try:
        loan = Loan.objects.get(id=id)
        renovations = Renovation.objects.filter(loan=loan)
        loan_data = {
            "loan_id": loan.id,
            "borrowed_date": loan.borrowed_date,
            "expected_return_date": loan.expected_return_date,
            "return_date": loan.return_date,
            "book_copy": {
                "id": loan.book_copy.id,
                "current_status": loan.book_copy.current_status,
                "book": {
                    "id": loan.book_copy.book.id,
                    "name": loan.book_copy.book.name,
                    "author": loan.book_copy.book.author,
                    "cover": (
                        loan.book_copy.book.cover.url
                        if loan.book_copy.book.cover
                        else ""
                    ),
                    "description": loan.book_copy.book.description,
                    "edition": loan.book_copy.book.edition,
                    "publisher": loan.book_copy.book.publisher,
                    "year": loan.book_copy.book.year,
                    "num_pages": loan.book_copy.book.num_pages,
                    "categories": [
                        category.name
                        for category in loan.book_copy.book.categories.all()
                    ],
                },
            },
            "borrower": (
                {
                    "cpf": loan.borrower.cpf,
                    "username": loan.borrower.username,
                }
                if loan.borrower
                else None
            ),
            "renovations": [
                {
                    "id": renovation.id,
                    "renovation_date": renovation.renovation_date,
                }
                for renovation in renovations
            ],
        }

        return JsonResponse(loan_data)
    except Loan.DoesNotExist:
        return JsonResponse({"error": "Loan not found"}, status=404)


@csrf_exempt
def add_loan(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            book_id = data.get("book_id")
            borrower_id = data.get("borrower_id")

            book = Book.objects.get(id=book_id)
            borrower = OurBookUser.objects.get(cpf=borrower_id)

            available_copy = book.get_available_copy()

            if not available_copy:
                return JsonResponse({"error": "No available book copies"}, status=400)

            loan = Loan.objects.create(book_copy=available_copy, borrower=borrower)
            available_copy.current_status = "BORROWED"
            available_copy.save()

            loan_data = {
                "loan_id": loan.id,
                "borrowed_date": loan.borrowed_date,
                "expected_return_date": loan.expected_return_date,
                "return_date": loan.return_date,
                "book_copy": {
                    "id": loan.book_copy.id,
                    "current_status": loan.book_copy.current_status,
                    "book": {
                        "id": loan.book_copy.book.id,
                        "name": loan.book_copy.book.name,
                        "author": loan.book_copy.book.author,
                        "cover": (
                            loan.book_copy.book.cover.url
                            if loan.book_copy.book.cover
                            else ""
                        ),
                        "description": loan.book_copy.book.description,
                        "edition": loan.book_copy.book.edition,
                        "publisher": loan.book_copy.book.publisher,
                        "year": loan.book_copy.book.year,
                        "num_pages": loan.book_copy.book.num_pages,
                        "categories": [
                            category.name
                            for category in loan.book_copy.book.categories.all()
                        ],
                    },
                },
                "borrower": (
                    {
                        "cpf": loan.borrower.cpf,
                        "username": loan.borrower.username,
                    }
                    if loan.borrower
                    else None
                ),
            }

            return JsonResponse(loan_data, status=201)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def return_book(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            loan_id = data.get("loan_id")

            loan = Loan.objects.get(id=loan_id)
            book_copy = BookCopy.objects.get(id=loan.book_copy.id)

            if book_copy.current_status == "AVAILABLE":
                return JsonResponse(
                    {"error": "This book has already been returned"}, status=400
                )
            book_copy.current_status = "AVAILABLE"
            book_copy.save()
            loan.return_date = timezone.now()
            loan.save()

            return_data = {
                "loan_id": loan.id,
                "loan_status": "Loan Returned Succesfully",
            }
            return JsonResponse(return_data, status=201)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
