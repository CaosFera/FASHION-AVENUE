# Generated by Django 5.1.1 on 2024-10-03 14:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Categoria')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Preço')),
                ('image', models.ImageField(blank=True, default='image_default.png', upload_to='imagens/', verbose_name='Imagem')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Estoque')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='products.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
            },
        ),
    ]
