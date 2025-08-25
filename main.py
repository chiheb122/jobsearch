from metier.search import send_request



HEADERS = {"User-Agent": "Mozilla/5.0 (JobWatchLocal/0.1; +contact: you@example.com)"}



# exemple de payload pour une recherche
PAYLOAD = {
    "api": "https://job-search-api.jobup.ch/search",
    "query": "informatique",
    "location": "Genève",
}


if __name__ == "__main__":
    send_request(HEADERS, PAYLOAD)
