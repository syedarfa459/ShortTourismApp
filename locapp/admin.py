from django.contrib import admin
from .models import Destination,Tourist,DestinationDetails, DestinationMetaDetails
# Register your models here.
admin.site.register(Destination)
admin.site.register(Tourist)
admin.site.register(DestinationDetails)
admin.site.register(DestinationMetaDetails)

