import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select

from klase import Customer, Product, Offer, CustomerProductLink

engine = create_engine("sqlite:///parcijalaDB_Modul.db")
SQLModel.metadata.create_all(engine)

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

def print_offer(offer: dict)-> None: # funkcija ispisuje u konzolu, ali ne vraća ništa (prazna varijabla)
    # dict u parametru je rezultat offers[index]
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")
    
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