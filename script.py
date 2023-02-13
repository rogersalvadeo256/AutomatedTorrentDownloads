import qbittorrentapi
from array import *
from lxml import html
import requests


animes = [["Vinland Saga",0,""],["KanColle",0,""]]

qbt_client = qbittorrentapi.Client(
    host='XXX.XXX.XXX.XXX',
    port=XXXXX,
    username='XXXXX',
    password='XXXXXXXXX',
)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)
listorrent = []

# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
    listorrent.append(torrent.name)
    
for i in range(len(animes)):
    animes[i][1]= len(list(filter(lambda x: animes[i][0] in x,listorrent)))
    if i==0:
      animes[i][2]=f'https://nyaa.si/user/AnimeChap?f=0&c=0_0&q=Vinland+Saga+S02E{ str(animes[i][1]+1).rjust(2,"0") }'
    if i==1:
      animes[i][2]=f'https://nyaa.si/user/Erai-raws?f=0&c=0_0&q=%5BErai-raws%5D+KanColle+-+Itsuka+Ano+Umi+de+-+{str(animes[i][1]+1).rjust(2,"0")}+%5B1080p%5D%5BPOR-BR%5D'


for i in range(len(animes)):
    url = animes[i][2]
    print(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    try:
        print(tree.xpath("/html/body/div/div/h3[2]")[0].text_content())
    except:
        urlTorrent= tree.xpath("/html/body/div/div/div[1]/table/tbody/tr/td[3]/a[2]/@href")[0]
        qbt_client.torrents_add(urlTorrent)
