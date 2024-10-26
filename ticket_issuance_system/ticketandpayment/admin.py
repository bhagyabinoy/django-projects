from django.contrib import admin
from .models import *
from .djongo_models import TicketCollection

# Register your models here.


admin.site.register(AdminModule)
admin.site.register(TicketCollection)
admin.site.register(Payment)
admin.site.register(Pricing)