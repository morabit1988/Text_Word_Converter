<<<<<<< HEAD


def is_pro_user():
    try:
        with open("license.key", "r") as f:
            key = f.read().strip()
        return key == "ABC123-PRO-LICENSE"  # Clé que tu fournis aux clients pro
    except FileNotFoundError:
=======


def is_pro_user():
    try:
        with open("license.key", "r") as f:
            key = f.read().strip()
        return key == "ABC123-PRO-LICENSE"  # Clé que tu fournis aux clients pro
    except FileNotFoundError:
>>>>>>> 25f230b2df4e1f41045a3770d62bc0440a339fce
        return False