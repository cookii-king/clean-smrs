from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=50)
    subscription_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.name} ({self.status})"

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.order_id}"

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Subscription for {self.user.name} ({self.subscription_type})"

class DataPoint(models.Model):
    data_point_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    coordinates = models.CharField(max_length=255)
    temperature_water = models.FloatField()
    temperature_air = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    precipitation = models.FloatField()
    haze = models.FloatField()
    becquerel = models.FloatField()

    def __str__(self):
        return f"DataPoint at {self.timestamp}"
