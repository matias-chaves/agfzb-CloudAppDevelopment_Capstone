from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=30, default='car make')
    description = models.CharField(max_length=500, default='car make description')

    def __str__(self):
        return "Name:" + self.name + ", "+ \
        "Description:" + self.description
    

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TYPE_CHOICES = (
        (SEDAN, "SEDAN"),
        (SUV, "SUV"),
        (WAGON, "WAGON")
    )

    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30, default='car model')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(default=now)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: " + self.name + ", " + \
            "DealerId: " + self.dealer_id.__str__() + "," + \
            "Type: " + self.type + "," + \
            "Year: " + self.year.__str__()
    


# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

        def __str__(self):
            return "Dealer name: " + self.full_name
        


# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review

    def __str__(self):
        return "Review: " + self.review
        