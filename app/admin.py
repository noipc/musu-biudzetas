import csv
import io
from django.contrib import admin
from .models import User, Entity, Budget, Program, Region, Municipality, PublicSector, EntitySector, EntityType
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

class ProgramInline(admin.TabularInline):
    model = Program

    exclude = ['slug']

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

    list_display = ['name', 'municipality', 'pub_sector']

    inlines = [ ProgramInline, BudgetInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if not isinstance(inline, ProgramInline) or obj is not None:
                yield inline.get_formset(request, obj), inline

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                if col[3] == '':
                    start_date_val = None
                else:
                    start_date_val = col[3]

                if col[4] == '':
                    end_date_val = None
                else:
                    end_date_val = col[4]

                if col[7] == '':
                    pub_sector_val = None
                else:
                    pub_sector_val = col[7]

                if col[8] == '':
                    pub_subsector_val = None
                else:
                    pub_subsector_val = col[8]
                _, created = Entity.objects.update_or_create(
                    legal_id = col[0],
                    name = col[1],
                    municipality_id = col[2],
                    start_date = start_date_val,
                    end_date = end_date_val,
                    entity_cat_id = col[5],
                    entity_type_id = col[6],
                    pub_sector_id = pub_sector_val,
                    pub_subsector = pub_subsector_val,
                    status = int(col[9]),
                    is_funder = col[10],
                    is_accountable = col[11],
                    accounts_url = col[12],
                    comments = col[13],
                    created_by_id = 1
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})


@admin.register(Program)
class ProgramAdmin(CommonAdminModel):
    inlines = [BudgetInline]

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = Region.objects.update_or_create(
                    id = col[0],
                    name = col[1],
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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = Municipality.objects.update_or_create(
                    id = col[0],
                    name = col[1],
                    region_id = col[2],
                    child_pop = col[3],
                    adult_pop = col[4],
                    senior_pop = col[5],
                    area = col[6],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(PublicSector)
class PublicSectorAdmin(CommonAdminModel):

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = PublicSector.objects.update_or_create(
                    id = col[0],
                    name = col[1],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})
    
@admin.register(EntitySector)
class EntitySectorAdmin(CommonAdminModel):

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = EntitySector.objects.update_or_create(
                    id = col[0],
                    name = col[1],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(EntityType)
class EntityTypeAdmin(CommonAdminModel):

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = EntityType.objects.update_or_create(
                    id = col[0],
                    name = col[1],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

# Laikinai reikia registruoti Biudžeto modelį, masiniam duomenų užkrovimui.

@admin.register(Budget)
class BudgetAdmin(CommonAdminModel):

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
            for col in csv.reader(io_string, delimiter=';', quotechar='"'):
                _, created = Budget.objects.update_or_create(
                    entity_id = col[0],
                    amount = col[1],
                    year = col[2],
                    b_source = col[3],
                    b_type = col[4],
                    created_by_id = 1,
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})
