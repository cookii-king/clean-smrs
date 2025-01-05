from django.contrib import admin
from django import forms
from decimal import Decimal, InvalidOperation
from ...models import Price, Product

# Custom MultiWidget with increased width for Interval Count and Meter
class RecurringWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(
                choices=[
                    ('', '-- Select Interval --'),
                    ('day', 'Day'),
                    ('week', 'Week'),
                    ('month', 'Month'),
                    ('year', 'Year'),
                ],
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select Interval',
                    'aria-label': 'Interval'
                }
            ),
            forms.Select(
                choices=[
                    ('', '-- Select Aggregate Usage --'),
                    ('sum', 'Sum (default)'),
                    ('last_during_period', 'Last During Period'),
                    ('last_ever', 'Last Ever'),
                    ('max', 'Max'),
                ],
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select Aggregate Usage',
                    'aria-label': 'Aggregate Usage'
                }
            ),
            forms.Select(
                choices=[
                    ('', '-- Select Usage Type --'),
                    ('licensed', 'Licensed'),
                    ('metered', 'Metered'),
                ],
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select Usage Type',
                    'aria-label': 'Usage Type'
                }
            ),
            forms.NumberInput(
                attrs={
                    'class': 'form-control wider-input',  # Using custom CSS class
                    'placeholder': 'Enter Interval Count',
                    'aria-label': 'Interval Count',
                    'min': '1',
                    'max': '156',
                }
            ),
            forms.TextInput(  # Widget for 'meter'
                attrs={
                    'class': 'form-control wider-input',  # Apply a custom class if needed
                    'placeholder': 'Enter Meter',
                    'aria-label': 'Meter',
                    'style': 'width: 300px;',  # Adjust width as desired
                }
            ),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [
                value.get('interval'),
                value.get('aggregate_usage'),
                value.get('usage_type'),
                value.get('interval_count'),
                value.get('meter'),
            ]
        return [None, None, None, None, None]

# Custom MultiValueField with labels and help texts
class RecurringField(forms.MultiValueField):
    """
    Custom field to handle recurring dictionary for Stripe prices.
    """
    def __init__(self, *args, **kwargs):
        fields = [
            forms.ChoiceField(
                choices=[
                    ('', '-- Select Interval --'),
                    ('day', 'Day'),
                    ('week', 'Week'),
                    ('month', 'Month'),
                    ('year', 'Year'),
                ],
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False,  # Set to False to make it optional
                label="Interval",
            ),
            forms.ChoiceField(
                choices=[
                    ('', '-- Select Aggregate Usage --'),
                    ('sum', 'Sum (default)'),
                    ('last_during_period', 'Last During Period'),
                    ('last_ever', 'Last Ever'),
                    ('max', 'Max'),
                ],
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False,
                label="Aggregate Usage",
            ),
            forms.ChoiceField(
                choices=[
                    ('', '-- Select Usage Type --'),
                    ('licensed', 'Licensed'),
                    ('metered', 'Metered'),
                ],
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False,
                label="Usage Type",
            ),
            forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control wider-input'}),
                required=False,
                label="Interval Count",
                help_text=(
                    "The number of intervals between subscription billings. "
                    "For example, interval=month and interval_count=3 bills every 3 months. "
                    "Maximum of three years interval allowed (3 years, 36 months, or 156 weeks)."
                )
            ),
            forms.CharField(  # Added 'meter' field
                widget=forms.TextInput(attrs={'class': 'form-control wider-input'}),
                required=False,
                label="Meter",
                help_text="The meter tracking the usage of a metered price."
            ),
        ]
        self.widget = RecurringWidget()
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Combine inputs into a dictionary, excluding empty fields.
        """
        if not data_list or not any(data_list):
            return None  # Allow 'recurring' to be None if all subfields are empty

        field_names = ['interval', 'aggregate_usage', 'interval_count', 'usage_type', 'meter']
        recurring = {name: value for name, value in zip(field_names, data_list) if value not in [None, '']}

        # Only include 'aggregate_usage' and 'meter' if 'usage_type' is 'metered'
        usage_type = recurring.get('usage_type')
        if usage_type != 'metered':
            recurring.pop('aggregate_usage', None)
            recurring.pop('meter', None)

        return recurring

# Custom ModelForm with help texts and labels
class PriceAdminForm(forms.ModelForm):
    """
    Custom form for Price model validation.
    """
    recurring = RecurringField(required=False)  # Make the whole recurring field optional

    class Meta:
        model = Price
        fields = '__all__'

    def clean_recurring(self):
        """
        Validate and ensure recurring values are correctly formatted.
        """
        recurring = self.cleaned_data.get('recurring')

        # If recurring is None or all subfields are empty, it's valid
        if not recurring:
            return None

        # Check if at least one field in recurring has a value
        if not any(recurring.values()):
            return None

        # If any subfield is filled, require 'interval'
        if not recurring.get('interval'):
            raise forms.ValidationError("Recurring interval is required when configuring recurring billing.")

        # Validate 'interval_count' if provided
        interval_count = recurring.get('interval_count')
        if interval_count:
            if interval_count <= 0:
                raise forms.ValidationError("Interval count must be a positive number.")
            # Maximum validation based on interval
            interval = recurring.get('interval')
            max_counts = {
                'week': 156,
                'month': 36,
                'year': 3,
                'day': None,  # Define as needed
            }
            max_count = max_counts.get(interval)
            if max_count and interval_count > max_count:
                raise forms.ValidationError(f"Interval count for {interval} cannot exceed {max_count}.")

        # If 'usage_type' is 'metered', ensure 'aggregate_usage' and 'meter' are provided
        usage_type = recurring.get('usage_type')
        if usage_type == 'metered':
            if not recurring.get('aggregate_usage'):
                raise forms.ValidationError("Aggregate usage is required for metered usage type.")
            if not recurring.get('meter'):
                raise forms.ValidationError("Meter is required for metered usage type.")

        return recurring

    def clean_unit_amount(self):
        """
        Validate and ensure the amount is a positive decimal.
        """
        unit_amount = self.cleaned_data.get('unit_amount')
        if unit_amount is None or (isinstance(unit_amount, str) and unit_amount.strip() == ""):
            raise forms.ValidationError("Amount must be provided.")
        try:
            unit_amount = Decimal(unit_amount)
            if unit_amount <= 0:
                raise forms.ValidationError("Amount must be a positive number.")
        except (ValueError, InvalidOperation):
            raise forms.ValidationError("Amount must be a valid decimal number.")
        return unit_amount

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
        # Customize the queryset and display format for the product field
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.stripe_product_id} ({obj.name})"
        # Add overall help text for the recurring field
        self.fields['recurring'].help_text = "Configure the recurring billing parameters for this price."

# Admin configuration with fieldsets
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Stripe subscription prices.
    """
    list_display = ('product', 'unit_amount', 'currency', 'stripe_price_id', 'created', 'updated')
    search_fields = ('product__name', 'stripe_price_id')
    list_filter = ('currency', 'created')
    readonly_fields = ('stripe_price_id', 'created', 'updated')
    form = PriceAdminForm
    fieldsets = (
        (None, {
            'fields': ('product', 'unit_amount', 'currency', 'stripe_price_id',)
        }),
        ('Recurring Parameters', {
            'fields': ('recurring',),
            'description': 'Configure the recurring billing parameters for this price.',
        }),
        ('Timestamps', {
            'fields': ('created', 'updated',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to create or update Stripe price when saving in admin.
        """
        super().save_model(request, obj, form, change)
        try:
            # Automatically create or update the Stripe price
            stripe_price = obj.create_or_get_stripe_price()
            self.message_user(request, f"Stripe price synced: {stripe_price['id']}")
        except Exception as e:
            self.message_user(request, f"Error syncing Stripe price: {e}", level='error')

    def delete_model(self, request, obj):
        """
        Override delete_model to delete associated Stripe price.
        """
        try:
            if obj.stripe_price_id:
                obj.delete_stripe_price()
                self.message_user(request, f"Deleted Stripe price: {obj.stripe_price_id}")
        except Exception as e:
            self.message_user(request, f"Error deleting Stripe price: {e}", level='error')
        super().delete_model(request, obj)