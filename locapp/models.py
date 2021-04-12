from django.db import models

# Create your models here.

class Tourist(models.Model):

    tourist_name = models.CharField(max_length = 30)
    tourist_latitude = models.FloatField(null = True)
    tourist_longitude = models.FloatField(null = True)
    tourist_location = models.CharField(max_length = 50)

    def __str__(self):
        return self.tourist_name + self.tourist_location

class Destination(models.Model):
    
    destination = models.CharField(max_length = 150)
    distance = models.DecimalField(max_digits = 10, decimal_places = 2)
    dated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Distance from TouristLocation to {self.destination} is {self.distance} km"

class DestinationDetails(models.Model):

    destination_name = models.CharField(max_length=50)
    destinationImage = models.ImageField(upload_to='destinationImages', blank = True, null = True)
    destination_desc = models.CharField(max_length = 256)
    destination_extras = models.CharField(max_length=200)

    def __str__(self):

        return self.destination_name

class DestinationMetaDetails(models.Model):

    meta_destination = models.ForeignKey(DestinationDetails, models.CASCADE)
    meta_destination_name = models.CharField(max_length=60)
    meta_destination_Image = models.ImageField(upload_to='metadestinationImages')
    meta_destination_desc = models.CharField(max_length=256)
    destination_extras = models.CharField(max_length=200)


    def __str__(self):

        return self.meta_destination_name + " " + self.meta_destination.destination_name