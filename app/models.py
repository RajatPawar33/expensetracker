from django.db import models
import uuid
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Transaction(BaseModel):
    TRANSACTION_TYPES = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )

    description = models.CharField(max_length=100)
    amount = models.FloatField()
    transtype = models.CharField(max_length=10,default='Debit' ,choices=TRANSACTION_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)  # Balance after the transaction
    income = models.FloatField(default=0.0)  # Total income after the transaction
    expense = models.FloatField(default=0.0)  # Total expense after the transaction

    class Meta:
        ordering = ('-created_at',)  # Most recent transactions first

    # def __str__(self):
    #     return f"{self.description} - {self.transtype} - {self.amount}"
