from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
# from ...models import Product
from ...models import Product, ProductImage, ProductVideo, Price
from ...forms import ProductForm, ProductImageForm, ProductVideoForm  # Assume you have these forms
from ...views import authenticate_user, check_mfa
class ProductView(APIView):
    def post(self, request, product_id=None):
        try:
            if product_id:
                # Check if the action is to delete the product
                if request.POST.get('action') == 'delete':
                    product = get_object_or_404(Product, id=product_id)
                    product.delete_stripe_product()  # Delete from Stripe
                    product.delete()  # Delete from local database
                    message = "Product deleted successfully."
                    is_error = False
                    status_code = 200
                    return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

                # Update existing product
                product = get_object_or_404(Product, id=product_id)
                form = ProductForm(request.POST, request.FILES, instance=product)
            else:
                # Create new product
                form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                product = form.save()

                # Handle image uploads
                for image in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                    ProductVideo.objects.create(product=product, video=video)

                # Create product in Stripe if it doesn't already exist
                if not product.stripe_product_id:
                    product.create_stripe_product()

                # Handle price creation
                price_amount = request.POST.get('price_amount')
                price_currency = request.POST.get('price_currency', 'usd')
                price_interval = request.POST.get('price_interval', 'one_time')

                if price_amount:  # Only create a price if the amount is provided
                    recurring = (
                        {"interval": price_interval}
                        if price_interval in ["month", "year"]
                        else None
                    )
                    try:
                        # Create a local Price instance
                        price = Price.objects.create(
                            product=product,
                            unit_amount=float(price_amount),
                            currency=price_currency,
                            recurring=recurring,
                        )

                        # Create the Stripe price and save the Stripe ID
                        price.create_stripe_price()

                    except Exception as e:
                        print(f"Error creating price: {e}")
                        message = f"Failed to create price: {e}"
                        is_error = True
                        status_code = 500
                        return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

                message = "Product and price saved successfully."
                is_error = False
                status_code = 201
            else:
                print("Form errors:", form.errors)
                message = "Form is not valid."
                is_error = True
                status_code = 400

            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'POST' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    # def post(self, request, product_id=None):
    #     try:
    #         if product_id:
    #             # Check if the action is to delete the product
    #             if request.POST.get('action') == 'delete':
    #                 product = get_object_or_404(Product, id=product_id)
    #                 product.delete_stripe_product()  # Delete from Stripe
    #                 product.delete()  # Delete from local database
    #                 message = "Product deleted successfully."
    #                 is_error = False
    #                 status_code = 200
    #                 return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    #             # Update existing product
    #             product = get_object_or_404(Product, id=product_id)
    #             form = ProductForm(request.POST, request.FILES, instance=product)
    #         else:
    #             # Create new product
    #             form = ProductForm(request.POST, request.FILES)

    #         if form.is_valid():
    #             product = form.save()

    #             # Handle image uploads
    #             for image in request.FILES.getlist('images'):
    #                 ProductImage.objects.create(product=product, image=image)

    #             # Handle video uploads
    #             for video in request.FILES.getlist('videos'):
    #                 ProductVideo.objects.create(product=product, video=video)

    #             # Create product in Stripe if it doesn't already exist
    #             if not product.stripe_product_id:
    #                 product.create_stripe_product()

    #             message = "Product saved successfully."
    #             is_error = False
    #             status_code = 201
    #         else:
    #             print("Form errors:", form.errors)
    #             message = "Form is not valid."
    #             is_error = True
    #             status_code = 400

    #         return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    #     except Exception as e:
    #         message = f"'POST' Method Failed for ProductView: {e}"
    #         is_error = True
    #         status_code = 500
    #         return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request, product_id=None):
        try:
            # account = authenticate_user(request)
            # check_mfa(account=account)
            action = request.GET.get('action', 'view')
            print(f"${action}")
            product = None
            images = None
            videos = None

            if product_id:
                product = get_object_or_404(Product, id=product_id)
                images = ProductImage.objects.filter(product=product)
                videos = ProductVideo.objects.filter(product=product)

            if action == 'create' and request.user.is_superuser:
                form = ProductForm()
                return render(request, 'product/create.html', {'form': form})
            elif action == 'edit' and request.user.is_superuser:
                form = ProductForm(instance=product)
                return render(request, 'product/edit.html', {
                    'form': form,
                    'images': images,
                    'videos': videos,
                    'product': product
                })
            else:
                return render(request, 'product/product.html', {
                    'product': product,
                    'images': images,
                    'videos': videos
                })
        except Exception as e:
            message = f"'GET' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    # def get(self, request, product_id=None):
    #     try:
    #         if product_id:
    #             # Editing an existing product
    #             product = get_object_or_404(Product, id=product_id)
    #             form = ProductForm(instance=product)
    #             images = ProductImage.objects.filter(product=product)
    #             videos = ProductVideo.objects.filter(product=product)
    #         else:
    #             # Creating a new product
    #             form = ProductForm()
    #             images = None
    #             videos = None

    #         return render(request, 'product/create.html', {
    #             'form': form,
    #             'images': images,
    #             'videos': videos,
    #             'product': product if product_id else None
    #         })
    #     except Exception as e:
    #         message = f"'GET' Method Failed for ProductView: {e}"
    #         is_error = True
    #         status_code = 500
    #         return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            message = "Product deleted successfully."
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for ProductView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class ProductsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            message = "POST request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'POST' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Filter products to show only goods
            products = Product.objects.filter(deleted__isnull=True, type='good')
            return render(request, 'product/products.html', {'products': products})
        except Exception as e:
            message = f"'GET' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        
    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            product.deleted = now()
            product.save()
            message = "Product deleted successfully."
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for ProductsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')