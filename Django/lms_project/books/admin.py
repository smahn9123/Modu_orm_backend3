from django.contrib import admin
from .models import Book, Loan,Reservation
# Register your models here.

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Reservation)
