from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Account, Currency, Asset, AssetType, UnitType, Category, AssetTimeData
from django.db.models import Q
from .forms import AssetCreateForm
from django.core.exceptions import ObjectDoesNotExist



class BaseTemplateObjects():   
   def __init__(self, web_page="", verb=""):
      self.objects = {
         "message" : f"{web_page} buradan {verb}",
         "time_slogan" : self.get_time_slogan(),
         "categories": self.get_categories(),
         "title":"Finansal Varlık Sistemi "
      }

   def get_categories(self, is_all=True, is_liquid=True):
      if is_all is True:
         return Category.objects.all().order_by('name')
      else:
         return Category.objects.filter(is_liquid=is_liquid).order_by('name')

   def get_time_slogan(self):
      now = datetime.now()
      if 0 <= now.hour <= 7:
         return "İyi Geceler"
      elif 7 <= now.hour <= 10:
         return "Günaydın"
      elif 10 <= now.hour <= 18:
         return "İyi Günler"
      elif 18 <= now.hour <= 22:
         return "İyi Akşamlar"
      elif 22 <= now.hour <= 23:
         return "İyi Geceler"
      else:
         return "İyi Geceler"
      
   def get_total_calculated_parities(self,assets):
      total_calculated_parities = {}
      
      for item in assets:       
         for currency, calculated_amount in item.calculated_parities.items():
            if currency not in total_calculated_parities:
               total_calculated_parities[currency] = 0.0
            total_calculated_parities[currency] += calculated_amount

      return total_calculated_parities
   
class PageObjects(BaseTemplateObjects):
   def __init__(self, web_page, verb):
      super().__init__(web_page, verb)
      self.objects['currencies'] = Currency.objects.all()

   def get_account_page_objects(self):
      self.objects['title'] += "| Hesaplar"
      self.objects['accounts'] = Account.objects.all().order_by('name')
      self.objects['accounts_count'] = Account.objects.all().count()
      return self.objects
   
   def alert_message(self,name, operation, alert_class):
      self.objects = self.get_account_page_objects()
      self.objects["form_message"] = f"{name} başarıyla {operation}"
      self.objects["alert_class"] = alert_class      
      return self.objects
   
   def get_asset_page_objects(self, category_id):
      
      self.objects['accounts'] = Account.objects.all().order_by('name')
      self.objects['assets'] = Asset.objects.filter(asset_type__category__pk = category_id).order_by('account','asset_type__name')
      self.objects['assets_count'] = Asset.objects.filter(asset_type__category__pk = category_id).count()
      asset_types = AssetType.objects.filter(category__pk = category_id).order_by('name').values()
      self.objects['asset_types'] =asset_types
      try:
         latest_asset_type = asset_types.latest('updated_at')
      except ObjectDoesNotExist:
         latest_asset_type = None
      try:
         self.objects['latest_asset_time'] = latest_asset_type.updated_at.strftime("%d.%m.%Y %H:%M")
      except AttributeError:
         self.objects['latest_asset_time'] = None
      self.objects['unit_types'] = UnitType.objects.all()
      self.objects['category'] = Category.objects.get(pk = category_id)
      self.objects['title'] += "| " + self.objects['category'].name + " Varlıkları"
      assets = self.objects['assets']
      self.objects['create_asset_form'] = AssetCreateForm(category_id=category_id)
      self.objects['update_asset_form'] = AssetCreateForm(category_id=category_id)
      self.objects['assetCRUD'] = True
      # total_cost = 0
      # for item in assets:
      #    total_cost += item.buy_unit_price * item.number
      
      # self.objects["total_cost"] = total_cost

      # total_instant_price = 0
      
      # for item in assets:
      #    total_instant_price += item.asset_type.current_price * item.number
      # self.objects["total_instant_price"] = total_instant_price
      
      # total_calculated_parities = {}
      
      # for item in assets:       
      #    for currency, calculated_amount in item.calculated_parities.items():
      #       if currency not in total_calculated_parities:
      #          total_calculated_parities[currency] = 0.0
      #       total_calculated_parities[currency] += calculated_amount

      self.objects["total_calculated_parities"] = self.get_total_calculated_parities(assets)   

      # net_profit = total_instant_price - total_cost
      # self.objects['net_profit'] = net_profit
      # try:
      #    net_percantage = ((total_instant_price / total_cost) - 1) *100
      # except ZeroDivisionError:
      #    net_percantage = 0
      # self.objects['net_percantage'] = f'% {net_percantage:.2f}'

      # if net_percantage < 0:
      #    self.objects['general_percantage_color'] = 'danger'
      #    self.objects['general_percantage_arrow'] = 'down'
      # else:
      #    self.objects['general_percantage_color'] = 'success'
      #    self.objects['general_percantage_arrow'] = 'up'
      return self.objects
   
   def summerized_asset_table(self, is_all, is_liquid):
      categories = self.get_categories(is_all=is_all, is_liquid=is_liquid)
      data = []
      totals = {'TRY': 0, 'EUR': 0, 'USD': 0, 'CHF': 0}
      for category in categories:         
         asset = Asset.objects.filter(asset_type__category__pk = category.id)
         if asset.exists():
            parities = self.get_total_calculated_parities(asset)
            data.append({
                  'name': category.name,
                  'parities': parities
               })
            # Sum up the totals for each currency
            for key in totals:
               totals[key] += parities.get(key, 0)
      return data, totals
   
   def create_doughnut_chart_data(self,  data):
      simplified_assets = [{'name': asset['name'], 'value': asset['parities']['TRY']} for asset in data]
      total_value = sum(asset['value'] for asset in simplified_assets)

      colors = [
            "#1F3BB3", "#05C3FB", "#34B1AA", "#F95F53", "#E29E09", "#51B1E1", "#E9E9E9",
            # Additional colors that complement the existing palette
            "#166D8B", "#0492C2", "#B15F34", "#C98B2F", "#B1D034", "#4E8AE6", "#8C52FF",
            "#FFC61E", "#FF7477", "#9EE09E", "#CC99C9", "#C390D4", "#A7D0CD", "#FFD3B4",
            "#DECBA4", "#FAD0C9", "#9C6D57", "#99B898", "#D1E8E4"
         ]
      
            
      doughnut_chart_data = []
      for asset, color in zip(simplified_assets, colors):
         doughnut_chart_data.append({
               'name': asset['name'],
               'value': asset['value'],
               'ratio': (asset['value'] / total_value) * 100,
               'color': color
         })

      return doughnut_chart_data
   
   def get_index_objects(self):
      self.objects['all_asset_count'] = Asset.objects.count()      
      self.objects['liquid_asset_count'] = Asset.objects.filter(asset_type__category__is_liquid=True).count()
      self.objects['non_liquid_asset_count'] = Asset.objects.filter(asset_type__category__is_liquid=False).count()

      self.objects['liquid_assets'] = Asset.objects.filter(asset_type__category__is_liquid=True).order_by('account','asset_type__name')
      self.objects["total_calculated_liquid_parities"] = self.get_total_calculated_parities(self.objects['liquid_assets'])
      
      self.objects['non_liquid_assets'] = Asset.objects.filter(asset_type__category__is_liquid=False).order_by('account','asset_type__name')
      self.objects["total_calculated_non_liquid_parities"] = self.get_total_calculated_parities(self.objects['non_liquid_assets'])
      
      self.objects['all_assets'] = Asset.objects.all().order_by('account','asset_type__name')
      self.objects["total_calculated_all_parities"] = self.get_total_calculated_parities(self.objects['all_assets'])

      liquid_data, liquid_totals = self.summerized_asset_table(is_all=False, is_liquid=True)
      self.objects["summerized_liquid_asset_table"] = liquid_data
      self.objects["liquid_totals"] = liquid_totals
      self.objects["liquid_doughnut_chart_data"] = self.create_doughnut_chart_data(liquid_data)

      non_liquid_data, non_liquid_totals = self.summerized_asset_table(is_all=False, is_liquid=False)
      self.objects["summerized_non_liquid_asset_table"] = non_liquid_data
      self.objects["non_liquid_totals"] = non_liquid_totals
      self.objects["non_liquid_doughnut_chart_data"] = self.create_doughnut_chart_data(non_liquid_data)

      all_data, all_totals = self.summerized_asset_table(is_all=True, is_liquid=True)
      self.objects["summerized_all_asset_table"] = all_data
      self.objects["all_totals"] = all_totals
      self.objects["all_doughnut_chart_data"] = self.create_doughnut_chart_data(all_data)


      
      return self.objects
   
   def get_currency_data(self):
      return self.objects
   
def prepare_doughnut_chart_data(request, data_type):
    
   page_objects = PageObjects(f"", "")
   objects = page_objects.get_index_objects()
   if data_type == "liquid_data":
      asset_data = objects["liquid_doughnut_chart_data"]
   elif data_type == "non_liquid_data":
      asset_data = objects["non_liquid_doughnut_chart_data"]
   elif data_type == "all_data":
      asset_data = objects["all_doughnut_chart_data"]
   return JsonResponse({
      'labels': [asset['name'] for asset in asset_data],
      'data': [asset['ratio'] for asset in asset_data],
      'backgroundColor': [asset['color'] for asset in asset_data],
      'borderColor': [asset['color'] for asset in asset_data],
   })

def get_performance_line_data(request, category_id, currency_id, time):
    category_id = int(category_id)
    currency_id = int(currency_id)

    if time == 'daily':
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)
        data = AssetTimeData.objects.filter(category_id=category_id, currency_id=currency_id, date__range=[start_date, end_date]).order_by('date')
        labels = [item.date.strftime('%Y-%m-%d') for item in data]
        values = [item.price for item in data]

    elif time == 'weekly':
        end_date = datetime.today()
        start_date = end_date - timedelta(weeks=30)
        data = AssetTimeData.objects.filter(category_id=category_id, currency_id=currency_id, date__range=[start_date, end_date], date__week_day=2).order_by('date')
        labels = [item.date.strftime('%Y-%W') for item in data]
        values = [item.price for item in data]

    elif time == 'monthly':
        raw_data = AssetTimeData.objects.raw('''
            SELECT id, category_id, currency_id, date, price
            FROM assets_assettimedata
            WHERE (category_id, currency_id, date) IN (
                SELECT category_id, currency_id, MAX(date) as date
                FROM assets_assettimedata
                WHERE category_id = %s AND currency_id = %s
                GROUP BY category_id, currency_id, strftime('%%Y-%%m', date)
            )
            ORDER BY date DESC
            LIMIT 30
        ''', [category_id, currency_id])
        
        month_names_tr = ["Ocak", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
        labels = [month_names_tr[item.date.month - 1] for item in raw_data]
        values = [item.price for item in raw_data]

    else:
        return JsonResponse({'error': 'Invalid time parameter'}, status=400)

    return JsonResponse({
        'labels': labels,
        'values': values
    })




def index(request):
   page_objects = PageObjects("Toplam varlıklarınıza", "bakabilirsiniz.")
   objects = page_objects.get_index_objects()
   return render(request, 'assets/index.html', objects)


def accounts(request):
   page_objects = PageObjects("Hesaplarınızı", "yönetebilirsiniz.")
   objects = page_objects.get_account_page_objects()

   if request.method == "POST":
      operation = request.POST.get('operation', False)

      if operation == "insertAccount":
         name = request.POST["name"]
         iban = request.POST["iban"]
         description = request.POST["description"]
         currency_id = request.POST["currency"]
         currency = Currency.objects.get(pk=currency_id)
         insert = Account(name=name, iban=iban, description=description, currency=currency)
         insert.save()
         objects = page_objects.alert_message(name, "kaydedildi", "success")
         return render(request, 'assets/accounts.html', objects)
      elif operation == "deleteAccount":
         deleteid = request.POST["deleteid"]
         delete =  get_object_or_404(Account, pk=deleteid)
         name = delete.name
         delete.delete()
         objects = page_objects.alert_message(name, "silindi", "danger")
         return render(request, 'assets/accounts.html', objects)
      elif operation == "updateAccount":
         pk = request.POST["pk"]
         name = request.POST["name"]
         iban = request.POST["iban"]
         description = request.POST["description"]
         currency_id = request.POST["currency"]
         currency = get_object_or_404(Currency, pk=currency_id)
         update_account = get_object_or_404(Account, pk=pk)
         update_account.name = name
         update_account.iban = iban
         update_account.description = description
         update_account.currency = currency
         update_account.save()
         objects = page_objects.alert_message(name, "güncellendi", "success")
         return render(request, 'assets/accounts.html', objects)      

   return render(request, 'assets/accounts.html', objects)

def asset(request, category_id):
   category = get_object_or_404(Category, pk=category_id)
   page_objects = PageObjects(f"{category.name} varlıklarınızı", "yönetebilirsiniz")
   objects = page_objects.get_asset_page_objects(category_id)         
   

   if request.method == "POST":
      operation = request.POST.get('operation', False)

      if operation == "delete":
         deleteid = request.POST["deleteid"]
         delete = get_object_or_404(Asset, pk=deleteid)
         asset_name = delete.asset_type.name
         delete.delete()
         objects = page_objects.get_asset_page_objects(category_id)
         objects = page_objects.alert_message(asset_name, "silindi", "danger")         
         objects['assets_count'] = Asset.objects.filter(asset_type__category__pk = category_id).count()
         return render(request, 'assets/asset.html', objects)
      if operation == "insert":
         form = AssetCreateForm(request.POST, category_id=category.id)
         print(request.POST)
         if request.method == 'POST':
            form = AssetCreateForm(request.POST, category_id=category.id)
            if form.is_valid():
               asset = form.save()
               asset_type = asset.asset_type
               objects = page_objects.get_asset_page_objects(category_id)
               objects = page_objects.alert_message(asset_type, "kaydedildi", "success")
               return render(request, 'assets/asset.html', objects)
            
      if operation == "update":
         pk = request.POST["update_asset_id"]
         asset = get_object_or_404(Asset, pk=pk)
         form = AssetCreateForm(request.POST, instance=asset, category_id=category.id)
         print(request.POST)
         if form.is_valid():
            asset = form.save()
            asset_type = asset.asset_type
            objects = page_objects.get_asset_page_objects(category_id)
            objects = page_objects.alert_message(asset_type, "güncellendi", "success")
            return render(request, 'assets/asset.html', objects)
      if operation == "insert_asset_type":
         name = request.POST["name"]
         category = Category.objects.get(pk=category_id)
         current_price = request.POST["current_price"]
         description = request.POST["description"]
         asset_type = AssetType(name=name,
                                category=category,
                                current_price = current_price,
                                description=description
                                )
         asset_type.save()
         objects = page_objects.get_asset_page_objects(category_id)
         objects = page_objects.alert_message(asset_type, "eklendi", "success")
      if operation == "update_asset_type":
         asset_type_id = request.POST["asset_type"]
         update_asset_type = AssetType.objects.get(pk=asset_type_id)
         update_asset_type.description = request.POST["description"]
         update_asset_type.current_price = request.POST["current_price"]
         update_asset_type.save()
         objects = page_objects.get_asset_page_objects(category_id)
         objects = page_objects.alert_message(update_asset_type.name, "güncellendi", "success")
      if operation == "delete_asset_type":
         asset_type_id = request.POST["asset_type_id"]
         delete_asset_type = AssetType.objects.get(pk=asset_type_id)
         name_asset_type = delete_asset_type.name
         delete_asset_type.delete()
         objects = page_objects.get_asset_page_objects(category_id)
         objects = page_objects.alert_message(name_asset_type, "silindi", "danger")
   else:
      return render(request, 'assets/asset.html', objects)   
   
