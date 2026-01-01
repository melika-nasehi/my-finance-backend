from django.db import models

import Account
import Category


# Create your models here.


class Transaction(models.Model):
    id = models.IntegerField()
    date = models.DateField()
    amount = models.FloatField()
    desc = models.CharField(max_length=200)
    INCOME = "income"
    OUTCOME = "outcome"
    TRANS_KIND ={
        INCOME : 'Income',
        OUTCOME : 'Outcome'
    }
    kind = models.CharField(max_length=7 , default=INCOME, choices=TRANS_KIND),
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol