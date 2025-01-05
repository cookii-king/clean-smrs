# from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
# from django.dispatch import receiver
# from ...models import Product, ProductImage
# from ...config.config import *
# import urllib.parse
# import mimetypes


# def get_or_create_stripe_product(product):
#     """
#     Check if a Stripe product with the given name exists.
#     If it exists, return the existing product. Otherwise, create a new one.
#     """
#     try:
#         if product.stripe_product_id:
#             # Retrieve existing Stripe product
#             stripe_product = stripe.Product.retrieve(product.stripe_product_id)
#             print(f"Found existing Stripe product: {stripe_product['id']}")
#             return stripe_product
#         else:
#             # Create a new Stripe product
#             stripe_product = stripe.Product.create(
#                 name=product.name,
#                 description=product.description or "",
#             )
#             product.stripe_product_id = stripe_product["id"]
#             product.save()
#             print(f"Created new Stripe product: {stripe_product['id']}")
#             return stripe_product
#     except Exception as e:
#         print(f"Error in get_or_create_stripe_product: {e}")
#         raise


# @receiver(post_save, sender=Product)
# def create_stripe_product(sender, instance, created, **kwargs):
#     if created and not instance.stripe_product_id:
#         stripe_product = get_or_create_stripe_product(instance)
#         instance.stripe_product_id = stripe_product["id"]
#         instance.save()

# @receiver(post_save, sender=Product)
# def sync_product_with_stripe(sender, instance, created, **kwargs):
#     """
#     Sync the local product with Stripe (create or update).
#     """
#     try:
#         if instance.stripe_product_id:
#             # Update existing Stripe product
#             stripe.Product.modify(
#                 instance.stripe_product_id,
#                 name=instance.name,
#                 description=instance.description or "",
#             )
#             print(f"Updated Stripe product: {instance.stripe_product_id}")
#         else:
#             # Create a new Stripe product
#             stripe_product = stripe.Product.create(
#                 name=instance.name,
#                 description=instance.description or "",
#             )
#             instance.stripe_product_id = stripe_product["id"]
#             instance.save()
#             print(f"Created new Stripe product: {stripe_product['id']}")
#     except Exception as e:
#         print(f"Error syncing product with Stripe: {e}")

# # def sync_stripe_product(sender, instance, created, **kwargs):
# #     """
# #     Create or update the Stripe product when the Product is saved.
# #     """
# #     try:
# #         if created:
# #             # Create a new Stripe product
# #             stripe_product = get_or_create_stripe_product(instance)
# #             print(f"Stripe product created: {stripe_product['id']}")
# #         else:
# #             # Update the existing Stripe product
# #             if instance.stripe_product_id:
# #                 stripe.Product.modify(
# #                     instance.stripe_product_id,
# #                     name=instance.name,
# #                     description=instance.description or "",
# #                 )
# #                 print(f"Updated Stripe product: {instance.stripe_product_id}")
# #     except Exception as e:
# #         print(f"Error syncing Stripe product: {e}")



# @receiver(post_delete, sender=Product)
# def delete_stripe_product(sender, instance, **kwargs):
#     """
#     Delete the Stripe product when a Product is deleted.
#     """
#     if instance.stripe_product_id:
#         try:
#             stripe.Product.delete(instance.stripe_product_id)
#             print(f"Deleted Stripe product: {instance.stripe_product_id}")
#         except Exception as e:
#             print(f"Error deleting Stripe product: {e}")

# def sanitize_file_name(file_name):
#     return urllib.parse.quote(file_name, safe='')

# # def upload_image_to_stripe(product_image):
# #     """
# #     Upload an image file to Stripe and update the Stripe file URL.
# #     """
# #     try:
# #         with product_image.image.open('rb') as img_file:
# #             file_name = sanitize_file_name(product_image.image.name)
# #             mime_type, _ = mimetypes.guess_type(product_image.image.path)
# #             if not mime_type:
# #                 mime_type = "application/octet-stream"

# #             stripe_file = stripe.File.create(
# #                 purpose="dispute_evidence",
# #                 file={
# #                     "data": img_file.read(),
# #                     "name": file_name,
# #                     "type": mime_type,
# #                 }
# #             )
# #             product_image.stripe_file_url = stripe_file["url"]
# #             product_image.save()
# #             print(f"Uploaded image to Stripe: {stripe_file['id']}")
# #             return stripe_file
# #     except Exception as e:
# #         print(f"Error uploading image to Stripe: {e}")
# #         raise

# def upload_image_to_stripe(product_image):
#     """
#     Upload an image file to Stripe and update the Stripe file URL.
#     Skips uploading if the image is an external URL.
#     """
#     try:
#         if product_image.image:  # Check if a local image is provided
#             with product_image.image.open('rb') as img_file:
#                 # Directly pass the file object to the `file` parameter
#                 stripe_file = stripe.File.create(
#                     purpose="dispute_evidence",
#                     file=img_file
#                 )
#                 product_image.stripe_file_url = stripe_file["url"]
#                 product_image.save()
#                 print(f"Uploaded image to Stripe: {stripe_file['id']}")
#                 return stripe_file
#         elif product_image.image_url:  # Skip uploading for external URLs
#             print("Skipping Stripe upload for external URL images.")
#             return None
#         else:
#             raise ValueError("No image or URL provided for upload.")
#     except Exception as e:
#         print(f"Error uploading image to Stripe: {e}")
#         raise



# @receiver(post_save, sender=ProductImage)
# def create_stripe_file(sender, instance, created, **kwargs):
#     """
#     Upload the product image to Stripe after it is saved in the database.
#     """
#     if created and not instance.stripe_file_url:
#         try:
#             stripe_file = upload_image_to_stripe(instance)
#             print(f"Stripe file created: {stripe_file['id']}")
#         except Exception as e:
#             print(f"Error creating Stripe file: {e}")

# @receiver(post_delete, sender=ProductImage)
# def delete_stripe_file(sender, instance, **kwargs):
#     """
#     Delete the Stripe file when a ProductImage is deleted.
#     """
#     if instance.stripe_file_url:
#         try:
#             stripe_file_id = instance.stripe_file_url.split("/")[-1]  # Extract file ID from URL
#             stripe.File.delete(stripe_file_id)
#             print(f"Deleted Stripe file: {stripe_file_id}")
#         except Exception as e:
#             print(f"Error deleting Stripe file: {e}")

