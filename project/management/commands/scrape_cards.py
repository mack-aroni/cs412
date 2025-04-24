from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import time

from project.models import *

class Command(BaseCommand):
    help = 'Scrape cards from Limitless TCG'

    def handle(self, *args, **kwargs):
        BASE_URL = "https://pocket.limitlesstcg.com/cards/A1/{}"
        HEADERS = {"User-Agent": "Mozilla/5.0"}
        START = 0
        END = 286
        DELAY = 0.5

        Card.objects.all().delete()
        OwnedBy.objects.all().delete()
        p = PocketProfile.objects.get(user__username="etanm")

        for x in range(START, END + 1):
            url = BASE_URL.format(x)
            try:
                response = requests.get(url, headers=HEADERS)
                if response.status_code != 200:
                    self.stdout.write(self.style.WARNING(f"[{x}] Skipped (HTTP {response.status_code})"))
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                element1 = soup.select_one("body > main > div > section > div.card-profile > div.card-details > div > div > div:nth-child(1) > p.card-text-type")
                element2 = soup.select_one("body > main > div > section > div.card-profile > div.card-details > div > div > div:nth-child(1) > p.card-text-title")
                element3 = soup.select_one("body > main > div > section > div.card-prints > div > a > div > span:nth-child(2)")
            
                if element1 and element2 and element3:
                    num = str(x)
                    while len(num) < 3:
                        num = '0' + num

                    text1 = element1.get_text(strip=True)
                    text1 = text1.split('-')
                    text1 = [i.strip() for i in text1]

                    is_poke = text1[0] == 'Pokémon'
                    card_type = text1[1]     

                    text2 = element2.get_text(strip=True)
                    text2 = text2.split('-')
                    text2 = [i.strip() for i in text2]

                    name = text2[0]
                    if len(name.split(' ')) == 2 and name.split(' ')[1] == 'ex':
                        arr = name.split(' ')
                        arr[1] = arr[1].upper()
                        name = arr[0]+arr[1]

                    if is_poke:
                        poke_type = text2[1]
                    else :
                        poke_type = ''

                    text3 = element3.get_text(strip=True)
                    text3 = text3.split('·')
                    text3 = [i.strip() for i in text3]

                    rarity = text3[1]
                    if rarity == "Crown Rare":
                        rarity = "♕"

                    if len(text3) < 3:
                        booster = "Shared"
                    else:
                        booster = text3[2].split(" ")[0]
                    
                    # print(f'A1-{x}, {name}, {poke_type}, {card_type}, {rarity}, {booster}')

                    new_card = Card(
                    uid=f'A1-{x}',
                    pack='Genetic Apex',
                    booster=booster,
                    rarity=rarity,
                    name=name,
                    poke_type=poke_type,
                    card_type=card_type,
                    card_image_url=f'https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/pocket/A1/A1_{num}_EN.webp')
                    
                    new_card.save()
                    print(f'Created New Card: A1-{x}, {name}, {poke_type}, {card_type}, {rarity}, {booster}')

                    new_rel = OwnedBy(profile=p, card=new_card)
                    new_rel.save()

                else:
                    print("Element not found")

                time.sleep(DELAY)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[{x}] Error: {e}"))

