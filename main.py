import json

#TODO: dodati type hinting na sve funkcije


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers, products, customers):
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
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
    ime_kupca = str(input("Unesite broj pored imena kupca: "))

    # unos datuma
    dan = input("Unesite koji je danas dan u mjesecu: ")
    datum = "2024-11-" + dan

    # odabir proizvoda -> PETLJA
    idd = []  # lista koja sakuplja id proizvoda (str) iz products
    kolicina_proizvoda = []  # lista koja sakuplja broj kupljenih komada (int) - positional u odnosu na idd listu
    while True:
        print("Odaberite proizvod")
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
        broj_proizvoda = input("Odaberite id broj proizvoda na sasvim lijevoj strani tablice: ")
        kolicina = int(input("Koliko komada tog proizvoda želite kupiti? Unesite broj: "))
        idd.append(broj_proizvoda)
        kolicina_proizvoda.append(kolicina)
        nastavak = input("Želite li nastaviti kupovati? (da/ne): ").lower()
        if nastavak == "ne":
            break
    kosarica_proizvoda = {"id" : idd,
                            "kolicina" : kolicina_proizvoda}
    print(kosarica_proizvoda)
    collected = {

    }




    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers
    pass


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    print("\nIzaberite opciju upravljanja proizvodima: ")
    print("1. Dodavanje novog proizvoda")
    print("2. Izmjena podataka postojećeg proizvoda")
    choice = input("Odabrana opcija: ")
    # TODO: petlja ako želi odabrati još jednu opciju upravljanja proizvodima (petlja: opet dodavanje ili izmjena)
    # products  
    if choice == "1":  
        print("Unesite detalje proizvoda: ")
        new_dict = {}
        new_dict["id"] += len(products) + 1
        new_dict["name"] = input("Unesite naziv proizvoda: ")
        new_dict["description"] = input("Unesite opis proizvoda")
        new_dict["price"] = round(float(input("Unesite cijenu proizvoda")), 1)
        products.append(new_dict)     #save_data() ima način "w"
        # save_data("products.json", products)  # ne spremati jer sprema u main() pri izlasku

    if choice == "2":
        print("Izaberite proizvod kojem želite izmijeniti podatke: ")
        count = 0
        for item in products:
            count += 1
            print(item["name"])
            naziv_proizvoda = f"{count}.{item["name"]}"
            print(naziv_proizvoda)
        id_proizvoda = input("Odaberite broj pored proizvoda: ")

        # pretty print of a dictionary
        proizvod_dict = products[id_proizvoda - 1]
        print(json.dumps(products[proizvod_dict], indent = 4))   # jer lista
        print("Odabrite stavku čiji unos želite promijeniti: ")
        print("1.id")
        print("2.name")
        print("3.description")
        print("4.price")
        stavka = input("Odabrite broj pored stavke koju želite mijenjati: ")
        keys = [key for key in products[id_proizvoda -1]]
        new_value = input("Unesite novu vrijednost stavke koju želite mijenjati: ")
        # unos nove vrijednosti u dictionary
        proizvod_dict[keys[stavka - 1]] = new_value
        products[id_proizvoda - 1] = proizvod_dict
        # save_data("products.json", products)  # ne spremati jer sprema u main() pri izlasku





# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers):
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    ime = input("Unesite ime kupca: ")
    mejl = input("Unesite email kupca: ")
    print("********************************")
    vat_id = input("Unesite kupčev vat_id: ")
    new_dict = {
        "name" : ime,
        "email" : mejl,
        "vat_id" : vat_id
    }
    customers.append(new_dict)
    # Za pregled: prikaži listu svih kupaca
    print("-"*110)
    print(f"id\tname\t\t\t\temail\t\t\t\t\t\t\tvat_id")
    print("-"*110)
    count = 0
    for item in customers:
            id = count + 1
            ime = item["name"]
            mail = item["email"]
            vat_id = item["vat_id"]
            if len(ime) < 16:
                print(f"{id}\t{ime}\t\t\t{mail}\t\t\t\t\t {vat_id}")
            else:
                print(f"{id}\t{ime}\t\t{mail}\t\t\t\t {vat_id}")
        
        
    


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    print("\nIzaberite pregled ponuda: ")
    print("1. sve ponude")
    print("2. ponude po mjesecu: ")
    print("3. pojedinačna ponuda")  # print_offer()
    choice = input("Odabranan opcija: ")
    # Prikaz relevantnih ponuda na temelju izbora
    if choice == "1":
        return offers
    elif choice == "2":
        mjesec = input("Unesite željeni mjesec: ")
        dostupni_mjeseci = []
        for item in offers:
            mjesec = item["date"][5:7]
            dostupni_mjeseci.append(mjesec)
            set_mjesec = set(dostupni_mjeseci)
        if mjesec in set_mjesec:
            date_list = []
            for item in offers:
                if item["date"][5:7] == mjesec:
                    date_list.append(item)
            for offer in date_list:
                return print_offer(offer)
        else:
            print(f"Za željeni mjesec nema podataka")
    elif choice == "3":
        offer_num_list = []
        for offer in offers:
             offer_num_list.append(offer["offer_number"])
        # TODO try except blok i petlja (ako unese krivi broj)
        print("Brojevi ponuda na raspolaganju: ", *offer_num_list)
        izbor_broja_ponude = int(input("Unesite broj ponude: "))
        return print_offer(offers[izbor_broja_ponude])
    else:
        print("Krivi izbor. Pokušajte ponovo.")
       


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
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
