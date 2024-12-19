from django.urls import path
from .views import IndexView, AboutView, ContactView, SupportView, TermsOfServiceView, PrivacyPolicyView, ProductView, ProductsView, PriceView, PricesView, PlanView, PlansView, SubscriptionView, SubscriptionsView, PaymentLinksView, AccountView, ConfirmEmailView, VerifyMfaView, EnableMfaView, DisableMfaView, LoginView, LogoutView, RegisterView

urlpatterns = [
    # # system start
    path('', IndexView.as_view(), name="index"),
    path('about', AboutView.as_view(), name="about"),
    path('contact', ContactView.as_view(), name="contact"),
    path('contact/submit', ContactView.as_view(), name="contact-submit"),
    path('support', SupportView.as_view(), name="support"),
    path('support/submit', SupportView.as_view(), name="support-submit"),
    path('terms-of-service', TermsOfServiceView.as_view(), name="terms-of-service"),
    path('privacy-policy', PrivacyPolicyView.as_view(), name="privacy-policy"),
    # # system end
    # # ========================================================================== #
    # # ========================================================================== #
    # # account start
    path('account', AccountView.as_view(), name="account"),
    # # account end
    # # ========================================================================== #
    # # ========================================================================== #
    # # payment-links start
    path('payment-links', PaymentLinksView.as_view(), name="payment-links"),
    path('payment-link/create', PaymentLinksView.as_view(), name="payment-link-create"), 
    # # payment-links end
    # # ========================================================================== #
    # # ========================================================================== #
    # # product start
    path('product', ProductView.as_view(), name="product"),
    path('product/create', ProductView.as_view(), name="product-create"),
    path('product/<uuid:product_id>', ProductView.as_view(), name="product"),
    path('products/', ProductsView.as_view(), name="products"),
    # # product end
    # # ========================================================================== #
    # # ========================================================================== #
    # # prices start
    path('price', PriceView.as_view(), name="price"),
    path('price/create', PriceView.as_view(), name="price-create"),
    path('price/<uuid:price_id>', PriceView.as_view(), name="price"),
    path('prices', PricesView.as_view(), name="prices"),
    # # prices end
    # # ========================================================================== #
    # # ========================================================================== #
    # # plans start
    path('plan', PlanView.as_view(), name="plan"),
    path('plan/create', PlanView.as_view(), name="plan-create"),
    path('plan/<uuid:plan_id>', PlanView.as_view(), name="plan"),
    path('plans', PlansView.as_view(), name="plans"),
    # # plans end
    # # ========================================================================== #
    # # ========================================================================== #
    # # subscriptions start
    path('subscription', SubscriptionView.as_view(), name="subscription"),
    path('subscription/create', SubscriptionView.as_view(), name="subscription-create"),
    path('subscription/<uuid:subscription_id>', SubscriptionView.as_view(), name="subscription"),
    path('subscriptions', SubscriptionsView.as_view(), name="subscriptions"),
    # # subscriptions end
    # # ========================================================================== #
    # # ========================================================================== #
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
]
