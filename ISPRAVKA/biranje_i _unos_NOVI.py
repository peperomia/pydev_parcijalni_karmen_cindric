from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date, datetime

from klase_nove import Customer, Product, Offer, OfferProductLink

from funkcije_nove import oblikovanje_datuma

# engine = create_engine("sqlite:///parcijalaDB_Modul_NOVE_KLASE.db")
# #SQLModel.metadata.create_all(engine)



def manage_customers()->None:  #    RADI OK
    """
    Allows the user to add a new customer or view all customers.
    """
    flag = True
    while flag:
        try: 
            print("Unesite broj pored stavke koju želite odabrati:")
            print("1. Unos novog kupca u listu kupaca.")
            print("2. Pregled liste svih kupaca")
            print("3. Izlaz")
            odabir_akcije = input("Vaš odabir: ")  # str
            # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
            if odabir_akcije == "1":
                ime = input("Unesite ime kupca: ")
                mejl = input("Unesite email kupca: ")
                vat_id = int(input("Unesite kupčev vat_id: "))  # ima 11 znakova, ne ispiše dobro ako je manje
                new_customer = Customer(name = ime, email = mejl, vat_id = vat_id)
                with Session(engine) as session:
                    session.add(new_customer)
                    session.commit()
                                        
        except Exception as e:
            print("*" * 20)
            print(f"Dogodila se greška - {e}")
            print("Pazite da unesete tip podatka koji se očekuje za pojedinu stavku. ")
            print("*" * 20)

        # Za pregled: prikaži listu svih kupaca
        if odabir_akcije == "2":
            print("-"*110)
            print(f"id\tname\t\t\t\temail\t\t\t\t\t\t  vat_id")
            print("-"*110)
            with Session(engine) as session:
                    statement = select(Customer)
                    result = session.exec(statement)
                    for customer in result:             
                        if len(customer.name) < 16:
                            print(f"{customer.id}\t{customer.name}\t\t\t{customer.email}\t\t\t\t\t {customer.vat_id}")
                        else:
                            print(f"{customer.id}\t{customer.name}\t\t{customer.email}\t\t\t\t {customer.vat_id}")
                    session.commit()
        if odabir_akcije == "3":
            flag = False
        
        
# manage_customers()

def manage_products()-> None:  # RADI OK
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    flag = True
    while flag:
        print("\nIzaberite opciju upravljanja proizvodima: ")
        print("1. Dodavanje novog proizvoda")
        print("2. Izmjena podataka postojećeg proizvoda")
        print("3. Izlaz")
        choice = input("Odabrana opcija: ")
        # TODO: petlja ako želi odabrati još jednu opciju upravljanja proizvodima (petlja: opet dodavanje ili izmjena)
        # products  
        if choice == "1":  
            print("Unesite detalje proizvoda: ")
            name = input("Unesite naziv proizvoda: ")
            description = input("Unesite opis proizvoda: ")
            flag = True
            while flag:
                try:
                    price = round(float(input("Unesite cijenu proizvoda: ")), 1)
                    flag = False
                except Exception as e:
                    print(f"Dogodila se greška - {e}")
                    print("Pokušajte ponovno. Pazite da unesete broj, može s decimalnom točkom. ")
                        
            with Session(engine, expire_on_commit=False) as session:
                novi_proizvod = Product(name = name, description = description, price = price)   
                print(f"Pregled: name = {novi_proizvod.name} \ndescription = {novi_proizvod.description} \ncijena = {novi_proizvod.price} ")
                session.add(novi_proizvod)
                session.commit()
            # save_data("products.json", products)  # ne spremati jer sprema u main() pri izlasku
            

        if choice == "2":
            flag = True
            while flag:
                try:
                    print("Izaberite proizvod kojem želite izmijeniti podatke: ")
                    with Session(engine, expire_on_commit=False) as session:
                        all_products = select(Product)
                        result = session.exec(all_products).all()
                        for product in result:
                            print(f"{product.id}. {product.name}")
                        id_proizvoda = int(input("Odaberite broj pored proizvoda: "))
                        statement = select(Product).where(Product.id == id_proizvoda)
                        azurirani_proizvod = session.exec(statement).first()
                        print("Dosadašnje stanje proizvoda kojeg želite ažurirati = ", azurirani_proizvod)

                        flag = False
                except Exception as e:
                    print(f"Dogodila se greška - {e}")
                    print("*" *20)
                    print("Pazite da odaberete broj koji je ponuđen lijevo od imena proizvoda.")
                    print("*" *20)

            flag = True
            while flag: 
                try:
                    print("Odabrite stavku čiji unos želite promijeniti: ")
                    print("1.name")
                    print("2.description")
                    print("3.price")
                    stavka = int(input("Odabrite broj pored stavke koju želite mijenjati: "))
                    
                    if stavka == 1:
                        azurirani_proizvod.name = input("Unesite novu vrijednost stavke koju želite mijenjati: ")
                    elif stavka == 2:
                        azurirani_proizvod.description = input("Unesite novu vrijednost stavke koju želite mijenjati: ")
                    elif stavka == 3:
                        azurirani_proizvod.price = round(float(input("Unesite novu vrijednost stavke koju želite mijenjati: ")), 1)                  
                    
                    session.add(azurirani_proizvod)
                    session.commit()
                    statement = select(Product).where(Product.id == id_proizvoda)
                    kontrola_azuriranog_proizvoda = session.exec(statement).first()  # bez ovog first() printa mem. adresu                    
                    print(f"Pregled novog stanja ažuriranog proizvoda: {kontrola_azuriranog_proizvoda.name} \n {kontrola_azuriranog_proizvoda.description} \n {kontrola_azuriranog_proizvoda.price}")
                    # save_data("products.json", products)  # ne spremati jer sprema u main() pri izlasku

                    flag = False
                except Exception as e:
                    print("*" * 20)
                    print(f"Dogodila se greška - {e}")
                    print("Pazite da nova unesena vrijednost odgovara tipu podatka koji se očekuje za određenu stavku.")
                    print("*" * 20)
                finally:
                    jos_stavki = input("Želite li promijeniti još koju stavku u ovome istom proizvodu? (da/ne) ")
                    if jos_stavki == "da":
                        flag = True

        if choice == "3":
            break



# manage_products()

def create_new_offer()-> None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    with Session(engine) as session:
        # flag = True
        while True:
            print("Kreirajte novu ponudu")
            # Omogućite unos kupca
            print("Izaberite kupca iz liste kupaca: ")
            statement = select(Customer)
            result = session.exec(statement) 
            for customer in result:  
                print(customer.id, customer.name)  # printa sve kupce radi odabira
            
            id_kupca = int(input("Unesite broj pored imena kupca: "))
            ime_kupca = session.exec(select(Customer).where(Customer.id == id_kupca)).first()  # bez .first() (ili .all()) printa mem adresu

            # unos datuma
            flag = True
            while flag:
                try:
                    print("Unesite datum ponude: ")
                    dan = int(input("Unesite dan u mjesecu, od 1 do 31 \n (vodite računa o mjesecu):").rstrip(chars = "."))
                    mjesec = int(input("Unesite mjesec kao broj: (1 do 12): ").rstrip(chars = "."))
                    godina = int(input("Unesite godinu sa 4 znamenke: ").rstrip(chars = "."))
                    datum = oblikovanje_datuma(godina, mjesec, dan)
                except Exception as e:
                    print(e)                        
                    print("Krivo ste unijeli datum")
                finally:
                    unos_datuma = input("Želite li unijeti današnji datum? da/ne: ").lower()
                    if unos_datuma == "da":
                        datum_long = datetime.now()   # 2024-12-23 20:00:16.208832

                        datum = date(datum_long.year, datum_long.month, datum_long.day)
                        print(datum)
                        flag = False
                    else:
                        unos_datuma = input("Želite li ponovno pokušati unijeti datum? da/ne: ").lower()
                        if unos_datuma == "da":
                            flag = True
                        else:
                            flag = False
                            



            # odabir proizvoda -> PETLJA
            kontejner_id_brojeva = []  # sakuplja id brojeve kupljrnih proizvoda
            kolicina_proizvoda = []
            while True:
                print("-"*110)
                print(f"id\tname\t\t\t\tdescription\t\t\t\t\t\tprice")
                print("-"*110)
                statement = select(Product)
                result = session.exec(statement)
                for product in result:
                    print(f"{product.id}\t{product.name: <20}\t\t{product.description: <45}\t\t{product.price}") 
                print()
                print("-"*110)
                print()
                broj_proizvoda = input("Odaberite id broj proizvoda na sasvim lijevoj strani tablice: ")
                kolicina = int(input("Koliko komada tog proizvoda želite kupiti? Unesite broj: "))
                kontejner_id_brojeva.append(broj_proizvoda)  # lista s id brojevima kupljenih proizvoda
                kolicina_proizvoda.append(kolicina)  # lista s količinama kupljenih proizvoda (indexi odgovaraju onima u kontejner_id_brojeva listi)
                nastavak = input("Želite li nastaviti kupovati? (da/ne): ").lower()
                if nastavak == "ne":
                    break

            try:
                collected_item_totals = []  # lista
                for i in range(len(kontejner_id_brojeva)):   # kontejner_id_brojeva = lista s id brojevima kupljenih proizvoda
                    statement = select(Product).where(Product.id == int(kontejner_id_brojeva[i]))
                    product_bought = session.exec(statement).first()  # bez first() printa mem adresu
                    kolicina = kolicina_proizvoda[i]
                    item_total = product_bought.price * kolicina
                    collected_item_totals.append(item_total)


                    
            
                # Izračunajte sub_total, tax i total            
                sub_total = sum(collected_item_totals)
                tax = round(float(sub_total * (0.1)), 1) # tax = 10% od sub_total
                total = sub_total + tax
                statement = select(Customer).where(Customer.id == id_kupca)
                result = session.exec(statement).first()
                ime_kupca = result.name

                
                new_offer = Offer(customer_name=ime_kupca, date=datum, sub_total=sub_total, tax=tax, total=total)
                print(new_offer)
                session.add(new_offer)
                session.commit()
                with Session(engine) as session:
                    statement = select(Offer)
                    result = session.exec(statement).all()
                    for offer in result:
                        last_offer_id = offer.id  # ostaje u memoriji zadnji upisani id u tablici offer, a to je ovaj maloprije commitan
                        
                    
                    for i in range(len(kontejner_id_brojeva)):
                        new_offer_specs = OfferProductLink(product_id=kontejner_id_brojeva[i], offer_id=last_offer_id, quantity=kolicina_proizvoda[i], item_total=collected_item_totals[i])
                        session.add(new_offer_specs)
                    session.commit()

            except Exception as e:
                print(f"Dogodila se greska - {e}")
                print("Pažljivo pročitajte upute prilikom unosa podataka i pazite da se uneseni brojevi za opciju nalaze među ponuđenima")
            
            nova_nova_ponuda = input("Želite li stvoriti još jednu novu ponudu? (da/ne) ")
            if nova_nova_ponuda != "da":
                break

# create_new_offer()
# -----------------------------------------------------------------------------------------------------------------------------------

# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer: Offer)-> None: # funkcija ispisuje u konzolu, ali ne vraća ništa (prazna varijabla)   
    #
    #  RADI SADA
    # dict u parametru je rezultat offers[index]
    """Display details of a single offer."""
    print()
    print(f"Ponuda br: {offer.id}, Kupac: {offer.customer_name}, Datum ponude: {offer.date}")
    print("Stavke:")
    with Session(engine) as session:
        statement = select(OfferProductLink).where(OfferProductLink.offer_id == offer.id)
        Link_list = session.exec(statement).all()   # lista od onoliko redova koliko proizvoda ima ponuda
        
        for i in range(len(offer.products)):
            print(f"  - {offer.products[i].name} (ID: {offer.products[i].id}): {offer.products[i].description}")
 
            print(f"    Kolicina: {Link_list[i].quantity}, Cijena: ${offer.products[i].price}, Ukupno: ${Link_list[i].item_total}")
    print(f"Ukupno: ${offer.sub_total}, Porez: ${offer.tax}, Ukupno za platiti: ${offer.total}")


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers()->None:
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    flag = True
    while flag:
        print("\nIzaberite pregled ponuda: ")
        print("1. sve ponude")
        print("2. ponude po mjesecu: ")
        print("3. pojedinačna ponuda")  # print_offer()
        print("4. izlaz")
        choice = input("Odabrana opcija: ")
        # Prikaz relevantnih ponuda na temelju izbora
        if choice == "1":
            with Session(engine) as session:
                statement = select(Offer)
                offers = session.exec(statement).all()  # ako se ne stavi all() ili first() printa mem adresu
                for offer in offers:
                    print_offer(offer)

        elif choice == "2":
            try:
                with Session(engine) as session:
                    dostupni_mjeseci = []
                    statement = select(Offer)
                    offers = session.exec(statement).all()
                    for offer in offers:
                        print(offer.date)
                        mjesec = offer.date.month
                        print(mjesec)
                        dostupni_mjeseci.append(mjesec)
                    set_mjesec = set(dostupni_mjeseci)
                    print(f"Podaci dostupni za sljedeće mjesece: {set_mjesec}")
                    mjesec_unos = int(input("Unesite željeni mjesec od dostupnih: "))
                    if mjesec_unos in set_mjesec:
                        for offer in offers:
                            if offer.date.month == mjesec_unos:
                                print_offer(offer)
                    else:
                        print("*" * 20)
                        print(f"Za željeni mjesec nema podataka.")
            except Exception as e:
                print("*" * 20)
                print(f"Dogodila se greška - {e}")
                print("*" * 20)


        elif choice == "3":
            flag2 = True
            while flag2:
                with Session(engine) as session:
                    try:
                        offer_num_list = []
                        statement = select(Offer)
                        offers = session.exec(statement).all()
                        for offer in offers:
                            offer_num_list.append(offer.id)
                                     
                        # TODO try except blok i petlja (ako unese krivi broj)
                        print(f"Brojevi ponuda na raspolaganju:")
                        print(*offer_num_list)
                        izbor_broja_ponude = int(input("Unesite broj ponude: "))
                        statement = select(Offer).where(Offer.id == izbor_broja_ponude)  # izbor_broja_ponude OK (nije u funkciji print_offer())
                        offer = session.exec(statement).first()

                        print_offer(offer = offer) # izbor_broja_ponude = izbor_broja_ponude)  # za index liste offers moramo - 1
                        flag2 = False
                    except Exception as e:
                        print("*" * 20)
                        print(f"Dogodila se greška - {e}")
                        print("Pazite da unosite broj ponude koji je na raspolaganju")
                        print("*" * 20)

        
        elif choice == "4":
            print("Izlaz")
            flag = False

        else:
            print("Krivi izbor. Pokušajte ponovo.")

# display_offers()

def main():
    # konstrukcija baze

    engine = create_engine("sqlite:///parcijalaDB_Modul_NOVE_KLASE.db")
    SQLModel.metadata.create_all(engine)

    # konstrukcija klasa/tablica
    klase_nove



    # # Učitavanje podataka iz JSON datoteka
    # offers = load_data(OFFERS_FILE)
    # products = load_data(PRODUCTS_FILE)
    # customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
     main()



