test = {"products": [{"product": 5, "quantity": 1}, {"product": 6, "quantity": 4}],
        "firstname": "Фридрех", "lastname": "Энгельс ", "phonenumber": "+767990", "address": "Москва"}

print(test["products"])

for product in test["products"]:
    print(product)
