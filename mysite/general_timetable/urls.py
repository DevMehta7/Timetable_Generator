from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('admin/', admin.site.urls),
    path('generate-time-table/', views.generate_time_table_page, name='generate_time_table'),
    path('view-time-table/', views.view_time_table_page, name='view_time_table'),
    path('test-ajax/', views.test_ajax),
    path('generate-time-table-api/', views.generate_time_table_api),

    # path('', views.home, name='home'),
    # path('tt/', views.main, name='main'),
    path('unallocate/', views.unalloc_func, name='unalloc_func'),
    path('unallocate/unallocate', views.unalloc_func, name='unalloc_func'),
    path('try/', views.try_sft, name='try_sft'),
]
