from django.contrib import admin
from .models import City, ProgrammingLanguage, Vacancy, Error, Url

# Register your models here.

admin.site.register(City)
admin.site.register(ProgrammingLanguage)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
