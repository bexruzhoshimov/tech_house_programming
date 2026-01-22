import auth
import utils
import language
import reports
import storage

storage = storage.Storage()
utils = utils.Utils()
auth = auth.Auth()


def run_admin(data, username):
    while True:
        utils.clear()
        print(language.t("menu_admin_title"))
        print()
        print("1. " + language.t("admin_products_title"))
        print("2. " + language.t("menu_reports"))
        print("3. " + language.t("menu_manage_orders"))
        print("4. " + language.t("menu_settings"))
        print("0. " + language.t("menu_logout"))
        choice = utils.menu_choice(language.t("choose_option"), 4)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            exit()
        if choice == 1:
            product_management_menu(data)
        elif choice == 2:
            reports.reports_menu(data)
        elif choice == 3:
            orders_management_menu(data)
        elif choice == 4:
            auth.settings_menu(data, username)


def product_management_menu(data):
    while True:
        utils.clear()
        print(language.t("admin_products_title"))
        print()
        print("1. " + language.t("add_product"))
        print("2. " + language.t("view_update_product"))
        print("3. " + language.t("delete_deactivate_product"))
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
            add_product_flow(data)
        elif choice == 2:
            update_product_flow(data)
        elif choice == 3:
            delete_deactivate_flow(data)


def add_product_flow(data):
    utils.clear()
    print(language.t("add_product"))
    print()
    name = utils.read_text(language.t("enter_product_name"))
    if not name:
        print()
        print(language.t("field_required"))
        utils.pause(language.t("press_enter"))
        return
    price = utils.read_float(language.t("enter_product_price"))
    if price is None or price <= 0:
        print()
        print(language.t("price_invalid"))
        utils.pause(language.t("press_enter"))
        return
    stock = utils.read_int(language.t("enter_product_stock"))
    if stock is None or stock < 0:
        print()
        print(language.t("stock_invalid"))
        utils.pause(language.t("press_enter"))
        return
    category_id = choose_category_admin(data)
    if category_id is None:
        return
    status = choose_status_admin()
    if status is None:
        return
    description = utils.read_text(language.t("enter_product_desc"))
    product_id = storage.next_product_id(data)
    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "category_id": category_id,
        "status": status,
        "description": description
    }
    data.get("products", []).append(product)
    storage.save_data(data)
    print()
    print(language.t("product_added"))
    utils.pause(language.t("press_enter"))


def update_product_flow(data):
    products = data.get("products", [])
    if not products:
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return
    while True:
        utils.clear()
        print(language.t("view_update_product"))
        print()
        for idx, p in enumerate(products, 1):
            line = p.get("name", "")
            line += " | " + utils.money(p.get("price", 0))
            line += " | " + language.t("product_stock") + \
                ": " + str(p.get("stock", 0))
            line += " | " + category_name(data, p.get("category_id"))
            line += " | " + (language.t("status_active") if p.get("status")
                             == "active" else language.t("status_inactive"))
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
        edit_product_menu(data, product)


def edit_product_menu(data, product):
    while True:
        utils.clear()
        print(language.t("update_menu_title"))
        print()
        print(language.t("product_name") + ": " + str(product.get("name", "")))
        print(language.t("product_price") + ": " +
              utils.money(product.get("price", 0)))
        print(language.t("product_stock") +
              ": " + str(product.get("stock", 0)))
        print(language.t("product_category") + ": " +
              category_name(data, product.get("category_id")))
        print(language.t("product_status") + ": " + (language.t("status_active")
              if product.get("status") == "active" else language.t("status_inactive")))
        print()
        print("1. " + language.t("update_field_name"))
        print("2. " + language.t("update_field_price"))
        print("3. " + language.t("update_field_stock"))
        print("4. " + language.t("update_field_category"))
        print("5. " + language.t("update_field_desc"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 6)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            new_name = utils.read_text(language.t("enter_product_name"))
            if not new_name:
                print(language.t("field_required"))
                utils.pause(language.t("press_enter"))
                continue
            product["name"] = new_name
        elif choice == 2:
            new_price = utils.read_float(language.t("enter_product_price"))
            if new_price is None or new_price <= 0:
                print(language.t("price_invalid"))
                utils.pause(language.t("press_enter"))
                continue
            product["price"] = new_price
        elif choice == 3:
            new_stock = utils.read_int(language.t("enter_product_stock"))
            if new_stock is None or new_stock < 0:
                print(language.t("stock_invalid"))
                utils.pause(language.t("press_enter"))
                continue
            product["stock"] = new_stock
        elif choice == 4:
            new_cid = choose_category_admin(data)
            if new_cid is None:
                continue
            product["category_id"] = new_cid
        elif choice == 5:
            new_desc = utils.read_text(language.t("enter_product_desc"))
            product["description"] = new_desc
        storage.save_data(data)
        print(language.t("product_updated"))
        utils.pause(language.t("press_enter"))


def delete_deactivate_flow(data):
    products = data.get("products", [])
    if not products:
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return
    while True:
        utils.clear()
        print(language.t("delete_deactivate_product"))
        print()
        for idx, p in enumerate(products, 1):
            line = p.get("name", "")
            line += " | " + category_name(data, p.get("category_id"))
            line += " | " + (language.t("status_active") if p.get("status")
                             == "active" else language.t("status_inactive"))
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
        delete_or_deactivate_menu(data, product)


def delete_or_deactivate_menu(data, product):
    while True:
        utils.clear()
        print(language.t("delete_or_deactivate"))
        print()
        print(language.t("product_name") + ": " + str(product.get("name", "")))
        print("1. " + language.t("delete"))
        print("2. " + language.t("deactivate"))
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
        if choice == 2:
            product["status"] = "inactive"
            storage.save_data(data)
            print(language.t("product_deactivated"))
            utils.pause(language.t("press_enter"))
            return
        if choice == 1:
            products = data.get("products", [])
            pid = product.get("id")
            data["products"] = [p for p in products if p.get("id") != pid]
            storage.remove_product_references(data, pid)
            storage.save_data(data)
            print(language.t("product_deleted"))
            utils.pause(language.t("press_enter"))
            return


def orders_management_menu(data):
    while True:
        orders = data.get("orders", [])
        utils.clear()
        print(language.t("manage_orders_title"))
        print()
        if not orders:
            print(language.t("order_list_empty"))
            utils.pause(language.t("press_enter"))
            return
        for idx, o in enumerate(orders, 1):
            line = o.get("id", "")
            line += " | " + o.get("username", "")
            line += " | " + o.get("date", "")
            line += " | " + o.get("status", "")
            line += " | " + utils.money(o.get("total", 0))
            print(str(idx) + ". " + line)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(orders))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        order = orders[choice - 1]
        order_details_admin(data, order)


def order_details_admin(data, order):
    while True:
        utils.clear()
        print(language.t("order_details"))
        print()
        print(language.t("order_id") + ": " + order.get("id", ""))
        print(language.t("username") + ": " + order.get("username", ""))
        print(language.t("order_date") + ": " + order.get("date", ""))
        print(language.t("order_status") + ": " + order.get("status", ""))
        print(language.t("total") + ": " + utils.money(order.get("total", 0)))
        print()
        print("1. " + language.t("change_status"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 1)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            change_order_status_flow(data, order)


def change_order_status_flow(data, order):
    statuses = data.get("order_statuses", [
                        "Pending", "Completed", "Cancelled"])
    while True:
        utils.clear()
        print(language.t("select_status"))
        print()
        for idx, s in enumerate(statuses, 1):
            print(str(idx) + ". " + s)
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), len(statuses))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        new_status = statuses[choice - 1]
        ok, message = apply_order_status_change(data, order, new_status)
        if not ok:
            print(message)
            utils.pause(language.t("press_enter"))
            return
        storage.save_data(data)
        print(language.t("order_updated"))
        utils.pause(language.t("press_enter"))
        return


def apply_order_status_change(data, order, new_status):
    old_status = order.get("status")
    if old_status == new_status:
        return True, ""
    if old_status != "Cancelled" and new_status == "Cancelled":
        restore_stock_from_order(data, order)
        order["status"] = new_status
        return True, ""
    if old_status == "Cancelled" and new_status != "Cancelled":
        ok = deduct_stock_for_order(data, order)
        if not ok:
            return False, language.t("stock_not_enough")
        order["status"] = new_status
        return True, ""
    order["status"] = new_status
    return True, ""


def restore_stock_from_order(data, order):
    for it in order.get("items", []):
        pid = it.get("product_id")
        qty = it.get("qty", 0)
        p = storage.find_product(data, pid)
        if p:
            p["stock"] = p.get("stock", 0) + qty


def deduct_stock_for_order(data, order):
    for it in order.get("items", []):
        pid = it.get("product_id")
        qty = it.get("qty", 0)
        p = storage.find_product(data, pid)
        if not p:
            return False
        if p.get("status") != "active":
            return False
        if qty > p.get("stock", 0):
            return False
    for it in order.get("items", []):
        pid = it.get("product_id")
        qty = it.get("qty", 0)
        p = storage.find_product(data, pid)
        if p:
            p["stock"] = p.get("stock", 0) - qty
            if p["stock"] < 0:
                p["stock"] = 0
    return True


def choose_category_admin(data):
    categories = data.get("categories", [])
    if not categories:
        print(language.t("no_products"))
        utils.pause(language.t("press_enter"))
        return None
    while True:
        utils.clear()
        print(language.t("choose_category"))
        print()
        for idx, c in enumerate(categories, 1):
            print(str(idx) + ". " + language.value(c.get("name")))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t(
            "choose_option"), len(categories))
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return None
        return categories[choice - 1].get("id")


def choose_status_admin():
    while True:
        utils.clear()
        print(language.t("choose_status"))
        print()
        print("1. " + language.t("status_active"))
        print("2. " + language.t("status_inactive"))
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
        if choice == 1:
            return "active"
        if choice == 2:
            return "inactive"


def category_name(data, category_id):
    cat = storage.find_category(data, category_id)
    if cat and cat.get("name"):
        return language.value(cat.get("name"))
    return "-"
