from django.db import models

# Create your models here.

class Category(models.Model):
    """
    Category model represents a category for assets.

    Attributes:
        name (str): The name of the category.
        is_liquid (bool): Whether the category is liquid or not.
        description (str): A brief description of the category.
        is_delatable (bool): Whether the category can be deleted.
        is_auto_updated (bool): Whether the category is automatically updated.
        created_at (datetime): The date and time when the category was created.
        updated_at (datetime): The date and time when the category was last updated.
    """
    name = models.CharField(max_length=100)
    is_liquid = models.BooleanField(default=True)
    description = models.TextField(null=True, blank = True)
    is_delatable = models.BooleanField(default = True)
    is_auto_updated = models.BooleanField(default = True, null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the category, which is its name.
        """
        return self.name
    
class Currency(models.Model):
    """
    Currency model represents a currency.

    Attributes:
        currency_code (str): The code of the currency.
        currency_name (str): The name of the currency.
        created_at (datetime): The date and time when the currency was created.
        updated_at (datetime): The date and time when the currency was last updated.
    """
    currency_code = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the currency, which is its code.
        """
        return self.currency_code
    
class UnitType(models.Model):
    """
    UnitType model represents a unit type for assets.

    Attributes:
        name (str): The name of the unit type.
        description (str): A brief description of the unit type.
        created_at (datetime): The date and time when the unit type was created.
        updated_at (datetime): The date and time when the unit type was last updated.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the unit type, which is its name.
        """
        return self.name
    
class SwissStockHTMLContent(models.Model):
    """
    SwissStockHTMLContent model stores HTML content related to Swiss stocks.

    Attributes:
        html_content (str): The HTML content.
    """
    html_content = models.TextField()

    def __str__(self):
        """
        Returns the string representation of the SwissStockHTMLContent, which is its primary key.
        """
        return str(self.pk)
    
class AssetType(models.Model):
    """
    AssetType model represents a type of asset.

    Attributes:
        name (str): The name of the asset type.
        category (ForeignKey): The category the asset type belongs to.
        current_price (float): The current price of the asset type.
        description (str): A brief description of the asset type.
        created_at (datetime): The date and time when the asset type was created.
        updated_at (datetime): The date and time when the asset type was last updated.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_price = models.FloatField() 
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the asset type, which is its name.
        """
        return f"{self.name}"
    
class Account(models.Model):
    """
    Account model represents a financial account.

    Attributes:
        name (str): The name of the account.
        iban (str): The IBAN of the account.
        currency (ForeignKey): The currency of the account.
        description (str): A brief description of the account.
        created_at (datetime): The date and time when the account was created.
        updated_at (datetime): The date and time when the account was last updated.
    """
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=50, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the account, which is its name.
        """
        return self.name
    
class ExchangeRate(models.Model):
    """
    ExchangeRate model represents the exchange rate between two currencies.

    Attributes:
        from_currency_id (ForeignKey): The currency to convert from.
        to_currency_id (ForeignKey): The currency to convert to.
        rate (float): The exchange rate.
        rate_date (date): The date of the exchange rate.
        created_at (datetime): The date and time when the exchange rate was created.
        updated_at (datetime): The date and time when the exchange rate was last updated.
    """
    from_currency_id = models.ForeignKey(Currency, related_name='from_currency_id', on_delete=models.CASCADE)
    to_currency_id = models.ForeignKey(Currency, related_name='to_currency_id', on_delete=models.CASCADE)
    rate = models.FloatField()
    rate_date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Returns the string representation of the exchange rate, which is a combination of the from and to currency codes.
        """
        return  f"{self.from_currency_id} - {self.to_currency_id}"
    
class Asset(models.Model):
    """
    Asset model represents an asset.

    Attributes:
        account (ForeignKey): The account that holds the asset.
        asset_type (ForeignKey): The type of the asset.
        buy_date (date): The date the asset was bought.
        buy_unit_price (float): The price per unit at the time of purchase.
        currency (ForeignKey): The currency of the asset.
        number (float): The number of units of the asset.
        unit_type (ForeignKey): The unit type of the asset.
        created_at (datetime): The date and time when the asset was created.
        updated_at (datetime): The date and time when the asset was last updated.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    buy_date = models.DateField(null=True, blank=True)
    buy_unit_price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    number =  models.FloatField()
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    @property
    def current_price(self):
        """
        Returns the current price of the asset based on its type.
        """
        current_price = self.asset_type.current_price
        return  current_price
    
    @property
    def cost(self):
        """
        Returns the total cost of the asset (number of units multiplied by the buy unit price).
        """
        cost = self.number * self.buy_unit_price
        return  cost
    
    @property
    def instant_value(self):
        """
        Returns the instant value of the asset (number of units multiplied by the current price).
        """
        instant_value = self.number * self.current_price
        return  instant_value
    
    @property
    def profit_decoration(self):
        """
        Returns a string indicating whether the asset's profit is positive ('success') or negative ('danger').
        """
        if self.instant_value < self.cost:
            return 'danger'
        else:
            return 'success'
        
    @property
    def profit(self):
        profit = self.instant_value - self.cost                    
        return profit

    @property
    def percentage(self):
        try:
            percentage = ((self.instant_value / self.cost) - 1) *100
        except ZeroDivisionError:
            percentage = 0
        return percentage
    
    @property
    def calculated_parities(self):
        currencies = Currency.objects.all()
        calculated_parities = {}
        for currency in currencies:
            curr = Currency.objects.get(currency_code = currency)
            rate = ExchangeRate.objects.get(
                from_currency_id=self.currency.pk, 
                to_currency_id = curr.pk).rate
            calculated_parities[curr.currency_code] = rate * self.instant_value
        return calculated_parities
    
    def __str__(self):
        return str(self.asset_type)
    
class AssetTimeData(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.category.name}-{self.currency.currency_code}-{self.date}"

class DailySummary(models.Model):
    """
    DailySummary model stores the calculated parities for assets on a daily basis.

    Attributes:
        date (date): The date of the summary.
        currency (str): The currency code.
        is_liquid (bool): The liquidity status of the assets.
        total_value (float): The total calculated parity value.
    """
    date = models.DateField()
    currency = models.CharField(max_length=10)
    is_liquid = models.BooleanField(null=True)  # True, False, or None for all assets
    total_value = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.currency} - {'Liquid' if self.is_liquid else 'Non-Liquid' if self.is_liquid is not None else 'All'}"
    
