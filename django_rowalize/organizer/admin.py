from django.contrib import admin

from .models import Rower,Boat,CoxBox, Blades, Event, Crew
# Register your models here.
admin.site.register(Rower)
admin.site.register(Boat)
admin.site.register(CoxBox)
admin.site.register(Blades)
admin.site.register(Event)
admin.site.register(Crew)