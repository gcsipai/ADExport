PROGRAM CÉLJA
===========

Az ADExport egy grafikus felületű alkalmazás, amely Active Directory (AD) környezetből való adatExportálásra szolgál. A program lehetővé teszi a felhasználók, szervezeti egységek (OU-k) és csoportok strukturált exportálását CSV fájlokba.

FŐ FUNKCIÓK
-----------

1. Active Directory Kapcsolat
   - Távoli és lokális kapcsolat: DC szerverekhez való kapcsolódás IP cím vagy hostnév alapján
   - Automatikus felderítés: Lokális Domain Controller automatikus észlelése
   - Több hitelesítési mód: SSL/TLS támogatással
   - Port konfigurálás: Alapértelmezett (389) és SSL portok (636)

2. AdatExportálási Opciók
   a. Felhasználók és OU-k Exportálása
      * Felhasználói adatok:
         - Felhasználónév (sAMAccountName)
         - Teljes név (CN)
         - Keresztnév és vezetéknév
         - Email cím
         - Mobil telefonszám
         - Leírás
         - Distinguished Name (DN)
         - Fiók állapota (engedélyezett/letiltott)
      * Szervezeti egységek (OU-k):
         - OU neve
         - Distinguished Name
   b. Csoportok Exportálása
      - Csoport neve és leírása
      - Csoport tagjainak listája
      - Distinguished Name

3. Szűrési Lehetőségek
   * Felhasználói Állapot Szűrő
      - Összes felhasználó - minden felhasználó függetlenül állapotától
      - Csak engedélyezett felhasználók - aktív fiókok
      - Csak letiltott felhasználók - inaktív fiókok

TECHNIKAI HÁTTERE
=================

Használt Technológiák
---------------------
- Python 3 - programozási nyelv
- LDAP3 könyvtár - Active Directory kommunikáció
- CustomTkinter - modern grafikus felület
- CSV modul - adatExportálás

LDAP Lekérdezések
-----------------
A program a következő LDAP szűrőket használja:
- (objectClass=user) - felhasználók
- (objectClass=organizationalUnit) - OU-k
- (objectClass=group) - csoportok
- userAccountControl attribútum - fiók állapot ellenőrzése

CÉLKÖZÖNSÉG ÉS HASZNÁLATI TERÜLETEK
===================================

- Rendszergazdák
   - Felhasználói lista generálás - teljes felhasználói nyilvántartás
   - Fiók állapot ellenőrzés - letiltott fiókok azonosítása
   - Szervezeti struktúra dokumentálás - OU hierarchia exportálása

- Biztonsági Audit
   - Hozzáférési jogosultságok nyomon követése - csoporttagságok exportálása
   - Compliance reporting - regulatív követelmények teljesítése
   - Naplózás - historikus adatok rögzítése

- AdatMigráció és Átállás
   - RendszerMigráció előkészítés - adatok exportálása új rendszerbe
   - Adatátvitel - külső alkalmazásokba való importáláshoz
   - Backup - fontos AD információk biztonsági mentése

GYAKORLATI ALKALMAZÁSI PÉLDÁK
-----------------------------

1. HR Reporting
   - Dolgozói lista generálása részlegek szerint
   - Új alkalmazottak nyilvántartása
   - Kilépő munkavállalók listája

2. IT Support
   - Helpdesz számára felhasználói alapadatok
   - Csoporttagságok ellenőrzése jogosultsági problémáknál
   - Telepítési listák készítése

3. Biztonsági Csoport
   - Biztonsági csoportok tagjainak listája
   - Jogosultsági vizsgálatok
   - Compliance auditok támogatása

ELŐNYÖK
======

1. Egyszerűség
   - Grafikus felület - nem igényel programozási ismereteket
   - Automatikus beállítások - lokális DC automatikus felismerése
   - Intuitív kezelés - felhasználóbarát elrendezés

2. Rugalmasság
   - Többnyelvűség - magyar és angol nyelv támogatása
   - Téma választás - sötét/világos megjelenés
   - Részleges export - csak kiválasztott elemek exportálása

3. Biztonság
   - SSL/TLS titkosítás támogatása
   - Időtúllépések beállítása
   - Hibakezelés és validáció

KIMENETI FORMÁTUM
=================

Felhasználók CSV
----------------
ObjektumTípus;Állapot;Név;Felhasználónév;Keresztnév;Vezetéknév;Email;Mobil;Leírás;DN

Csoportok CSV
-------------
Név;Csoportnév;Leírás;DN;Tagok DN-jei

JÖVŐBELI FEJLESZTÉSI LEHETŐSÉGEK
=================================

- További nyelvi támogatások
- Speciális szűrési feltételek
- Exportálás JSON és XML formátumba
- Kötegelt feldolgozás
- Jelentéskészítő modul
- API integráció

ÖSSZEFOGLALÁS
=============

Az ADExport tehát egy komplett Active Directory adatkezelő megoldás, amely leegyszerűsíti a rendszergazdák számára az AD-beli információk exportálását és feldolgozását.
