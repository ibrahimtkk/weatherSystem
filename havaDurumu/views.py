from django.shortcuts import render
from django.http import HttpResponseRedirect
from geopy.geocoders import Nominatim
import sqlite3 as sql
from django.views.decorators.csrf import  csrf_protect
from django.http import HttpResponse
import json, os, time, datetime, urllib.request


def login(request):
	global loginID
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()
	imUser.execute("CREATE TABLE IF NOT EXISTS Users (username, password, userID)")
	imUser.execute("SELECT * FROM Users WHERE username=? AND password=?", ('root', 'toor'))
	rows = imUser.fetchall()
	if (rows==[]):
		imUser.execute("INSERT INTO Users VALUES ('root', 'toor', '0')")
		userDB.commit()

	userDB.close()
	return render(request, 'havaDurumu/login.html', {})


def paravanAjax(request):
	global imLocation, imUser, locationDB, userDB, geolocator, USERNAME

	loginID, loginPW = globalLoginID, globalLoginPW
	USERNAME = loginID

	locationDB = sql.connect('location.sqlite3')
	imLocation = locationDB.cursor()

	try:
		imLocation.execute("CREATE TABLE IF NOT EXISTS Locations (location, lat, lng, locationID)")
		imLocation.execute("SELECT * FROM Locations")
		rows = imLocation.fetchall()
		data = []
		for row in rows:
			data.append(row[0])
	except:
		print("ilk lokasyon ekle")

	geolocator = Nominatim(user_agent="havaDurumu")
	if loginID == 'root' and loginPW == 'toor':
		return render(request, 'havaDurumu/rootHome.html', {'rows': data})
	else:
		return render(request, 'havaDurumu/standartHome.html', {'rows': data})

def rootHome(request):
	return render(request, 'havaDurumu/rootHome.html', {})

def standartHome(request):
	return render(request, 'havaDurumu/standartHome.html', {})





@csrf_protect
def loginFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		return HttpResponse(data, content_type='application/json')
	else:
		print("else location add")
		return HttpResponse(data, content_type='application/json')

@csrf_protect
def loginToAjax(request):
	data = gonderilecekVeri.split(':')
	global globalLoginID, globalLoginPW
	loginID, loginPW = data[0], data[1]
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()

	globalLoginID, globalLoginPW = loginID, loginPW


	imUser.execute("SELECT * FROM Users WHERE username=? and password=?", (loginID, loginPW))
	rows = imUser.fetchall()


	if rows == []:
		error = 'Böyle Bir Kullanici Yok'
		error = json.dumps(error)
		return HttpResponse(error, content_type='application/json')
	else:
		if loginID == 'root' and loginPW == 'toor':
			print("147")
			data = 'havaDurumu/rootHome.html'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')
			#return render(request, 'havaDurumu/rootHome.html', {'rows': data})
		else:
			print("153")
			data = 'havaDurumu/standartHome.html'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')



### ============================================= MENU 1 ============================================= ### 



def addLocationToDB(request):
	locationDB = sql.connect('location.sqlite3')
	imLocation = locationDB.cursor()
	imLocation.execute("CREATE TABLE IF NOT EXISTS Locations (location, lat, lng, locationID)")
	locationDB.commit()

	data = gonderilecekVeri

	imLocation.execute("SELECT * FROM Locations WHERE location = ?", (data,))
	rows = imLocation.fetchall()	

	if rows != []:
		locationDB.close()
		return 'varmis'
	elif rows == []:
		imLocation.execute("INSERT INTO Locations VALUES (?, ?, ?, ?)", (data, 0, 0, 0, ))
		locationDB.commit()
		locationDB.close()
		return 'yeniVeriEklendi'

@csrf_protect
def locationAddFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		return HttpResponse(data, content_type='application/json')
	else:
		print("else location add")
		return HttpResponse(data, content_type='application/json')

@csrf_protect
def locationAddToAjax(request):
	if request.is_ajax():
		deger = addLocationToDB(request)
		if deger == 'varmis':
			data = 'BoyleBirYerVarmis'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')
		else:
			data = 'YeniLocationEklendi'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')



def removeLocationToDB(request):
	locationDB = sql.connect('location.sqlite3')
	imLocation = locationDB.cursor()
	
	data = gonderilecekVeri

	imLocation.execute("SELECT * FROM Locations WHERE location = ?", (data,))
	rows = imLocation.fetchall()	

	if rows != []:
		imLocation.execute("DELETE FROM Locations WHERE location = ?", (data,))
		locationDB.commit()
		locationDB.close()
		return 'silindi'
	elif rows == []:
		return 'BoyleBirYerYokmus'

@csrf_protect
def locationRemoveFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		return HttpResponse(data, content_type='application/json')
	else:
		print("else location remove")
		return HttpResponse(data, content_type='application/json')

@csrf_protect
def locationRemoveToAjax(request):
	if request.is_ajax():
		deger = removeLocationToDB(request)
		if deger == 'BoyleBirYerYokmus':
			data = 'BoyleBirYerYokmus'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')
		else:
			data = 'LocationSilindi'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')





def updateLocationToDB(request):
	locationDB = sql.connect('location.sqlite3')
	imLocation = locationDB.cursor()
	
	data = gonderilecekVeri
	data = data.split(':')
	eskiSehir, yeniSehir = data[0], data[1]


	imLocation.execute("SELECT * FROM Locations WHERE location = ?", (data[0],))
	rows = imLocation.fetchall()	

	if rows != []:
		imLocation.execute("UPDATE Locations SET location = ? WHERE location = ?", (data[1], data[0]))
		locationDB.commit()
		locationDB.close()
		return 'silindi'
	elif rows == []:
		return 'BoyleBirYerYokmus'

@csrf_protect
def locationUpdateFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		return HttpResponse(data, content_type='application/json')
	else:
		print("else location update")
		return HttpResponse(data, content_type='application/json')

@csrf_protect
def locationUpdateToAjax(request):
	if request.is_ajax():
		deger = updateLocationToDB(request)
		if deger == 'BoyleBirYerYokmus':
			data = 'BoyleBirYerYokmus'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')
		else:
			data = 'LocationGuncellendi'
			data = json.dumps(data)
			return HttpResponse(data, content_type='application/json')



# Burasi duzenlenecek
def listLocationToDB(request):
	locationDB = sql.connect('location.sqlite3')
	imLocation = locationDB.cursor()

	imLocation.execute("SELECT * FROM Locations")
	rows = imLocation.fetchall()	

	if rows != []:
		return rows
	elif rows == []:
		return 'HicLocationYok'

@csrf_protect
def locationListFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		
	else:
		print("else location update")
	
	return HttpResponse(data, content_type='application/json')

@csrf_protect
def locationListToAjax(request):
	if request.is_ajax():
		deger = listLocationToDB(request)
		if deger == 'HicLocationYok':
			data = 'HicLocationYok'
		else:
			data = deger

		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')





### ============================================= MENU 3 ============================================= ### 



def addUserToDB(request):
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()
	
	
	data = gonderilecekVeri
	data = data.split(':')


	imUser.execute("SELECT * FROM Users WHERE username = ?", (data[0],))
	rows = imUser.fetchall()	

	if rows != []:
		userDB.close()
		return 'varmis'
	elif rows == []:
		imUser.execute("INSERT INTO Users VALUES (?, ?, ?)", (data[0], data[1], 0))
		userDB.commit()
		userDB.close()
		return 'yeniKullaniciEklendi'

@csrf_protect
def userAddFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		
	else:
		print("else user add")
	
	return HttpResponse(data, content_type='application/json')

@csrf_protect
def userAddToAjax(request):
	if request.is_ajax():
		deger = addUserToDB(request)
		if deger == 'varmis':
			data = 'BoyleBiriVarmis'
			
		else:
			data = 'YeniKullaniciEklendi'
		
		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')



def removeUserToDB(request):
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()
	
	data = gonderilecekVeri

	imUser.execute("SELECT * FROM Users WHERE username = ?", (data,))
	rows = imUser.fetchall()	

	if rows != []:
		imUser.execute("DELETE FROM Users WHERE username = ?", (data,))
		userDB.commit()
		userDB.close()
		return 'silindi'
	elif rows == []:
		return 'BoyleBiriYokmus'

@csrf_protect
def userRemoveFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
		
	else:
		print("else user remove")
	
	return HttpResponse(data, content_type='application/json')

@csrf_protect
def userRemoveToAjax(request):
	if request.is_ajax():
		print(",,,,,,,,,,,,,,,,", gonderilecekVeri)
		if gonderilecekVeri == 'root':
			print('buada')
			data = 'rootSilinemez'
			
		else:
			deger = removeUserToDB(request)
			if deger == 'BoyleBiriYokmus':
				data = 'BoyleBiriYokmus'
				
			else:
				data = 'UserSilindi'
		
		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')





def updateUserToDB(request):
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()
	
	data = gonderilecekVeri
	data = data.split(':')
	ID, yeniPW = data[0], data[1]
	print("*********************** : ", yeniPW)

	if (ID == 'root'):
		return 'ROOTGUNCELLENEMEZ'


	imUser.execute("SELECT * FROM Users WHERE username = ?", (data[0],))
	rows = imUser.fetchall()	

	if rows != []:
		imUser.execute("UPDATE Users SET password = ? WHERE username = ?", (data[1], data[0]))
		userDB.commit()
		userDB.close()
		return 'guncellendi'
	elif rows == []:
		return 'BoyleBiriYokmus'

@csrf_protect
def userUpdateFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}
	else:
		print("else user update")
	
	return HttpResponse(data, content_type='application/json')

@csrf_protect
def userUpdateToAjax(request):
	if request.is_ajax():
		deger = updateUserToDB(request)
		if deger == 'ROOTGUNCELLENEMEZ':
			data = 'ROOTGUNCELLENEMEZ'
		elif deger == 'BoyleBiriYokmus':
			data = 'BoyleBiriYokmus'
		else:
			data = 'UserGuncellendi'

		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')


# Burasi duzenlenecek
def listUserToDB(request):
	userDB = sql.connect('users.sqlite3')
	imUser = userDB.cursor()

	imUser.execute("SELECT * FROM Users")
	rows = imUser.fetchall()	

	if rows != []:
		return rows
	elif rows == []:
		return 'HicUserYok'

@csrf_protect
def userListFromAjax(request):
	global gonderilecekVeri
	data = request.POST.get("data")
	gonderilecekVeri = data

	if request.is_ajax() and request.POST:
		data = {}	
	else:
		print("else user update")
	
	return HttpResponse(data, content_type='application/json')

@csrf_protect
def userListToAjax(request):
	if request.is_ajax():
		deger = listUserToDB(request)
		if deger == 'HicUserYok':
			data = 'HicUserYok'
			
		else:
			data = deger
		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')










### ============================================= MENU 2 ============================================= ### 


### BURAYA ILK OLARAK AJAX ILE VERITABANINDAKI LOCATIONLARI GONDEREN KODU YAZ ###


def DarkWeatherAPI(request):
	# data = sehir
	global sorguSonucu
	data = sorguLokasyon
	print("--------------DarkWeatherAPI--------------")
	global hataDurumu, sorguSonucu
	try:
		location = geolocator.geocode(data, timeout=None)
		hataDurumu, sorguSonucu = "Başarılı", "Başarılı"
	except:
		hataDurumu = "Başarısız"
		return 'Sorgu Başarısız'

	try:
		lat, lng = location.latitude, location.longitude
		print(lat, lng, data)
	except:
		return 'Veritabanında Şehir Yok'
	jsonURL = 'https://api.darksky.net/forecast/12204d4f75238b6aecaacc7fd094182b/{},{}'.format(lat, lng)
	with urllib.request.urlopen(jsonURL) as url:
		data = json.loads(url.read().decode())

		currently = data["currently"]
		ozet = currently['summary']
		sicaklik = (int(currently['temperature'])-32)/1.8
		try:
			tahminiOlay = currently['precipType']
			tahminiOlayIhtimali = currently['precipProbability']
			data = [sorguLokasyon, ': ', ozet, str(sicaklik), tahminiOlay, str(tahminiOlayIhtimali)]
			data = " ".join(data)
		except KeyError:
			data = [sorguLokasyon, ':', ozet, str(sicaklik)]
			data = " ".join(data)

		with open('havaDurumu.json', 'w') as fp:
			sjj = json.dumps(data, indent=4)
			fp.write(str(sjj))

		sorguSonucu = data
		return data


	
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




	#return havaDurumuDeğerleri
def loging(request):
	raporDB = sql.connect('rapor.sqlite3')
	imRapor = raporDB.cursor()
	imRapor.execute("CREATE TABLE IF NOT EXISTS Report (username, queryTime, queryLocation, userIP, queryResult, timeDifference, queryState)")
	raporDB.commit()


	try:
		uname, queryTime, queryLocation, queryResult = USERNAME, timeDif, sorguLokasyon, sorguSonucu
	except:
		return 'VeriTabaniBos'
	ipAddr = get_client_ip(request)
	now = datetime.datetime.now()

	imRapor.execute("INSERT INTO Report VALUES (?, ?, ?, ?, ?, ?, ?)", (uname, now, queryLocation, ipAddr, queryResult, timeDif, hataDurumu))
	raporDB.commit()
	raporDB.close()



@csrf_protect
def weatherFromAjax(request):
	global sorguLokasyon, startTime, finishTime
	# data = combobox'tan secilen(veritabanindaki) sehir
	data = request.POST.get("data")
	sorguLokasyon = data
	startTime = time.time()

	if request.is_ajax() and request.POST:
		data = {}
	else:
		print("else weather add")
	
	return HttpResponse(data, content_type='application/json')



@csrf_protect
def weatherToAjax(request):
	if request.is_ajax():
		global havaDurumuSonuc, timeDif
		# deger = hava durumu bilgiler
		deger = DarkWeatherAPI(request)
		finishTime = time.time()
		timeDif = finishTime - startTime

		data = json.dumps(deger)
		havaDurumuSonuc = data


		vtSonuc = loging(request)
		if vtSonuc == 'VeriTabaniBos':
			data = 'Veritabanında Veri(Location) Yok'
		return HttpResponse(data, content_type='application/json')








	#return havaDurumuDeğerleri
def reportingLizbon(request):
	global raporSonucu
	raporDB = sql.connect('rapor.sqlite3')
	imRapor = raporDB.cursor()

	imRapor.execute("SELECT * FROM Report ORDER BY queryTime DESC")
	rows = imRapor.fetchall()
	raporSonucu = rows
	raporDB.close()



@csrf_protect
def reportFromAjax(request):
	# data = combobox'tan secilen(veritabanindaki) sehir
	data = request.POST.get("data")
	print("helehelehele")

	if request.is_ajax() and request.POST:
		print(1111111111)
		data = {}	
	else:
		print("else report add")
	
	return HttpResponse(data, content_type='application/json')



@csrf_protect
def reportToAjax(request):
	if request.is_ajax():
		print(222222222)
		# deger = rapor Sonucu
		reportingLizbon(request)
		data = str(raporSonucu)
		print('\n\n\ndata: ', data)
		return HttpResponse(data)
	else:
		print("elseesesssesesese")




	#return havaDurumuDeğerleri
def reportingStandartLizbon(request):
	global raporSonucuStandart
	raporDB = sql.connect('rapor.sqlite3')
	imRapor = raporDB.cursor()

	imRapor.execute("SELECT * FROM Report WHERE username=? ORDER BY queryTime DESC", (globalLoginID,))
	rows = imRapor.fetchall()
	raporSonucuStandart = rows
	raporDB.close()



@csrf_protect
def reportStandartFromAjax(request):
	# data = combobox'tan secilen(veritabanindaki) sehir
	data = request.POST.get("data")
	print("helehelehele")

	if request.is_ajax() and request.POST:
		print(1111111111)
		data = {}
	else:
		print("else report add")
	
	return HttpResponse(data, content_type='application/json')



@csrf_protect
def reportStandartToAjax(request):
	if request.is_ajax():
		print(222222222)
		# deger = rapor Sonucu
		reportingStandartLizbon(request)
		data = str(raporSonucuStandart)
		print('\n\n\ndata: ', data)
		return HttpResponse(data)
	else:
		print("elseesesssesesese12")

