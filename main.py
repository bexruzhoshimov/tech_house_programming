import admin
import utils
import storage
import language
import customer
import auth


def select_language_start(data):
    while True:
        utils.clear()
        print(language.t("welcome"))
        print()
        print(language.t("select_language"))
        print("1. " + language.t("language_uz"))
        print("2. " + language.t("language_en"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print()
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 1:
            code = "uz"
        else:
            code = "en"
        if "settings" not in data or not isinstance(data.get("settings"), dict):
            data["settings"] = {}
        data["settings"]["language"] = code
        storage.save_data(data)
        language.set_language(code)
        return


def main():
    data = storage.load_data()
    language.load()
    saved = data.get("settings", {}).get("language", "en")
    if saved not in ["en", "uz"]:
        saved = "en"
    language.set_language(saved)
    select_language_start(data)
    while True:
        data = storage.load_data()
        user = auth.login(data)
        if not user:
            return
        role = user.get("role")
        if role == "admin":
            admin.run_admin(data, user.get("username"))
        else:
            customer.run_customer(data, user.get("username"))
        utils.clear()
        print(language.t("menu_logout"))
        utils.pause(language.t("press_enter"))


if __name__ == "__main__":
    main()
