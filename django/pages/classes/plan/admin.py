from django.contrib import admin
from django import forms
from decimal import Decimal, InvalidOperation
from ...models import Plan, Product

class PlanAdminForm(forms.ModelForm):
    """
    Custom form for Plan model validation.
    """
    class Meta:
        model = Plan
        fields = '__all__'


    def clean_amount(self):
        """
        Validate and ensure the amount is a positive decimal.
        """
        amount = self.cleaned_data.get('amount')
        if amount is None or isinstance(amount, str) and amount.strip() == "":
            raise forms.ValidationError("Amount must be provided.")
        try:
            # Ensure amount is a valid Decimal
            amount = Decimal(amount)
            if amount <= 0:
                raise forms.ValidationError("Amount must be a positive number.")
        except (ValueError, InvalidOperation):
            raise forms.ValidationError("Amount must be a valid decimal number.")
        return amount

    def clean(self):
        """
        Perform additional validations for the form.
        """
        cleaned_data = super().clean()
        currency = cleaned_data.get('currency')
        interval = cleaned_data.get('interval')
        product = cleaned_data.get('product')

        if not currency:
            raise forms.ValidationError("Currency is required.")
        if not interval:
            raise forms.ValidationError("Interval is required.")
        if not product:
            raise forms.ValidationError("Product is required.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Searchable dropdowns for currency and interval
        self.fields['currency'].widget = forms.Select(
            choices= [
                ('AED', 'United Arab Emirates Dirham'),
                ('AFN', 'Afghan Afghani'),
                ('ALL', 'Albanian Lek'),
                ('AMD', 'Armenian Dram'),
                ('ANG', 'Netherlands Antillean Guilder'),
                ('AOA', 'Angolan Kwanza'),
                ('ARS', 'Argentine Peso'),
                ('AUD', 'Australian Dollar'),
                ('AWG', 'Aruban Florin'),
                ('AZN', 'Azerbaijani Manat'),
                ('BAM', 'Bosnia-Herzegovina Convertible Mark'),
                ('BBD', 'Barbadian Dollar'),
                ('BDT', 'Bangladeshi Taka'),
                ('BGN', 'Bulgarian Lev'),
                ('BHD', 'Bahraini Dinar'),
                ('BIF', 'Burundian Franc'),
                ('BMD', 'Bermudan Dollar'),
                ('BND', 'Brunei Dollar'),
                ('BOB', 'Bolivian Boliviano'),
                ('BOV', 'Bolivian Mvdol'),
                ('BRL', 'Brazilian Real'),
                ('BSD', 'Bahamian Dollar'),
                ('BTN', 'Bhutanese Ngultrum'),
                ('BWP', 'Botswanan Pula'),
                ('BYN', 'Belarusian Ruble'),
                ('BZD', 'Belize Dollar'),
                ('CAD', 'Canadian Dollar'),
                ('CDF', 'Congolese Franc'),
                ('CHF', 'Swiss Franc'),
                ('CLF', 'Chilean Unit of Account (UF)'),
                ('CLP', 'Chilean Peso'),
                ('CNY', 'Chinese Yuan'),
                ('COP', 'Colombian Peso'),
                ('COU', 'Unidad de Valor Real'),
                ('CRC', 'Costa Rican Colón'),
                ('CUC', 'Cuban Convertible Peso'),
                ('CUP', 'Cuban Peso'),
                ('CVE', 'Cape Verdean Escudo'),
                ('CZK', 'Czech Republic Koruna'),
                ('DJF', 'Djiboutian Franc'),
                ('DKK', 'Danish Krone'),
                ('DOP', 'Dominican Peso'),
                ('DZD', 'Algerian Dinar'),
                ('EGP', 'Egyptian Pound'),
                ('ERN', 'Eritrean Nakfa'),
                ('ETB', 'Ethiopian Birr'),
                ('EUR', 'Euro'),
                ('FJD', 'Fijian Dollar'),
                ('FKP', 'Falkland Islands Pound'),
                ('GBP', 'British Pound Sterling'),
                ('GEL', 'Georgian Lari'),
                ('GHS', 'Ghanaian Cedi'),
                ('GIP', 'Gibraltar Pound'),
                ('GMD', 'Gambian Dalasi'),
                ('GNF', 'Guinean Franc'),
                ('GTQ', 'Guatemalan Quetzal'),
                ('GYD', 'Guyanaese Dollar'),
                ('HKD', 'Hong Kong Dollar'),
                ('HNL', 'Honduran Lempira'),
                ('HRK', 'Croatian Kuna'),
                ('HTG', 'Haitian Gourde'),
                ('HUF', 'Hungarian Forint'),
                ('IDR', 'Indonesian Rupiah'),
                ('ILS', 'Israeli New Shekel'),
                ('INR', 'Indian Rupee'),
                ('IQD', 'Iraqi Dinar'),
                ('IRR', 'Iranian Rial'),
                ('ISK', 'Icelandic Króna'),
                ('JMD', 'Jamaican Dollar'),
                ('JOD', 'Jordanian Dinar'),
                ('JPY', 'Japanese Yen'),
                ('KES', 'Kenyan Shilling'),
                ('KGS', 'Kyrgystani Som'),
                ('KHR', 'Cambodian Riel'),
                ('KMF', 'Comorian Franc'),
                ('KPW', 'North Korean Won'),
                ('KRW', 'South Korean Won'),
                ('KWD', 'Kuwaiti Dinar'),
                ('KYD', 'Cayman Islands Dollar'),
                ('KZT', 'Kazakhstani Tenge'),
                ('LAK', 'Laotian Kip'),
                ('LBP', 'Lebanese Pound'),
                ('LKR', 'Sri Lankan Rupee'),
                ('LRD', 'Liberian Dollar'),
                ('LSL', 'Lesotho Loti'),
                ('LYD', 'Libyan Dinar'),
                ('MAD', 'Moroccan Dirham'),
                ('MDL', 'Moldovan Leu'),
                ('MGA', 'Malagasy Ariary'),
                ('MKD', 'Macedonian Denar'),
                ('MMK', 'Myanma Kyat'),
                ('MNT', 'Mongolian Tugrik'),
                ('MOP', 'Macanese Pataca'),
                ('MRU', 'Mauritanian Ouguiya'),
                ('MUR', 'Mauritian Rupee'),
                ('MVR', 'Maldivian Rufiyaa'),
                ('MWK', 'Malawian Kwacha'),
                ('MXN', 'Mexican Peso'),
                ('MXV', 'Mexican Unidad de Inversion (UDI)'),
                ('MYR', 'Malaysian Ringgit'),
                ('MZN', 'Mozambican Metical'),
                ('NAD', 'Namibian Dollar'),
                ('NGN', 'Nigerian Naira'),
                ('NIO', 'Nicaraguan Córdoba'),
                ('NOK', 'Norwegian Krone'),
                ('NPR', 'Nepalese Rupee'),
                ('NZD', 'New Zealand Dollar'),
                ('OMR', 'Omani Rial'),
                ('PAB', 'Panamanian Balboa'),
                ('PEN', 'Peruvian Nuevo Sol'),
                ('PGK', 'Papua New Guinean Kina'),
                ('PHP', 'Philippine Peso'),
                ('PKR', 'Pakistani Rupee'),
                ('PLN', 'Polish Złoty'),
                ('PYG', 'Paraguayan Guaraní'),
                ('QAR', 'Qatari Rial'),
                ('RON', 'Romanian Leu'),
                ('RSD', 'Serbian Dinar'),
                ('RUB', 'Russian Ruble'),
                ('RWF', 'Rwandan Franc'),
                ('SAR', 'Saudi Riyal'),
                ('SBD', 'Solomon Islands Dollar'),
                ('SCR', 'Seychellois Rupee'),
                ('SDG', 'Sudanese Pound'),
                ('SEK', 'Swedish Krona'),
                ('SGD', 'Singapore Dollar'),
                ('SHP', 'Saint Helena Pound'),
                ('SLL', 'Sierra Leonean Leone'),
                ('SOS', 'Somali Shilling'),
                ('SRD', 'Surinamese Dollar'),
                ('SSP', 'South Sudanese Pound'),
                ('STN', 'São Tomé and Príncipe Dobra'),
                ('SVC', 'Salvadoran Colón'),
                ('SYP', 'Syrian Pound'),
                ('SZL', 'Eswatini Lilangeni'),
                ('THB', 'Thai Baht'),
                ('TJS', 'Tajikistani Somoni'),
                ('TMT', 'Turkmenistani Manat'),
                ('TND', 'Tunisian Dinar'),
                ('TOP', 'Tongan Paʻanga'),
                ('TRY', 'Turkish Lira'),
                ('TTD', 'Trinidad and Tobago Dollar'),
                ('TWD', 'New Taiwan Dollar'),
                ('TZS', 'Tanzanian Shilling'),
                ('UAH', 'Ukrainian Hryvnia'),
                ('UGX', 'Ugandan Shilling'),
                ('USD', 'United States Dollar'),
                ('USN', 'United States Dollar (Next day)'),
                ('UYI', 'Uruguay Peso en Unidades Indexadas (UI)'),
                ('UYU', 'Uruguayan Peso'),
                ('UYW', 'Unidad Previsional'),
                ('UZS', 'Uzbekistan Som'),
                ('VES', 'Venezuelan Bolívar Soberano'),
                ('VND', 'Vietnamese Dong'),
                ('VUV', 'Vanuatu Vatu'),
                ('WST', 'Samoan Tala'),
                ('XCD', 'East Caribbean Dollar'),
                ('XOF', 'CFA Franc BCEAO'),
                ('XPF', 'CFP Franc'),
                ('YER', 'Yemeni Rial'),
                ('ZAR', 'South African Rand'),
                ('ZMW', 'Zambian Kwacha'),
                ('ZWL', 'Zimbabwean Dollar'),
            ],
            attrs={'class': 'form-control select2'}
        )

        self.fields['interval'].widget = forms.Select(
            choices=[
                ('day', 'Daily'),
                ('week', 'Weekly'),
                ('month', 'Monthly'),
                ('year', 'Yearly'),
            ],
            attrs={'class': 'form-control select2'}
        )

        # Customize the queryset and display format for the product field
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.stripe_product_id} ({obj.name})"




@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Stripe subscription plans.
    """
    list_display = ('product', 'amount', 'currency', 'interval', 'stripe_plan_id', 'created', 'updated')
    search_fields = ('product__name', 'stripe_plan_id')
    list_filter = ('currency', 'interval', 'created')
    readonly_fields = ('stripe_plan_id', 'created', 'updated')
    form = PlanAdminForm

    def save_model(self, request, obj, form, change):
        """
        Override save_model to create or update Stripe plan when saving in admin.
        """
        super().save_model(request, obj, form, change)
        try:
            # Automatically create or update the Stripe plan
            stripe_plan = obj.create_or_get_stripe_plan()
            self.message_user(request, f"Stripe plan synced: {stripe_plan['id']}")
        except Exception as e:
            self.message_user(request, f"Error syncing Stripe plan: {e}", level='error')

    def delete_model(self, request, obj):
        """
        Override delete_model to delete associated Stripe plan.
        """
        try:
            if obj.stripe_plan_id:
                obj.delete_stripe_plan()
                self.message_user(request, f"Deleted Stripe plan: {obj.stripe_plan_id}")
        except Exception as e:
            self.message_user(request, f"Error deleting Stripe plan: {e}", level='error')
        super().delete_model(request, obj)
