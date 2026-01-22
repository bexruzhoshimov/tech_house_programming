import admin
import utils
import storage
import language
import customer
import auth

auth = auth.Auth()
utils = utils.Utils()
storage = storage.Storage()

class LanguageStart:
    def run(self, data):
        while True:
            utils.clear()
            print(language.t("welcome"))
            print()
            print(language.t("select_language"))
            print("1. " + language.t("language_uz"))
            print("2. " + language.t("language_en"))

            choice = utils.read_text(language.t("choose_option")).strip()

            if choice not in ["1", "2"]:
                print(language.t("invalid_choice"))
                utils.pause(language.t("press_enter"))
                continue

            code = "uz" if choice == "1" else "en"

            if "settings" not in data or not isinstance(data.get("settings"), dict):
                data["settings"] = {}

            data["settings"]["language"] = code
            storage.save_data(data)
            language.set_language(code)
            return data


class AuthMenu:
    def run(self):
        while True:
            utils.clear()
            print(language.t("auth_menu_title"))
            print()
            print("1. " + language.t("menu_login"))
            print("2. " + language.t("register_title"))
            print("0. " + language.t("menu_back"))

            choice = utils.read_text(language.t("choose_option")).strip()

            if choice in ["0", "1", "2"]:
                return int(choice)

            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))


class Program:
    def __init__(self):
        self.data = storage.load_data()
        language.load()

        saved = self.data.get("settings", {}).get("language", "en")
        if saved not in ["en", "uz"]:
            saved = "en"
        language.set_language(saved)

        self.language_start = LanguageStart()
        self.auth_menu = AuthMenu()

    def run(self):
        self.data = self.language_start.run(self.data)

        while True:
            self.data = storage.load_data()

            action = self.auth_menu.run()
            if action == 0:
                return

            if action == 1:
                user = auth.login(self.data)
            else:
                user = auth.register(self.data)

            if not user:
                continue

            role = user.get("role")
            username = user.get("username")

            if role == "admin":
                admin.run_admin(self.data, username)
            else:
                customer.run_customer(self.data, username)

            utils.clear()
            print(language.t("menu_logout"))
            utils.pause(language.t("press_enter"))


if __name__ == "__main__":
    program = Program()
    program.run()
