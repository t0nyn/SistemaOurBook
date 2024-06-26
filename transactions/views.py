import json
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.contrib.auth.decorators import login_required
from book.models import Book, BookCopy
from transactions.models import Loan, Renovation
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone

from user.models import OurBookUser
from book.models import BookCopy


# Create your views here.
@login_required
def loans(request):
    loans = Loan.objects.filter(Q(borrower=request.user) & Q(return_date__isnull=True))
    past_loans = Loan.objects.filter(
        Q(borrower=request.user) & Q(return_date__isnull=False)
    )
    context = {"loans": loans, "past_loans": past_loans}
    return render(request, "loans/loans.html", context=context)


def search_user_loans(request):
    if request.method == "POST":
        cpf = request.POST.get("search-input")
        try:
            user = OurBookUser.objects.get(cpf=cpf)
        except OurBookUser.DoesNotExist:
            return redirect(resolve_url("home"))

        past_loans = Loan.objects.filter(return_date__isnull=True, borrower=user)
        loans = Loan.objects.filter(return_date__isnull=False, borrower=user)
        context = {
            "past_loans": past_loans,
            "loans": loans,
        }
        return render(request, "adm/adm.html", context=context)


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

            current_number_of_loans = Loan.objects.filter(borrower=borrower_id).count()
            if current_number_of_loans > 5:
                return JsonResponse(
                    {"error": "Número máximo de empréstimos atingidos(5)."}, status=400
                )

            available_copy = book.get_available_copy()

            if not available_copy:
                return JsonResponse(
                    {"error": "Não existem exemplares disponíveis."}, status=400
                )

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
                return JsonResponse({"error": "O livro já foi devolvido"}, status=400)
            book_copy.current_status = "AVAILABLE"
            book_copy.save()
            loan.return_date = timezone.now()
            loan.save()

            return_data = {
                "loan_id": loan.id,
                "loan_status": "Livro devolvido com sucesso",
            }
            return JsonResponse(return_data, status=201)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def add_renovation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            loan_id = data.get("loan_id")

            loan = Loan.objects.get(id=loan_id)

            if not loan_id:
                return JsonResponse({"error": "Missing loan_id field"}, status=400)

            loan = get_object_or_404(Loan, id=loan_id)

            renovation_count = Renovation.objects.filter(loan=loan).count()

            if loan.book_copy.current_status == "RESERVED":
                return JsonResponse(
                    {
                        "error": "Não foi possível realizar a renovação, o exemplar encontra-se reservado."
                    },
                    status=403,
                )

            if renovation_count >= 2:
                return JsonResponse(
                    {
                        "error": "Não foi possível realizar a renovação, você já atingiu o limite de renovações disponíveis."
                    },
                    status=403,
                )

            if timezone.now().date != loan.expected_return_date:
                return JsonResponse(
                    {
                        "error": "Só é possível renovar o empréstimo no último dia do prazo de devolução."
                    },
                    status=403,
                )

            loan.expected_return_date = timezone.now() + timedelta(days=15)
            loan.save()

            renovation = Renovation.objects.create(loan=loan)

            renovation_data = {
                "id": renovation.id,
                "renovation_date": renovation.renovation_date,
                "expected_return_date": renovation.loan.expected_return_date,
                "loan_id": renovation.loan.id,
                "renovation_status": "Renovation Added Succesfully",
            }

            return JsonResponse(renovation_data, status=201)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Loan.DoesNotExist:
            return JsonResponse({"error": "Loan not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
