U folderu BAZE nalaze se skripte čije pokretanje određenim redoslijedom omogućava kreiranje baze podataka pod nazivom
ParcijalaDB.db i koja je napunjena podacima iz .json dokumenata customers.json, products.json i offers.json.   
   
Skripte se pokreću ovim redoslijedom:  
1.klase_za_bazu.py  
2.funkcije.py  
3.json_u_bazu.py   
4.main_baze.py   
   
Nakon pokretanja gorespomenutim redoslijedom, u folderu u kojem se nalazi folder BAZE, PYDEV_PARCIJALNI_KARMEN_CINDRIC sprema se 
stvorena baza. U slučaju da ona već postoji/da ponovno pokrećete skripte, tada tu bazu treba obrisati da ne bi došlo do dupliranja 
zapisa u bazi.   

Skripta main_baze.py podrazumijeva da su skripte prije nje pokrenute. Ona omogućava pretraživnaje baze, te preinaku ili unošenje posve 
novih zapisa u bazu.   