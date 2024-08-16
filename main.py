import requests
from bs4 import BeautifulSoup
from csv import DictWriter
url = "https://www.wikipedia.org/"
r = requests.get(url)
htmlContent1 = r.content
soup = BeautifulSoup(htmlContent1, 'html.parser')

url1 = "https://en.wikipedia.org/wiki/Index_of_history_articles"
r1 = requests.get(url1)
htmlContent1 = r1.content
soup1 = BeautifulSoup(htmlContent1, 'html.parser')

url2 = "https://en.wikipedia.org/wiki/Book"
r2 = requests.get(url2)
htmlContent2 = r2.content
soup2 = BeautifulSoup(htmlContent2, 'html.parser')

with open('test.csv', 'w', encoding='utf-8') as csvfile:
    header = ('TITLE_OF_HISTORY_ARTICLE', 'HISTORY_ARTICLE_LINK', 'TITLE_OF_BOOK', 'BOOK_LINK', 'LINKS')
    csv_writer = DictWriter(csvfile, fieldnames=header, lineterminator='\n\n\n')

    csv_writer.writeheader()

    history_articles = soup1.find_all('li')
    book_articles = soup2.find_all('li')
    anchors = soup.find_all('a')
    all_links = set()
    for link in anchors:
        href = link.get('href')
        if href and href.startswith('/'):  # Check if href is not empty and starts with '/'
            linkText = "https://www.wikipedia.org/" + href
            all_links.add(linkText)
    links = '\n'.join(all_links)
    csv_writer.writerows([{'LINKS': links}])

    for article1, article2 in zip(history_articles, book_articles):
        title1 = article1.text.strip()
        a_tag = article1.find('a')
        if a_tag and 'href' in a_tag.attrs:
            url1 = "https://en.wikipedia.org/wiki/Index_of_history_articles" + a_tag['href']
        else:
            url1 = "https://en.wikipedia.org/wiki/Index_of_history_articles"
        title2 = article2.text.strip()
        a_tag = article2.find('a')
        if a_tag and 'href' in a_tag.attrs:
            url2 = "https://en.wikipedia.org/wiki/Book" + a_tag['href']
        else:
            url2 = "https://en.wikipedia.org/wiki/Book"
        csv_writer.writerows([{'TITLE_OF_HISTORY_ARTICLE': title1, 'HISTORY_ARTICLE_LINK': url1,
                               'TITLE_OF_BOOK': title2, 'BOOK_LINK': url2}])

