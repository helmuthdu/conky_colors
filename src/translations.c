#define _ISOC99_SOURCE // for snprintf
#include <string.h>
#include <stdio.h>
#include "translations.h"
#include "options.h"

char 	sys[31],
		processes[31],
		battery[31],
		uptime[31],
		packages[31],
		date[31],
		photo[31],
		hd[31],
		temperature[31],
		network[31],
		total[31],
		up[31],
		down[31],
		//upload[31],
		//download[31],
		sinal[31],
		localip[31],
		publicip[31],
		nonet[40],
		Weather[31],
		noweather[62],
		//station[31],
		//rain[31],
		humidity[31],
		//sunrise[31],
		//sunset[31],
		//moon[31],
		updates[31],
		nouve[31],
		status[31],
		song[31],
		tempo[31],
		nopidgin[43],
		//norhythmbox[31],
		unknownstatus[34];

char 	language[31];

//Languages
void translation () {
	OR_OPTION_START("pt", language) OR_OPTION_END("portuguese", language) {
		snprintf(sys, 31, "SISTEMA");
		snprintf(battery, 31, "Bateria");
		snprintf(uptime, 31, "Atividade");
		snprintf(processes, 31, "Processos");
		snprintf(packages, 31, "Pacotes");
		snprintf(date, 31, "DATA");
		snprintf(photo, 31, "FOTO");
		snprintf(hd, 31, "HD");
		snprintf(temperature, 31, "Temperatura");
		snprintf(updates, 31, "Atualizações");
		snprintf(nouve, 31, "Novo(s)");
		snprintf(network, 31, "REDE");
		snprintf(up, 31, "Up");
		snprintf(down, 31, "Down");
		//snprintf(upload, 31, "Upload");
		//snprintf(download, 31, "Download");
		snprintf(sinal, 31, "Sinal");
		snprintf(total, 31, "Total");
		snprintf(localip, 31, "Ip local");
		snprintf(publicip, 31, "Ip externo");
		snprintf(nonet, 31, "Rede indisponível");
		snprintf(Weather, 31, "TEMPO");
		snprintf(noweather, 31, "Tempo indisponível");
		//snprintf(station, 31, "Estação");
		//snprintf(rain, 31, "Chuva");
		snprintf(humidity, 31, "Umidade");
		//snprintf(sunrise, 31, "Amanhecer");
		//snprintf(sunset, 31, "Anoitecer");
		//snprintf(moon, 31, "Lua");
		snprintf(status, 31, "Status");
		snprintf(song, 31, "Música");
		snprintf(tempo, 31, "Tempo");
		snprintf(nopidgin, 31, "Pidgin não está rodando");
		//snprintf(norhythmbox, 31, "Rhythmbox não está rodando");
		snprintf(unknownstatus, 31, "Status desconhecido");
	}
	else OR_OPTION_START("it",language) OR_OPTION_END("italian",language) {
		snprintf(sys, 31, "SISTEMA");
		snprintf(battery, 31, "Batteria");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Processi");
		snprintf(packages, 31, "Pacchetti");
		snprintf(date, 31, "DATA");
		snprintf(photo, 31, "FOTO");
		snprintf(hd, 31, "HD");
		snprintf(temperature, 31, "Temperatura");
		snprintf(updates, 31, "Aggiornamenti");
		snprintf(nouve, 31, "Nouve");
		snprintf(network, 31, "RETE");
		snprintf(up, 31, "Up");
		snprintf(down, 31, "Down");
		//snprintf(upload, 31, "Upload");
		//snprintf(download, 31, "Download");
		snprintf(sinal, 31, "Segnale");
		snprintf(total, 31, "Totale");
		snprintf(localip, 31, "Ip Locale");
		snprintf(publicip, 31, "Ip Pubblico");
		snprintf(nonet, 31, "Rete Non Disponibile");
		snprintf(Weather, 31, "METEO");
		snprintf(noweather, 31, "Meteo Non Disponibile");
		//snprintf(station, 31, "Stazione");
		//snprintf(rain, 31, "Pioggia");
		snprintf(humidity, 31, "Umidità");
		//snprintf(sunrise, 31, "Alba");
		//snprintf(sunset, 31, "Tramonto");
		//snprintf(moon, 31, "Luna");
		snprintf(status, 31, "Status");
		snprintf(song, 31, "Canzone");
		snprintf(tempo, 31, "Tempo");
		snprintf(nopidgin, 31, "Pidgin non è in esecuzione");
		//snprintf(norhythmbox, 31, "Rhythmbox non è in esecuzione");
		snprintf(unknownstatus, 31, "Stato sconosciuto");
	}
	else OR_OPTION_START("es", language) OR_OPTION_END("spanish", language) {
		snprintf(sys, 31, "SISTEMA");
		snprintf(battery, 31, "Batería");
		snprintf(uptime, 31, "Actividad");
		snprintf(processes, 31, "Procesos");
		snprintf(packages, 31, "Paquetes");
		snprintf(date, 31, "FECHA");
		snprintf(photo, 31, "FOTO");
		snprintf(hd, 31, "HD");
		snprintf(temperature, 31, "Temperatura");
		snprintf(updates, 31, "Actualizaciones");
		snprintf(nouve, 31, "Nuevo(s)");
		snprintf(network, 31, "RED");
		snprintf(up, 31, "Envío");
		snprintf(down, 31, "Recibo");
		//snprintf(upload, 31, "Enviado");
		//snprintf(download, 31, "Recibido");
		snprintf(sinal, 31, "Señal");
		snprintf(total, 31, "Total");
		snprintf(localip, 31, "Ip Local");
		snprintf(publicip, 31, "Ip Pública");
		snprintf(nonet, 31, "Red no disponible");
		snprintf(Weather, 31, "CLIMA");
		snprintf(noweather, 31, "Clima no disponible");
		//snprintf(station, 31, "Estación");
		//snprintf(rain, 31, "Lluvia");
		snprintf(humidity, 31, "Humedad");
		//snprintf(sunrise, 31, "Amanecer");
		//snprintf(sunset, 31, "Anochecer");
		//snprintf(moon, 31, "Luna");
		snprintf(status, 31, "Situación");
		snprintf(song, 31, "Canción");
		snprintf(tempo, 31, "Tiempo");
		snprintf(nopidgin, 31, "Pidgin no esta corriendo");
		//snprintf(norhythmbox, 31, "Rhythmbox no esta corriendo");
		snprintf(unknownstatus, 31, "Estado desconocido");
	}
	else OR_OPTION_START("de", language) OR_OPTION_END("deutsch", language) {
		snprintf(sys, 31, "SYSTEM");
		snprintf(battery, 31, "Batterie");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Prozesse");
		snprintf(packages, 31, "Pakete");
		snprintf(date, 31, "DATUM");
		snprintf(photo, 31, "PHOTO");
		snprintf(hd, 31, "HD");
		snprintf(temperature, 31, "Temperatur");
		snprintf(updates, 31, "Updates");
		snprintf(nouve, 31, "Neu");
		snprintf(network, 31, "NETZWERK");
		snprintf(up, 31, "Up");
		snprintf(down, 31, "Down");
		//snprintf(upload, 31, "Upload");
		//snprintf(download, 31, "Download");
		snprintf(sinal, 31, "sinal");
		snprintf(total, 31, "Insgesamt");
		snprintf(localip, 31, "Lokale IP");
		snprintf(publicip, 31, "Öffentliche IP");
		snprintf(nonet, 31, "Netzwerk nicht verfügbar");
		snprintf(Weather, 31, "WETTER");
		snprintf(noweather, 31, "Wetter nicht verfügbar");
		//snprintf(station, 31, "Station");
		//snprintf(rain, 31, "Regen");
		snprintf(humidity, 31, "Feuchte");
		//snprintf(sunrise, 31, "Sonnenaufgang");
		//snprintf(sunset, 31, "Sonnenuntergang");
		//snprintf(moon, 31, "Mond");
		snprintf(status, 31, "Status");
		snprintf(song, 31, "Gesang");
		snprintf(tempo, 31, "Zeit");
		snprintf(nopidgin, 31, "Pidgin nicht läuft");
		//snprintf(norhythmbox, 31, "Rhythmbox nicht läuft");
		snprintf(unknownstatus, 31, "Unbekannter Status");
	}
	else OR_OPTION_START("pl", language) OR_OPTION_END("polish", language) {
		snprintf(sys, 31, "SYSTEM");
		snprintf(battery, 31, "Bateria");
		snprintf(uptime, 31, "Uruchomiony");
		snprintf(processes, 31, "Procesów");
		snprintf(packages, 31, "Pakiety");
		snprintf(date, 31, "DATA");
		snprintf(photo, 31, "ZDJĘCIE");
		snprintf(hd, 31, "DYSKI");
		snprintf(temperature, 31, "Temperatura");
		snprintf(updates, 31, "Aktualizacje");
		snprintf(nouve, 31, "Nowe");
		snprintf(network, 31, "SIEĆ");
		snprintf(up, 31, "Wys.");
		snprintf(down, 31, "Pob.");
		//snprintf(upload, 31, "Wysłano");
		//snprintf(download, 31, "Pobrano");
		snprintf(sinal, 31, "Sygnał");
		snprintf(total, 31, "Oddanych");
		snprintf(localip, 31, "Lokalne IP");
		snprintf(publicip, 31, "Publiczne IP");
		snprintf(nonet, 31, "Sieć Niedostępna");
		snprintf(Weather, 31, "POGODA");
		snprintf(noweather, 31, "Pogoda niedostępna");
		//snprintf(station, 31, "Dworzec");
		//snprintf(rain, 31, "Deszcz");
		snprintf(humidity, 31, "Wilgotność");
		//snprintf(sunrise, 31, "Świt");
		//snprintf(sunset, 31, "Zachód słońca");
		//snprintf(moon, 31, "Księżyc");
		snprintf(status, 31, "Stan");
		snprintf(song, 31, "Utwór");
		snprintf(tempo, 31, "Pozycja");
		snprintf(nopidgin, 31, "Pidgin nie działa");
		//snprintf(norhythmbox, 31, "Rhythmbox nie działa");
		snprintf(unknownstatus, 31, "Stan nieznany");
	}
	else OR_OPTION_START("et", language) OR_OPTION_END("estonian", language) {
		snprintf(sys, 31, "SÜSTEEM");
		snprintf(battery, 31, "Aku");
		snprintf(uptime, 31, "Tööaeg");
		snprintf(processes, 31, "Protsessid");
		snprintf(packages, 31, "Pakendid");
		snprintf(date, 31, "KUUPÄEV");
		snprintf(photo, 31, "FOTO");
		snprintf(hd, 31, "KÕVAKETAS");
		snprintf(temperature, 31, "Temperatuur");
		snprintf(updates, 31, "Uuendused");
		snprintf(nouve, 31, "uut");
		snprintf(network, 31, "VÕRK");
		snprintf(up, 31, "Üles");
		snprintf(down, 31, "Alla");
		//snprintf(upload, 31, "Üleslaetud");
		//snprintf(download, 31, "Allalaetud");
		snprintf(sinal, 31, "Signaal");
		snprintf(total, 31, "Kokku");
		snprintf(localip, 31, "Kohalik IP");
		snprintf(publicip, 31, "Avalik IP");
		snprintf(nonet, 31, "Võrk pole saadaval");
		snprintf(Weather, 31, "ILM");
		snprintf(noweather, 31, "Ilm pole saadaval");
		//snprintf(station, 31, "Jaam");
		//snprintf(rain, 31, "Vihm");
		snprintf(humidity, 31, "Niiskus");
		//snprintf(sunrise, 31, "Päikesetõus");
		//snprintf(sunset, 31, "Päikeseloojangu");
		//snprintf(moon, 31, "Kuu");
		snprintf(status, 31, "Staatus");
		snprintf(song, 31, "Laul");
		snprintf(tempo, 31, "Aeg");
		snprintf(nopidgin, 31, "Pidgin ei tööta");
		//snprintf(norhythmbox, 31, "Rhythmbox ei tööta");
		snprintf(unknownstatus, 31, "Unknown Status");
	}
	else OR_OPTION_START("ru", language) OR_OPTION_END("russian", language) {
		snprintf(sys, 31, "СИСТЕМА");
		snprintf(battery, 31, "Батарея");
		snprintf(uptime, 31, "Время работы");
		snprintf(processes, 31, "Процессы");
		snprintf(packages, 31, "Пакеты");
		snprintf(date, 31, "ДАТА");
		snprintf(photo, 31, "ФОТО");
		snprintf(hd, 31, "ДИСКИ");
		snprintf(temperature, 31, "Температура");
		snprintf(updates, 31, "Обновления");
		snprintf(nouve, 31, "Новое");
		snprintf(network, 31, "СЕТЬ");
		snprintf(up, 31, "Отправка");
		snprintf(down, 31, "Приём");
		//snprintf(upload, 31, "Всего отправлено");
		//snprintf(download, 31, "Всего получено");
		snprintf(sinal, 31, "Сигнал");
		snprintf(total, 31, "Всего");
		snprintf(localip, 31, "Локальный IP");
		snprintf(publicip, 31, "Внешний IP");
		snprintf(nonet, 31, "Сеть недоступна");
		snprintf(Weather, 31, "ПОГОДА");
		snprintf(noweather, 59, "Информация о погоде недоступна");
		//snprintf(station, 31, "Станция");
		//snprintf(rain, 31, "Дождь");
		snprintf(humidity, 31, "Влажность");
		//snprintf(sunrise, 31, "Восход");
		//snprintf(sunset, 31, "Закат");
		//snprintf(moon, 31, "Луна");
		snprintf(status, 31, "Статус");
		snprintf(song, 31, "Композиция");
		snprintf(tempo, 31, "Время");
		snprintf(nopidgin, 31, "Pidgin не запущен");
		//snprintf(norhythmbox, 31, "Rhythmbox не запущен");
		snprintf(unknownstatus, 31, "Unknown Status");
	}
	else OR_OPTION_START("bg", language) OR_OPTION_END("bulgarian", language) {
		snprintf(sys, 31, "СИСТЕМА");
		snprintf(battery, 31, "Батерия");
		snprintf(uptime, 31, "Време на работа");
		snprintf(processes, 31, "Процеси");
		snprintf(packages, 31, "пакет(а)");
		snprintf(date, 31, "ДАТА");
		snprintf(photo, 31, "СНИМКА");
		snprintf(hd, 31, "ТВЪРД ДИСК");
		snprintf(temperature, 31, "Температура");
		snprintf(updates, 31, "Актуализации");
		snprintf(nouve, 31, "Нови");
		snprintf(network, 31, "МРЕЖА");
		snprintf(up, 31, "Качване");
		snprintf(down, 31, "Сваляне");
		//snprintf(upload, 31, "Качено");
		//snprintf(download, 31, "Свалено");
		snprintf(sinal, 31, "Сила на сигнала");
		snprintf(total, 31, "Общо");
		snprintf(localip, 31, "Локален IP");
		snprintf(publicip, 31, "Външен IP");
		snprintf(nonet, 39, "Мрежата е недостъпна");
		snprintf(Weather, 31, "ВРЕМЕТО");
		snprintf(noweather, 50, "Няма информация за времето");
		//snprintf(station, 31, "станция");
		//snprintf(rain, 31, "дъжд");
		snprintf(humidity, 31, "влажност");
		//snprintf(sunrise, 31, "изгрев");
		//snprintf(sunset, 31, "залез");
		//snprintf(moon, 31, "луна");
		snprintf(status, 31, "Статус");
		snprintf(song, 31, "Песен");
		snprintf(tempo, 31, "Време");
		snprintf(nopidgin, 34, "Pidgin не е стартиран");
		//snprintf(norhythmbox, 31, "Rhythmbox не е стартиран");
		snprintf(unknownstatus, 31, "Unknown Status");
	}
	else OR_OPTION_START("uk",language) OR_OPTION_END("ukrainian",language) {
		snprintf(sys, 31, "СИСТЕМА");
		snprintf(battery, 31, "Батарея");
		snprintf(uptime, 31, "Час роботи");
		snprintf(processes, 31, "Процеси");
		snprintf(packages, 31, "Пакунки");
		snprintf(date, 31, "ДАТА");
		snprintf(photo, 31, "ФОТО");
		snprintf(hd, 31, "ДИСКИ");
		snprintf(temperature, 31, "Температура");
		snprintf(updates, 31, "Оновлення");
		snprintf(nouve, 31, "Нове");
		snprintf(network, 31, "МЕРЕЖА");
		snprintf(up, 31, "Відправка");
		snprintf(down, 31, "Прийом");
		//snprintf(upload, 31, "Всього відправлено");
		//snprintf(download, 31, "Всього отримано");
		snprintf(sinal, 31, "Сигнал");
		snprintf(total, 31, "Всього");
		snprintf(localip, 31, "Локальний IP");
		snprintf(publicip, 31, "Зовнішній IP");
		snprintf(nonet, 34, "Мережа недоступна");
		snprintf(Weather, 31, "ПОГОДА");
		snprintf(noweather, 62, "Інформация про погоду недоступна");
		//snprintf(station, 31, "Станція");
		//snprintf(rain, 31, "Дощ");
		snprintf(humidity, 31, "Вологість");
		//snprintf(sunrise, 31, "Схід");
		//snprintf(sunset, 31, "Захід");
		//snprintf(moon, 31, "Місяць");
		snprintf(status, 31, "Статус");
		snprintf(song, 31, "Композиція");
		snprintf(tempo, 31, "Час");
		snprintf(nopidgin, 31, "Pidgin не запущений");
		//snprintf(norhythmbox, 31, "Rhythmbox не запущений");
		snprintf(unknownstatus, 31, "Невідомий стан");
	}
	else OR_OPTION_START("fr", language) OR_OPTION_END("french", language) {
		snprintf(sys, 31, "SYSTÈME");
		snprintf(battery, 31, "Batterie");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Processus");
		snprintf(packages, 31, "Paquets");
		snprintf(date, 31, "DATE");
		snprintf(photo, 31, "PHOTO");
		snprintf(hd, 31, "DD");
		snprintf(temperature, 31, "Température");
		snprintf(updates, 31, "Mises à jour");
		snprintf(nouve, 31, "nouveau(x)");
		snprintf(network, 31, "RÉSEAU");
		snprintf(up, 31, "Émission");
		snprintf(down, 31, "Réception");
		//snprintf(upload, 31, "Envoyés");
		//snprintf(download, 31, "Reçus");
		snprintf(sinal, 31, "sinal");
		snprintf(total, 31, "Total");
		snprintf(localip, 31, "IP locale");
		snprintf(publicip, 31, "IP publique");
		snprintf(nonet, 31, "Réseau indisponible");
		snprintf(Weather, 31, "MÉTÉO");
		snprintf(noweather, 31, "Météo indisponible");
		//snprintf(station, 31, "Station");
		//snprintf(rain, 31, "Pluie");
		snprintf(humidity, 31, "Humidité");
		//snprintf(sunrise, 31, "Lever de soleil");
		//snprintf(sunset, 31, "Coucher de soleil");
		//snprintf(moon, 31, "Lune");
		snprintf(status, 31, "Status");
		snprintf(song, 31, "Morceau");
		snprintf(tempo, 31, "Temps");
		snprintf(nopidgin, 31, "Pidgin non démarré");
		//snprintf(norhythmbox, 31, "Rhythmbox non démarré");
		snprintf(unknownstatus, 31, "État inconnu");
	}
	else OR_OPTION_START("cs", language) OR_OPTION_END("czech", language) {
		snprintf(sys, 31, "SYSTEM");
		snprintf(battery, 31, "Baterie");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Procesy");
		snprintf(packages, 31, "Balíčky");
		snprintf(date, 31, "DATUM");
		snprintf(photo, 31, "FOTO");
		snprintf(hd, 31, "DISKY");
		snprintf(temperature, 31, "Teplota");
		snprintf(updates, 31, "Aktualizace");
		snprintf(nouve, 31, "Nové");
		snprintf(network, 31, "SÍŤ");
		snprintf(up, 31, "Up.");
		snprintf(down, 31, "Down.");
		//snprintf(upload, 31, "Odesláno");
		//snprintf(download, 31, "Staženo");
		snprintf(sinal, 31, "Signál");
		snprintf(total, 31, "Celkem");
		snprintf(localip, 31, "Lokální IP");
		snprintf(publicip, 31, "Veřejná IP");
		snprintf(nonet, 31, "Síť není dostupná");
		snprintf(Weather, 31, "POČASÍ");
		snprintf(noweather, 31, "Počasí není dostupné");
		//snprintf(station, 31, "Stanice");
		//snprintf(rain, 31, "Déšť");
		snprintf(humidity, 31, "Vlhkost");
		//snprintf(sunrise, 31, "Východ Slunce");
		//snprintf(sunset, 31, "Západ SLunce");
		//snprintf(moon, 31, "Měsíc");
		snprintf(status, 31, "Stav");
		snprintf(song, 31, "Skladba");
		snprintf(tempo, 31, "Čas");
		snprintf(nopidgin, 31, "Pidgin není spuštěn");
		//snprintf(norhythmbox, 31, "Rhythmbox není spuštěn");
		snprintf(unknownstatus, 31, "Neznámý stav");
	}
	else OR_OPTION_START("el", language) OR_OPTION_END("greek", language) {
		snprintf(sys, 31, "ΣΥΣΤΗΜΑ");
		snprintf(battery, 31, "Μπαταρία");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Διεργασίες");
		snprintf(packages, 31, "Πακέτα");
		snprintf(date, 31, "ΗΜ/ΝΙΑ");
		snprintf(photo, 31, "ΦΩΤΟΓΡΑΦΙΑ");
		snprintf(hd, 31, "ΔΙΣΚΟΣ");
		snprintf(temperature, 31, "Θερμοκρασία");
		snprintf(updates, 31, "Ενημερώσεις");
		snprintf(nouve, 31, "Νέο");
		snprintf(network, 31, "ΔΙΚΤΥΟ");
		snprintf(up, 31, "Φόρτωση");
		snprintf(down, 31, "Λήψη");
		//snprintf(upload, 31, "Φόρτωση");
		//snprintf(download, 31, "Λήψη");
		snprintf(sinal, 31, "Σήμα");
		snprintf(total, 31, "Σύνολο");
		snprintf(localip, 31, "Τοπική IP");
		snprintf(publicip, 31, "Δημόσια IP");
		snprintf(nonet, 37, "Δίκτυο μη διαθέσιμο");
		snprintf(Weather, 31, "ΚΑΙΡΟΣ");
		snprintf(noweather, 39, "Καιρός μη διαθέσιμος");
		//snprintf(station, 31, "Σταθμός");
		//snprintf(rain, 31, "Βροχή");
		snprintf(humidity, 31, "Υγρασία");
		//snprintf(sunrise, 31, "Ανατολή ηλίου");
		//snprintf(sunset, 31, "Δύση ηλίου");
		//snprintf(moon, 31, "Φεγγάρι");
		snprintf(status, 31, "Κατάσταση");
		snprintf(song, 31, "Τραγούδι");
		snprintf(tempo, 31, "Χρόνος");
		snprintf(nopidgin, 43, "Το Pidgin δεν είναι ενεργό");
		//snprintf(norhythmbox, 31, "Το Rhythmbox δεν είναι ενεργό");
		snprintf(unknownstatus, 35, "Άγνωστη κατάσταση");
	}
	else {
		snprintf(sys, 31, "SYSTEM");
		snprintf(battery, 31, "Battery");
		snprintf(uptime, 31, "Uptime");
		snprintf(processes, 31, "Processes");
		snprintf(packages, 31, "Packages");
		snprintf(date, 31, "DATE");
		snprintf(photo, 31, "PHOTO");
		snprintf(hd, 31, "HD");
		snprintf(temperature, 31, "Temperature");
		snprintf(updates, 31, "Updates");
		snprintf(nouve, 31, "New");
		snprintf(network, 31, "NETWORK");
		snprintf(up, 31, "Up");
		snprintf(down, 31, "Down");
		//snprintf(upload, 31, "Upload");
		//snprintf(download, 31, "Download");
		snprintf(sinal, 31, "Signal");
		snprintf(total, 31, "Total");
		snprintf(localip, 31, "Local IP");
		snprintf(publicip, 31, "Public IP");
		snprintf(nonet, 31, "Network Unavailable");
		snprintf(Weather, 31, "WEATHER");
		snprintf(noweather, 31, "Weather Unavailable");
		//snprintf(station, 31, "Station");
		//snprintf(rain, 31, "Rain");
		snprintf(humidity, 31, "Humidity");
		//snprintf(sunrise, 31, "Sunrise");
		//snprintf(sunset, 31, "Sunset");
		//snprintf(moon, 31, "Moon");
		snprintf(status, 31, "Status");
		snprintf(song, 31, "Song");
		snprintf(tempo, 31, "Time");
		snprintf(nopidgin, 31, "Pidgin not running");
		//snprintf(norhythmbox, 31, "Rhythmbox not running");
		snprintf(unknownstatus, 31, "Unknown Status");
	}
}
