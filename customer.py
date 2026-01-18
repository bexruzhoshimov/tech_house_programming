import auth
import language
import storage
import utils


def run_customer(data, username):
    storage.ensure_user_lists(data, username)
    while True:
        utils.clear()
        user = storage.find_user(data, username)
        name = username
        if user and user.get("name"):
            name = language.value(user.get("name"))
        print(language.t("menu_customer_title") + " - " + name)
        print()
        print("1. " + language.t("menu_products"))
        print("2. " + language.t("menu_favorites"))
        print("3. " + language.t("menu_cart"))
        print("4. " + language.t("menu_orders"))
        print("5. " + language.t("menu_info"))
        print("6. " + language.t("menu_support"))
        print("7. " + language.t("menu_settings"))
        print("0. " + language.t("menu_logout"))
        choice = utils.menu_choice(language.t("choose_option"), 7)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            products_menu(data, username)
        elif choice == 2:
            favorites_menu(data, username)
        elif choice == 3:
            cart_menu(data, username)
        elif choice == 4:
            orders_menu(data, username)
        elif choice == 5:
            info_menu(data)
        elif choice == 6:
            support_screen(data)
        elif choice == 7:
            auth.settings_menu(data, username)


def products_menu(data, username):
    while True:
        utils.clear()
        print(language.t("menu_products"))
        print()
        print("1. " + language.t("view_by_category"))
        print("2. " + language.t("search_products"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            browse_by_category(data, username)
        elif choice == 2:
            search_products_flow(data, username)


def browse_by_category(data, username):
    categories = data.get("categories", [])
    if not categories:
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return
    while True:
        utils.clear()
        print(language.t("choose_category"))
        print()
        for idx, cat in enumerate(categories, 1):
            print(str(idx) + ". " + language.value(cat.get("name")))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(categories))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        category = categories[choice - 1]
        show_products_in_category(data, username, category.get("id"))


def show_products_in_category(data, username, category_id):
    products = []
    for p in data.get("products", []):
        if p.get("category_id") == category_id and p.get("status") == "active":
            products.append(p)
    if not products:
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return
    product_list_screen(data, username, products)


def search_products_flow(data, username):
    utils.clear()
    print(language.t("search_products"))
    print()
    keyword = utils.read_text(language.t("search_keyword"))
    if not keyword:
        print()
        print(language.t("enter_search_empty"))
        utils.pause(language.t("press_enter"))
        return
    keyword_low = keyword.lower()
    results = []
    for p in data.get("products", []):
        if p.get("status") == "active" and keyword_low in str(p.get("name", "")).lower():
            results.append(p)
    if not results:
        print()
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return
    product_list_screen(data, username, results,keyword_low)


def product_list_screen(data, username, products,keyword_low):
    while True:
        utils.clear()
        print(language.t("menu_products"))
        print(keyword_low)
        print()
        for idx, p in enumerate(products, 1):
            stock = p.get("stock", 0)
            stock_text = str(stock)
            if stock <= 0:
                stock_text = language.t("out_of_stock")
            line = p.get("name", "") + " | " + utils.money(p.get("price", 0)) + " | " + language.t("product_stock") + ": " + stock_text
            print(str(idx) + ". " + line)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(products))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        product = products[choice - 1]
        product_detail_screen(data, username, product.get("id"))


def product_detail_screen(data, username, product_id):
    while True:
        product = storage.find_product(data, product_id)
        if not product:
            utils.clear()
            print(language.t("no_products"))
            utils.pause(language.t("press_enter"))
            return
        utils.clear()
        print(language.t("product_details"))
        print()
        print(language.t("product_name") + ": " + str(product.get("name", "")))
        print(language.t("product_category") + ": " + category_name(data, product.get("category_id")))
        print(language.t("product_price") + ": " + utils.money(product.get("price", 0)))
        stock = product.get("stock", 0)
        if stock <= 0:
            print(language.t("product_stock") + ": " + language.t("out_of_stock"))
        else:
            print(language.t("product_stock") + ": " + str(stock))
        print(language.t("product_status") + ": " + status_text(product.get("status")))
        desc = product.get("description", "")
        if desc:
            print(language.t("product_desc") + ": " + desc)
        print()
        print("1. " + language.t("action_add_cart"))
        print("2. " + language.t("action_buy_now"))
        print("3. " + language.t("action_add_fav"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 3)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            add_to_cart_flow(data, username, product_id)
        elif choice == 2:
            buy_now_flow(data, username, product_id)
        elif choice == 3:
            add_to_favorites_flow(data, username, product_id)


def add_to_cart_flow(data, username, product_id):
    product = storage.find_product(data, product_id)
    if not product or product.get("status") != "active":
        print(language.t("product_inactive"))
        utils.pause(language.t("press_enter"))
        return
    stock = product.get("stock", 0)
    if stock <= 0:
        print(language.t("out_of_stock"))
        utils.pause(language.t("press_enter"))
        return
    qty = ask_quantity(stock)
    if qty is None:
        return
    cart = data.get("carts", {}).get(username, [])
    for item in cart:
        if item.get("product_id") == product_id:
            new_qty = item.get("qty", 0) + qty
            if new_qty > stock:
                print(language.t("quantity_exceeds_stock"))
                utils.pause(language.t("press_enter"))
                return
            item["qty"] = new_qty
            storage.save_data(data)
            print(language.t("cart_updated"))
            utils.pause(language.t("press_enter"))
            return
    cart.append({"product_id": product_id, "qty": qty})
    data["carts"][username] = cart
    storage.save_data(data)
    print(language.t("added_to_cart"))
    utils.pause(language.t("press_enter"))


def buy_now_flow(data, username, product_id):
    product = storage.find_product(data, product_id)
    if not product or product.get("status") != "active":
        print(language.t("product_inactive"))
        utils.pause(language.t("press_enter"))
        return
    stock = product.get("stock", 0)
    if stock <= 0:
        print(language.t("out_of_stock"))
        utils.pause(language.t("press_enter"))
        return
    qty = ask_quantity(stock)
    if qty is None:
        return
    items = [{"product_id": product_id, "qty": qty}]
    checkout_flow(data, username, items, "buy_now")


def add_to_favorites_flow(data, username, product_id):
    storage.ensure_user_lists(data, username)
    favs = data.get("favorites", {}).get(username, [])
    if product_id in favs:
        print(language.t("already_in_favorites"))
        utils.pause(language.t("press_enter"))
        return
    favs.append(product_id)
    data["favorites"][username] = favs
    storage.save_data(data)
    print(language.t("added_to_favorites"))
    utils.pause(language.t("press_enter"))


def favorites_menu(data, username):
    storage.ensure_user_lists(data, username)
    while True:
        fav_ids = data.get("favorites", {}).get(username, [])
        products = []
        for pid in fav_ids:
            p = storage.find_product(data, pid)
            if p:
                products.append(p)
        utils.clear()
        print(language.t("menu_favorites"))
        print()
        if not products:
            print(language.t("favorites_empty"))
            utils.pause(language.t("press_enter"))
            return
        for idx, p in enumerate(products, 1):
            stock = p.get("stock", 0)
            stock_text = str(stock)
            if stock <= 0:
                stock_text = language.t("out_of_stock")
            line = p.get("name", "") + " | " + utils.money(p.get("price", 0)) + " | " + language.t("product_stock") + ": " + stock_text
            print(str(idx) + ". " + line)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(products))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        product = products[choice - 1]
        favorite_item_menu(data, username, product.get("id"))


def favorite_item_menu(data, username, product_id):
    while True:
        product = storage.find_product(data, product_id)
        if not product:
            print(language.t("no_products"))
            utils.pause(language.t("press_enter"))
            return
        utils.clear()
        print(language.t("product_details"))
        print()
        print(language.t("product_name") + ": " + str(product.get("name", "")))
        print(language.t("product_price") + ": " + utils.money(product.get("price", 0)))
        print(language.t("product_stock") + ": " + str(product.get("stock", 0)))
        print()
        print("1. " + language.t("action_remove_fav"))
        print("2. " + language.t("action_add_cart"))
        print("3. " + language.t("action_buy_now"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 3)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            remove_favorite(data, username, product_id)
            return
        if choice == 2:
            add_to_cart_flow(data, username, product_id)
            return
        if choice == 3:
            buy_now_flow(data, username, product_id)
            return


def remove_favorite(data, username, product_id):
    favs = data.get("favorites", {}).get(username, [])
    if product_id in favs:
        favs = [x for x in favs if x != product_id]
        data["favorites"][username] = favs
        storage.save_data(data)
    print(language.t("removed_from_favorites"))
    utils.pause(language.t("press_enter"))


def cart_menu(data, username):
    storage.ensure_user_lists(data, username)
    while True:
        cart_items = data.get("carts", {}).get(username, [])
        utils.clear()
        print(language.t("menu_cart"))
        print()
        if not cart_items:
            print(language.t("cart_empty"))
            utils.pause(language.t("press_enter"))
            return
        display_items = []
        for it in cart_items:
            p = storage.find_product(data, it.get("product_id"))
            qty = it.get("qty", 0)
            if not p:
                name = "?"
                price = 0
                line_total = 0
                note = language.t("product_inactive")
            else:
                name = str(p.get("name", ""))
                price = p.get("price", 0)
                line_total = price * qty
                note = ""
                if p.get("status") != "active":
                    note = language.t("status_inactive")
                elif qty > p.get("stock", 0):
                    note = language.t("quantity_exceeds_stock")
            display_items.append({"product": p, "qty": qty, "line_total": line_total, "note": note, "product_id": it.get("product_id")})
        for idx, d in enumerate(display_items, 1):
            text = str(d.get("qty", 0)) + " x " + d.get("product", {}).get("name", "?")
            text = text + " | " + utils.money(d.get("line_total", 0))
            if d.get("note"):
                text = text + " | " + d.get("note")
            print(str(idx) + ". " + text)
        print()
        print("1. " + language.t("change_quantity"))
        print("2. " + language.t("remove_item"))
        print("3. " + language.t("checkout_title"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 3)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            change_cart_quantity(data, username, display_items)
        elif choice == 2:
            remove_cart_item(data, username, display_items)
        elif choice == 3:
            items = []
            for it in cart_items:
                items.append({"product_id": it.get("product_id"), "qty": it.get("qty", 0)})
            checkout_flow(data, username, items, "cart")


def change_cart_quantity(data, username, display_items):
    utils.clear()
    print(language.t("change_quantity"))
    print()
    for idx, d in enumerate(display_items, 1):
        name = d.get("product", {}).get("name", "?")
        print(str(idx) + ". " + name + " (" + str(d.get("qty", 0)) + ")")
    print("0. " + language.t("menu_back"))
    choice = utils.menu_choice(language.t("choose_option"), len(display_items))
    if choice is None:
        print()
        print(language.t("invalid_choice"))
        utils.pause(language.t("press_enter"))
        return
    utils.clear()
    if choice == 0:
        return
    selected = display_items[choice - 1]
    product = selected.get("product")
    if not product or product.get("status") != "active":
        print(language.t("product_inactive"))
        utils.pause(language.t("press_enter"))
        return
    stock = product.get("stock", 0)
    if stock <= 0:
        print(language.t("out_of_stock"))
        utils.pause(language.t("press_enter"))
        return
    qty = ask_quantity(stock)
    if qty is None:
        return
    cart_items = data.get("carts", {}).get(username, [])
    for it in cart_items:
        if it.get("product_id") == selected.get("product_id"):
            it["qty"] = qty
            storage.save_data(data)
            print(language.t("saved"))
            utils.pause(language.t("press_enter"))
            return


def remove_cart_item(data, username, display_items):
    utils.clear()
    print(language.t("remove_item"))
    print()
    for idx, d in enumerate(display_items, 1):
        name = d.get("product", {}).get("name", "?")
        print(str(idx) + ". " + name)
    print("0. " + language.t("menu_back"))
    choice = utils.menu_choice(language.t("choose_option"), len(display_items))
    if choice is None:
        print()
        print(language.t("invalid_choice"))
        utils.pause(language.t("press_enter"))
        return
    utils.clear()
    if choice == 0:
        return
    selected = display_items[choice - 1]
    cart_items = data.get("carts", {}).get(username, [])
    cart_items = [x for x in cart_items if x.get("product_id") != selected.get("product_id")]
    data["carts"][username] = cart_items
    storage.save_data(data)
    print(language.t("saved"))
    utils.pause(language.t("press_enter"))


def checkout_flow(data, username, items, source):
    storage.ensure_user_lists(data, username)
    valid_items = []
    for it in items:
        pid = it.get("product_id")
        qty = it.get("qty", 0)
        product = storage.find_product(data, pid)
        if not product:
            valid_items = None
            break
        if product.get("status") != "active":
            valid_items = None
            break
        if qty <= 0:
            valid_items = None
            break
        if qty > product.get("stock", 0):
            valid_items = None
            break
        valid_items.append({"product": product, "qty": qty})
    if valid_items is None or not valid_items:
        print(language.t("cart_invalid"))
        print(language.t("fix_cart"))
        utils.pause(language.t("press_enter"))
        return

    delivery_method, address = choose_delivery(data)
    if delivery_method is None:
        return

    membership = choose_membership(data)
    if membership is None:
        return

    promo = choose_promotion(data, valid_items)

    subtotal = 0
    for it in valid_items:
        subtotal += it["product"].get("price", 0) * it["qty"]

    promo_discount = calc_promo_discount(data, promo, valid_items)

    member_rule = data.get("membership_rules", {}).get(membership, {"discount_percent": 0, "free_delivery": False})
    member_percent = member_rule.get("discount_percent", 0)
    membership_discount = (subtotal - promo_discount) * (member_percent / 100)
    if membership_discount < 0:
        membership_discount = 0

    delivery_fee = 0
    if delivery_method == "Delivery":
        delivery_fee = data.get("settings", {}).get("delivery_fee", 30000)
        if member_rule.get("free_delivery"):
            delivery_fee = 0

    total = subtotal - promo_discount - membership_discount + delivery_fee
    if total < 0:
        total = 0

    confirm = confirm_order_screen(valid_items, subtotal, promo, promo_discount, membership, membership_discount, delivery_method, delivery_fee, total)
    if confirm is None:
        return

    if confirm is False:
        order = build_order(data, username, valid_items, delivery_method, address, membership, promo, subtotal, promo_discount, membership_discount, delivery_fee, total, "Cancelled")
        data.get("orders", []).append(order)
        storage.save_data(data)
        print(language.t("order_cancelled"))
        print(language.t("order_id") + ": " + order.get("id", ""))
        utils.pause(language.t("press_enter"))
        return

    order = build_order(data, username, valid_items, delivery_method, address, membership, promo, subtotal, promo_discount, membership_discount, delivery_fee, total, "Pending")
    data.get("orders", []).append(order)

    for it in valid_items:
        p = it["product"]
        p["stock"] = p.get("stock", 0) - it["qty"]
        if p["stock"] < 0:
            p["stock"] = 0

    if source == "cart":
        data["carts"][username] = []

    storage.save_data(data)
    utils.clear()
    print(language.t("order_created"))
    print_receipt(order)
    utils.pause(language.t("press_enter"))


def choose_delivery(data):
    while True:
        utils.clear()
        print(language.t("choose_delivery_method"))
        print()
        print("1. " + language.t("delivery"))
        print("2. " + language.t("pickup"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return None, None
        if choice == 1:
            address = utils.read_text(language.t("enter_address"))
            if not address:
                print()
                print(language.t("address_required"))
                utils.pause(language.t("press_enter"))
                continue
            return "Delivery", address
        if choice == 2:
            return "Pickup", ""


def choose_membership(data):
    memberships = list(data.get("membership_rules", {}).keys())
    if not memberships:
        return "Bronze"
    while True:
        utils.clear()
        print(language.t("choose_membership"))
        print()
        for idx, name in enumerate(memberships, 1):
            rule = data.get("membership_rules", {}).get(name, {})
            percent = rule.get("discount_percent", 0)
            free = rule.get("free_delivery")
            text = name + " (" + str(percent) + "%)"
            if free:
                text = text + " + " + language.t("delivery") + " " + language.t("free")
            print(str(idx) + ". " + text)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(memberships))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return None
        return memberships[choice - 1]


def choose_promotion(data, valid_items):
    promos = []
    for pr in data.get("promotions", []):
        if pr.get("active"):
            promos.append(pr)
    applicable = []
    for pr in promos:
        cid = pr.get("category_id")
        if not cid:
            applicable.append(pr)
        else:
            for it in valid_items:
                if it["product"].get("category_id") == cid:
                    applicable.append(pr)
                    break
    if not applicable:
        return None
    while True:
        utils.clear()
        print(language.t("choose_promotion"))
        print()
        print("0. " + language.t("no_promotion"))
        for idx, pr in enumerate(applicable, 1):
            name = language.value(pr.get("name", ""))
            percent = pr.get("discount_percent", 0)
            text = name + " (" + str(percent) + "%)"
            cid = pr.get("category_id")
            if cid:
                text = text + " - " + category_name(data, cid)
            print(str(idx) + ". " + text)
        choice = utils.menu_choice(language.t("choose_option"), len(applicable))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return None
        return applicable[choice - 1]


def calc_promo_discount(data, promo, valid_items):
    if not promo:
        return 0
    percent = promo.get("discount_percent", 0)
    if percent <= 0:
        return 0
    cid = promo.get("category_id")
    total = 0
    for it in valid_items:
        p = it["product"]
        if cid and p.get("category_id") != cid:
            continue
        total += p.get("price", 0) * it["qty"]
    return total * (percent / 100)


def confirm_order_screen(valid_items, subtotal, promo, promo_discount, membership, membership_discount, delivery_method, delivery_fee, total):
    while True:
        utils.clear()
        print(language.t("summary_title"))
        print()
        for it in valid_items:
            p = it["product"]
            qty = it["qty"]
            line_total = p.get("price", 0) * qty
            print(str(qty) + " x " + p.get("name", "") + " = " + utils.money(line_total))
        print()
        print(language.t("subtotal") + ": " + utils.money(subtotal))
        if promo:
            print(language.t("promo_discount") + ": -" + utils.money(promo_discount))
        else:
            print(language.t("promo_discount") + ": -" + utils.money(0))
        print(language.t("membership_discount") + ": -" + utils.money(membership_discount))
        if delivery_method == "Delivery":
            print(language.t("delivery_fee") + ": " + utils.money(delivery_fee))
        else:
            print(language.t("delivery_fee") + ": " + utils.money(0))
        print(language.t("total") + ": " + utils.money(total))
        print()
        print(language.t("confirm_order"))
        print("1. " + language.t("confirm"))
        print("2. " + language.t("cancel"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return None
        if choice == 2:
            return False
        if choice == 1:
            return True


def build_order(data, username, valid_items, delivery_method, address, membership, promo, subtotal, promo_discount, membership_discount, delivery_fee, total, status):
    order_id = storage.next_order_id(data)
    date = storage.now_str()
    items = []
    for it in valid_items:
        p = it["product"]
        qty = it["qty"]
        items.append({
            "product_id": p.get("id"),
            "name": p.get("name"),
            "qty": qty,
            "unit_price": p.get("price", 0)
        })
    promo_name = ""
    if promo:
        promo_name = language.value(promo.get("name", ""))
    return {
        "id": order_id,
        "username": username,
        "date": date,
        "status": status,
        "delivery_method": delivery_method,
        "address": address,
        "membership": membership,
        "promotion": promo_name,
        "subtotal": subtotal,
        "promo_discount": promo_discount,
        "membership_discount": membership_discount,
        "delivery_fee": delivery_fee,
        "total": total,
        "items": items
    }


def print_receipt(order):
    print()
    print(language.t("receipt_title"))
    print()
    print(language.t("order_id") + ": " + order.get("id", ""))
    print(language.t("order_date") + ": " + order.get("date", ""))
    print(language.t("order_status") + ": " + order.get("status", ""))
    print(language.t("order_items") + ":")
    for it in order.get("items", []):
        qty = it.get("qty", 0)
        name = it.get("name", "")
        line_total = it.get("unit_price", 0) * qty
        print("- " + str(qty) + " x " + name + " = " + utils.money(line_total))
    print(language.t("total") + ": " + utils.money(order.get("total", 0)))


def orders_menu(data, username):
    while True:
        user_orders = []
        for o in data.get("orders", []):
            if o.get("username") == username:
                user_orders.append(o)
        utils.clear()
        print(language.t("order_history"))
        print()
        if not user_orders:
            print(language.t("no_orders"))
            utils.pause(language.t("press_enter"))
            return
        for idx, o in enumerate(user_orders, 1):
            line = o.get("id", "") + " | " + o.get("date", "") + " | " + o.get("status", "") + " | " + utils.money(o.get("total", 0))
            print(str(idx) + ". " + line)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(user_orders))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        order_details_screen(user_orders[choice - 1])


def order_details_screen(order):
    utils.clear()
    print(language.t("order_details"))
    print()
    print(language.t("order_id") + ": " + order.get("id", ""))
    print(language.t("order_date") + ": " + order.get("date", ""))
    print(language.t("order_status") + ": " + order.get("status", ""))
    print(language.t("delivery") + ": " + order.get("delivery_method", ""))
    if order.get("delivery_method") == "Delivery":
        print(language.t("enter_address") + order.get("address", ""))
    print(language.t("choose_membership") + " " + order.get("membership", ""))
    if order.get("promotion"):
        print(language.t("promotions") + ": " + order.get("promotion"))
    print()
    print(language.t("order_items") + ":")
    for it in order.get("items", []):
        qty = it.get("qty", 0)
        name = it.get("name", "")
        unit = it.get("unit_price", 0)
        line_total = unit * qty
        print("- " + str(qty) + " x " + name + " = " + utils.money(line_total))
    print()
    print(language.t("total") + ": " + utils.money(order.get("total", 0)))
    utils.pause(language.t("press_enter"))


def info_menu(data):
    utils.clear()
    print(language.t("info_title"))
    print()
    print(language.t("membership_packages"))
    rules = data.get("membership_rules", {})
    for name in rules:
        rule = rules.get(name, {})
        percent = rule.get("discount_percent", 0)
        free = rule.get("free_delivery")
        text = "- " + name + ": " + str(percent) + "%"
        if free:
            text = text + ", " + language.t("delivery") + " " + language.t("free")
        print(text)
    print()
    print(language.t("promotions"))
    active = []
    for pr in data.get("promotions", []):
        if pr.get("active"):
            active.append(pr)
    if not active:
        print(language.t("no_active_promotions"))
    else:
        for pr in active:
            name = language.value(pr.get("name", ""))
            percent = pr.get("discount_percent", 0)
            text = "- " + name + " (" + str(percent) + "%)"
            if pr.get("category_id"):
                text = text + " - " + category_name(data, pr.get("category_id"))
            print(text)
    utils.pause(language.t("press_enter"))


def support_screen(data):
    utils.clear()
    print(language.t("support_title"))
    print()
    support = data.get("support", {})
    phone = support.get("phone", "")
    email = support.get("email", "")
    print(language.t("support_text", phone=phone, email=email))
    utils.pause(language.t("press_enter"))


def ask_quantity(max_stock):
    while True:
        qty = utils.read_int(language.t("enter_quantity"))
        if qty is None:
            print()
            print(language.t("quantity_invalid"))
            utils.pause(language.t("press_enter"))
            utils.clear()
            continue
        if qty == 0:
            return None
        if qty < 0:
            print()
            print(language.t("quantity_invalid"))
            utils.pause(language.t("press_enter"))
            utils.clear()
            continue
        if qty > max_stock:
            print()
            print(language.t("quantity_exceeds_stock"))
            utils.pause(language.t("press_enter"))
            utils.clear()
            continue
        return qty


def category_name(data, category_id):
    cat = storage.find_category(data, category_id)
    if cat and cat.get("name"):
        return language.value(cat.get("name"))
    return "-"


def status_text(status):
    if status == "active":
        return language.t("status_active")
    return language.t("status_inactive")
