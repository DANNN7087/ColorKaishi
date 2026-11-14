from bs4 import BeautifulSoup
import requests
import csv

word_types = []
word_range = range(1000,1500)

with open("words.txt", "r") as file:
    words = file.read().splitlines()

    for i in word_range:

        word = words[i]

        word = word.strip()
        
        page_to_scrape = requests.get(f"https://jisho.org/word/{word}")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        scrape = soup.find("div", attrs={"class":"meaning-tags"})

        if not scrape:
            page_to_scrape = requests.get(f"https://jisho.org/search/{word}")
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")

            scrape = soup.find("div", attrs={"class":"meaning-tags"})        

        print(f"https://jisho.org/word/{word}")
        print(word)
        print(scrape)

        if scrape:
            scrape = scrape.get_text(strip=True)
        
        word_types.append([word, scrape])


words = []

with open("output.csv", "r") as file:
    reader = csv.reader(file)
    words = [row[0].strip() for row in reader if row]
    
with open("output.csv", "a") as file:
    writer = csv.writer(file)
    for word_type in word_types:
        if word_type[0].strip() not in words:
            writer.writerow(word_type)
