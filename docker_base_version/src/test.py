import requests

data = {"orderId": "unique_order_id",
 "items": [
    {"sku": "unique_sku_1", "count": 1, "a": 2, "b": 3, "c": 5,
     "weight": 0.34, "type": [20, 960]},
    {"sku": "unique_sku_2", "count": 3, "a": 20, "b": 30, "c": 5,
    "weight": 7.34, "type": [320, 440]},
    {"sku": "unique_sku_3", "count": 2, "a": 20, "b": 30, "c": 5,
    "weight": 7.34, "type": [160, 100]},
    # {"sku": "unique_sku_4", "count": 6, "a": 20, "b": 30, "c": 5,
    # "weight": 7.34, "type": [40]},
   ]
}


r = requests.post("http://localhost:8000/pack", json=data)

print(r.json())