# Collected from https://lichess.org/page/world-championships
#from bs4 import BeautifulSoup
#from requests_html import HTMLSession
import requests

studies = [
    'https://lichess.org/study/beM3pwZa/DYpkMZMs',
    'https://lichess.org/study/D9TyW8VV/qhoBgvPh',
    'https://lichess.org/study/QFkiT2sJ/Omofsew1',
    'https://lichess.org/study/G6WWBFU0/U3rBavyl',
    'https://lichess.org/study/qyDrsjZ2/wFFobbsk',
    'https://lichess.org/study/qQ60p6GU',
    'https://lichess.org/study/2k6CI0TT/tQ35bjyq',
    'https://lichess.org/study/TFFyOff1/Vlta6biz',
    'https://lichess.org/study/0KNdpNQd/r9kW0Nk7',
    'https://lichess.org/study/0udqWQdc/MZEeGtwu',
    'https://lichess.org/study/mUCqnOSS/2ZTvVbCn',
    'https://lichess.org/study/G5ogxOsz/0y5aChxa',
    'https://lichess.org/study/wnoAvzBk/ZT7FzGKm',
    'https://lichess.org/study/O9v2NaOU/SprQBXBI',
    'https://lichess.org/study/vNaOB23W/y6vfsKj8',
    'https://lichess.org/study/CcnVF8Aj/qpgFSkVW',
    'https://lichess.org/study/eA8PlINJ/Htf9glww',
    'https://lichess.org/study/Niha8CRu/vu0VKfsj',
    'https://lichess.org/study/YL4pmkIt/JGSYtR7d',
    'https://lichess.org/study/MPkpQJkr/0XiCd2ia',
    'https://lichess.org/study/AK4EthCc/V6SBPqXu',
    'https://lichess.org/study/wC9lnnUr/De9Kx6Uu',
    'https://lichess.org/study/eN0uvvNe/98sAdT0k',
    'https://lichess.org/study/5TfavKIP/BAdnmDNs',
    'https://lichess.org/study/hm6ViybN/fCcN6rJU',
    'https://lichess.org/study/4c6eS6SH/nVsijp6T',
    'https://lichess.org/study/Eyl4uwTZ/vEgRwuZ5',
    'https://lichess.org/study/iQgHCyqA/1z7T03UX',
    'https://lichess.org/study/G4s4xOR9/N9COM0M0',
    'https://lichess.org/study/wgJ634pR/OgjnOytq',
    'https://lichess.org/study/b6q7gDGK/BOuPW4Ti',
    'https://lichess.org/study/4S5UuAGn/WotVmrCv',
    'https://lichess.org/study/dXHewez0/29BNYOVm',
    'https://lichess.org/study/dOfsx9Cq/iYiqCfq9',
    'https://lichess.org/study/HdrEkPSF/uLyUIn3q',
    'https://lichess.org/study/HpQRsYHb/7HzZ7XCE',
    'https://lichess.org/study/XAbxnp53/PLh8MVkt',
    'https://lichess.org/study/9ubc1elI',
    'https://lichess.org/study/huDqpKnt/bt9BkP1K',
    'https://lichess.org/study/LeX7mHMl/53lCbUn4',
    'https://lichess.org/study/HALtyMwL/EqUWsgBy',
    'https://lichess.org/study/a3SlSwsE',
    'https://lichess.org/study/JSPeC3w6/9hctzCB',
    'https://lichess.org/study/PWQ5l7ky/wR210hVg',
    'https://lichess.org/study/nurfx2OL/KjQ17Dna',
    'https://lichess.org/study/edeMUtJW/EsSsv6uv',
    'https://lichess.org/study/7WCFYt0R/XVxUIL9r'
]

broadcasts = [
    'A6snaCgb', #'https://lichess.org/broadcast/world-chess-championship-2021/game-1/olFFWcs6',
    'lrdHUzyS' #'https://lichess.org/broadcast/fide-world-chess-championship-2023/lrdHUzyS'
]


for i, study in enumerate(studies):
    start = study.find('study') + 6
    end = start + 1
    while end < len(study) and study[end] != '/':
        end += 1
    studies[i] = study[start:end]

rel_path = 'project/pgns/'
for i, study in enumerate(studies):
    r = requests.get(f'https://lichess.org/api/study/{study}.pgn', allow_redirects=True)
    with open(f'{rel_path}/study{i}.pgn', 'wb') as f:
        f.write(r.content)

for i, broadcast in enumerate(broadcasts):
    r = requests.get(f'https://lichess.org/api/broadcast/{broadcast}.pgn', allow_redirects=True)
    with open(f'{rel_path}/broadcast{i}.pgn', 'wb') as f:
        f.write(r.content)

"""
url = links[0]
session = HTMLSession()
r = session.get(url)
r.html.render()

for result in r.html.find('div'):
    attrs = result.attrs
    if 'class' in attrs and 'advice-summary__acpl' in attrs['class']:
        print(result)
#print(r.html.text)
#acpl = r.html.find('acpl', first=True)
#print(acpl)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#results = soup.find_all('div', class_='advice-summary__acpl')
results = soup.find(id='main_wrap')
#for result in results:
    #print(result)
print(soup.prettify())
"""