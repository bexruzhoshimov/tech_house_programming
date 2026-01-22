import datetime
import language
import storage
import utils

utils = utils.Utils()
storage = storage.Storage()

def reports_menu(data):
    while True:
        utils.clear()
        print(language.t("reports_title"))
        print()
        print("1. " + language.t("report_sales_summary"))
        print("2. " + language.t("report_top_products"))
        print("3. " + language.t("report_low_stock"))
        print("4. " + language.t("report_membership"))
        print("5. " + language.t("report_delivery_pickup"))
        print("6. " + language.t("report_today"))
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
            sales_summary(data)
        elif choice == 2:
            top_selling_products(data)
        elif choice == 3:
            low_stock_products(data)
        elif choice == 4:
            membership_usage(data)
        elif choice == 5:
            delivery_vs_pickup(data)
        elif choice == 6:
            today_orders_and_revenue(data)


def sales_summary(data):
    orders = data.get("orders", [])
    total = len(orders)
    completed = 0
    pending = 0
    cancelled = 0
    revenue_completed = 0
    revenue_non_cancelled = 0
    for o in orders:
        status = o.get("status")
        if status == "Completed":
            completed += 1
            revenue_completed += o.get("total", 0)
        elif status == "Pending":
            pending += 1
        elif status == "Cancelled":
            cancelled += 1
        if status != "Cancelled":
            revenue_non_cancelled += o.get("total", 0)
    utils.clear()
    print(language.t("report_sales_summary"))
    print()
    print(language.t("total_orders") + ": " + str(total))
    print(language.t("completed_orders") + ": " + str(completed))
    print(language.t("pending_orders") + ": " + str(pending))
    print(language.t("cancelled_orders") + ": " + str(cancelled))
    print(language.t("revenue") + " (" + language.t("completed_orders") +
          "): " + utils.money(revenue_completed))
    print(language.t("revenue") + " (" + language.t("total_orders") + " - " +
          language.t("cancelled_orders") + "): " + utils.money(revenue_non_cancelled))
    utils.pause(language.t("press_enter"))


def top_selling_products(data):
    orders = data.get("orders", [])
    counts = {}
    names = {}
    for o in orders:
        if o.get("status") == "Cancelled":
            continue
        for it in o.get("items", []):
            pid = it.get("product_id")
            qty = it.get("qty", 0)
            if not pid:
                continue
            counts[pid] = counts.get(pid, 0) + qty
            if pid not in names:
                names[pid] = it.get("name", pid)
    if not counts:
        utils.clear()
        print(language.t("report_top_products"))
        print()
        print(language.t("top_nothing"))
        utils.pause(language.t("press_enter"))
        return
    ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top = ordered[:5]
    utils.clear()
    print(language.t("report_top_products"))
    print()
    rank = 1
    for pid, qty in top:
        p = storage.find_product(data, pid)
        name = names.get(pid, pid)
        if p and p.get("name"):
            name = p.get("name")
        print(str(rank) + ") " + str(name) + " - " + str(qty))
        rank += 1
    utils.pause(language.t("press_enter"))


def low_stock_products(data):
    threshold = 5
    products = []
    for p in data.get("products", []):
        if p.get("status") == "active" and p.get("stock", 0) <= threshold:
            products.append(p)
    utils.clear()
    print(language.t("report_low_stock"))
    print()
    if not products:
        print(language.t("low_stock_none"))
        utils.pause(language.t("press_enter"))
        return
    for p in products:
        line = p.get("name", "") + " | " + \
            language.t("product_stock") + ": " + str(p.get("stock", 0))
        print("- " + line)
    utils.pause(language.t("press_enter"))


def membership_usage(data):
    orders = data.get("orders", [])
    counts = {}
    for o in orders:
        if o.get("status") == "Cancelled":
            continue
        m = o.get("membership", "Bronze")
        counts[m] = counts.get(m, 0) + 1
    utils.clear()
    print(language.t("report_membership"))
    print()
    if not counts:
        print(language.t("top_nothing"))
        utils.pause(language.t("press_enter"))
        return
    for name in sorted(counts.keys()):
        print("- " + name + ": " + str(counts.get(name, 0)))
    utils.pause(language.t("press_enter"))


def delivery_vs_pickup(data):
    orders = data.get("orders", [])
    delivery_count = 0
    pickup_count = 0
    delivery_revenue = 0
    pickup_revenue = 0
    for o in orders:
        if o.get("status") == "Cancelled":
            continue
        method = o.get("delivery_method")
        if method == "Delivery":
            delivery_count += 1
            delivery_revenue += o.get("total", 0)
        else:
            pickup_count += 1
            pickup_revenue += o.get("total", 0)
    utils.clear()
    print(language.t("report_delivery_pickup"))
    print()
    print(language.t("delivery_orders") + ": " + str(delivery_count) +
          " | " + language.t("revenue") + ": " + utils.money(delivery_revenue))
    print(language.t("pickup_orders") + ": " + str(pickup_count) +
          " | " + language.t("revenue") + ": " + utils.money(pickup_revenue))
    utils.pause(language.t("press_enter"))


def today_orders_and_revenue(data):
    today = datetime.date.today().strftime("%Y-%m-%d")
    orders = data.get("orders", [])
    today_orders = []
    for o in orders:
        if str(o.get("date", "")).startswith(today):
            today_orders.append(o)
    total = len(today_orders)
    revenue = 0
    for o in today_orders:
        if o.get("status") != "Cancelled":
            revenue += o.get("total", 0)
    utils.clear()
    print(language.t("report_today"))
    print()
    print(language.t("today") + ": " + today)
    print(language.t("total_orders") + ": " + str(total))
    print(language.t("revenue") + ": " + utils.money(revenue))
    utils.pause(language.t("press_enter"))
