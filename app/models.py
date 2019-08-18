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
    name = models.CharField(max_length=300, unique=True, verbose_name=_("Savivaldybė"))
    slug = models.SlugField(unique=True)
    short_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Savivaldybės sutrumpintas pavadinimas"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_("Apskritis"))
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

class Currency(CommonModel):
    name = models.CharField(max_length=3, verbose_name=_("Valiutos trumpinys"))
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural =_("Valiutos")
        verbose_name = _("Valiuta")
        ordering = ["name"]

class Program(CommonModel):
    FUND_TYPE = (
        (1, "Valstybės finansavimas"),
        (2, "Savivaldybės finansavimas")
    )
    name = models.CharField(max_length=300, verbose_name=_("Programos pavadinimas"))
    slug = models.SlugField(unique=True, max_length=350)
    pub_sector = models.ForeignKey(PublicSector, on_delete=models.CASCADE, verbose_name=_("Viešosiso politikos sritis"))
    fund_source_type = models.IntegerField(choices=FUND_TYPE, verbose_name=_("Lėšų šaltinio tipas"))
    fund_source_entity = models.ForeignKey('Entity', on_delete=models.CASCADE, limit_choices_to={'is_funder': True}, verbose_name=_("Finansuotojas"))

    def __str__(self):
        return self.name
    
    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
    name = models.CharField(max_length=300, verbose_name=_("Juridinio asmens pavadinimas"))
    slug = models.SlugField(unique=True)
    legal_id = models.CharField(max_length=50, unique=True, null=False, verbose_name=_("Įmonės kodas"))
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE, verbose_name=_("Juridinio asmens tipas"))
    entity_cat = models.ForeignKey(EntitySector, on_delete=models.CASCADE, verbose_name=_("Juridinio asmens sektorius"))
    pub_sector = models.ForeignKey(PublicSector, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Viešosios politikos sritis"))
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name=_("Savivaldybė"))
    status = models.IntegerField(choices=ENTITY_STATUS, default=1, verbose_name=_("Juridinio asmens statusas"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Juridinio asmens įkūrimo data"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Juridinio asmens likvidavimo data"))
    is_funder = models.BooleanField(null=True, verbose_name=_("Finansuotojas"))
    is_accountable = models.BooleanField(null=True, verbose_name=_("Ar teikia ataskaitas?"))
    accounts_url = models.URLField(max_length=300, null=True, blank=True, verbose_name=_("Finansinių ataskaitų šaltinis Registrų centre"))
    program_participant = models.ManyToManyField(Program, blank=True, verbose_name=_("Programa"), help_text=_("Programa, iš kurios yra gaunamas finansavimas"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Pastabos"))

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
    b_source = models.IntegerField(choices=BUDGET_SOURCE, default=1, verbose_name=_("Finansavimo šaltinis"))
    b_type = models.IntegerField(choices=BUDGET_TYPE, default = 1, verbose_name=_("Biudžeto tipas"))
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True, to_field='legal_id', verbose_name=_("Juridinis asmuo"))
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Programa"))
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Suma"))
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name=_("Valiuta"))
    year = models.IntegerField(default=2015, verbose_name=_("Metai"))

    def clean(self):
        if self.b_type == 1 and self.entity is None:
            raise ValidationError(_("Jeigu pasirinkote juridinio asmens biudžeto tipą, tai turi būti pasirinktas juridinis asmuo"))

        if self.b_type == 2 and self.program is None:
            raise ValidationError(_("Jeigu pasirinkote programos biudžeto tipą, tai turi būti pasirinkta programa"))

    def __str__(self):
        if self.b_type == 1:
            return str(self.year) + " " + self.entity.name
        else:
            return str(self.year) + " " + self.program.name

    class Meta:
        verbose_name_plural =_("Biudžetai")
        verbose_name =_("Biudžetas")
        ordering = ["year", "amount"]

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