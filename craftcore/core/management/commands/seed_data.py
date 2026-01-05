import random
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.management.base import BaseCommand

from marketplace.models import Product, Category, Material, ArtisanProfile
from orders.models import Order, OrderItem

class Command(BaseCommand):
    help = "Seed dummy data for CraftCore"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        # ================================
        # SAFETY CHECK (RUN ONLY ONCE)
        # ================================
        if User.objects.filter(email="rageeni.dawale@demo.com").exists():
            self.stdout.write(self.style.WARNING("Seed already ran. Exiting."))
            return

        print("Running CraftCore seed script...")

        # ================================
        # ADMIN
        # ================================
        User.objects.create_superuser(
            username="admin@craftcore.com",
            email="admin@craftcore.com",
            password="admin1234"
        )

        # ================================
        # USERS
        # ================================
        USER_NAMES = [
            ("Rageeni", "Dawale"),
            ("Aarav", "Mehta"),
            ("Ananya", "Iyer"),
            ("Rohan", "Sharma"),
            ("Kavya", "Nair"),
            ("Aditya", "Kulkarni"),
            ("Pooja", "Patil"),
            ("Siddharth", "Verma"),
            ("Neha", "Joshi"),
            ("Rahul", "Malhotra"),
            ("Ishita", "Banerjee"),
            ("Kunal", "Gupta"),
            ("Sneha", "Deshpande"),
            ("Arjun", "Singh"),
            ("Meera", "Rao"),
        ]

        users = []

        for first, last in USER_NAMES:
            email = f"{first.lower()}.{last.lower()}@demo.com"
            user = User.objects.create_user(
                username=email,
                email=email,
                password="test1234",
                first_name=first,
                last_name=last
            )
            users.append(user)

        # ================================
        # ARTISANS
        # ================================
        ARTISAN_STORIES = [
            "I learned this craft from my mother, who worked with her hands long before it became a livelihood. Over the years, I’ve refined traditional techniques while keeping the soul of handmade work alive. Each piece reflects patience and care.",

            "What started as a small hobby slowly became my full-time pursuit. I work with locally sourced materials and believe handmade products should feel personal, not perfect. Every creation has its own character.",

            "Growing up around artisans shaped my love for craftsmanship. I focus on traditional methods passed down through generations. My work celebrates slow, intentional making.",

            "I believe sustainability and craftsmanship go hand in hand. Each product is made in small batches with close attention to detail. Handmade work allows me to stay connected to my roots.",

            "This craft has been in my family for decades. While tools have evolved, the values remain unchanged—quality, honesty, and authenticity in every piece.",
        ]

        artisan_users = random.sample(users, 8)
        inactive_artisans = random.sample(artisan_users, 3)

        artisans = []

        for user in artisan_users:
            artisan = ArtisanProfile.objects.create(
                user=user,
                display_name=f"{user.first_name} {user.last_name}",
                location=random.choice([
                    "Pune, Maharashtra",
                    "Jaipur, Rajasthan",
                    "Kochi, Kerala",
                    "Kutch, Gujarat",
                    "Mysuru, Karnataka",
                ]),
                story=random.choice(ARTISAN_STORIES),
                is_active=user not in inactive_artisans
            )
            artisans.append(artisan)

        # ================================
        # CATEGORIES & MATERIALS
        # ================================
        categories = []
        for name in ["Home Decor", "Jewelry", "Textiles", "Stationery"]:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)

        materials = []
        for name in ["Wood", "Clay", "Cotton", "Metal"]:
            material, _ = Material.objects.get_or_create(name=name)
            materials.append(material)

        # ================================
        # PRODUCTS
        # ================================
        PRODUCT_DESCRIPTIONS = [
            "This handcrafted product is created using traditional techniques and carefully selected materials. Each piece is made in small batches, ensuring attention to detail and authenticity. Slight variations are a natural part of handmade work.",

            "Designed to be both functional and beautiful, this product reflects hours of skilled craftsmanship. Made with sustainability in mind, it brings warmth and character to everyday use.",

            "Inspired by local art forms and handmade traditions, this product blends practicality with timeless design. Every item carries the story of the artisan behind it.",
        ]

        products = []

        for artisan in artisans:
            for _ in range(random.randint(3, 5)):
                stock = random.choice([0, 5, 10])
                is_active = artisan.is_active and random.choice([True, True, False])

                product = Product.objects.create(
                    artisan=artisan,
                    name=f"Handcrafted Item {random.randint(100,999)}",
                    description=random.choice(PRODUCT_DESCRIPTIONS),
                    category=random.choice(categories),
                    material=random.choice(materials),
                    price=random.randint(500, 3000),
                    stock=stock,
                    is_active=is_active
                )
                products.append(product)

        # ================================
        # ORDERS (Single Item Orders)
        # ================================
        STATUSES = ["Ordered", "Pending", "Shipped", "Delivered"]

        for _ in range(50):
            buyer = random.choice(users)
            product = random.choice(products)

            order = Order.objects.create(
                buyer=buyer,
                status=random.choice(STATUSES),
                created_at=timezone.now()
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price_at_purchase=product.price
            )

        print("Seed completed successfully.")
