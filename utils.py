import os


class Utils:
    def clear(self):
        cmd = "cls" if os.name == "nt" else "clear"
        os.system(cmd)

    def pause(self, message):
        input(message)

    def read_text(self, prompt):
        return input(prompt).strip()

    def read_int(self, prompt):
        try:
            return int(input(prompt).strip())
        except:
            return None

    def read_float(self, prompt):
        try:
            text = input(prompt).strip().replace(",", ".")
            return float(text)
        except:
            return None

    def menu_choice(self, prompt, max_choice):
        val = self.read_int(prompt)
        if val is None:
            return None
        if val < 0 or val > max_choice:
            return None
        return val

    def money(self, amount):
        try:
            return f"{float(amount):.0f} UZS"
        except:
            return str(amount)
