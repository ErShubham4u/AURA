from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
        ("unisex", "Unisex"),
        ("gift", "Gift Set"),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    size = models.CharField(
        max_length=50,
        default="50ml"
    )

    fragrance_notes = models.TextField(
        blank=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.name

class Order(models.Model):

    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
    ]

    name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="cod"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        default="Pending"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.name}"