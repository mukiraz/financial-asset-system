from django.urls import path
from . import views

urlpatterns=[	
	path('', views.index, name = 'index'),
    path('accounts', views.accounts, name = 'accounts'),
    path('asset/<int:category_id>', views.asset, name = 'asset'),
    path('asset/doughnut_chart_data/<str:data_type>', views.prepare_doughnut_chart_data, name="doughnut_chart_data"),
    path('asset/get_performance_line_data/<int:category_id>/<int:currency_id>/<str:time>/', views.get_performance_line_data, name='get_performance_line_data')
]
