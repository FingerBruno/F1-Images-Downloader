import os
import urllib.request
from bs4 import BeautifulSoup

def getRawHTML(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
             'Referer': 'https://www.statsf1.com/en/1950/grande-bretagne.aspx'}
    req = urllib.request.Request(url,headers=headers)
    return urllib.request.urlopen(req)

def getImageURL(html_code, filename):
    soup = BeautifulSoup(html_code, 'html.parser')
    div = soup.find('div', {'class':'gpaffiche'})
    name = div.findAll('a')
    img = div.findAll('img')
    return (['https://www.statsf1.com' + url['src'] for url in img], [n.text+f'_{filename}' for n in name])

def downImages(image_url, filename):
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'), 
                       ('Referer', 'https://www.statsf1.com/en/1950/grande-bretagne.aspx')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(image_url, filename)
    return print('Imagem Baixada')

def createFolder(path, folder_name):
    path = os.path.join(path, folder_name)
    os.mkdir(path)
    print(f'Pasta{folder_name} criada com sucesso...')
    return path

def main():
  for year in range(1950, 2022):
      folder = createFolder(path='/home/fingerbruno/Pictures/f1_images', folder_name=f'{year}/')
      html = getRawHTML(f'https://www.statsf1.com/en/{year}.aspx')
      urls, names = getImageURL(html, f'{year}')
      
      for url, name in zip(urls, names):
          downImages(url, f'{folder + name}')

