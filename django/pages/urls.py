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
    path('<path:dummy>/', Error404View.as_view(), name="Error-404"),
    # # system end
    # # ========================================================================== #
    # # ========================================================================== #
    # # product start
    path('product', ProductView.as_view(), name="product"),
    path('product/create', ProductView.as_view(), name="product-create"),
    path('product/<uuid:product_id>', ProductView.as_view(), name="product"),
    path('product/<uuid:product_id>/', ProductView.as_view(), name="product"),
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
    # # payment link start
    path('payment-link', PaymentLinkView.as_view(), name="payment-link"),
    path('payment-link/create', PaymentLinkView.as_view(), name="payment-link-create"),
    path('payment-link/<uuid:payment_link_id>', PaymentLinkView.as_view(), name="payment-link"),
    path('payment-links', PaymentLinksView.as_view(), name="payment-links"),
    path('payment-links/', PaymentLinksView.as_view(), name="payment-links"),
    # # payment link end
    # # ========================================================================== #
    # # ========================================================================== #
    # # checkout start
    path('checkout', CheckoutView.as_view(), name="checkout"),
    path('checkout/create', CheckoutView.as_view(), name="checkout-create"),
    path('checkout/subscribe', CheckoutView.as_view(), name="checkout-subscribe"),
    path('checkout/upgrade', CheckoutView.as_view(), name="checkout-upgrade"),
    path('checkout/<uuid:checkout_id>', CheckoutView.as_view(), name="checkout"),
    path('checkout/success/', CheckoutView.as_view(), name="checkout-success"),
    path('checkout/failure/', CheckoutView.as_view(), name="checkout-failure"),
    path('checkouts', CheckoutsView.as_view(), name="checkouts"),
    path('checkouts/', CheckoutsView.as_view(), name="checkouts"),
    # # checkout end
    # # ========================================================================== #
    # # ========================================================================== #
    # # cart start
    path('cart', CartView.as_view(), name="cart"),
    path('add-to-cart', CartView.as_view(), name='add_to_cart'),
    path('remove-from-cart', CartView.as_view(), name='remove_from_cart'),
    path('update-item/<uuid:cart_item_id>/', CartView.as_view(), name='update_cart_item'),
    path('remove-item/<uuid:cart_item_id>/', CartView.as_view(), name='remove_cart_item'),# # cart end
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
    path('api-key', ApiKeyView.as_view(), name="api-key"),
    path('api-key/validate', ApiKeyView.as_view(), name="api-key-validate"),
    path('api-key/validate/', ApiKeyView.as_view(), name="api-key-validate"),
    path('api-key/generate', ApiKeyView.as_view(), name="api-key-generate"),
    path('api-key/generate/', ApiKeyView.as_view(), name="api-key-generate"),
    path('api-key/re-generate', ApiKeyView.as_view(), name="api-key-re-generate"),
    path('api-key/re-generate/', ApiKeyView.as_view(), name="api-key-re-generate"),
    path('api-key/reveal', ApiKeyView.as_view(), name="api-key-reveal"),
    path('api-key/reveal/', ApiKeyView.as_view(), name="api-key-reveal"),
    path('api-key/set-primary', ApiKeyView.as_view(), name='set-primary-key'),
    path('api-key/set-primary/', ApiKeyView.as_view(), name='set-primary-key'),
    # # api key end
    # # ========================================================================== #
    # # ========================================================================== #
]