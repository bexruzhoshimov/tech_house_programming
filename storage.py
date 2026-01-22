import json
import os
import datetime

DATA_FILE = "data.json"


class Storage:
    def __init__(self, data_file=DATA_FILE):
        self.DATA_FILE = data_file
        self._base = os.path.dirname(os.path.abspath(__file__))

    def _path(self, filename):
        return os.path.join(self._base, filename)

    def _read_json(self, filename):
        path = self._path(filename)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return None
                return json.loads(content)
        except:
            return None

    def save_data(self, data):
        path = self._path(self.DATA_FILE)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        data = self._read_json(self.DATA_FILE)
        if not self._is_valid(data):
            data = {}
            self.save_data(data)
            return data
        changed = self._ensure_structure(data)
        if changed:
            self.save_data(data)
        return data

    def _is_valid(self, data):
        if not isinstance(data, dict):
            return False
        needed = [
            "users",
            "products",
            "categories",
            "carts",
            "favorites",
            "orders",
            "order_statuses",
            "membership_rules",
            "promotions",
            "settings",
            "support",
            "counters"
        ]
        for k in needed:
            if k not in data:
                return False
        return True

    def _ensure_structure(self, data):
        changed = False
        demo = {}
        for k, v in demo.items():
            if k not in data:
                data[k] = v
                changed = True

        if not isinstance(data.get("users"), list) or not data.get("users"):
            data["users"] = demo["users"]
            changed = True
        if not isinstance(data.get("products"), list) or not data.get("products"):
            data["products"] = demo["products"]
            changed = True
        if not isinstance(data.get("categories"), list) or not data.get("categories"):
            data["categories"] = demo["categories"]
            changed = True
        if not isinstance(data.get("carts"), dict):
            data["carts"] = {}
            changed = True
        if not isinstance(data.get("favorites"), dict):
            data["favorites"] = {}
            changed = True
        if not isinstance(data.get("orders"), list):
            data["orders"] = []
            changed = True
        if not isinstance(data.get("order_statuses"), list) or not data.get("order_statuses"):
            data["order_statuses"] = demo["order_statuses"]
            changed = True
        if not isinstance(data.get("membership_rules"), dict) or not data.get("membership_rules"):
            data["membership_rules"] = demo["membership_rules"]
            changed = True
        if not isinstance(data.get("promotions"), list):
            data["promotions"] = demo["promotions"]
            changed = True
        if not isinstance(data.get("settings"), dict):
            data["settings"] = demo["settings"]
            changed = True
        if "language" not in data["settings"]:
            data["settings"]["language"] = demo["settings"]["language"]
            changed = True
        if "delivery_fee" not in data["settings"]:
            data["settings"]["delivery_fee"] = demo["settings"]["delivery_fee"]
            changed = True
        if not isinstance(data.get("support"), dict):
            data["support"] = demo["support"]
            changed = True
        if not isinstance(data.get("counters"), dict):
            data["counters"] = demo["counters"]
            changed = True

        return changed

    def ensure_user_lists(self, data, username):
        if "carts" not in data or not isinstance(data["carts"], dict):
            data["carts"] = {}
        if "favorites" not in data or not isinstance(data["favorites"], dict):
            data["favorites"] = {}
        if username not in data["carts"] or not isinstance(data["carts"].get(username), list):
            data["carts"][username] = []
        if username not in data["favorites"] or not isinstance(data["favorites"].get(username), list):
            data["favorites"][username] = []

    def find_user(self, data, username):
        for u in data.get("users", []):
            if u.get("username") == username:
                return u
        return None

    def find_product(self, data, product_id):
        for p in data.get("products", []):
            if p.get("id") == product_id:
                return p
        return None

    def find_category(self, data, category_id):
        for c in data.get("categories", []):
            if c.get("id") == category_id:
                return c
        return None

    def active_products(self, data):
        return [p for p in data.get("products", []) if p.get("status") == "active"]

    def active_promotions(self, data):
        promos = []
        for pr in data.get("promotions", []):
            if pr.get("active") is True:
                promos.append(pr)
        return promos

    def next_order_id(self, data):
        if "counters" not in data or not isinstance(data["counters"], dict):
            data["counters"] = {"order": 1000, "product": 1, "category": 1}
        n = data["counters"].get("order", 1000)
        data["counters"]["order"] = n + 1
        return "O-" + str(n)

    def next_product_id(self, data):
        if "counters" not in data or not isinstance(data["counters"], dict):
            data["counters"] = {"order": 1000, "product": 1, "category": 1}
        n = data["counters"].get("product", 1)
        data["counters"]["product"] = n + 1
        return "P" + str(n)

    def now_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def remove_product_references(self, data, product_id):
        carts = data.get("carts", {})
        if isinstance(carts, dict):
            for username in list(carts.keys()):
                items = carts.get(username)
                if isinstance(items, list):
                    carts[username] = [it for it in items if it.get(
                        "product_id") != product_id]

        favs = data.get("favorites", {})
        if isinstance(favs, dict):
            for username in list(favs.keys()):
                items = favs.get(username)
                if isinstance(items, list):
                    favs[username] = [pid for pid in items if pid != product_id]
