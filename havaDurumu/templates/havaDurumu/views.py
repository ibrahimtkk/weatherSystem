from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import json
import random
from django.shortcuts import render, HttpResponse, get_object_or_404
import pyodbc
import time
from pykml import parser
import pickle
from stdevi.kodlar import stdevi
from stdevi.kodlar import SQLeBaglanKarma as sql
from analizz.kodlar import mypythoncode as mypythoncodeAnaliz
from analizz.kodlar import SQLeBaglanKarma as sqlAnaliz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


def home_view(request):
    print("home_view'dayiz")

    global cursor
    global cnxn
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "SERVER=HALIT;"
                          "Database=FusedData-2016-2017-2018;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    #if request.is_ajax():
    #    gonder = ['ali', 'veli']
    #    data = json.dumps(gonder)
    #    #data = {'message': '{} added'.format(request.POST.get('data'))}
    #    return HttpResponse(data, content_type='application/json')
    #if request.method=="POST":
    #    get_value = request.GET
    #    data = {}
    #    data['data'] = 'you made a request'
    #    print(get_value)
    #    print('yes ajax',request)
    #    return HttpResponse(json.dumps(data), content_type="application/json")
    #elif request.method=="GET":
    #    print(request.GET)
    #    print('no ajax', request)
    print("-------------------Veritabanına bağlandı")

    #vSegDir = request.POST.get('vSegDirAylik')
    #print(type(vSegDir))
    #if( vSegDir is None ):
    #    print("None")
    #    pass
    #else:
    #    if ( int(vSegDir)==0 ):
    #        print("vSegDir=0")
    #        return render(request, 'analizz/aylikGrafik.html', {'sifirMi': 'sifir',})
    #    elif ( int(vSegDir)==1 ):
    #        print("vSegDir=0")
    #        return JsonResponse({'sifirMi':'bir'})
    #        #return render(request, 'home.html', {'sifirMi': 'bir',})


    yagmurluList = ['10/25/2017', '10/26/2017']
    return render(request, 'home.html', {'yagmurluList': yagmurluList})


def home_to_stdevi(request):
    start = time.time()
    print("home to stdevideyiz yani artik harita gosterilecek")
    vSegDir = request.POST.get('vSegDirStandartSapma')
    tarih = request.POST.get('datepicker5')
    tarihParcalanmisListe = tarih.split('/')
    year = tarihParcalanmisListe[2]
    # yil = request.POST.get('year')
    month = tarihParcalanmisListe[1].replace('0', '')
    # ay = request.POST.get('month')
    day = tarihParcalanmisListe[0].replace('0', '')
    # ayinKaci = request.POST.get('day')
    vSegDir = request.POST.get('vSegDirStandartSapma')
    print("\n\n--------: ", vSegDir, type(tarih), "\n\n")
    liste = tarih.split('/')
    print(liste)

    stdevi.degerleriAl(request, cursor, cnxn, 'home_to_stdevi')

    ### inputFile: KML dosyasi
    ### IDList[]: vSegID'lerin eklenecegi liste
    ### coordinateList[]: Koordinatlarin eklenecegi liste ( icinde x ve y koordinati virgulle ayrilmis olarak bulunuyor)
    print("/////bitti")
    inputFile = "C:\\Users\\ASUS\\Desktop\\trafSite\\docu.kml"
    IDList = []
    coordinateList = []
    stdeviAdres = "C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\stdevi\\"
    siraliStandartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-SiraliStandartSapma.csv".format(year, month, day, vSegDir)
    acikAdres = 'C:\\Users\\ASUS\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
    havaDurumuAdres = 'C:\\Users\\ASUS\\Desktop\\trafSite\\adresler\\havaDurumuAdres.txt'

    ### standart sapma miktarlarinin sirali listesi.
    ### sensorNo, sapmaMiktari
    with open(siraliStandartSapmaAdres, 'rb') as fp:
        siraliStandartSapmaListesi = pickle.load(fp)

    ### her bir sensorun acik adresini verir.
    ### vSegID, yKoor, xKoor, ?, acikAdres
    with open(acikAdres, 'rb') as fp:
        acikAdresListesi = pickle.load(fp)

    ### her bir sensore dusen en yakin hava durumu sensorunu verir.
    with open(havaDurumuAdres, 'rb') as fp:
        havaDurumuList = pickle.load(fp)


    ### Acik adres listesindeki sensorleri ayri bir listeye ekliyoruz, boylece index islemi daha rahat yapilabilecek.
    acikAdresIDList = []
    for adres in acikAdresListesi:
        acikAdresIDList.append(adres[0])

    ### HTML'e gonderilecek liste
    ### Bazi sensorler bulunamadigindan ValueError veriyor, ona tekrardan bak
    returnListe = []
    for i in range(20):
        vSegID = siraliStandartSapmaListesi[i][0]
        try:
            acikAdresIDIndex = acikAdresIDList.index(vSegID)
            yKoor = acikAdresListesi[acikAdresIDIndex][1]
            xKoor = acikAdresListesi[acikAdresIDIndex][2]
            standartSapmaSirasi = i
            standartSapmaMiktari = siraliStandartSapmaListesi[i][1]
            acikAdres = acikAdresListesi[acikAdresIDIndex][4]
            innerReturnList = [vSegID, yKoor, xKoor, standartSapmaSirasi, standartSapmaMiktari, acikAdres]
            returnListe.append(innerReturnList)
        except ValueError:
            pass


    returnListe100luk = []
    for i in range(100):
        vSegID = siraliStandartSapmaListesi[i][0]
        try:
            acikAdresIDIndex = acikAdresIDList.index(vSegID)
            yKoor = acikAdresListesi[acikAdresIDIndex][1]
            xKoor = acikAdresListesi[acikAdresIDIndex][2]
            standartSapmaSirasi = i
            standartSapmaMiktari = siraliStandartSapmaListesi[i][1]
            acikAdres = acikAdresListesi[acikAdresIDIndex][4]
            acikAdresList = acikAdres.split(',')
            innerReturnList = [vSegID, yKoor, xKoor, standartSapmaSirasi+1, round(standartSapmaMiktari, 4), acikAdresList[-5]]
            returnListe100luk.append(innerReturnList)
        except ValueError:
            pass

    return render(request, 'stdevi/harita.html', {'allOf': returnListe,
                                                    'alll': returnListe100luk,
                                                })

def strKoordinatDondur(x, y):
    koor = "{}, {}".format(str(x), str(y) )
    return koor

def home_to_tumGun(request):
    start = time.time()

    basSaat = request.POST.get('datetimepicker7')
    bitSaat = request.POST.get('datetimepicker8')
    basSaatList = basSaat.split(':')
    bitSaatList = bitSaat.split(':')
    basSaatSaat = basSaatList[0]
    basSaatDakika = basSaatList[1]
    bitSaatSaat = bitSaatList[0]
    bitSaatDakika = bitSaatList[1]
    kDegeri = request.POST.get('KTumGun')


    secilenX = request.POST.get('lat')
    secilenY = request.POST.get('lng')
    enYakinSensorID = mypythoncodeAnaliz.haritadanEnYakinSensorBul(request)
    print(enYakinSensorID)
    vSegID = enYakinSensorID
    #vSegID = request.POST.get('vSegIDTumGun')
    vSegDir = request.POST.get('vSegDirTumGun')
    #tarih = request.POST.get('datepicker1')

    mypythoncodeAnaliz.degerleriAl(request, cursor, vSegID,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    end = time.time()
    tarihParcalanacakString = request.POST.get('datepicker1')
    #koordinatlar = request.POST.get('lat') + request.POST.get('lng')
    #print("***************koordinatlar: ", koordinatlar)
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    #vSegDir = request.POST.get('vSegDirTumGun')
    #vSegID = request.POST.get('vSegIDTumGun')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1]
    ayinKaci = tarihParcalanmisListe[0]
    #print("ay: ", ay)
    if (ay[0] == "0"):
        ay = ay.replace("0", "")
    if (ayinKaci[0] == "0"):
        ayinKaci = ayinKaci.replace("0", "")
    ayinKaci = tarihParcalanmisListe[0]
    resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" + str(vSegID) + "-" + vSegDir + "-" + basSaatSaat + "." + basSaatDakika + "-" + bitSaatSaat + "." + bitSaatDakika + ".png"
    #resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" +"-" + ".png"
    #print("resimBilgisi: ", resimBilgisi, sep="")
    #mypythoncodeAnaliz.degerleriAl(request, cursor)
    return render(request, 'analizz/grafik.html', {'resimIsmi': resimBilgisi})

def home_to_renkliHarita(request):
    start = time.time()
    ### siraliKoorVeHiz = [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
    siraliKoorVeHiz = stdevi.basBitKoorRenkKodu(request, cursor)
    end = time.time()
    print("siraliKoorVeHiz: ", end-start)
    global uzunluk
    uzunluk = len(siraliKoorVeHiz)
    print("-*/-*/-*/-*/*-/uzunluk: ", uzunluk)
    return render(request, 'analizz/renkliHarita.html', {'siraliKoorVeHiz': siraliKoorVeHiz,
                                                        'uzunluk': uzunluk})

def home_to_tahmin(request):
    vSegDir = request.POST.get('vSegDirTahmin')
    vSegID = request.POST.get('vSegIDTahmin')
    # tarih = tahmin edilecek tarih
    tarih = request.POST.get('tarihTahmin')
    k = request.POST.get('KTahmin')

    siraliKoorVeHizTahmin = stdevi.tarihIcinOnTemizlik(request, cursor)

    return render(request, 'analizz/renkliHarita.html', {'siraliKoorVeHiz': siraliKoorVeHizTahmin})


def home_to_aylikHiz(request):
    print("----------------------------------------")
    acikAdresDosyaYolu = 'C:\\Users\\ASUS\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
    lat = request.POST.get('latAylik')
    lng = request.POST.get('lngAylik')
    vSegDir = request.POST.get('vSegDirAylik')
    check = request.POST.getlist('checksAylar[]')
    print("---------Kontrol: ", check, len(check))
    resimAdresi, lat, lng, vSegID = mypythoncodeAnaliz.aylikOrtHizBul(cursor, lat, lng, vSegDir, check)
    if (resimAdresi=='error'):
        print("errorda")
        #messages.info(request, 'Your password has been changed successfully!')
        #return HttpResponseRedirect('')
        return render(request, 'analizz/aylikGrafik.html', 
            {'resimAdresi': resimAdresi,
            })
    #resimAdresi = 'C:\\Users\\ASUS\\Desktop\\trafSite\\static\\images\\aylik15DakikalikHızOrtCizgiGrafigi.png'
    else:
        print("errorda değil")
        with open(acikAdresDosyaYolu, 'rb') as fp:
            acikAdresListesi = pickle.load(fp)
        acikAdresIDList = []
        for adres in acikAdresListesi:
            acikAdresIDList.append(adres[0])
        indexx = acikAdresIDList.index(vSegID)
        acikAdres = acikAdresListesi[indexx][4]
        return render(request, 'analizz/aylikGrafik.html', 
            {'resimAdresi': resimAdresi,
                'lat': lat,
                'lng': lng,
                'acikAdres': acikAdres,
            })

# js tarafindan djangoya bilgi geldi
def aylikOrtKoorGonder(request):
    print("1")
    if request.is_ajax() and request.POST:
        global jsyeGonderilecekAylik, gelenVeri
        gelenVeri = request.POST.get("data")

        lat, lng, vSegDir = gelenVeri.split(',')[0], gelenVeri.split(',')[1], gelenVeri.split(',')[2]
        resimAdresi, lat, lng, vSegID = mypythoncodeAnaliz.aylikOrtHizBul(cursor, lat, lng, vSegDir)
        jsyeGonderilecekAylik = resimAdresi
        print("+++++++: ", jsyeGonderilecekAylik)
        gonder = ['ali', 'veli']
        data = json.dumps(jsyeGonderilecekAylik)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

# djangodan jsye gonderilecek bilgi
def aylikOrtAlertAl(request):
    print("2")
    if request.is_ajax():
        resimAdresi = jsyeGonderilecekAylik
        data = json.dumps(resimAdresi)
        return HttpResponse(data, content_type='application/json')



# js tarafindan djangoya bilgi geldi
def djangoyaGonder(request):
    if request.is_ajax() and request.POST:
        global jsyeGonderilecek, gelenVeri
        gelenVeri = request.POST.get("data")
        #jsyeGonderilecek = gelenVeri
        lat, lng = gelenVeri.split(',')[0], gelenVeri.split(',')[1]
        enYakinSensorID, enYakinSensorY, enYakinSensorX = mypythoncodeAnaliz.haritadanEnYakinSensorBulLatLong(lat, lng)
        jsyeGonderilecek = mypythoncodeAnaliz.koordanEnYakinHavaDurumuSemtiBulMy(lat, lng)
        print("+++++++: ", jsyeGonderilecek)
        gonder = ['ali', 'veli']
        data = json.dumps(jsyeGonderilecek)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

# djangodan jsye gonderilecek bilgi
def djangodanAl(request):
    if request.is_ajax():
        semt = jsyeGonderilecek
        print("ilaksflasdfalkkjalskdjf: ", semt)
        global havaOlayliGunler
        global distinctHavaOlayiYasananDegerler
        global ufakYagisListListesi
        havaOlayliGunler = []
        distinctHavaOlayiYasananDegerler, ufakYagisListListesi = mypythoncodeAnaliz.havaDurumuAjax(cursor, semt)
        for innerList in distinctHavaOlayiYasananDegerler:
            string = ''
            yil, ay, gun = int(innerList[2]), int(innerList[3]), int(innerList[4])
            string = string + str(ay)+ '/'+ str(gun)+'/'+str(yil)
            havaOlayliGunler.append(string)
        yagmurluList = ['10/11/2017', '10/10/2017']
        data = json.dumps(havaOlayliGunler)
        return HttpResponse(data, content_type='application/json')

# js tarafindan djangoya bilgi geldi
def djangoyaGonderTumGun(request):
    print("111111111111djangoyaGonderTumGun")
    if request.is_ajax() and request.POST:
        global jsyeGonderilecekTumGun, gelenVeriTumGun
        gelenVeriTumGun = request.POST.get("data")
        lat, lng, vSegDir, tarih = gelenVeriTumGun.split(',')[0], gelenVeriTumGun.split(',')[1], str(gelenVeriTumGun.split(',')[2]), gelenVeriTumGun.split(',')[3]
        enYakinSensorID = str(mypythoncodeAnaliz.haritadanEnYakinSensorBulLatLong(lat, lng)[0])
        print("------------------: ", enYakinSensorID)
        gun, ay, yil = str(tarih.split('/')[0]), str(tarih.split('/')[1]), str(tarih.split('/')[2])
        if int(gun)<10:
            gun = gun.replace('0', '')
        if int(ay)<10:
            ay = ay.replace('0', '')
        dosyaYolu = 'C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\analiz\\SensorDolulukOranlari\\' + yil + '-' + ay + '-' + vSegDir + '.csv'
        with open(dosyaYolu) as fp:
            satir = fp.readlines()
        satir = [x.strip() for x in satir]
        var = 0
        for sat in satir:
            #print("sat", sat)
            sat = sat.split(';')
            if enYakinSensorID == sat[0]:
                print(enYakinSensorID, sat[0], gun, sat[1])
                if gun == sat[1]:
                    print("kaç acaba", sat[2])
                    if int(sat[2]) < 60:
                        print("altmışın altı")
                        var = 1
                        jsyeGonderilecekTumGun = 'error'
                    else:
                        var = 1
                        jsyeGonderilecekTumGun = 'errorDegil'
        if var == 0:
            jsyeGonderilecekTumGun = 'error'
        #print("////////////////:", sensorList)
    
        #if enYakinSensorID in sensorList[0]:
        #    vDir = 0
        #else:
        #    vDir = 1
        #print("3333333333333333333: ", type(vDir), type(vSegDir), vDir, vSegDir)
        #if vDir != vSegDir:
        #    print("farklısı")
        #    jsyeGonderilecekTumGun = 'error'
        #elif vDir == vSegDir:
        #    jsyeGonderilecekTumGun = 'errorDegil'
        #    print("aynısı")

        data = json.dumps(jsyeGonderilecekTumGun)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

# djangodan jsye gonderilecek bilgi
def djangodanAlTumGun(request):
    print("2222222222222djangodanAlTumGun")
    if request.is_ajax():
        resimAdresi = jsyeGonderilecekTumGun
        data = json.dumps(resimAdresi)
        return HttpResponse(data, content_type='application/json')

def aylikKoorGonder(request):
    print("1")
    if request.is_ajax() and request.POST:
        global jsyeGonderilecekAylik, gelenVeri
        gelenVeri = request.POST.get("data")
        checks = request.POST.getlist('checks[]')
        lat, lng, vSegDir = gelenVeri.split(',')[0], gelenVeri.split(',')[1], gelenVeri.split(',')[2]
        resimAdresi, lat, lng, vSegID = mypythoncodeAnaliz.aylikOrtHizBul(cursor, lat, lng, vSegDir, checks)
        jsyeGonderilecekAylik = resimAdresi
        print("+++++++: ", jsyeGonderilecekAylik)
        gonder = ['ali', 'veli']
        data = json.dumps(jsyeGonderilecekAylik)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

# js tarafindan djangoya bilgi geldi
def djangoyaGonderAylik(request):
    if request.is_ajax() and request.POST:
        print('---------djangoyaGonderAylik: ',request)
        gonder = ['40']
        data = json.dumps(gonder)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

def djangodanAlAylik(request):
    if request.is_ajax():
        havaOlayliGunler = {'foo': 3}
        #havaOlayliGunler = 60
        data = json.dumps(havaOlayliGunler)
        print("+++++++++++djangodanAlAylik:", data)
        return HttpResponse(data, content_type='application/json')
        #return JsonResponse(data)
    else:
        print("****ajax değil")

# djangodan jsye gonderilecek bilgi
def aylikAlertAl(request):
    print("2")
    if request.is_ajax():
        resimAdresi = jsyeGonderilecekAylik
        data = json.dumps(resimAdresi)
        return HttpResponse(data, content_type='application/json')

def home_to_havaDurumu(request):
    resimAdresi = mypythoncodeAnaliz.havaDurumu(request, cursor, ufakYagisListListesi, havaOlayliGunler)
    print("/////// resimAdresiCikardi")
    #djangodanAlHavaDurumu(request)
    print("/////// djangodanAlHavaDurumu")
    time.sleep(2)
    #cursor.close()
    #cnxn.close()
    return render(request, 'analizz/havaDurumu.html', {'resimAdresi': resimAdresi})

# js tarafindan djangoya bilgi geldi
def djangoyaGonderHavaDurumu(request):
    if request.is_ajax() and request.POST:
        print('---------djangoyaGonderHavaDurumu: ',request)
        gonder = ['40']
        data = json.dumps(gonder)
        #data = {'message': '{} added'.format(request.POST.get('data'))}
        return HttpResponse(data, content_type='application/json')

def djangodanAlHavaDurumu(request):
    if request.is_ajax():
        havaOlayliGunler = {'foo': 3}
        #havaOlayliGunler = 60
        data = json.dumps(havaOlayliGunler)
        print("+++++++++++djangodanAlHavaDurumu:", data)
        return HttpResponse(data, content_type='application/json')
        #return JsonResponse(data)
    else:
        print("**********ajax değil")


def djangodanAlRenkli(request):
    if request.is_ajax():
        data = json.dumps(uzunluk)
        return HttpResponse(data, content_type='application/json')

def aylar_gunler(request):
    resimAdresi = []
    resimAdresi = mypythoncodeAnaliz.aylarGunler(request, cursor)
    return render(request, 'analizz/aylarGunler.html', {'resimAdresi': resimAdresi})