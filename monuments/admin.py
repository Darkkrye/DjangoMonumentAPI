from django.contrib import admin
from .models import *

# Register your models here.

# Url : http://127.0.0.1:8000/admin/
# Username : admin
# Password : esgi4moc1

admin.site.register(Person)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Monument)
admin.site.register(Note)

