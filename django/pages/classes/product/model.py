import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('good', 'Good'),
        ('service', 'Service'),
    ]
    PRODUCT_REOCCURRENCE_CHOICES = [
        ('one-time', 'One Time'),
        ('reoccurring', 'Re-Occurring'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES, default='good')
    reoccurrence = models.CharField(max_length=255, choices=PRODUCT_REOCCURRENCE_CHOICES, default='one-time')
    description = models.TextField(blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    stock = models.IntegerField(default=1)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_stripe_product(self):
        """Creates a Stripe product and stores the product ID."""
        try:
            # Create a new Stripe product
            product = stripe.Product.create(
                name=self.name,
                type=self.type,
                description=self.description or None,
            )
            # Store the Stripe product ID in the product
            self.stripe_product_id = product.id
            self.save()
            return product
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to create Stripe product: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to create Stripe product: {e}")

    def update_stripe_product(self, **kwargs):
        """Updates the Stripe product with the provided details."""
        if not self.stripe_product_id:
            raise Exception("Stripe product ID not set for this product.")

        try:
            # Update the Stripe product
            product = stripe.Product.modify(
                self.stripe_product_id,
                **kwargs
            )
            # Optionally update local fields if needed
            if 'name' in kwargs:
                self.name = kwargs['name']
            if 'description' in kwargs:
                self.description = kwargs['description']
            self.save()
            return product
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to update Stripe product: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to update Stripe product: {e}")
    
    def delete_stripe_product(self):
        """Deletes the Stripe product associated with this product."""
        if not self.stripe_product_id:
            raise Exception("Stripe product ID not set for this product.")

        try:
            # Delete the Stripe product
            stripe.Product.delete(self.stripe_product_id)

            # Optionally, clear the stripe_product_id field
            self.stripe_product_id = None
            self.save()
            print("Stripe product deleted successfully.")
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to delete Stripe product: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to delete Stripe product: {e}")
        
    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_product"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # For external image URLs
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_product_image(product, image=None, image_url=None):
        """Creates a new ProductImage."""
        product_image = ProductImage.objects.create(
            product=product,
            image=image,
            image_url=image_url
        )
        return product_image
    
    def update_product_image(product_image, image=None, image_url=None):
        """Updates an existing ProductImage."""
        if image is not None:
            product_image.image = image
        if image_url is not None:
            product_image.image_url = image_url
        product_image.save()
        return product_image

    def delete_product_image(product_image):
        """Deletes a ProductImage."""
        # product_image.deleted = now()
        # product_image.save()
        # Alternatively, to permanently delete:
        product_image.delete()


    def __str__(self):
        return str(self.id)
    
    # Meta Class
    class Meta:
        db_table = "pages_product_image"


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='product/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)  # For external image URLs
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_product_video(product, video=None, video_url=None):
        """Creates a new ProductVideo."""
        product_video = ProductVideo.objects.create(
            product=product,
            video=video,
            video_url=video_url
        )
        return product_video

    def update_product_video(product_video, video=None, video_url=None):
        """Updates an existing ProductVideo."""
        if video is not None:
            product_video.video = video
        if video_url is not None:
            product_video.video_url = video_url
        product_video.save()
        return product_video

    def delete_product_video(product_video):
        """Deletes a ProductVideo."""
        # product_video.deleted = now()
        # product_video.save()
        # Alternatively, to permanently delete:
        product_video.delete()


    def __str__(self):
        return str(self.id)
    
    # Meta Class
    class Meta:
        db_table = "pages_product_video"
