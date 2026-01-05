from django.db import models

# Create your models here.


class Budget(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    month = models.PositiveIntegerField()  # 1 تا 12
    year = models.PositiveIntegerField()  # مثلا 2024

    class Meta:
        unique_together = ('category', 'month', 'year')

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}: {self.amount}"