import csv
import io
from django.contrib import admin
from .models import User, Entity, Budget, Program, Currency, Region, Municipality, PublicSector, EntitySector, EntityType, Currency
from .forms import CsvUploadForm
from django.urls import path
from django.shortcuts import render, redirect

# Register your models here.

admin.site.site_header = "Mūsų Biudžetas - administracija"

class BudgetInline(admin.TabularInline):
    model = Budget

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        else:
            obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)

class CommonAdminModel(admin.ModelAdmin):
    exclude = ['slug']

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        else:
            obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(Entity)
class EntityAdmin(CommonAdminModel):

    inlines = [ BudgetInline, ]

@admin.register(Program)
class ProgramAdmin(CommonAdminModel):
    pass

@admin.register(Region)
class RegionAdmin(CommonAdminModel):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_csv/', self.import_csv)]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for row in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = Region.objects.update_or_create(
                    id = row[0],
                    name = row[1],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})


@admin.register(Municipality)
class MunicipalityAdmin(CommonAdminModel):
    list_display = ['name', 'region', 'area', 'child_pop', 'adult_pop', 'senior_pop']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_csv/', self.import_csv)]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for row in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = Municipality.objects.update_or_create(
                    id = row[0],
                    name = row[1],
                    region_id = row[2],
                    child_pop = row[3],
                    adult_pop = row[4],
                    senior_pop = row[5],
                    area = row[6],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(PublicSector)
class PublicSectorAdmin(CommonAdminModel):
    pass
    
@admin.register(EntitySector)
class PublicSectorAdmin(CommonAdminModel):
    pass

@admin.register(EntityType)
class EntityTypeAdmin(CommonAdminModel):
    pass

@admin.register(Currency)
class CurrencyAdmin(CommonAdminModel):
    pass