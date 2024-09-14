import requests
from bs4 import BeautifulSoup
import sys
import json

def fetch_anime_data(query):
  url = f"https://nimegami.id/?s={query}&post_type=post"  # URL pencarian Nimegami
  response = requests.get(url)
  response.raise_for_status()  # Memastikan permintaan berhasil

  soup = BeautifulSoup(response.content, 'html.parser')

  results = []
  for article in soup.find_all('article'):
    # Mengambil judul dan URL anime
    title_element = article.find('h2', itemprop="name").find('a')
    title = title_element.text.strip()
    anime_url = title_element['href']

    # Mengambil gambar
    image_element = article.select_one('.thumbnail img')
    image = image_element['src'] if image_element else ""

    # Mengambil status
    status_element = article.select_one('.term_tag-a a')
    status = status_element.text.strip() if status_element else ""

    # Mengambil tipe
    type_element = article.select_one('.terms_tag a')
    type = type_element.text.strip() if type_element else ""

    # Mengambil rating (jika ada)
    rating_element = article.select_one('.rating-archive i')
    rating = rating_element.next_sibling.strip() if rating_element else ""

    # Mengambil jumlah episode (jika ada)
    episodes_element = article.select_one('.eps-archive')
    episodes = episodes_element.text.strip() if episodes_element else ""

    results.append({
      'title': title,
      'image': image,
      'status': status,
      'type': type,
      'rating': rating,
      'episodes': episodes,
      'anime_url': anime_url
    })

  return json.dumps(results)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python nimegami_search.py <query>", file=sys.stderr)
    sys.exit(1)

  query = sys.argv[1]
  data = fetch_anime_data(query)
  print(data)
