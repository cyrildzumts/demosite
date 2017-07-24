from django.db import models
# from django.core.urlresolvers import reverse
from catalog import choices
# from django.conf import settings
from django.template.defaultfilters import slugify

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
    # view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    @property
    def categories(self):
        """
        Return a list of Categories path from the Root
        Category to the current Category(self).
        """
        cat_list = []
        current_cat = self
        while current_cat is not None:
            cat_list.append(current_cat)
            current_cat = current_cat.parent
        cat_list.reverse()
        return cat_list

    def root_cat(self):
        """
        When the current Category is a root Category,
        that is, self.parent is None , self is returned
        instead of None.
        """
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def is_root(self):
        """
        Return True if this is a root
        Category.
        """
        return self.parent is None

    def is_parent(self):
        """
        Return True if this Category is a parent
        Category.
        """
        return Category.objects.filter(parent=self).exists()

    def __str__(self):
        return self.name

    def is_root_child(self, product):
        """
        Return true if product belongs to the current
        Category or to a child of the current
        Category.
        """
        flag = False
        current_cat = product.categories.get()
        if current_cat == self:
            flag = True
        else:
            while current_cat.parent is not None:
                current_cat = current_cat.parent
                if current_cat == self:
                    flag = True
        return flag

    def get_products(self):
        """
        Return every products which belong
        to this Category tree.
        """
        products = Product.objects.all().order_by('-created_at')
        items = [p for p in products if self.is_root_child(p)]
        return items

    def get_direct_products(self):
        """
        Return only products belonging
        to this Category
        """
        return self.product_set.all()

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:catalog_category', (), {'category_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


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
    image = models.ImageField(upload_to="products")
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

    def build_slug(self):
        self.slug = self.name + "-" + self.id

    def build_sku(self):
        self.sku = self.brand + "-" + self.name

    @property
    def cats_path(self):
        return self.categories.get().categories

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:product_details', (), {'product_slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def product_is_available(self):
        return self.quantity != 0


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # abstract = True
        db_table = 'ProductType'
        ordering = ['-created_at']

    def __str__(self):
        return self.type_name


class ModelNumber(models.Model):
    id = models.AutoField(primary_key=True)
    model_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ModelNumber'
        ordering = ['-created_at']


class Product(models.Model):
    TEMPLATE_NAME_CHOICES = (
        ('tags/product_phablet_options.html', 'Phablet'),
        ('tags/product_parfum_options.html', 'Parfum'),
        ('tags/product_chaussure_options.html', 'Chaussure'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='Texte unique representant la page du produit.',
        blank=True,
        null=False)
    size = models.CharField(max_length=5,
                            choices=choices.GENERIC_SIZE_CHOICES,
                            blank=True,
                            null=True)
    material = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=6,
                              choices=choices.GENDER_CHOICES,
                              blank=True,
                              null=True)
    categories = models.ManyToManyField(Category)
    price = models.IntegerField()
    old_price = models.IntegerField(default=0)
    sku = models.CharField(max_length=50,
                           blank=True,
                           null=False)
    model_number = models.ForeignKey(ModelNumber,
                                     related_name='product_model',
                                     unique=False,
                                     blank=True,
                                     null=True)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    short_description = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    sell_quantity = models.IntegerField(default=0)
    sell_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to="products")
    image2 = models.ImageField(upload_to="products", blank=True, null=True)
    image3 = models.ImageField(upload_to="products", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)
    product_type = models.ForeignKey(ProductType,
                                     related_name='product_type',
                                     on_delete=models.CASCADE,
                                     unique=False)
    view_count = models.IntegerField(default=0)
    coupon = models.PositiveIntegerField(blank=True, null=True)
    template_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=TEMPLATE_NAME_CHOICES)

    class Meta:
        # abstract = True
        db_table = 'Product'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def build_slug(self):
        tmp = self.brand + "-" + self.name
        if self.slug != tmp:
            self.slug = tmp

    def build_sku(self):
        tmp = self.brand + "-" + self.name
        if self.sku != tmp:
            self.sku = self.brand + "-" + self.name

    @property
    def cats_path(self):
        return self.categories.get().categories

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:product_details', (), {'slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def product_is_available(self):
        return self.quantity != 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.build_sku()
        super(Product, self).save(*args, **kwargs)


class RelatedModel(models.Model):
    related_model = models.OneToOneField(
        BaseProduct,
        null=True,
        blank=True,
        related_name='product_details'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.related_model.name


class Phablet(Product):

    screen = models.FloatField(choices=choices.SCREEN_SIZE_CHOICES,
                               default=5)
    rear_camera = models.IntegerField(
        choices=choices.CAMERA_RESOLUTION_CHOICES,
        default=13,
        blank=True,
        null=True)
    front_camera = models.IntegerField(
        choices=choices.CAMERA_RESOLUTION_CHOICES,
        default=5,
        blank=True,
        null=True)
    system = models.CharField(max_length=512)
    memory = models.IntegerField(choices=choices.MEMORY_SIZE_CHOICES,
                                 default=16
                                 )
    ram_memory = models.IntegerField(default=1,
                                     choices=choices.RAM_SIZE_CHOICES)

    extern_sdcard = models.BooleanField(default=False)
    sim_card = models.CharField(
        choices=choices.SIM_CARD_CONF_CHOICES,
        default="STANDARD",
        max_length=15
        )
    battery = models.CharField(max_length=128)

    class Meta:
        db_table = 'phones'


class Parfum(Product):

    capacity = models.IntegerField(choices=choices.PARFUMS_QUANTITY_CHOICES,
                                   default=100)
    typ = models.CharField(max_length=10,
                           choices=choices.PARFUM_TYP_CHOICES,
                           default='EDP')

    class Meta:
        db_table = 'parfums'

    def build_sku(self):
        self.sku = self.brand + "-" + self.name + "-" + str(self.capacity)


class Color(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=7, help_text="Valeur de la couleur\
     en hexadecimal")

    class Meta:
        db_table = 'colors'
        ordering = ['name']

    def __str__(self):
        return self.name
