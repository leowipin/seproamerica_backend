from django.urls import path
from equipment.views import EquipmentView, PhoneView, PhoneListView, AmmoView, AmmoListView, WeaponView, WeaponListView, LockView, LockListView, VehicleView, VehicleListView

urlpatterns = [
    path('equipment/', EquipmentView.as_view(), name='equipment'),
    path('phone/', PhoneView.as_view(), name='phone'),
    path('phoneList/', PhoneListView.as_view(), name='phonelist'),
    path('ammo/', AmmoView.as_view(), name='ammo'),
    path('ammoList/', AmmoListView.as_view(), name='ammolist'),
    path('weapon/', WeaponView.as_view(), name='weapon'),
    path('weaponList/', WeaponListView.as_view(), name='weaponlist'),
    path('lock/', LockView.as_view(), name='lock'),
    path('lockList/', LockListView.as_view(), name='locklist'),
    path('vehicle/', VehicleView.as_view(), name='vehicle'),
    path('vehicleList/', VehicleListView.as_view(), name='vehicleList'),
]