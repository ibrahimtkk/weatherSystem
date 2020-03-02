from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path(r'', login, name='login'),
    path(r'redirect/', paravanAjax, name='redirect'),

    ### Giris Kontrol
    path(r'giris_from_ajax/', loginFromAjax, name='loginFromAjax'),
    path(r'giris_to_ajax/', loginToAjax, name='loginToAjax'),
    path(r'paravanAjax/', paravanAjax, name='paravanAjax'),


    ### Menu 1
    path(r'sehir_ekle_from_ajax/', locationAddFromAjax, name='locationAddFromAjax'),
    path(r'sehir_ekle_to_ajax/', locationAddToAjax, name='locationAddToAjax'),

    path(r'sehir_sil_from_ajax/', locationRemoveFromAjax, name='locationRemoveFromAjax'),
    path(r'sehir_sil_to_ajax/', locationRemoveToAjax, name='locationRemoveToAjax'),

    path(r'sehir_guncelle_from_ajax/', locationUpdateFromAjax, name='locationUpdateFromAjax'),
    path(r'sehir_guncelle_to_ajax/', locationUpdateToAjax, name='locationUpdateToAjax'),

    path(r'sehir_listele_from_ajax/', locationListFromAjax, name='locationListFromAjax'),
    path(r'sehir_listele_to_ajax/', locationListToAjax, name='locationListToAjax'),




    ### Menu 3
    path(r'kullanici_ekle_from_ajax/', userAddFromAjax, name='userAddFromAjax'),
    path(r'kullanici_ekle_to_ajax/', userAddToAjax, name='userAddToAjax'),

    path(r'kullanici_sil_from_ajax/', locationRemoveFromAjax, name='userRemoveFromAjax'),
    path(r'kullanici_sil_to_ajax/', userRemoveToAjax, name='userRemoveToAjax'),

    path(r'kullanici_guncelle_from_ajax/', userUpdateFromAjax, name='userUpdateFromAjax'),
    path(r'kullanici_guncelle_to_ajax/', userUpdateToAjax, name='userUpdateToAjax'),

    path(r'kullanici_listele_from_ajax/', userListFromAjax, name='userListFromAjax'),
    path(r'kullanici_listele_to_ajax/', userListToAjax, name='userListToAjax'),




    ### Menu 4
    path(r'rapor_from_ajax/', reportFromAjax, name='reportFromAjax'),
    path(r'rapor_to_ajax/', reportToAjax, name='reportToAjax'),


    ### Menu 4
    path(r'rapor_standart_from_ajax/', reportStandartFromAjax, name='reportStandartFromAjax'),
    path(r'rapor_standart_to_ajax/', reportStandartToAjax, name='reportStandartToAjax'),



    ### Menu 2
    path(r'hava_durumu_from_ajax/', weatherFromAjax, name='weatherFromAjax'),
    path(r'hava_durumu_to_ajax/', weatherToAjax, name='weatherToAjax'),









]