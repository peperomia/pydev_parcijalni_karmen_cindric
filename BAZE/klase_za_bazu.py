import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

# LINK model mora biti definiran prije ostalih modela, inače baca grešku da 
# funkcija imena kao LINK model nije definirana (Ne može se Link tablica staviti na kraj, iza ostalih modela)
class OfferProductLink(SQLModel, table = True):
    """ ovdje printa def display_items_in_offers(offers) funkcija """
    __tablename__ = "offer_product"
    id: int = Field(default = None, primary_key=True)
    offer_id: int = Field(foreign_key = "offer.id")
    product_id: int = Field(foreign_key = "product.id")
    quantity: int
    item_total: float
    
    #  u tablici offer:
    # subtotal: float  # ukupna cijena (price * quantity)
    # tax: float   # % od subtotal
    # total: float


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

    offers: list["Offer"]= Relationship(back_populates = "products", link_model = OfferProductLink)

class Offer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    customer_name: str 
    date: date
    sub_total: float  # zbroj svih (item * quantity)
    tax: float  # izračunati porez kao % od prethodne stavke
    total: float   # subtotal + tax
    
    products: list["Product"] = Relationship(back_populates="offers", link_model=OfferProductLink)

    
    




    






 