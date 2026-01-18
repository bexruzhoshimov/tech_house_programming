import language
import storage
import utils


def login(data):
    attempts = 3
    while attempts > 0:
        utils.clear()
        print(language.t("login_title"))
        print()
        username = utils.read_text(language.t("username") + ": ")
        password = utils.read_text(language.t("password") + ": ")
        user = storage.find_user(data, username)
        if user and user.get("password") == password:
            storage.ensure_user_lists(data, username)
            storage.save_data(data)
            utils.clear()
            return user
        attempts -= 1
        utils.clear()
        print(language.t("login_failed"))
        if attempts > 0:
            print(language.t("login_attempts_left", n=attempts))
            utils.pause(language.t("press_enter"))
    utils.clear()
    print(language.t("login_locked"))
    utils.pause(language.t("press_enter"))
    return None


def change_password(data, username):
    user = storage.find_user(data, username)
    utils.clear()
    print(language.t("change_password"))
    print()
    if not user:
        utils.pause(language.t("press_enter"))
        return
    old = utils.read_text(language.t("enter_old_password"))
    if old != user.get("password"):
        print(language.t("wrong_old_password"))
        utils.pause(language.t("press_enter"))
        return
    new = utils.read_text(language.t("enter_new_password"))
    if not new:
        print(language.t("field_required"))
        utils.pause(language.t("press_enter"))
        return
    confirm = utils.read_text(language.t("confirm_new_password"))
    if new != confirm:
        print(language.t("password_mismatch"))
        utils.pause(language.t("press_enter"))
        return
    user["password"] = new
    storage.save_data(data)
    print(language.t("password_changed"))
    utils.pause(language.t("press_enter"))


def change_language(data):
    while True:
        utils.clear()
        print(language.t("change_language"))
        print()
        print("1. " + language.t("language_uz"))
        print("2. " + language.t("language_en"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        code = "uz" if choice == 1 else "en"
        data.setdefault("settings", {})["language"] = code
        language.set_language(code)
        storage.save_data(data)
        print(language.t("saved"))
        utils.pause(language.t("press_enter"))
        return


def settings_menu(data, username):
    while True:
        utils.clear()
        print(language.t("settings_title"))
        print()
        print("1. " + language.t("change_language"))
        print("2. " + language.t("change_password"))
        print("0. " + language.t("menu_back"))
        choice = utils.menu_choice(language.t("choose_option"), 2)
        if choice is None:
            print(language.t("invalid_choice"))
            utils.pause(language.t("press_enter"))
            continue
        utils.clear()
        if choice == 0:
            return
        if choice == 1:
            change_language(data)
        elif choice == 2:
            change_password(data, username)
