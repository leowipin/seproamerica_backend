from django.urls import path
from equipment.views import EquipmentView, PhoneView, PhoneListView, AmmoView, AmmoListView, WeaponView, WeaponListView, LockView, LockListView, VehicleView, VehicleListView, CategoryView, ColorView, BrandVehicleView, EngineView, BrandPhoneView, BrandWeaponView, WeaponTypeView

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
    path('category/', CategoryView.as_view(), name='category'),
    path('color/', ColorView.as_view(), name='color'),
    path('brandVehicle/', BrandVehicleView.as_view(), name='brandvehicle'),
    path('engine/', EngineView.as_view(), name='engine'),
    path('brandPhone/', BrandPhoneView.as_view(), name='brandphone'),
    path('brandWeapon/', BrandWeaponView.as_view(), name='brandweapon'),
    path('weaponTypes/', WeaponTypeView.as_view(), name='weapontypes'),
]