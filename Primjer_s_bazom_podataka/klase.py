import json

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

class Customer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    name: str
    email: str 
    vat_id: str

    customer_id = Field(foreign_key = "")

    offer_id = list("Customer") = Rela

    products: list("Product") = Relationship(back_populates = "customers")

class Product(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    name: str 
    description: str 
    price: float


    
    customers: Customer = Relationship(back_populates = "products")

class Offer(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    customer_name: str
    date: str
    #items:  #list["Product"] = Relationship(back_populates="offer")
    sub_total: float  # zbroj svih (item * quantity)
    tax: float  # izračunati porez kao % od prethodne stavke
    total: float   # subtotal + tax
    

    proizvodi = list["CustomerProductLink"] = Relationship(back_populates="product_id")

    # product_id: Field(foreign_key = "product.id")  # nakon dodatka ove linije baca grešku

class CustomerProductLink(SQLModel, table = True):
    """ ovdje printa print_offer() funkcija """
    __tablename__ = "customer_product"
    product_id: int = Field(foreign_key = "product.id", primary_key = True)
    customer_id: int = Field(foreign_key = "customer.id", primary_key = True)
    offer_id: int = Field(foreign_key = "offer.id")
    quantity: int
    item_total: int
    #  u tablici offer:
    # subtotal: float  # ukupna cijena (price * quantity)
    # tax: float   # % od subtotal
    # total: float



    






 