import requests
from bs4 import BeautifulSoup
import os
import csv
import shutil

class Scraper:
    # Class constructor, initializes with the URL to be scraped.
    def __init__(self, url):
        self.url = url

    # Method to obtain the HTML of the web page.
    def fetch_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            formatted_html = soup.prettify()
            return formatted_html
        else:
            raise Exception(f"Error getting the page: {response.status_code}")

    # Method to save the HTML obtained in a file.
    def save_html(self, html, filename="html_temp.html"):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html)

    # Method to extract news links from a given HTML.
    def extract_news_links(self, html, max_links):
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.find('ul', {'data-testid': 'topic-promos'}).find_all('li', limit=max_links)
        links = [item.find('a')['href'] for item in news_items]
        return links

    # Method to create a folder if it does not exist.
    def create_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            print(f"The folder '{folder_name}' already exists.")

    # Method to extract relevant information from an HTML file.
    def extracting_information_html(self, archivo_html):
        # Try to open and read the HTML file
        try:
            with open(archivo_html, 'r', encoding='utf-8') as file:
                contenido = file.read()
                soup = BeautifulSoup(contenido, 'html.parser')
                
                # Attempts to extract the title, author and text from the HTML content.
                try:
                    title_element = soup.select_one("div h1[id='content']")
                    title = title_element.get_text().replace('\n', ' ').strip() if title_element else "Title not founf."

                    author_element = soup.select_one('section[aria-labelledby="article-byline"]')
                    author = author_element.get_text().replace('\n', '').strip() if author_element else "Author not found."

                    # Extract text elements (paragraphs and subheadings)
                    text_elements = soup.select('div[dir="ltr"] div[dir="ltr"] h2, p[dir="ltr"]')

                    # Compile the total text from the extracted elements
                    total_text = ""
                    for elem in text_elements:
                        text = elem.get_text().replace('\n', ' ').strip()
                        total_text = total_text + "\n"+ text

                    return title, author, total_text 
                    
                except FileNotFoundError:
                    return "Information not found"
        
        except FileNotFoundError:
            return "File not found."

    # Method to save the extracted information in a CSV file.
    def save_in_csv(self, datos, file_name_csv):
        with open(file_name_csv, mode='w', newline='', encoding='utf-8') as file:
            writer_csv = csv.writer(file)
            writer_csv.writerow(['Title', 'Author', 'Text'])
            for dato in datos:
                writer_csv.writerow(dato)

    # Method to delete a folder and its contents.
    def delete_folder(self, folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been deleted.")
        else:
            print(f"The folder '{folder_path}' does not exist or is not a folder.")

    # Main method orchestrating the execution of scraping.
    def run(self, max_links=18):
        if max_links > 18:
            raise Exception(f"Only a maximum of 18.")
        else:
            formatted_html = self.fetch_html()
            #self.save_html(formatted_html,"html_main.py")
            news_links = self.extract_news_links(formatted_html, max_links)
            self.create_folder("news")
            
            datos_para_csv = []

            for link in news_links:
                self.url = link
                formatted_html = self.fetch_html()
                self.save_html(formatted_html,"news/" + str(link.replace("/","")) + ".html")
                title, author, total_text  = self.extracting_information_html("news/" + str(link.replace("/","")) + ".html")
                datos_para_csv.append([title,author,total_text])

            self.save_in_csv(datos_para_csv, 'News_data.csv')

            self.delete_folder("news")
