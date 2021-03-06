"""from django.conf.urls import url
from .views import *
from home.views import *
import home

app_name = 'analizz'

urlpatterns = [

    url(r'^', home.views.home_to_aylikHiz, name='analiz_home'),

    #url(r'^grafikler/', analiz_grafikler, name='analiz_grafikler'),


    # urlsi analiz/grafikler olan sayfa icin home_to_tumGun fonku calistir.
    url(r'^grafikler/', home.views.home_to_tumGun, name='analiz_grafikler'),

    url(r'^renkliHarita/', home.views.home_to_renkliHarita, name='analiz_renkliHarita'),

    url(r'^aylikGrafik/', home.views.home_to_aylikHiz, name='analiz_aylikHiz'),

    url(r'^havaDurumuEtkisi/', home.views.home_to_havaDurumu, name='analiz_havaDurumu'),

]
"""

from django.conf.urls import url
from .views import *
from home.views import *

app_name = 'analizz'

urlpatterns = [

    url(r'^$', analiz_home, name='analiz_home'),

    #url(r'^grafikler/', analiz_grafikler, name='analiz_grafikler'),


    # urlsi analiz/grafikler olan sayfa icin home_to_tumGun fonku calistir.
    url(r'^grafikler/', home_to_tumGun, name='analiz_grafikler'),

    url(r'^renkliHarita/', home_to_renkliHarita, name='analiz_renkliHarita'),

    url(r'^aylikGrafik/', home_to_aylikHiz, name='analiz_aylikHiz'),

    url(r'^havaDurumuEtkisi/', home_to_havaDurumu, name='analiz_havaDurumu'),

    url(r'^aylarGunler/', aylar_gunler, name='analiz_aylarGunler'),

    url(r'^djangoyaGonder/', djangoyaGonder, name='analiz_djangoyaGonder'),

    url(r'^djangodanAl/', djangodanAl, name='analiz_djangodanAl'),

    url(r'^aylikKoorGonder/', aylikKoorGonder, name='analiz_djangodanAl'),

    url(r'^aylikAlertAl/', aylikAlertAl, name='analiz_djangodanAl'),

    url(r'^djangoyaGonderHavaDurumu/', djangoyaGonderHavaDurumu, name='analiz_djangoyaGonderHavaDurumu'),

    url(r'^djangodanAlHavaDurumu/', djangodanAlHavaDurumu, name='analiz_djangodanAlHavaDurumu'),

    url(r'^djangodanAlRenkli/', djangodanAlRenkli, name='analiz_djangodanAlRenkli'),

    url(r'^djangoyaGonderAylik/', djangoyaGonderAylik, name='analiz_djangoyaGonderAylik'),

    url(r'^djangodanAlAylik/', djangodanAlAylik, name='analiz_djangodanAlAylik'),

    url(r'^djangoyaGonderTumGun/', djangoyaGonderTumGun, name='analiz_djangoyaGonderAylik'),

    url(r'^djangodanAlTumGun/', djangodanAlTumGun, name='analiz_djangodanAlAylik'),

]