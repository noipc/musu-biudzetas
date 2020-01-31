import csv
import io
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import User, Entity, Budget, Program, Region, Municipality, PublicSector, EntitySector, EntityType, Comment
from .forms import CsvUploadForm
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

# Register your models here.

admin.site.site_header = "Mūsų Biudžetas - administracija"

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password' )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
    (None, {'fields': ('username', 'password')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'entity')}),
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')})
    )

admin.site.register(User, UserAdmin)
    
class BudgetInline(admin.TabularInline):
    model = Budget

    fields = ('year', 'amount', 'b_source', )

    extra = 0

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        else:
            obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)

class ProgramInline(admin.TabularInline):
    model = Program

    exclude = ['slug', 'program_code']

    extra = 0

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        else:
            obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)

class CommentInline(admin.TabularInline):
    model = Comment

    fields = ("year", "comments")

    extra = 0

class CommonAdminModel(admin.ModelAdmin):
    exclude = ['slug']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import_csv/', self.import_csv)]
        return my_urls + urls


    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        else:
            obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(Entity)
class EntityAdmin(CommonAdminModel):

    list_display = ['name', 'municipality', 'pub_sector', 'status', 'is_accountable', 'no_users', 'no_employees']

    inlines = [ ProgramInline, BudgetInline, CommentInline]

    # def get_formsets_with_inlines(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         # hide MyInline in the add view
    #         if not isinstance(inline, ProgramInline) or obj is not None:
    #             yield inline.get_formset(request, obj), inline

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Entity.objects.update_or_create(
                    id = col[0],
                    defaults = {
                       'legal_id':col[1], 'name':col[2], 'municipality_id':col[3], 'start_date':col[4], 'end_date':col[5],
                       'entity_cat_id':col[6], 'entity_type_id':col[7], 'pub_sector_id':col[8], 'pub_subsector':col[9], 
                       'status':col[10], 'is_funder':col[10], 'is_municipality':col[11], 'is_ministry':col[12], 
                       'is_accountable':col[13], 'accounts_url':col[14], 'no_employees':col[15], 'no_users':col[16], 'created_by_id':1,
                    }  
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(Program)
class ProgramAdmin(CommonAdminModel):

    exclude = ['program_code']

    inlines = [BudgetInline]

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Program.objects.update_or_create(
                    id = col[0],
                    defaults = {
                        'program_code':col[1], 'name':col[2], 'fund_source_type':col[3], 'fund_source_entity_id':col[4],
                        'pub_sector_id':col[5], 'created_by_id':1,
                    }  
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

# @admin.register(Region)
# class RegionAdmin(CommonAdminModel):
#     # resource_class = RegionResources

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [path('import_csv/', self.import_csv)]
#         return my_urls + urls

#     def import_csv(self, request):
#         if request.method == 'POST':
#             csv_file = request.FILES['csv_file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for col in csv.reader(io_string, delimiter=',', quotechar='"'):
#                 _, created = Region.objects.update_or_create(
#                     id = col[0],
#                     defaults = {
#                         'name':col[1], 'created_by_id':1,
#                     }  
#                 )
#             self.message_user(request, "Your csv file has been imported")
#             return redirect('..')
#         form = CsvUploadForm()
#         return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(Municipality)
class MunicipalityAdmin(CommonAdminModel):

    list_display = ['name', 'region', 'area', 'child_pop', 'adult_pop', 'senior_pop']

    inlines = [CommentInline]

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
            for col in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Municipality.objects.update_or_create(
                    id = col[0],
                    defaults = {
                        'name':col[1], 'region':col[2], 'area':col[3],
                        'child_pop':col[4], 'adult_pop':col[5], 'senior_pop':col[6], 'created_by_id':1
                    }
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

# @admin.register(PublicSector)
# class PublicSectorAdmin(CommonAdminModel):

#     def import_csv(self, request):
#         if request.method == 'POST':
#             csv_file = request.FILES['csv_file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for col in csv.reader(io_string, delimiter=',', quotechar='"'):
#                 _, created = PublicSector.objects.update_or_create(
#                     id = col[0],
#                     defaults = {
#                         'name':col[1], 'created_by_id':1
#                     }
#                 )
#             self.message_user(request, "Your csv file has been imported")
#             return redirect('..')
#         form = CsvUploadForm()
#         return render(request, 'admin/import_csv.html', {'form': form})
    
# @admin.register(EntitySector)
# class EntitySectorAdmin(CommonAdminModel):
#     def import_csv(self, request):
#         if request.method == 'POST':
#             csv_file = request.FILES['csv_file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for col in csv.reader(io_string, delimiter=',', quotechar='"'):
#                 _, created = EntitySector.objects.update_or_create(
#                     id = col[0],
#                     defaults = {
#                         'name':col[1], 'created_by_id':1
#                     }
#                 )
#             self.message_user(request, "Your csv file has been imported")
#             return redirect('..')
#         form = CsvUploadForm()
#         return render(request, 'admin/import_csv.html', {'form': form})



# @admin.register(EntityType)
# class EntityTypeAdmin(CommonAdminModel):

#     def import_csv(self, request):
#         if request.method == 'POST':
#             csv_file = request.FILES['csv_file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for col in csv.reader(io_string, delimiter=',', quotechar='"'):
#                 _, created = EntityType.objects.update_or_create(
#                     id = col[0],
#                     defaults = {
#                         'name':col[1], 'created_by_id':1
#                     }
#                 )
#             self.message_user(request, "Your csv file has been imported")
#             return redirect('..')
#         form = CsvUploadForm()
#         return render(request, 'admin/import_csv.html', {'form': form})

# Laikinai reikia registruoti Biudžeto ir Komentarų modelius, masiniam duomenų užkrovimui.

@admin.register(Budget)
class BudgetAdmin(CommonAdminModel):
    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Budget.objects.update_or_create(
                    id = col[0],
                    defaults = {
                        'entity_id':col[1],'program_id':col[2], 'amount':col[3], 
                        'year':col[4], 'b_source':col[5], 'b_type':col[6], 'created_by_id':1
                    }
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})

@admin.register(Comment)
class CommentAdmin(CommonAdminModel):

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Budget.objects.update_or_create(
                    id = col[0],
                    defaults = {
                        'entity_id':col[1],'municipality_id':col[2], 'year':col[3], 
                        'comments':col[4], 'created_by_id':1
                    }
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect('..')
        form = CsvUploadForm()
        return render(request, 'admin/import_csv.html', {'form': form})
