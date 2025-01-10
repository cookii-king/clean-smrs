from django.urls import path
from .views import *

urlpatterns = [
    path('account', AccountView.as_view(), name="account"),
    path('account/edit', AccountView.as_view(), name="account-edit"),
    # # authentication start
    path('confirm-email', ConfirmEmailView.as_view(), name="confirm-email"),
    path('verify-mfa', VerifyMfaView.as_view(), name="verify-mfa"),
    path('verify-mfa/<uuid:otp>', VerifyMfaView.as_view(), name="verify-mfa"),
    path('enable-mfa', EnableMfaView.as_view(), name="enable-mfa"),
    path('disable-mfa', DisableMfaView.as_view(), name="disable-mfa"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', RegisterView.as_view(), name="register"),
    # # authentication end
    # # ========================================================================== #
    # # ========================================================================== #

    # # system start
    path('', IndexView.as_view(), name="index"),
    path('about', AboutView.as_view(), name="about"),
    path('contact', ContactView.as_view(), name="contact"),
    path('contact/submit', ContactView.as_view(), name="contact-submit"),
    path('support', SupportView.as_view(), name="support"),
    path('support/submit', SupportView.as_view(), name="support-submit"),
    path('terms-of-service', TermsOfServiceView.as_view(), name="terms-of-service"),
    path('privacy-policy', PrivacyPolicyView.as_view(), name="privacy-policy"),
    path('plans-and-pricing', PlansAndPricingView.as_view(), name="plans-and-pricing"),
    path('resources', ResourcesView.as_view(), name="resources"),
    path('user-guides', UserGuidesView.as_view(), name="user-guides"),
    path('tutorials', TutorialsView.as_view(), name="tutorials"),
    path('community-forum', CommunityForumView.as_view(), name="community-forum"),
    path('support-ticket', SupportTicketView.as_view(), name="support-ticket"),
    path('submit-support-ticket', SupportTicketView.as_view(), name="submit-support-ticket"),
    path('user-guide-smr', UserGuideView.as_view(), name="user-guide-smr"),
    path('user-guide-portal', UserGuideView.as_view(), name="user-guide-portal"),
    path('tutorial-setup', TutorialView.as_view(), name="tutorial-setup"),
    path('tutorial-maintenance', TutorialView.as_view(), name="tutorial-maintenance"),
    path('whitepaper-clean-energy', WhitePaperView.as_view(), name="whitepaper-clean-energy"),
    path('whitepaper-smr-technology', WhitePaperView.as_view(), name="whitepaper-smr-technology"),
    path('faqs', FAQsView.as_view(), name="faqs"),
    # path('<path:dummy>/', Error404View.as_view(), name="Error-404"),
    # # system end
    # # ========================================================================== #
    # # ========================================================================== #
    # # product start
    # Product-related URLs
    path('products/', ProductsView.as_view(), name="products-list"),
    path('product/create/', ProductView.as_view(), name="product-create"),
    path('product/create', ProductView.as_view(), name="product-create"),
    path('products/buy-now/<uuid:product_id>/', ProductsView.as_view(), name="buy-now"),
    path('products/<uuid:product_id>/', ProductView.as_view(), name="product-detail"),
    path('products/<uuid:product_id>/update/', ProductView.as_view(), name="product-update"),
    path('products/<uuid:product_id>/update', ProductView.as_view(), name="product-update"),
    path('products/<uuid:product_id>/delete/', ProductView.as_view(), name="product-delete"),
    path('products/<uuid:product_id>/delete', ProductView.as_view(), name="product-delete"),
    # path('product', ProductView.as_view(), name="product"),
    # path('product/create', ProductView.as_view(), name="product-create"),
    # path('product/update/<uuid:product_id>', ProductView.as_view(), name="product-update"),
    # path('product/delete/<uuid:product_id>', ProductView.as_view(), name="product-delete"),
    # path('product/<uuid:product_id>', ProductView.as_view(), name="product"),
    # path('product/<uuid:product_id>/', ProductView.as_view(), name="product"),
    path('products', ProductsView.as_view(), name="products"),
    path('products/', ProductsView.as_view(), name="products"),
    # # product end
    # # ========================================================================== #
    # # ========================================================================== #
    # # subscription start
    path('subscription', SubscriptionView.as_view(), name="subscription"),
    path('subscription/create', SubscriptionView.as_view(), name="subscription-create"),
    path('subscription/cancel', SubscriptionView.as_view(), name="subscription-cancel"),
    path('subscription/<uuid:subscription_id>', SubscriptionView.as_view(), name="subscription"),
    path('subscriptions', SubscriptionsView.as_view(), name="subscriptions"),
    path('subscriptions/',SubscriptionsView.as_view(), name="subscriptions"),
    # # order end
    # # ========================================================================== #
    # # ========================================================================== #    
    # # checkout start
    path('checkout', CheckoutView.as_view(), name="checkout"),
    path('checkout/create', CheckoutView.as_view(), name="checkout-create"),
    path('checkout/subscribe', CheckoutView.as_view(), name="checkout-subscribe"),
    path('checkout/upgrade', CheckoutView.as_view(), name="checkout-upgrade"),
    path('checkout/<uuid:checkout_id>', CheckoutView.as_view(), name="checkout"),
    path('checkout/success', CheckoutView.as_view(), name="checkout-success"),
    path('checkout/success/', CheckoutView.as_view(), name="checkout-success"),
    path('checkout/failure', CheckoutView.as_view(), name="checkout-failure"),
    path('checkout/failure/', CheckoutView.as_view(), name="checkout-failure"),
    # # checkout end
    # # ========================================================================== #
    # # ========================================================================== #
    # # cart start
    path('cart', CartView.as_view(), name="cart"),
    # path('add-to-cart', CartView.as_view(), name='add-to-cart'),
    # Updated URL pattern for 'add-to-cart' to accept a product_id
    path('add-to-cart/<uuid:product_id>/', CartView.as_view(), name='add-to-cart'),
    path('remove-from-cart', CartView.as_view(), name='remove-from-cart'),
    path('update-item/<uuid:cart_item_id>/', CartView.as_view(), name='update-cart-item'),
    path('remove-item/<uuid:cart_item_id>/', CartView.as_view(), name='remove-cart-item'),# # cart end
    # # ========================================================================== #
    # # ========================================================================== #
    # # order start
    path('order', OrderView.as_view(), name="order"),
    path('order/create', OrderView.as_view(), name="order-create"),
    path('order/<uuid:order_id>', OrderView.as_view(), name="order"),
    path('orders', OrdersView.as_view(), name="orders"),
    path('orders/', OrdersView.as_view(), name="orders"),
    # # order end
    # # ========================================================================== #
    # # ========================================================================== #
    # # observation start
    path('observation', ObservationView.as_view(), name="observation"),
    path('observation/create', ObservationView.as_view(), name="observation-create"),
    path('observation/<uuid:observation_id>', ObservationView.as_view(), name="observation"),
    path('observations', ObservationsView.as_view(), name="observations"),
    path('observations/', ObservationsView.as_view(), name="observations"),
    # # order end
    # # ========================================================================== #
    # # ========================================================================== #
    # # webhook start
    path('webhook', WebhookView.as_view(), name="webhook"),
    # # webhook end
    # # ========================================================================== #
    # # ========================================================================== #
    # # api key start
    path('api-key', ApiView.as_view(), name="api-key"),
    path('api-key/validate', ApiView.as_view(), name="api-key-validate"),
    path('api-key/validate/', ApiView.as_view(), name="api-key-validate"),
    path('api-key/generate', ApiView.as_view(), name="api-key-generate"),
    path('api-key/generate/', ApiView.as_view(), name="api-key-generate"),
    path('api-key/re-generate', ApiView.as_view(), name="api-key-re-generate"),
    path('api-key/re-generate/', ApiView.as_view(), name="api-key-re-generate"),
    path('api-key/reveal', ApiView.as_view(), name="api-key-reveal"),
    path('api-key/reveal/', ApiView.as_view(), name="api-key-reveal"),
    path('api-key/set-primary', ApiView.as_view(), name='set-primary-key'),
    path('api-key/set-primary/', ApiView.as_view(), name='set-primary-key'),
    # # api key end
    # # ========================================================================== #
    # # ========================================================================== #
    path('response', ResponseView.as_view(), name="response"),
]