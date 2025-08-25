import requests
import json
import os
from telegramBot import send_telegram_message, BOT_TOKEN, CHAT_ID

SEEN_FILE = "seen.json"


def send_request(header, payload):
    # Envoi de la requête HTTP Get
    response = requests.get(payload["api"], headers=header, params={"location": payload["location"], "query": payload["query"]})
    if response.status_code == 200:
        seen = load_seen()
        new_messages = []
        for item in response.json().get("documents", []):
            # Use a unique identifier for the job (like ID or URL) instead of the entire dict
            job_id = item.get("id") or item.get("url") or str(hash(frozenset(item.items())))
            if job_id not in seen:
                message = cleanup_data(item, "jobup")
                new_messages.append(message)
                seen.add(job_id)
        save_seen(seen)
        if new_messages:
            # Concatène tous les messages en un seul bloc
            full_message = "\n".join(new_messages)
            send_telegram_message(full_message)
        return response.json()

    else:
        response.raise_for_status()
        print("Erreur lors de la requête:", response.status_code)

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(seen)), f, ensure_ascii=False, indent=2)

# Nettoyer les données a envoyer
def cleanup_data(data, source):
    if source == "jobup":
        message = "<b>Nouvelle offre d'emploi trouvée:</b>\n\n"
        message += f"🔹 <b>{data.get('title')}</b>\n"
        message += f"   <b>taux d'activité : </b>{data.get('employmentGrades')}\n"
        message += f"   📍 {data.get('place')}\n"
        message += f"   💼 {data.get('company', {}).get('name', 'N/A')}\n"
        message += f"   🗓️ {data.get('publicationDate')}\n"
        message += f"   🔗 <a href='https://www.jobup.ch/fr/emplois/detail/{data.get('id')}'>Voir l'offre</a>\n\n"
    return message

