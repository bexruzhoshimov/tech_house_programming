import os

def clear():#konsolni tozalaydi
    cmd = "cls" if os.name == "nt" else "clear"
    os.system(cmd)

def pause(message): #toxtab turad
    input(message)

def read_text(prompt):
    return input(prompt).strip()

def read_int(prompt):#butn son kiritish uchun
    try:
        return int(input(prompt).strip())
    except:
        return None

def read_float(prompt):
    try:
        text = input(prompt).strip().replace(",", ".")
        return float(text)
    except:
        return None

def menu_choice(prompt, max_choice):#menuni tanlash
    val = read_int(prompt)
    if val is None:
        return None
    if val < 0 or val > max_choice:
        return None
    return val

def money(amount):#pulni yaxlitlab olsh uchn
    try:
        return f"{float(amount):.0f} UZS"
    except:
        return str(amount)
