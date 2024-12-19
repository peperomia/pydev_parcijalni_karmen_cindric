# ovaj fajl je glavni i on krca bazu sa starim (postojećim) podacima
# ovo sve radi
#
# ---******************----*******----
#
#      Pitanje za Kevina: 
#  u funkcije.py morala sam staviti stvaranje engine-a i ime baze koja 
#  bi se trebala stvarati u ovom fajlu. Je li to u redu i može li drugačije, bolje?
# 
#  Napomena:  bazu ne stvara u paketu (ovo je sve u paketu) nego u folderu iznad (PYDEV_PARCIJALNI_KARMEN-CINDRIC)

import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

from klase_nove import Customer, Product, Offer, OfferProductLink

from funkcije_nove import *

engine = create_engine("sqlite:///parcijalaDB_Modul_NOVE_KLASE.db")
SQLModel.metadata.create_all(engine)


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"

offers = load_data(OFFERS_FILE)
products = load_data(PRODUCTS_FILE)
customers = load_data(CUSTOMERS_FILE)

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

with Session(engine) as session:
    offers_row_list = display_offers(offers)
    for offer in offers_row_list:
        print(offer, "*******-*")
        session.add(offer)
        print("*******")



    products_in_offers = display_items_in_offers(offers)
    for element in products_in_offers:
        print("*****ELEMENT*****", element)
        row = element
        print("row", row)
        session.add(row)
    session.commit()

