from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name
    

import uuid

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Paid")

    transaction_id = models.CharField(max_length=100, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.method}"
    


class MenuItem(models.Model):
   

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=50, default="Fast Food")
    def __str__(self):
        return self.name

class Order(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name