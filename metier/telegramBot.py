import os
import requests


def load_env_from_file(filename="data.env"):
    """Charge les variables d'environnement depuis un fichier .env"""
    env_vars = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

# Charger les variables depuis data.env
env_vars = load_env_from_file()
BOT_TOKEN = env_vars.get("BOT_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = env_vars.get("CHAT_ID") or os.getenv("CHAT_ID") 


def send_telegram_message(message):
    # Vérifier que les variables d'environnement sont définies
    if not BOT_TOKEN:
        print("Erreur: BOT_TOKEN n'est pas défini dans les variables d'environnement")
        return None

    if not CHAT_ID:
        print("Erreur: CHAT_ID n'est pas défini dans les variables d'environnement")
        return None

    print(f"Envoi du message vers chat_id: {CHAT_ID}")
    print(f"Token utilisé: {BOT_TOKEN[:10]}..." if len(BOT_TOKEN) > 10 else f"Token: {BOT_TOKEN}")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message envoyé avec succès!")
            return response.json()
        else:
            print(f"Erreur lors de l'envoi du message Telegram: {response.status_code}")
            print(f"Réponse: {response.text}")
            
            # Suggérer des solutions selon le code d'erreur
            if response.status_code == 404:
                print("Solutions possibles:")
                print("1. Vérifiez que le BOT_TOKEN est correct")
                print("2. Assurez-vous que le bot a été créé avec @BotFather")
                print("3. Vérifiez que le CHAT_ID est correct")
            elif response.status_code == 403:
                print("Le bot n'a pas l'autorisation d'envoyer des messages à ce chat")
                print("Assurez-vous d'avoir démarré une conversation avec le bot")
            
            return None
    except requests.RequestException as e:
        print(f"Erreur de connexion: {e}")
        return None

def test_bot_connection(bot_token):
    """Test la connexion avec le bot Telegram"""
    if not bot_token:
        print("BOT_TOKEN non défini")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            print("Bot trouvé:", bot_info["result"]["first_name"], f"(@{bot_info['result']['username']})")
            return True
        else:
            print(f"Erreur de connexion au bot: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Erreur de connexion: {e}")
        return False
    


if __name__ == "__main__":    
    print("=== Test de configuration Telegram ===")
    print(f"BOT_TOKEN défini: {'Oui' if BOT_TOKEN else 'Non'}")
    print(f"CHAT_ID défini: {'Oui' if CHAT_ID else 'Non'}")
    
    if BOT_TOKEN:
        print("\n=== Test de connexion au bot ===")
        if test_bot_connection(BOT_TOKEN):
            print("\n=== Envoi du message de test ===")
            message = "Test message from Job Search Bot"
            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
        else:
            print("Impossible de se connecter au bot. Vérifiez votre BOT_TOKEN.")
    else:
        print("\nPour configurer Telegram:")
        print("1. Créez un bot avec @BotFather sur Telegram")
        print("2. Définissez BOT_TOKEN dans vos variables d'environnement")
        print("3. Obtenez votre CHAT_ID et définissez-le dans les variables d'environnement")
