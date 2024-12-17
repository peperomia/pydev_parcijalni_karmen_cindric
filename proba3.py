# Da li many to many tablica u SQL-u uvijek mora imati samo 3 stupca? 
# Ne, many-to-many tablica u SQL-u ne mora uvijek imati samo tri stupca. Iako je uobičajeno da takva tablica ima tri stupca 
# (dva za strane ključeve koji povezuju dvije druge tablice i jedan za primarni ključ), može imati i dodatne stupce za pohranu 
# dodatnih informacija. Na primjer, ako imate tablicu koja povezuje studente i predmete, možete dodati stupce za ocjene, datume 
# upisa ili druge relevantne podatke. Fleksibilnost SQL-a omogućuje prilagodbu tablica prema specifičnim potrebama aplikacije ili baze podataka.


import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

class Customer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    name: str
    email: str 
    vat_id: str

class Product(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    name: str 
    description: str 
    price: float

class Offer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    customer_name: str
    date: str
    #items:  #list["Product"] = Relationship(back_populates="offer")
    sub_total: float  # zbroj svih (item * quantity)
    tax: float  # izračunati porez kao % od prethodne stavke
    total: float   # subtotal + tax

    # product_id: Field(foreign_key = "product.id")  # nakon dodatka ove linije baca grešku

class CustomerProductLink(SQLModel, table = True):
    """ ovdje printa print_offer() funkcija """
    __tablename__ = "customer_product"
    product_id: int = Field(foreign_key = "product.id", primary_key = True)
    customer_id: int = Field(foreign_key = "customer.id", primary_key = True)
    offer_id: int = Field(foreign_key="offer.id", primary_key = True)
    quantity: int
    item_total: int
    #  u tablici offer:
    # subtotal: float  # ukupna cijena (price * quantity)
    # tax: float   # % od subtotal
    # total: float



    

engine = create_engine("sqlite:///parcijalaDB.db")
SQLModel.metadata.create_all(engine)




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


customers = load_data(CUSTOMERS_FILE)
# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers: list)->None:
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za pregled: prikaži listu svih kupaca
    customer_list = []
    for item in customers:
            ime = item["name"]
            mail = item["email"]
            vat_id = item["vat_id"]
            customer = Customer(name = ime, email = mail, vat_id = vat_id)
            customer_list.append(customer)
    return customer_list

            # if len(ime) < 16:
            #     print(f"{count}\t{ime}\t\t\t{mail}\t\t\t\t\t {vat_id}")
            # else:
            #     print(f"{count}\t{ime}\t\t{mail}\t\t\t\t {vat_id}")

# print(manage_customers(customers))


offers = load_data(OFFERS_FILE)
def display_offers(offers: list)->None:
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    offer_list = []
    items_list = []
    for offer in offers:
        customer_name = offer["customer"]
        date = offer["date"]
        items = offer["items"]  # another list of dicts->  petlja?
        for item in items:
            product_id = item["product_id"]
            name = item["product_name"]
            description = item["description"]
            price = item["price"]
            quantity = item["quantity"]
            item_total = item["item_total"]  # price * quantity za taj item
            with Session(engine) as session:
                #print("ušlo u 'with Session'")  # OK, radi linija
                statement = select(Customer).where(Customer.name == "Alice Johnson")
                result = session.exec(statement).first()
                #print(result.id, "ušlo u 'with Session'") # OK, radi linija
                customer_id = result.id
                #print(customer_id, "customer_id ušlo u 'with Session'")  # OK, radi linija
                #print(result.id) # OK, radi linija
                item_bought = CustomerProductLink(product_id = product_id, quantity = quantity, customer_id = customer_id, item_total = item_total)
                items_list.append(item_bought)

        sub_total = offer["sub_total"]
        tax = offer["tax"]
        total = offer["total"]
        offer_single = Offer(customer_name=customer_name, date = date, sub_total = sub_total, tax=tax, total = total)
        offer_list.append(offer_single)
        
    return offer_list



# ---------------------------------------------------------------------
# items_bought = display_items_in_offers(offers)
# print("type(items_bought)", type(items_bought[0]))
# print(items_bought)
# print(items_bought[0])
# print(display_offers(offers)[0])
# print("type(display_offers)", type(display_offers(offers)[0]))
#---------------------------------------------------------------------

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
    

# rezultat_display_offers = display_offers(offers)
# # print( "rezultat_display_offers" ,rezultat_display_offers)
# print("DUŽINA rezultat_display_offers", len(rezultat_display_offers))
# print("TYPE rezultat_display_offers", type(rezultat_display_offers))
# print("TYPE rezultat_display_offers[1]", type(rezultat_display_offers[1]))
# print("LENGTH of member of rezultat_display_offers", "0=", len(rezultat_display_offers[0]), "1=", len(rezultat_display_offers[1]))  # 9 i 21, respectively




def get_names_from_offers(offers: list):
    """vadi imena iz liste offers, jer kupaca u većini slučajeva nema u customers.json"""
    customers_from_offers = []
    for item in offers:
        print(item)
        kupac = item["customer"] # nema nikakvih dodatnih podataka o kupcu, niti mail niti vat_id
        print(kupac)
        kupac_objekt = Customer(name = kupac, email = "", vat_id = "")
        customers_from_offers.append(kupac_objekt)
    return customers_from_offers

# print(get_names_from_offers(offers = offers))  # ovo radi OK







    

products = load_data(PRODUCTS_FILE)
def manage_products(products: list)-> None:  # novi podaci se spremaju u listu
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    product_list = []
    for item in products:
        name = item["name"]
        description = item["description"]
        price = item["price"]
        product_list.append(Product(name = name, description=description, price=price))
    return product_list

            
                
            
            

        
        

print(manage_products(products))

with Session(engine) as session:
    try:
        customer_list = manage_customers(customers)
        product_list = manage_products(products)
        for customer in customer_list:
            print(customer)
            session.add(customer)
        for product in product_list:
            session.add(product)
        
        session.commit()
    except Exception as e:
        print(e)
    
extra_customers = get_names_from_offers(offers = offers) 
# print(extra_customers[1].name, " ****************")

with Session(engine) as session:
    try:
        for customer in extra_customers:
            statement = select(Customer).where(Customer.name == customer.name)
            result = session.exec(statement).first()

            if not result:
                session.add(customer)
                print(customer, "added")
        session.commit()
    except Exception as e:
        print(e)

customer_name = "Tech Solutions"
customer_name_extra = "Alice Johnson"
with Session(engine) as session:
    statement = select(Customer).where(Customer.name == customer_name_extra)
    result = session.exec(statement).first()
    print(result)
    print(result.id)

# print("**********DISPLAY_OFFERS*****", display_offers(offers))
# print(display_offers(offers)[0])



def display_items_in_offers(offers):
    """pakira u klasu CustomerProductLink 
    artikle koje je kupio pojedini kupac"""
    items_list = []
    for offer in offers:
        offer_number = offer["offer_number"]
        customer_name = offer["customer"]
        print(customer_name)
        date = offer["date"]
        items = offer["items"]  # another list of dicts->  petlja?
        for item in items:
            product_id = item["product_id"]
            name = item["product_name"]
            description = item["description"]
            price = item["price"]
            quantity = item["quantity"]
            item_total = item["item_total"]  # price * quantity za taj item
            with Session(engine) as session:
                print("ušlo u 'with Session'")  # OK, radi linija
                statement = select(Customer).where(Customer.name == customer_name)
                result = session.exec(statement).first()
                print(result.id, "ušlo u 'with Session'") # OK, radi linija
                customer_id = result.id
                #print(customer_id, "customer_id ušlo u 'with Session'")  # OK, radi linija
                #print(result.id) # OK, radi linija
                item_bought = CustomerProductLink(product_id = product_id, quantity = quantity, customer_id = customer_id, item_total = item_total, offer_id = offer_number)
                items_list.append(item_bought)
    return items_list    

with Session(engine) as session:
    offers_row_list = display_offers(offers)
    for offer in offers_row_list:
        print(offer, "*******-*")
        session.add(offer)
        print("*******")

#-------------------do ovdje radi-----------------


    products_in_offers = display_items_in_offers(offers)
    for element in products_in_offers:
        print("*****ELEMENT*****", element)
        row = element
        print("row", row)
        session.add(row)
    session.commit()


