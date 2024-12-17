import json

#TODO: dodati type hinting na sve funkcije


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename: str)-> list:
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename: str, data: dict)-> None:
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers: list, products: list, customers: list)-> None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    flag = True
    while flag:
        print("Kreirajte novu ponudu")
        offer = len(offers) + 1
        # Omogućite unos kupca
        print("Izaberite kupca iz liste kupaca: ")
        names_list = []
        count = 0
        for item in customers:
            count += 1
            name = str(count) + "." + item["name"]
            names_list.append(name)
        print(*names_list, sep = "\n")
        ime_kupca = int(input("Unesite broj pored imena kupca: "))

        # unos datuma
        flag = True
        while flag:
            dan = input("Unesite koji je danas dan u mjesecu: ")
            if abs(int(dan)) < 31:
                datum = "2024-11-" + dan
                flag = False
            else:
                print("Krivi datum. Broj treba biti između 1 i 30 (uključivo. )")

        # odabir proizvoda -> PETLJA
        idd = []
        kolicina_proizvoda = []
        while True:
            print("-"*110)
            print(f"id\tname\t\t\t\tdescription\t\t\t\t\t\tprice")
            print("-"*110)
            for item in products:
                id = item["id"]
                name = item["name"]
                description = item["description"]
                price = item["price"]
                print(f"{id}\t{name: <20}\t\t{description: <45}\t\t{price}")
            print()
            print("-"*110)
            print()
            broj_proizvoda = input("Odaberite id broj proizvoda na sasvim lijevoj strani tablice: ")
            kolicina = int(input("Koliko komada tog proizvoda želite kupiti? Unesite broj: "))
            idd.append(broj_proizvoda)
            kolicina_proizvoda.append(kolicina)
            nastavak = input("Želite li nastaviti kupovati? (da/ne): ").lower()
            if nastavak == "ne":
                break

        try:
            collected_items = []  # lista
            for item in idd:   
                item_dict = {}
                item_dict["product_id"] = products[int(item) - 1]["id"]
                item_dict["product_name"] = products[int(item) - 1]["name"]
                item_dict["description"] = products[int(item) - 1]["description"]
                item_dict["price"] = products[int(item) - 1]["price"]
                item_dict["quantity"] = kolicina_proizvoda[idd.index(item)]
                item_dict["item_total"] = products[int(item) - 1]["price"] * kolicina_proizvoda[idd.index(item)]
                
                collected_items.append(item_dict)  # lista proizvoda koje je kupac stavio u košaricu (kupio)
        
            # Izračunajte sub_total, tax i total
        
            sub_total = sum([item["item_total"] for item in collected_items])
            tax = round(float(sum([item["item_total"] for item in collected_items])) * (0.1), 1) # tax = 10% od sub_total
            final_dict = {}
            final_dict["offer_number"] = int(offer)
            final_dict["customer"] = customers[ime_kupca - 1]["name"] 
            final_dict["date"] = datum
            final_dict["items"] = collected_items
            final_dict["sub_total"] = sub_total
            final_dict["tax"] = tax
            final_dict["total"] = sub_total + tax
            print("Pregled:", json.dumps(final_dict, indent = 4), sep = "\n")
            
            # Dodajte novu ponudu u listu offers
            offers.append(final_dict)   # offers je lista koja se sastoji od rječnika koji predstavljaju pojedinu ponudu
            # nova ponuda se dodaje na kraj liste postojećih ponuda, zato jer funkcija koja piše offers.json ima način "w"
        except Exception as e:
            print(f"Dogodila se greska - {e}")
            print("Pažljivo pročitajte upute prilikom unosa podataka i pazite da se uneseni brojevi za opciju nalaze među ponuđenima")
        nova_nova_ponuda = input("Želite li stvoriti još jednu novu ponudu? (da/ne) ")
        if nova_nova_ponuda != "da":
            flag = False



# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products: list)-> None:  # novi podaci se spremaju u listu
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
            new_dict = {}
            new_dict["id"] = len(products) + 1
            new_dict["name"] = input("Unesite naziv proizvoda: ")
            new_dict["description"] = input("Unesite opis proizvoda: ")
            flag = True
            while flag:
                try:
                    new_dict["price"] = round(float(input("Unesite cijenu proizvoda: ")), 1)
                    flag = False
                except Exception as e:
                    print(f"Dogodila se greška - {e}")
                    print("Pokušajte ponovno. Pazite da unese broj, može s decimalnom točkom. ")
                
            print("Pregled:", json.dumps(new_dict, indent = 4), sep = "\n")
            products.append(new_dict)     #save_data() ima način "w"
            # save_data("products.json", products)  # ne spremati jer sprema u main() pri izlasku
            

        if choice == "2":
            flag = True
            while flag:
                print("Izaberite proizvod kojem želite izmijeniti podatke: ")
                count = 0
                for item in products:
                    count += 1
                    #print(item["name"])
                    naziv_proizvoda = f"{count}.{item["name"]}"
                    print(naziv_proizvoda)
                try:
                    id_proizvoda = int(input("Odaberite broj pored proizvoda: "))
                    proizvod_dict = products[id_proizvoda - 1]
                    flag = False
                except Exception as e:
                    print(f"Dogodila se greška - {e}")
                    print("*" *20)
                    print("Pazite da odaberete broj koji je ponuđen lijevo od imena proizvoda.")
                    print("*" *20)

            # pretty print of a dictionary
            
            print(json.dumps(proizvod_dict, indent = 4))   # jer lista
            flag = True
            while flag: 
                try:
                    print("Odabrite stavku čiji unos želite promijeniti: ")
                    print("1.id")
                    print("2.name")
                    print("3.description")
                    print("4.price")
                    stavka = int(input("Odabrite broj pored stavke koju želite mijenjati: "))
                    keys = [key for key in products[id_proizvoda -1]]
                    
                    # unos nove vrijednosti u dictionary
                    if stavka == 1:
                        new_value = int(input("Unesite novu vrijednost stavke koju želite mijenjati: "))
                    elif stavka == 2:
                        new_value = input("Unesite novu vrijednost stavke koju želite mijenjati: ")
                    elif stavka == 3:
                        new_value = input("Unesite novu vrijednost stavke koju želite mijenjati: ")
                    elif stavka == 4:
                        new_value = int(input("Unesite novu vrijednost stavke koju želite mijenjati: "))

                    proizvod_dict[keys[stavka - 1]] = new_value
                    print("Pregled:", json.dumps(proizvod_dict, indent = 4), sep = "\n")
                    products[id_proizvoda - 1] = proizvod_dict
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





# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers: list)->None:
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
                vat_id = int(input("Unesite kupčev vat_id: "))
                new_dict = {
                    "name" : ime,
                    "email" : mejl,
                    "vat_id" : str(vat_id)
                }
                print(json.dumps(new_dict, indent = 4))
                customers.append(new_dict)
        except Exception as e:
            print("*" * 20)
            print(f"Dogodila se greška - {e}")
            print("Pazite da unesete tip podatka koji se očekuje za pojedinu stavku. ")
            print("*" * 20)

        # Za pregled: prikaži listu svih kupaca
        if odabir_akcije == "2":
            print("-"*110)
            print(f"id\tname\t\t\t\temail\t\t\t\t\t\t\tvat_id")
            print("-"*110)
            count = 0
            for item in customers:
                    count = count + 1
                    ime = item["name"]
                    mail = item["email"]
                    vat_id = item["vat_id"]
                    if len(ime) < 16:
                        print(f"{count}\t{ime}\t\t\t{mail}\t\t\t\t\t {vat_id}")
                    else:
                        print(f"{count}\t{ime}\t\t{mail}\t\t\t\t {vat_id}")
        if odabir_akcije == "3":
            flag = False
        
        
    


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers: list)->None:
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
            for item in offers:
                print_offer(item)

        elif choice == "2":
            try:
                dostupni_mjeseci = []
                for item in offers:
                    mjesec = int(item["date"][5:7])
                    dostupni_mjeseci.append(mjesec)
                    set_mjesec = set(dostupni_mjeseci)
                print(f"Podaci dostupni za sljedeće mjesece: {set_mjesec}")
                mjesec_unos = int(input("Unesite željeni mjesec od dostupnih: "))
                if mjesec_unos in set_mjesec:
                    date_list = []
                    for item in offers:
                        if item["date"][5:7] == str(mjesec):
                            date_list.append(item)
                    for offer in date_list:
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
                try:
                    offer_num_list = []
                    for offer in offers:
                        offer_num_list.append(offer["offer_number"])  # od 1 do kraja
                    # TODO try except blok i petlja (ako unese krivi broj)
                    print("Brojevi ponuda na raspolaganju: ", *offer_num_list)
                    izbor_broja_ponude = int(input("Unesite broj ponude: "))
                    print_offer(offers[izbor_broja_ponude - 1])  # za index liste offers moramo - 1
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


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer: dict)-> None: # funkcija ispisuje u konzolu, ali ne vraća ništa (prazna varijabla)
    # dict u parametru je rezultat offers[index]
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)
    # print(type(customers))   # <class 'list'>

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
