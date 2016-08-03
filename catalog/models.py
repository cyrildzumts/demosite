from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=255, unique=True, help_text='Texte unique\
                            representant la page du produit.')
    # parent_category = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                               null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:catalog_category', (), {'category_slug': self.slug})


class BaseProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    slug = models.SlugField(max_length=255, unique=True, help_text='Texte unique\
                            representant la page du produit.')
    price = models.IntegerField()
    old_price = models.IntegerField(default=0)
    sku = models.CharField(max_length=50)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    sell_quantity = models.IntegerField(default=0)
    sell_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField()
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)

    class Meta:
        # abstract = True
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:product_details', (), {'product_slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None


class Phone(BaseProduct):
    screen = models.CharField(max_length=512)
    camera = models.CharField(max_length=512)
    system = models.CharField(max_length=512)
    memory = models.CharField(max_length=512)
    sim_card = models.CharField(max_length=512)
    battery = models.CharField(max_length=128)
    frequency_band = models.CharField(max_length=512)
    color = models.ForeignKey('catalog.Color', unique=False)

    class Meta:
        db_table = 'phones'
        ordering = ['-created_at']


class Shoe(BaseProduct):
    material = models.CharField(max_length=30)
    typ = models.CharField(max_length=30)
    size = models.ForeignKey('catalog.Size', unique=False)
    color = models.ForeignKey('catalog.Color', unique=False)

    class Meta:
        db_table = 'shoes'
        ordering = ['-created_at']


class Parfum(BaseProduct):
    capacity = models.IntegerField()
    typ = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)

    class Meta:
        db_table = 'parfums'
        ordering = ['-created_at']


class Bag(BaseProduct):
    material = models.CharField(max_length=30)
    size = models.ForeignKey('catalog.Size', unique=False)
    color = models.ForeignKey('catalog.Color', unique=False)

    class Meta:
        db_table = 'bags'
        ordering = ['-created_at']


class Size(models.Model):
    value = models.CharField(blank=True, max_length=3)

    class Meta:
        db_table = 'sizes'
        ordering = ['value']

    def __str__(self):
        return self.value


class Color(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=7, help_text="Valeur de la couleur\
     en hexadecimal")

    class Meta:
        db_table = 'colors'
        ordering = ['name']

    def __str__(self):
        return "name : %s -- value : %s " % (self.name, self.value)
