from . import views
from django.urls import path
# from django.contrib.auth.decorators import login_required

app_name = 'locapp'
urlpatterns = [
    # path('', views.soclogin),
    path('', views.DestinationView, name='dest'),
    # path('tourist/', views.TouristView, name='tourist'),
    path('logout/', views.logoutuser, name='logout'),
    path('loc_meta_detail/<int:pk>', views.loc_meta_view, name="loc_meta_detail")
]