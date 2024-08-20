from django.db import models

class MyModel(models.Model):
    Category = models.CharField(max_length=255)
    url = models.CharField(max_length=255)  # URL stored as a string
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)  # Store price as a string
    MRP = models.CharField(max_length=255)    # Store MRP as a string
    available_skus = models.CharField(max_length=255)  # Store SKU as a string
    fit = models.CharField(max_length=255)
    fabric = models.CharField(max_length=255)
    neck = models.CharField(max_length=255)
    sleeve = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
    length = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)  # Assuming longer text, adjust as needed

