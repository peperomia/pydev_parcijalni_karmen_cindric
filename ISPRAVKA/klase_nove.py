import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

# LINK model mora biti definiran prije ostalih modela, inače baca grešku da 
# funkcija imena kao LINK model nije definirana (Ne može se Link tablica staviti na kraj, iza ostalih modela)
class OfferProductLink(SQLModel, table = True):
    """ ovdje printa def display_items_in_offers(offers) funkcija """
    __tablename__ = "offer_product"
    id: int = Field(default = None, primary_key=True)
    product_id: int = Field(foreign_key = "product.id")
    # customer_id: int = Field(foreign_key = "customer.id", primary_key = True)
    offer_id: int = Field(foreign_key = "offer.id")
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

    # offer_id: int = Field(foreign_key = "offer.id")

    # moguće je da 1 customer ima više ponuda, ali 1 offer ima samo 1 customer
    # offers: list["Offer"] = Relationship(back_populates = "offer.id")

    # products: list("Product") = Relationship(back_populates = "product.id")  # type: ignore # izlista SVE proizvode ikad kupljene, ne samo

class Product(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    name: str 
    description: str 
    price: float
    # offer_id: int = Field(foreign_key="offer.id")

    offers: list["Offer"]= Relationship(back_populates = "products", link_model = OfferProductLink)
    # customers: Customer = Relationship(back_populates = "products")

class Offer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    customer_name: str 
    date: str
    #items:  #list["Product"] = Relationship(back_populates="offer")
    sub_total: float  # zbroj svih (item * quantity)
    tax: float  # izračunati porez kao % od prethodne stavke
    total: float   # subtotal + tax
    
    # product_id:int = Field(foreign_key = "product.id")  # nakon dodatka ove linije baca grešku

    products: list["Product"] = Relationship(back_populates="offers", link_model=OfferProductLink)

    
    




    






 