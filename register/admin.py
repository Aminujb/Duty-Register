from django.contrib import admin

from .models import Employee, Unit, UnitType, Country, State, Rank, Speciality, Tcomm

admin.site.register(Employee)
admin.site.register(Unit)
admin.site.register(UnitType)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Rank)
admin.site.register(Speciality)
admin.site.register(Tcomm)
