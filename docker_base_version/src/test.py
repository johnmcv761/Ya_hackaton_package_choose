import requests

data = {"orderId": "unique_order_id",
 "items": [
    {"sku": "unique_sku_1", "count": 10, "a": 20, "b": 30, "c": 5,
     "weight": 7.34, "type": [2]},
   ]
}


r = requests.get("http://localhost:8000/pack", json=data)

print(r.json())