import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class LeieneWebScraper:
    def __init__(self):
        self.base_url = "https://www.iene.mediaset.it"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_video_page(self, url):
        """Estrae i dati dal video principale della pagina"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            # Estrarre il titolo
            title = soup.find('h1')
            title_text = title.text.strip() if title else "N/A"

            # Estrarre la data
            date_elem = soup.find('generic', string=lambda x: x and 'aprile' in x or 'marzo' in x or 'maggio' in x)
            date_text = date_elem.text.strip() if date_elem else "N/A"

            # Estrarre la descrizione
            article = soup.find('article')
            description = ""
            if article:
                # Cerca il primo elemento generico che contiene il testo della descrizione
                desc_elem = article.find_all('generic')
                for elem in desc_elem:
                    text = elem.text.strip()
                    if len(text) > 50 and 'droga' in text.lower():
                        description = text
                        break

            # Estrarre l'immagine
            img = soup.find('article').find('img')
            image_url = img.get('src') if img else "N/A"

            return {
                'titolo': title_text,
                'data': date_text,
                'descrizione': description[:200] + '...' if len(description) > 200 else description,
                'immagine': image_url,
                'url': url
            }

        except requests.exceptions.RequestException as e:
            print(f"Errore nel fetch della pagina: {e}")
            return None

    def scrape_videos_list(self, url):
        """Estrae la lista di tutti i video dalla pagina"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            videos = []

            # Trova tutti i video nella lista "Ultime puntate"
            video_items = soup.find_all('li', limit=10)

            for item in video_items:
                link = item.find('a', href=True)
                if not link:
                    continue

                # Titolo
                title_elem = item.find('h2') or item.find('h3')
                title = title_elem.text.strip() if title_elem else "N/A"

                # Data
                date_elems = item.find_all('generic')
                date = date_elems[-1].text.strip() if date_elems else "N/A"

                # Durata
                duration_text = ""
                for elem in date_elems:
                    if 'min' in elem.text:
                        duration_text = elem.text.strip()
                        break

                # Descrizione
                desc_elems = item.find_all('generic')
                description = desc_elems[-1].text.strip() if len(desc_elems) > 2 else "N/A"

                # URL
                video_url = link['href']
                if not video_url.startswith('http'):
                    video_url = self.base_url + video_url

                # Immagine
                img = item.find('img')
                image_url = img.get('src') if img else "N/A"

                videos.append({
                    'titolo': title,
                    'data': date,
                    'durata': duration_text,
                    'descrizione': description[:150] + '...' if len(description) > 150 else description,
                    'immagine': image_url,
                    'url': video_url
                })

            return videos

        except requests.exceptions.RequestException as e:
            print(f"Errore nel fetch della pagina: {e}")
            return []

    def save_to_json(self, data, filename='iene_videos.json'):
        """Salva i dati in un file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Dati salvati in {filename}")

    def save_to_csv(self, videos, filename='iene_videos.csv'):
        """Salva i video in un file CSV"""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if videos:
                writer = csv.DictWriter(f, fieldnames=videos[0].keys())
                writer.writeheader()
                writer.writerows(videos)
        print(f"Dati salvati in {filename}")


# Utilizzo dello scraper
if __name__ == "__main__":
    scraper = LeieneWebScraper()

    # URL della pagina che abbiamo visto
    url = "https://www.iene.mediaset.it/video/le-iene-presentano-inside---droghe-e-nuove-droghe_1449288.shtml"

    print("=== WEB SCRAPING LE IENE ===\n")

    # Scraping del video principale
    print("Scaricamento dati del video principale...")
    video_principale = scraper.scrape_video_page(url)

    if video_principale:
        print("\n📹 VIDEO PRINCIPALE:")
        print(f"  Titolo: {video_principale['titolo']}")
        print(f"  Data: {video_principale['data']}")
        print(f"  Descrizione: {video_principale['descrizione']}")
        print(f"  Immagine: {video_principale['immagine'][:80]}...")

    # Scraping della lista di video
    print("\n\nScaricamento lista di video...")
    videos = scraper.scrape_videos_list(url)

    print(f"\n📺 LISTA DI VIDEO ({len(videos)} video trovati):")
    for i, video in enumerate(videos, 1):
        print(f"\n  {i}. {video['titolo']}")
        print(f"     Data: {video['data']}")
        print(f"     Durata: {video['durata']}")
        print(f"     Descrizione: {video['descrizione']}")

    # Salvataggio in JSON
    all_data = {
        'video_principale': video_principale,
        'ultimi_video': videos,
        'data_scraping': datetime.now().isoformat()
    }
    scraper.save_to_json(all_data)

    # Salvataggio in CSV
    scraper.save_to_csv(videos)

    print("\n✅ Scraping completato!")