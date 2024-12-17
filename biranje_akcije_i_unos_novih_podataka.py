from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select

from Primjer_s_bazom_podataka.klase import Customer, Product, Offer, CustomerProductLink

engine = create_engine("sqlite:///parcijalaDB_Modul.db")
#SQLModel.metadata.create_all(engine)

def print_customers():
    with Session(engine) as session:
        statement = select(Customer)
        results = session.exec(statement)
        for result in results:
            print(result)

#print_customers()



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
        flag = True
        while flag:
            print("Kreirajte novu ponudu")
            # Omogućite unos kupca
            print("Izaberite kupca iz liste kupaca: ")
            statement = select(Customer)
            result = session.exec(statement) 
            for customer in result:
                print(customer.id, customer.name)
            
            id_kupca = int(input("Unesite broj pored imena kupca: "))

            # unos datuma
            flag = True
            while flag:
                dan = input("Unesite koji je danas dan u mjesecu: ")
                if abs(int(dan)) < 31:
                    datum = "2024-12-" + dan
                    flag = False
                else:
                    print("Krivi datum. Broj treba biti između 1 i 31 (uključivo. )")

            # odabir proizvoda -> PETLJA
            idd = []
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
                idd.append(broj_proizvoda)  # lista s id brojevima kupljenih proizvoda
                kolicina_proizvoda.append(kolicina)  # lista s količinama kupljenih proizvoda (indexi odgovaraju onima u idd listi)
                nastavak = input("Želite li nastaviti kupovati? (da/ne): ").lower()
                if nastavak == "ne":
                    break

        try:
            collected_item_totals = []  # lista
            print("print idd", idd)
            print("kolicina_proizvoda", kolicina_proizvoda)
            for i in range(len(idd)):   # idd = lista s id brojevima kupljenih proizvoda
                print(i, "Ušlo u petlju len(idd)")
                statement = select(Product).where(Product.id == int(idd[i]))
                product_bought = session.exec(statement).first()  # bez first() printa mem adresu
                print("product_bought", product_bought)
                kolicina = kolicina_proizvoda[i]
                print("kolicina =", kolicina)                
                item_total = product_bought.price * kolicina
                print("item_total =", item_total)
                collected_item_totals.append(item_total)


                # item_dict = {}
                # item_dict["product_id"] = products[int(item) - 1]["id"]
                # item_dict["product_name"] = products[int(item) - 1]["name"]
                # item_dict["description"] = products[int(item) - 1]["description"]
                # item_dict["price"] = products[int(item) - 1]["price"]
                # item_dict["quantity"] = kolicina_proizvoda[idd.index(item)]
                # item_dict["item_total"] = products[int(item) - 1]["price"] * kolicina_proizvoda[idd.index(item)]
                
                # collected_items.append(item_dict)  # lista proizvoda koje je kupac stavio u košaricu (kupio)
        
            # Izračunajte sub_total, tax i total
        
            sub_total = sum(collected_item_totals)
            print("sub_total = ", sub_total)
            tax = round(float(sub_total * (0.1)), 1) # tax = 10% od sub_total
            print("tax = ", tax)
            total = sub_total + tax
            statement = select(Customer).where(Customer.id == id_kupca)
            result = session.exec(statement).first()
            print(result)
            ime_kupca = result.name
            print(ime_kupca)

            
            new_offer = Offer(customer_name=ime_kupca, date=datum, sub_total=sub_total, tax=tax, total=total)
            print(new_offer)
            session.add(new_offer)
            session.commit()
            with Session(engine) as session:
                
                new_offer_specs = CustomerProductLink(product_id=idd, customer_id=id_kupca, offer_id=)
        except Exception as e:
            print(f"Dogodila se greska - {e}")
            print("Pažljivo pročitajte upute prilikom unosa podataka i pazite da se uneseni brojevi za opciju nalaze među ponuđenima")
        nova_nova_ponuda = input("Želite li stvoriti još jednu novu ponudu? (da/ne) ")
        if nova_nova_ponuda != "da":
            flag = False

create_new_offer()


