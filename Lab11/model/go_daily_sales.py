from dataclasses import dataclass
from datetime import datetime
from model.go_products import Go_Product

@dataclass
class GoDailySales:
    Product1: Go_Product
    Product2: Go_Product
    peso: int


    def __str__(self):
        return f'{self.Product1.Product_number}-{self.Product2.Product_number}-{self.peso}'