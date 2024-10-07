from django.core.management.base import BaseCommand
from products.models import Category, Products  

class Command(BaseCommand):
    help = "Cria registros de exemplo no banco de dados para Categorias e Produtos de Roupas"

    def handle(self, *args, **options):
        
        categories = [
            {"name": "Camisetas", "description": "Camisetas de vários estilos."},
            {"name": "Calças", "description": "Calças jeans, sociais e outras."},
            {"name": "Vestidos", "description": "Vestidos para diversas ocasiões."},
            {"name": "Acessórios", "description": "Acessórios como bolsas e cintos."}
        ]
        
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{category.name}" criada.'))
            else:
                self.stdout.write(self.style.WARNING(f'Categoria "{category.name}" já existe.'))

        
        products = [
            {
                "name": "Camiseta Estampada",
                "price": 49.99,
                "image": "imagens/camiseta_estampada.png", 
                "description": "Camiseta confortável com estampas modernas.",
                "stock": 100,
                "size": "Médio",
                "color": "Vermelho",
                "category": "Camisetas"
            },
            {
                "name": "Calça Jeans",
                "price": 89.99,
                "image": "imagens/calca_jeans.png",  
                "description": "Calça jeans confortável e estilosa.",
                "stock": 75,
                "size": "Médio",
                "color": "Azul",
                "category": "Calças"
            },
            {
                "name": "Vestido Floral",
                "price": 129.99,
                "image": "imagens/vestido_floral.png", 
                "description": "Vestido leve e elegante para o verão.",
                "stock": 40,
                "size": "Grande",
                "color": "Branco",
                "category": "Vestidos"
            },
            {
                "name": "Cinto de Couro",
                "price": 39.99,
                "image": "imagens/cinto_couro.png",  
                "description": "Cinto de couro genuíno.",
                "stock": 150,
                "size": "Médio",
                "color": "Preto",
                "category": "Acessórios"
            },
        ]

        for product_data in products:
            category = Category.objects.get(name=product_data['category'])
            product, created = Products.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': product_data['price'],
                    'image': product_data['image'],
                    'description': product_data['description'],
                    'stock': product_data['stock'],
                    'size': product_data['size'],
                    'color': product_data['color'],
                    'category': category,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Produto "{product.name}" criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Produto "{product.name}" já existe.'))
