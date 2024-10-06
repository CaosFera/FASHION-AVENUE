from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save


class Base(models.Model):
    active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado", auto_now_add=True)
    updated_at = models.DateTimeField("Modificado", auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Base Models'
        ordering = ['-created_at']


class Category(Base):
    name = models.CharField("Categoria", max_length=100, unique=True, blank=False, null=False)
    description = models.TextField("Descrição", blank=True, null=True)
    slug = models.SlugField("Slug", max_length=100, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

def categories_pre_save(sender, instance, **kwargs):    
    instance.slug = slugify(instance.name)

pre_save.connect(categories_pre_save, sender=Category)





class Products(Base):
    SIZE_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
        ('Extra-Grande', 'Extra-Grande'),
    ]

    COLOR_CHOICES = [
        ('Vermelho', 'Vermelho'),
        ('Verde', 'Verde'),
        ('Azul', 'Azul'),
        ('Branco', 'Branco'),
        ('Preto', 'Preto'),
        ('Rosa', 'Rosa'),
        ('Laranja', 'Laranja'),
        ('Marron', 'Marron'),
    ]
    name = models.CharField("Nome", max_length=100, blank=False, null=False)
    price = models.DecimalField("Preço", max_digits=6, decimal_places=2, blank=False, 
    null=False, default=0, validators=[MinValueValidator(0)])
    image = models.ImageField("Imagem", upload_to="imagens/", default="image_default.png", blank=True)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    description = models.TextField("Descrição", blank=True, null=True)
    stock = models.PositiveIntegerField("Estoque", blank=False, null=False, default=0)
    size = models.CharField("Tamanho", max_length=15, choices=SIZE_CHOICES, blank=False, default="")
    color = models.CharField("Cor", max_length=10, choices=COLOR_CHOICES, blank=False, default="")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="categories")

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name

def products_pre_save(sender, instance, **kwargs):    
    instance.slug = slugify(instance.name)

pre_save.connect(products_pre_save, sender=Products)


