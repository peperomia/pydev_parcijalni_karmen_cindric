import json

with open("offers.json", "r") as file:
    lst = json.load(file)
# print(lst)
# dd = []
# for item in lst:
#     print(item["date"][5:7])  # svi su u jedanaestom mjesecu
#     dd.append(item["date"][5:7])
#     print(dd)
#     print("set", set(dd))
# print(*dd)

# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")  # bez ["name"] pored offer["customer"] radi
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


# for item in lst:
#     print_offer(item)
#     print("#############")
#     print(type(item["offer_number"]))
#     print(item["customer"])
#     print(item["date"])

#print("Brojevi ponuda na raspolaganju: ", *dd)

     
print("****************")

with open("products.json", "r") as file:
    products = json.load(file)
    print(products)
    print(type(products))  # list
    print(len(products))  # 15 products originally

# print("Unesite detalje proizvoda: ")
# new_dict = {}
# new_dict["id"] = len(products) + 1
# new_dict["name"] = input("Unesite naziv proizvoda: ")
# new_dict["description"] = input("Unesite opis proizvoda: ")
# new_dict["price"] = round(float(input("Unesite cijenu proizvoda: ")), 1)
# products.append(new_dict)
# print(new_dict)

def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# save_data("proba.json", new_dict)

# count = 0
# for item in products:
#     count += 1
#     print(item["name"])
#     naziv_proizvoda = f"{count}.{item["name"]}"
#     print(naziv_proizvoda)

# pretty print of a dictionary
print(json.dumps(products[1], indent = 4))
        
proizv = products[1]
keys = [key for key in proizv.keys()]
print(keys)
print(type(keys))
print(proizv[keys[1]])

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

customers = load_data("customers.json")
print(type(customers))
print(len(customers))
print(json.dumps(customers, indent = 4))

names_list = []
count = 0
for item in customers:
    count += 1
    name = str(count) + "." + item["name"]
    names_list.append(name)
print(*names_list, sep = "\n")

# dan = input("Unesite koji je danas dan u mjesecu: ")
# datum = "2024-11-" + dan
# print(datum)

for item in customers: 
        ime = item["name"]
        mail = item["email"]
        vat_id = item["vat_id"]
        print(f"{ime}\t\t\t{mail}\t\t\t {vat_id}")
print(len("Future Solutions"))

### ----------------- ISPIS KUPACA
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

### ----------------- ISPIS 
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
    print("111. Ne želim više kupovati. ")
    print("-"*110)
    print()
    broj_proizvoda = input("Odaberite id broj proizvoda na sasvim lijevoj strani tablice: ")
    kolicina = int(input("Koliko komada tog proizvoda želite kupiti? Unesite broj: "))
    idd.append(broj_proizvoda)
    kolicina_proizvoda.append(kolicina)
    nastavak = input("Želite li nastaviti kupovati? (da/ne): ").lower()
    if nastavak == "ne":
        break
print(id)

kosarica_proizvoda = {"id" : idd,
                        "kolicina" : kolicina_proizvoda}
#cijena =

print(kosarica_proizvoda)
collected_items = []  # lista
for item in idd:
    item_dict = products[int(item) - 1]
    item_dict["quantity"] = kolicina_proizvoda[idd.index(item)]
    item_dict["item_total"] = products[int(item) - 1]["price"] * kolicina_proizvoda[idd.index(item)]
    item_dict["product_id"] = item_dict.pop("id")
    item_dict["product_name"] = item_dict.pop("name")

    collected_items.append(item_dict)

print(collected_items)
final_dict = {
    "offer_number" : offer
}

print(final_dict)


    
    
    