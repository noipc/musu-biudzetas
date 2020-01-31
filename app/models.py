import uuid
from os.path import join
from typing import Optional
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


#Common fields that are shared among all models.
class CommonModel(models.Model):    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, editable=False, related_name="+")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, editable=False, null=True, blank=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["slug"]


class EntityType(CommonModel):
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Juridinio asmens tipas"))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Juridinio asmens tipai")
        verbose_name =_("Juridinio asmens tipas")


class EntitySector(CommonModel):
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Juridinio asmens sektorius"))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Juridinio asmens sektoriai")
        verbose_name =_("Juridinio asmens sektorius")


class PublicSector(CommonModel):
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Viešosios politikos sritis"))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Viešosios politikos sritys")
        verbose_name =_("Viešosios politikos sritis")

class Region(CommonModel):
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Apskritis"))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save( *args, **kwargs)
    
    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Apskritys")
        verbose_name =_("Apskritis")

class Municipality(CommonModel):
    REGION = ( 
        (1,	"Alytaus apskritis"),
        (2,	"Kauno apskritis"),
        (3,	"Klaipėdos apskritis"),
        (4,	"Marijampolės apskritis"),
        (5,	"Panevėžio apskritis"),
        (6,	"Šiaulių apskritis"),
        (7,	"Tauragės apskritis"),
        (8,	"Telšių apskritis"),
        (9,	"Utenos apskritis"),
        (10, "Vilniaus apskritis")
    )
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Savivaldybė"))
    slug = models.SlugField(unique=True)
    short_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Savivaldybės sutrumpintas pavadinimas"))
    region = models.IntegerField(choices=REGION, verbose_name=_("Apskritis"))
    child_pop = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Gyentojų skaičius nuo 0 iki 15 metų"))
    adult_pop = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Gyventojų skaičius nuo 15 iki 65 metų"))
    senior_pop = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Gyventojų skaičius nuo 65 metų"))
    area = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Savivaldybės plotas, kv. km"))

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save( *args, **kwargs)
    
    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Savivaldybės")
        verbose_name =_("Savivaldybė")

class Program(CommonModel):
    FUND_TYPE = (
        (1, "Valstybės finansavimas"),
        (2, "Savivaldybės finansavimas")
    )
    program_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=300, verbose_name=_("Programos pavadinimas"))
    slug = models.SlugField(unique=True, max_length=350)
    pub_sector = models.ForeignKey(PublicSector, on_delete=models.CASCADE, verbose_name=_("Viešosiso politikos sritis"))
    fund_source_type = models.IntegerField(choices=FUND_TYPE, verbose_name=_("Lėšų šaltinio tipas"))
    fund_source_entity = models.ForeignKey('Entity', to_field='branch_id', on_delete=models.CASCADE, limit_choices_to={'is_funder': True}, verbose_name=_("Finansuotojas"))

    def __str__(self):
        return self.name

    def create_program_code(self, entity_id):
        program = Program.objects.get(fund_source_entity = entity_id)
        if not program.program_code:
            new_id =  entity_id + '-1'
        else:       
            last_id = int(program.program_code.split('-', 1)[1])
            last_id += 1
            new_id = program.program_code.split('-', 1)[0] + '-' + str(last_id)
        return new_id
    
    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.program_code:
            self.program_code = self.create_program_code(self.fund_source_entity)
        super().save( *args, **kwargs)

    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Programos")
        verbose_name =_("Programa")
        
class Entity(CommonModel):
    ENTITY_STATUS = (
        (1, "Aktyvus"),
        (2, "Neaktyvus"),
        (3, "Likviduojamas"),
        (4, "Likviduotas")
    )
    ENTITY_TYPE = (
        (1,	"Asociacija"),
        (2,	"Bendrija"),
        (3,	"Biudžetinė įstaiga"),
        (4,	"Labdaros ir paramos fondas"),
        (5,	"Politinė partija"),
        (6,	"Prekybos, pramonės ir amatų rūmai"),
        (7,	"Profesinė sąjunga ar susivienijimas"),
        (8,	"Religinė bendruomenė ar bendrija"),
        (9, "Sodininkų bendrija"),
        (10, "Šeimyna"),
        (11, "Tradicinė religinė bendruomenė ar bendrija"),
        (12, "Viešoji įstaiga"),
        (13, "UAB"),
        (14, "AB"),
        (15, "Individuali Veikla"),
        (16, "Mažoji Bendrija"),
        (17, "Asociacijos filialas"),
        (18, "Individuali Įmonė"),
        (19, "Draugija"),
        (20, "Kita")
    )
    ENTITY_SECTORS = ( 
        (1,	"Viešasis sektorius"),
        (2,	"Privatus sektorius"),
        (3,	"Nevyriausybinis sektorius"),
        (4,	"Kitos, nepelno organizacijos")
    )
    PUB_SECTORS = (
        (1,	"Sportas"),
        (2,	"Kultūra"),
        (3,	"Socialinė apsauga"),
        (4,	"Sveikatos apsauga"),
        (5,	"Švietimas"),
        (6,	"NVO"),
        (7,	"Aplinkos apsauga"),
        (8,	"Žmogaus teisės, demokratija")
    )
    PUB_SUB_SECTORS = (
        (1, "Vaikai"),
        (2, "Jaunimas"),
        (3, "Senjorai")
    )
    name = models.CharField(max_length=300, verbose_name=_("Juridinio asmens pavadinimas"))
    slug = models.SlugField(unique=True, max_length=300)
    legal_id = models.CharField(max_length=50, null=False, verbose_name=_("Įmonės kodas"))
    branch_id = models.CharField(max_length=50, unique=True, null=False)
    entity_type = models.IntegerField(choices=ENTITY_TYPE, null=True, blank=True, verbose_name=_("Juridinio asmens tipas"))
    entity_cat = models.IntegerField(choices=ENTITY_SECTORS, null=True, blank=True, verbose_name=_("Juridinio asmens sektorius"))
    pub_sector = models.IntegerField(choices=PUB_SECTORS, null=True, blank=True, verbose_name=_("Viešosios politikos sritis"))
    pub_subsector = models.IntegerField(choices=PUB_SUB_SECTORS, null=True, blank=True, verbose_name=_("Viešosios politikos srities kategorija"), help_text=_("Vaikai, Jaunimas, Senjorai"))
    municipality = models.ForeignKey(Municipality, related_name='entities', on_delete=models.CASCADE, verbose_name=_("Savivaldybė"))
    status = models.IntegerField(choices=ENTITY_STATUS, default=1, verbose_name=_("Juridinio asmens statusas"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Juridinio asmens įkūrimo data"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Juridinio asmens likvidavimo data"))
    is_funder = models.BooleanField(null=True, verbose_name=_("Finansuotojas"))
    is_municipality = models.BooleanField(null=True, blank=True, default=0, verbose_name=_("Ar savivaldybės administracija?"))
    is_ministry = models.BooleanField(null=True, blank=True, default=0, verbose_name=_("Ar ministerija?"))
    is_accountable = models.BooleanField(null=True, verbose_name=_("Ar teikia ataskaitas?"))
    accounts_url = models.URLField(max_length=300, null=True, blank=True, verbose_name=_("Finansinių ataskaitų šaltinis Registrų centre"))
    no_users = models.IntegerField(null=True, blank=True, verbose_name=_("Vartotojų skaičius"), help_text=_("Žmonių skaičius, kurie nuolatos naudojasi įstaigos paslaugomis"))
    no_employees = models.IntegerField(null=True, blank=True, verbose_name=_("Datbuotojų skaičius"))
    beneficial_owner = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="entity", verbose_name=_("Naudos gavėjas"), help_text=_("Juridinis asmuo, kuris valdo įmonę"))
    

    def __str__(self):
        return self.name

    def create_branch_id(self):
        branch_id = self.legal_id + "-" + str(self.municipality)
        return branch_id

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.branch_id:
            branch_id = self.create_branch_id(self)
        super().save( *args, **kwargs)
    
    class Meta(CommonModel.Meta):
        verbose_name_plural =_("Juridiniai asmenys")
        verbose_name =_("Juridinis asmuo")

class Budget(CommonModel):
    BUDGET_SOURCE = (
        (1, "Savivaldybės finansavimas"),
        (2, "Valstybės finansavimas"),
        (3, "2 proc. GPM"),
        (4, "Gyventojų parama"),
        (5, "Kitos pajamos"),
        (6, "Bendras biudžetas")
    )
    BUDGET_TYPE = (
        (1, "Juridinio asmens biudžetas"),
        (2, "Programos biudžetas")
    )
    b_source = models.IntegerField(choices=BUDGET_SOURCE, default= 0, verbose_name=_("Finansavimo šaltinis"))
    b_type = models.IntegerField(choices=BUDGET_TYPE, default = 0, verbose_name=_("Biudžeto tipas"))
    entity = models.ForeignKey(Entity, related_name='budgets', on_delete=models.CASCADE, null=True, blank=True, to_field='branch_id', verbose_name=_("Juridinis asmuo"))
    program = models.ForeignKey(Program, related_name='budgets', on_delete=models.CASCADE, null=True, blank=True, to_field='program_code', verbose_name=_("Programa"))
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Suma, EUR"))
    year = models.IntegerField(default=2015, verbose_name=_("Metai"))


    def __str__(self):
        if self.b_type == 1:
            return str(self.year) + " " + self.entity.name
        else:
            return str(self.year) + " " + self.program.name


    class Meta:
        verbose_name_plural =_("Biudžetai")
        verbose_name =_("Biudžetas")
        ordering = ["year", "amount"]

class Comment(CommonModel):
    entity = models.ForeignKey(Entity, related_name="comments", null=True, blank=True, on_delete=models.CASCADE, to_field="branch_id")
    municipality = models.ForeignKey(Municipality, related_name="comments", null=True, blank=True, on_delete=models.CASCADE)
    year = models.IntegerField(default=2015, verbose_name=_("Metai"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Pastabos"))

    def __str__(self):
        return str(self.year) + " " + self.comment

    class Meta:
        verbose_name_plural = _("Pastabos")
        verbose_name = _("Pastaba")
        ordering = ["year"]

#custom User model
class User(AbstractUser):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, verbose_name=_("Darbovietė"))

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural=_("Registruoti vartotojai")
        verbose_name=_("Registruotas vartotojas")