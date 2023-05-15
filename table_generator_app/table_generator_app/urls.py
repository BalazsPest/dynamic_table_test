"""
URL configuration for table_generator_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from table_generator import views


router = routers.DefaultRouter()



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/table', views.GenerateDynamicTable.as_view(), name='generate_dynamic_table'),
    path('api/table/<int:id>', views.UpdateDynamicTable.as_view(), name='update_dynamic_table'),
    path('api/table/<int:id>/row', views.AddDynamicRow.as_view(), name='add_dynamic_row'),
    path('api/table/<int:id>/rows', views.GetDynamicRows.as_view(), name='get_dynamic_rows'),

]
