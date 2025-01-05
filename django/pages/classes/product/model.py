import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    PRODUCT_REOCCURRENCE_CHOICES = [
        ('one-time', 'One Time'),
        ('reoccurring', 'Re-Occurring'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES, default='product')
    reoccurrence = models.CharField(max_length=255, choices=PRODUCT_REOCCURRENCE_CHOICES, default='one-time')
    description = models.TextField(blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_or_get_stripe_product(self):
        """Get an existing Stripe product or create a new one."""
        try:
            if self.stripe_product_id:
                stripe_product = stripe.Product.retrieve(self.stripe_product_id)
                print(f"Found existing Stripe product with ID: {self.stripe_product_id}")
                return stripe_product
            else:
                stripe_product = stripe.Product.create(
                    name=self.name,
                    description=self.description or None,
                )
                self.stripe_product_id = stripe_product["id"]
                self.save()
                print(f"Created new Stripe product with ID: {stripe_product['id']}")
                return stripe_product
        except Exception as e:
            print(f"Error in create_or_get_stripe_product: {e}")
            raise

    def update_stripe_images(self):
        """Update Stripe product with associated image URLs."""
        if not self.stripe_product_id:
            raise ValueError("Cannot update images for a product without a Stripe product ID.")

        # Collect Stripe file URLs from related images
        image_urls = [
            image.stripe_file_url for image in self.images.all() if image.stripe_file_url
        ]

        try:
            stripe.Product.modify(
                self.stripe_product_id,
                images=image_urls,
            )
            print(f"Updated Stripe product images for {self.stripe_product_id}")
        except Exception as e:
            print(f"Error updating Stripe product images: {e}")
            raise

    def save(self, *args, **kwargs):
        # Automatically update product images in Stripe after saving the product
        super().save(*args, **kwargs)
        # self.update_stripe_images()

    def __str__(self):
        return str(self.id)


# class Product(models.Model):
#     PRODUCT_TYPE_CHOICES = [
#         ('product', 'Product'),
#         ('service', 'Service'),
#     ]
#     PRODUCT_REOCCURRENCE_CHOICES = [
#         ('one-time', 'One Time'),
#         ('reoccurring', 'Re-Occurring'),
#     ]
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES, default='product')
#     reoccurrence = models.CharField(max_length=255, choices=PRODUCT_REOCCURRENCE_CHOICES, default='one-time')
#     description = models.TextField(blank=True, null=True)
#     # images = models.JSONField(blank=True, default=list)
#     stripe_product_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
#     created = models.DateTimeField(default=now)
#     updated = models.DateTimeField(auto_now=True)
#     deleted = models.DateTimeField(null=True, blank=True)

#     def create_or_get_stripe_product(self):
#         """Get an existing Stripe product or create a new one."""
#         try:
#             if self.stripe_product_id:
#                 # Check if the product already exists in Stripe
#                 stripe_product = stripe.Product.retrieve(self.stripe_product_id)
#                 print(f"Found existing Stripe product with ID: {self.stripe_product_id}")
#                 return stripe_product
#             else:
#                 # Create a new Stripe product
#                 stripe_product = stripe.Product.create(
#                     name=self.name,
#                     description=self.description or "",  # Use an empty string if description is None
#                 )
#                 self.stripe_product_id = stripe_product["id"]
#                 self.save()
#                 print(f"Created new Stripe product with ID: {stripe_product['id']}")
#                 return stripe_product
#         except Exception as e:
#             print(f"Error in create_or_get_stripe_product: {e}")
#             raise

#     def update_stripe_product(self):
#         """Update the Stripe product with the latest details from the model."""
#         if not self.stripe_product_id:
#             raise ValueError("Stripe product ID does not exist. Cannot update non-existent Stripe product.")
        
#         try:
#             stripe.Product.modify(
#                 self.stripe_product_id,
#                 name=self.name,
#                 description=self.description or "",
#             )
#             print(f"Updated Stripe product with ID: {self.stripe_product_id}")
#         except Exception as e:
#             print(f"Error updating Stripe product: {e}")
#             raise

#     def delete_stripe_product(self):
#         """
#         Delete the Stripe product associated with this model.
#         """
#         if self.stripe_product_id:
#             try:
#                 stripe.Product.delete(self.stripe_product_id)
#                 print(f"Deleted Stripe product: {self.stripe_product_id}")
#                 self.stripe_product_id = None
#                 self.save()
#             except Exception as e:
#                 print(f"Error deleting Stripe product: {e}")
#                 raise

#     def update_stripe_images(self):
#         """Update Stripe product with associated image URLs."""
#         if not self.stripe_product_id:
#             raise ValueError("Cannot update images for a product without a Stripe product ID.")

#         # Collect Stripe file URLs from related images
#         image_urls = [
#             image.stripe_file_url for image in self.images.all() if image.stripe_file_url
#         ]

#         try:
#             stripe.Product.modify(
#                 self.stripe_product_id,
#                 images=image_urls,
#             )
#             print(f"Updated Stripe product images for {self.stripe_product_id}")
#         except Exception as e:
#             print(f"Error updating Stripe product images: {e}")
#             raise

#     def save(self, *args, **kwargs):
#         if not self.stripe_product_id:
#             self.create_or_get_stripe_product()
#         else:
#             self.update_stripe_product()  # Update the Stripe product details
#         super().save(*args, **kwargs)
#         self.update_stripe_images()

#     def delete(self, *args, **kwargs):
#         """
#         Override the delete method to delete the Stripe product first.
#         """
#         if self.stripe_product_id:
#             self.delete_stripe_product()
#         super().delete(*args, **kwargs)

#     def __str__(self):
#         return str(self.id)

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/', blank=True, null=True)
#     image_url = models.URLField(blank=True, null=True)  # For external image URLs
#     stripe_file_url = models.CharField(max_length=255, blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def upload_to_stripe(self):
#         """Upload the image file to Stripe."""
#         if self.image:
#             try:
#                 with self.image.open('rb') as img_file:
#                     stripe_file = stripe.File.create(
#                         purpose="dispute_evidence",
#                         file=img_file
#                     )
#                     self.stripe_file_url = stripe_file["url"]
#                     self.save()
#                     print(f"Uploaded file to Stripe: {stripe_file['id']}")
#                     return stripe_file
#             except Exception as e:
#                 print(f"Error uploading file to Stripe: {e}")
#                 raise
#         elif self.image_url:
#             print("Skipping Stripe upload for external URL images.")
#         else:
#             raise ValueError("No image or URL provided for upload.")

#     def __str__(self):
#         return f"Image for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # For external image URLs
    stripe_file_url = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def upload_to_stripe(self):
        """Upload the image file to Stripe."""
        if self.image:
            try:
                with self.image.open('rb') as img_file:
                    stripe_file = stripe.File.create(
                        purpose="product_image",  # Correct Stripe purpose
                        file=img_file
                    )
                    self.stripe_file_url = stripe_file["url"]
                    self.save()
                    print(f"Uploaded file to Stripe: {stripe_file['id']}")
                    return stripe_file["id"]  # Return the file ID
            except Exception as e:
                print(f"Error uploading file to Stripe: {e}")
                raise
        elif self.image_url:
            print("Skipping Stripe upload for external URL images.")
            return None
        else:
            raise ValueError("No image or URL provided for upload.")

    def save(self, *args, **kwargs):
        # Automatically upload to Stripe on save
        if not self.stripe_file_url and self.image:
            self.upload_to_stripe()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"

