import configparser
conf = configparser.ConfigParser()
conf.read("./api/yoyo.ini", encoding="utf-8")

def getPrice():
    price = conf.get("price_info", "price")
    return price

def editPrice(price):
    conf.set("price_info", "price",price)
    price = conf.get("price_info", "price")
    with open("./api/yoyo.ini", "w") as f:
        conf.write(f)
    return price