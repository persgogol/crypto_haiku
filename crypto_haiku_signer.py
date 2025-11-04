import hashlib
import random

haiku_templates = [
    ["Ветви – код в тени,", "Бит за битом – осень,", "Шифрует судьбу."],
    ["Под звёздами – ключ,", "По ветру крипто-сказ,", "Тайна блокчейна."],
    ["Ночь и цифра, шум…", "Секреты тихих строк", "Восход алгоритма."]
]

def generate_haiku():
    template = random.choice(haiku_templates)
    return "\n".join(template)

def sign_haiku(haiku):
    sha = hashlib.sha256(haiku.encode('utf-8')).hexdigest()
    return sha

if __name__ == "__main__":
    haiku = generate_haiku()
    signature = sign_haiku(haiku)
    print("--- Crypto Haiku ---\n" + haiku)
    print(f"Signature (SHA-256): {signature}")
