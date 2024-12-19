CREATE TABLE customer (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	email VARCHAR, 
	vat_id VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

CREATE TABLE offer (
	id INTEGER NOT NULL, 
	offer_number INTEGER NOT NULL, 
	customer_name VARCHAR NOT NULL, 
	date DATETIME NOT NULL, 
	sub_total FLOAT NOT NULL, 
	tax FLOAT NOT NULL, 
	total FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (offer_number), 
	FOREIGN KEY(customer_name) REFERENCES customer (name)
)

CREATE TABLE offeritem (
	id INTEGER NOT NULL, 
	offer_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	price FLOAT NOT NULL, 
	item_total FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(offer_id) REFERENCES offer (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
)



CREATE TABLE product (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR NOT NULL, 
	price FLOAT NOT NULL, 
	PRIMARY KEY (id)
)