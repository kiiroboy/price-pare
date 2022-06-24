from cProfile import label
from django.db import models
from .utils import get_link_data, convert_to_localtime
# Create your models here.
class Main(models.Model):
    name = models.CharField(max_length=220, blank=True)
    url = models.URLField(max_length=220, blank=True)
    current_price = models.FloatField(default=-1)
    previous_price = models.FloatField(default=-1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    logo_url = models.CharField(max_length=220, blank=True)
    price_change = models.FloatField(default=-1)
    
    def __str__(self):
        return self.name
    def save(self, *arg, **kwargs):
        name, price, logo_url = get_link_data(self.url)
        price = float(price[1:])
        previous_price = self.current_price
        self.previous_price = previous_price
        self.name = name
        self.logo_url = logo_url
        self.current_price = price
        if previous_price != -1:
            self.price_change=abs(self.current_price-self.previous_price)/self.previous_price*100
        super().save(*arg, **kwargs)