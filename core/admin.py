from django.contrib import admin

# Register your models here.
from .models import Booking

admin.site.register(Booking)



from .models import Payment

admin.site.register(Payment)

from .models import MenuItem
admin.site.register(MenuItem)