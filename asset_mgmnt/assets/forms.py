from django import forms
from assets.models import Asset, AssetType, Account

class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('account', 
                  'asset_type', 
                  'buy_date', 
                  'buy_unit_price', 
                  'currency', 
                  'number',
                  'unit_type')
        labels = {
            'account': 'Hesap',
            'asset_type': 'Varlık Türü',
            'buy_date': 'Alım Tarihi',
            'buy_unit_price': 'Birim Maliyet',
            'currency': 'Para Birimi',
            'number': 'Adet/Gram/Nakit',
            'unit_type': 'Birim',
        }
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select text-dark', 'id': 'asset_account'}),
            'asset_type': forms.Select(attrs={'class': 'form-select text-dark', 'id': 'asset_asset_type'}),
            'buy_date': forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'asset_buy_date','type': 'date'}),
            'buy_unit_price': forms.NumberInput(attrs={'class': 'form-control unit-price', 'id': 'asset_buy_unit_price', 'min': '0', 'step': 'any'}),
            'currency': forms.Select(attrs={'class': 'form-select text-dark', 'id': 'asset_currency'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'id': 'asset_number', 'min': '1', 'step': 'any'}),
            'unit_type': forms.Select(attrs={'class': 'form-select text-dark cash-unit', 'id': 'asset_unit_type'}),
        }

    def __init__(self, *args, **kwargs):
        category_id = kwargs.pop('category_id', None)
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.all().order_by('name')
        if category_id:
            self.fields['asset_type'].queryset = AssetType.objects.filter(category_id=category_id).order_by('name')


