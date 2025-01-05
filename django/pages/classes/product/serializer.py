from rest_framework import serializers
from ...models import Product, ProductImage

# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ['id', 'image_url', 'stripe_file_url', 'uploaded_at']
#         read_only_fields = ['stripe_file_url', 'uploaded_at']


class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
 
            'name',
 
 
            'description',
 
        ]
        read_only_fields = ['stripe_product_id', 'created', 'updated']

    def create(self, validated_data):
        """
        Create a new Product and handle Stripe product creation.
        """
        # images_data = self.context.get('view').request.FILES.getlist('images', [])
        product = Product.objects.create(**validated_data)
        # # Save images if provided
        # for image in images_data:
        #     ProductImage.objects.create(product=product, image=image)
        product.create_or_get_stripe_product()
        return product

    def update(self, instance, validated_data):
        """
        Update an existing Product and sync changes with Stripe.
        """
        instance.name = validated_data.get('name', instance.name)
        # instance.type = validated_data.get('type', instance.type)
        # instance.reoccurrence = validated_data.get('reoccurrence', instance.reoccurrence)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        instance.create_or_get_stripe_product()  # Sync changes with Stripe
        return instance
