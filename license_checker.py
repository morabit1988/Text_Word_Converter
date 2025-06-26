

def is_pro_user():
    try:
        with open("license.key", "r") as f:
            key = f.read().strip()
        return key == "ABC123-PRO-LICENSE"  # Clé que tu fournis aux clients pro
    except FileNotFoundError:
        return False