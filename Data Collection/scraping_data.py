from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

class AmazonScraper:
    def __init__(self, csv_file_path, url):
        self.csv_file_path = csv_file_path
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=")
        self.driver = webdriver.Chrome(options=self.options)

    def get_availability(self, soup):
        try:
            available = soup.find('span', {'id': 'availability'}).text.strip()
        except:
            available = "Not Available"
        return available

    def get_title(self, soup):
        try:
            title = soup.find('span', {'id': 'productTitle'})
            title_string = title.text.strip()
        except:
            title_string = ""
        return title_string

    def get_price(self, soup):
        try:
            price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
        except:
            try:
                price = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip()
            except:
                price = ""
        return price

    def get_rating(self, soup):
        try:
            rating = soup.select_one('i.a-icon.a-icon-star span').get_text(strip=True)
        except:
            try:
                rating = soup.find('span', {'class': 'a-icon-alt'}).text.strip()
            except:
                rating = ""
        return rating

    def get_review_count(self, soup):
        try:
            review_count = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
        except:
            review_count = ""
        return review_count
    
    def get_product_type(self, soup):
        try:
            product_type = soup.find('a', {'class': 'a-link-normal'}).text.strip()
        except:
            product_type = ""
        return product_type
    
    def get_description(self, soup):
        try:
            description_element = soup.find('div', {'id': 'productDescription'})
            description = description_element.get_text(strip=True)

            if not description:
                try:
                    about_item_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#feature-bullets span.a-size-base-plus.a-text-bold'))
                    )
                    about_this_item = about_item_element.text.strip()
                    description = f"About this item: {about_this_item}"
                except Exception as e:
                    print(f"Failed to retrieve 'About this item': {str(e)}")
        except Exception as e:
            print(f"Failed to retrieve product description: {str(e)}")
            description = ""

        return description

    def get_src(self, soup):
        try:
            src = soup.find('div', {'class': 'imgTagWrapper'}).find('img')['src']
        except:
            src = ""
        return src

    def get_product_name(self, soup):
        try:
            product_name = soup.find('span', {'id': 'productTitle'}).text.strip()
        except:
            product_name = ""
        return product_name

    def scrape_amazon_data(self):
        file_exists = os.path.isfile(self.csv_file_path)

        if file_exists:
            amazon_df = pd.read_csv(self.csv_file_path)
        else:
            amazon_df = pd.DataFrame(columns=["title", "price", "rating", "reviews", "description", "product_name",'product_type',"src"])

        self.driver.get(self.url)
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline')
        links_list = [link.get_attribute('href') for link in links]

        # d = {"title": [], "price": [], "rating": [], "reviews": [], "description": [], "product_type": [], "src": []}
        d = {"title": [], "price": [], "rating": [], "reviews": [], "description": [], "product_name": [], "src": []}

        for link in links_list:
            self.driver.get(link)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            d['title'].append(self.get_title(soup))
            d['price'].append(self.get_price(soup))
            d['rating'].append(self.get_rating(soup))
            d['reviews'].append(self.get_review_count(soup))
            # d['availability'].append(self.get_availability(soup))
            d['description'].append(self.get_description(soup))
            d['product_name'].append(self.get_product_name(soup))

            # d['product_type'].append(self.get_product_type(soup))
            d['src'].append(self.get_src(soup))


        new_data_df = pd.DataFrame.from_dict(d)
        amazon_df = pd.concat([amazon_df, new_data_df], ignore_index=True)
        amazon_df.drop_duplicates(subset=['title'], keep='last', inplace=True)
        amazon_df.to_csv(self.csv_file_path, header=True, index=False)
        self.driver.quit()

# if __name__ == '__main__':
#     url = 'https://www.amazon.com/s?k=smart+watch&crid=14FV7IZI70WX&sprefix=SMA%2Caps%2C238&ref=nb_sb_ss_ts-doa-p_1_3'
#     csv_file_path = "amazon_data.csv"
#     scraper = AmazonScraper(csv_file_path=csv_file_path, url=url)
#     scraper.scrape_amazon_data()













from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from selenium.common.exceptions import TimeoutException
import random

class NoonScraper:
    def __init__(self, csv_file_path, url, max_pages=200):
        self.csv_file_path = csv_file_path
        self.base_url = url
        self.max_pages = max_pages
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=")  # Specify a user-agent here
        self.driver = webdriver.Chrome(options=self.options)

    def get_title(self, soup):
        try:
            title = soup.find('h1', {'data-qa': True, 'class': 'sc-6f72a2a1-17'}).text.strip()
        except:
            title = ""
        return title
            # Save to CSV after every page to preserve data
    def get_src(self, soup):
        try:
            div = soup.find('div', {'class': 'sc-d8caf424-2 fJBKzl'})
            if div:
                src = div.find('img')['src']
                return src
            else:
                print("Image div not found.")
                time.sleep(10000)
                return ""
        except Exception as e:
            print(f"Error getting the source of the image: {e}")
            return ""



    def scrape_page(self, url, page_number, max_attempts=3):
        attempts = 0
        scraped_data = []

        while attempts < max_attempts:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-926ab76d-7'))
                )
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                product_containers = soup.select('div.sc-926ab76d-7 a')
                print(f"Page {page_number}: Found {len(product_containers)} products.")

                for link in product_containers:
                    product_url = 'https://www.noon.com' + link['href']
                    self.driver.get(product_url)
                    product_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    title = self.get_title(product_soup)
                    src = self.get_src(product_soup)
                    if src:
                        scraped_data.append({
                            'title': title,
                            'src': src,
                            'href': product_url
                        })
                    else:
                        print(f"Image not found for product at {product_url}")
                break  # Exit the while loop after successful scraping

            except TimeoutException:
                print(f"Attempt {attempts+1}: Timeout occurred while loading page {page_number} with URL: {url}")
                attempts += 1
                time.sleep(5)  # Wait before retrying

        if attempts == max_attempts:
            print(f"Failed to load page {page_number} after {max_attempts} attempts.")

        return scraped_data


    def scrape_noon_data(self):
        # Check if the CSV file exists and read it if it does
        if os.path.isfile(self.csv_file_path):
            noon_df = pd.read_csv(self.csv_file_path)
        else:
            noon_df = pd.DataFrame(columns=["title", "src", "href"])
        
        # Generate URLs and scrape data for each page
        for page_number in range(57, self.max_pages + 1):
            page_url = self.base_url.replace("page=2", f"page={page_number}")
            scraped_data = self.scrape_page(page_url, page_number)
            new_data_df = pd.DataFrame(scraped_data)
            noon_df = pd.concat([noon_df, new_data_df], ignore_index=True)
            
            # Save to CSV after every page to preserve data
            noon_df.drop_duplicates(keep='first', inplace=True)
            noon_df.to_csv(self.csv_file_path, index=False)
            
            # Break after first page for demonstration purposes
            # break
        
        # Close the browser after scraping
        self.driver.quit()



def generate_noon_urls(base_url, total_pages):
    urls = []
    for page in range(1, total_pages + 1):
        # Replace 'page=2' with the current page number
        page_url = base_url.replace("page=2", f"page={page}")
        urls.append(page_url)
    return urls
if __name__ == '__main__':
    url = "https://www.noon.com/saudi-en/fashion-women/?limit=50&page=49&searchDebug=false&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc&gclid=Cj0KCQiAv8SsBhC7ARIsALIkVT0EMrUZ_jS1ZrZo-duNogz1BK3Nfv5acqHQKAURVTDVkZcDSsekWIwaAnVDEALw_wcB&utm_campaign=C1000148709N_sa_ar_web_homeappliancesx25012022_noon_web_c1000087l_remarketing_plassc_&utm_medium=cpc&utm_source=c1000087L"
    csv_file_path = "noon_data_200_pages.csv"
    scraper = NoonScraper(csv_file_path=csv_file_path, url=url)
    scraper.scrape_noon_data()









# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from bs4 import BeautifulSoup
# import pandas as pd
# import os

# class NoonScraper:
#     def __init__(self, csv_file_path, url):
#         self.csv_file_path = csv_file_path
#         self.url = url
#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument("user-agent=")
#         self.driver = webdriver.Chrome(options=self.options)

#     def get_product_info(self, product):
#         product_html = product.get_attribute('outerHTML')
#         product_soup = BeautifulSoup(product_html, 'html.parser')

#         product_container = product_soup.find('div', {'class': 'sc-d52968a7-7 EQtWK grid'})

#         if product_container:
#             classes_inside = product_container.find_all('span', {'class': 'sc-5c17cc27-0 eCGMdH wrapper productContainer'})
#             links = [span.find('a')['href'] for span in classes_inside]

#             return links

#         return []

#     def get_product_name(self, product_container):
#         try:
#             product_name_element = product_container.find_element(By.CSS_SELECTOR, 'h1.sc-750eefb7-17.ftpDAI')
#             product_name = product_name_element.text.strip()
#             print(f"Product Name: {product_name}")
#         except TimeoutException:
#             product_name = "None"
#             print(product_name)

#         return product_name

#     def get_product_price(self, product_container):
#         try:
#             product_price_element = product_container.find_element(By.CSS_SELECTOR, 'div.priceNow[data-qa="div-price-now"]')
#             product_price = product_price_element.text
#             print(product_price)
#         except NoSuchElementException:
#             product_price = "None"
#             print(product_price)

#         return product_price
#     def get_product_overview(self, product_container):
#         try:
#             key_features_element = product_container.find_element(By.CSS_SELECTOR, 'div.sc-97eb4126-2.oPZpQ')
#             key_features = key_features_element.find_element(By.CSS_SELECTOR, 'span.sc-97eb4126-3.ghStOs').text.strip()
#             key_features_list = [li.text.strip() for li in key_features_element.find_elements(By.CSS_SELECTOR, 'ul li')]
#             print("Key Features:")
#             print(key_features)
#             print("Key Features List:")
#             print(key_features_list)

#         except NoSuchElementException:
#             key_features = 'None'
#             key_features_list = []

#         try:
#             overview_element = product_container.find_element(By.CSS_SELECTOR, 'span.sc-cdd75544-0.bHXbPt')
#             strong_element = overview_element.find_element(By.XPATH, './following-sibling::strong')
#             overview = strong_element.text.strip()
#             print("Overview:\n", overview)

#         except NoSuchElementException:
#             overview = 'None'

#         return key_features, key_features_list, overview




#     def get_product_image(self, product_container):
#         try:
#             image_element = product_container.find_element(By.CSS_SELECTOR, 'div.sc-d8caf424-2.fJBKzl img')
#             image_url = image_element.get_attribute('src')
#             print("Image URL:", image_url)

#         except NoSuchElementException:
#             image_url = "Image Not Found"

#         return image_url

#     def save_to_csv(self, product_data):
#         if os.path.isfile(self.csv_file_path):
#             existing_noon_df = pd.read_csv(self.csv_file_path)
#         else:
#             existing_noon_df = pd.DataFrame(columns=["Product Name", "Product Price", "Key Features", "Overview", "Image URL"])

#         existing_noon_df = pd.concat([existing_noon_df, product_data], ignore_index=True)
#         existing_noon_df.drop_duplicates(subset=['Product Name'], keep='last', inplace=True)
#         existing_noon_df.to_csv(self.csv_file_path, header=True, index=False)

#     def scrape_noon_data(self):
#         self.driver.get(self.url)

#         for page_num in range(1, 4):
#             page_url = f"{self.url}&page={page_num}"
#             self.driver.get(page_url)

#             WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'sc-926ab76d-7.eCDCTP.grid')))

#             products = self.driver.find_elements(By.CSS_SELECTOR, 'sc-926ab76d-7.eCDCTP.grid')
#             for product in products:
#                 links = self.get_product_info(product)
#                 self.visit_links(links)

#         self.driver.quit()

#     def visit_links(self, links):
#         base_url = 'https://www.noon.com'  # Replace this with the actual base URL

#         # DataFrame to store product information
#         product_data = pd.DataFrame(columns=["Product Name", "Product Price", "Key Features", "Overview", "Image URL"])

#         for link in links:
#             full_url = f"{base_url}{link}"
#             print(f"Visiting link: {full_url}")
#             self.driver.get(full_url)

#             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-e6ac681c-0.bFFsDo')))

#             product_container = self.driver.find_element(By.CSS_SELECTOR, 'div.sc-e6ac681c-0.bFFsDo')

#             product_soup = BeautifulSoup(product_container.get_attribute('outerHTML'), 'html.parser')

#             product_container_html = product_soup.prettify()

#             product_name = self.get_product_name(product_container)
#             product_price = self.get_product_price(product_container)
#             key_features, key_features_list, overview = self.get_product_overview(product_container)
#             image_url = self.get_product_image(product_container)
            
#             # Print all classes in the specified class
#             classes_inside = product_soup.find_all(class_="sc-e6ac681c-0 bFFsDo")
#             classes_inside_text = [cls.prettify() for cls in classes_inside]

#             # Append data to the DataFrame
#             product_data = pd.concat([product_data, pd.DataFrame([[product_name, product_price, key_features, overview, image_url]], columns=product_data.columns)], ignore_index=True)

#         # Save the extracted information to a CSV file
#         self.save_to_csv(product_data)


# # if __name__ == '__main__':
# #     url = 'https://www.noon.com/saudi-ar/fashion-men/?limit=50&page=1&searchDebug=false&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc'
# #     csv_file_path = "noon_data.csv"
# #     scraper = NoonScraper(csv_file_path=csv_file_path, url=url)
# #     scraper.scrape_noon_data()







from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PrimarkScraper:
    def __init__(self, csv_file_path, url):
        self.csv_file_path = csv_file_path
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=")
        self.driver = webdriver.Chrome(options=self.options)

    def get_urls(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links_list = []

            # Find all the <a> elements with the specified class
            product_links = soup.find_all('a', class_='MuiTypography-root MuiLink-root MuiLink-underlineAlways MuiTypography-colorPrimary')

            for link in product_links:
                href = link.get('href')
                if href and href.startswith('/en-us/p/'):
                    full_url = f'https://www.primark.com{href}'  # Construct full URL
                    links_list.append(full_url)

            return links_list
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")
            return []

    # ... (rest of your class methods remain the same)

    def scrape_amazon_data(self):
        file_exists = os.path.isfile(self.csv_file_path)

        if file_exists:
            amazon_df = pd.read_csv(self.csv_file_path)
        else:
            amazon_df = pd.DataFrame(columns=["title", "description", "src"])

        product_links = self.get_urls()

        d = {"title": [], "description": [], "src": []}

        for link in product_links:
            self.driver.get(link)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            title = soup.find('h5', {'class': 'MuiTypography-root jss161 MuiTypography-body1'})
            description = soup.find('div', {'class': 'MuiAccordionDetails-root jss227'})
            image = soup.find('div', {'data-evergage-image-url': True})
            d['title'].append(title.text.strip() if title else "")
            d['description'].append(description.text.strip() if description else "")
            d['src'].append(image['data-evergage-image-url'] if image else "")
            print(description)

        new_data_df = pd.DataFrame.from_dict(d)
        amazon_df = pd.concat([amazon_df, new_data_df], ignore_index=True)
        amazon_df.drop_duplicates(subset=['title'], keep='last', inplace=True)
        amazon_df.to_csv(self.csv_file_path, header=True, index=False)
        self.driver.quit()

if __name__ == '__main__':
    url = 'https://www.primark.com/en-us/r/women/clothing/winter-warmers'
    csv_file_path = "primark_data.csv"
    scraper = PrimarkScraper(csv_file_path=csv_file_path, url=url)
    scraper.scrape_amazon_data()







import pandas as pd
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AnimeScraper:
    def __init__(self, csv_file_path, base_url):
        base_url = "https://animeslayer.space/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%85%D9%8A/page/"
        self.csv_file_path = csv_file_path
        self.base_url = base_url
        self.driver = webdriver.Chrome()

    def scrape_anime_data(self, num_pages=56):
        anime_data_list = []
        for page_number in range(1, num_pages + 1):
            anime_hrefs = self.get_anime_hrefs(page_number)
            for href in anime_hrefs:
                anime_data = self.scrape_anime_info(href)
                if anime_data:
                    anime_data_list.append(anime_data)

            print(f"Scraped data from page {page_number}")

        # Save data to CSV
        self.save_to_csv(anime_data_list)

        # Preprocess the saved CSV data
        self.preprocess_anime_data()

    def get_anime_hrefs(self, page_number):
        base_url = self.base_url + f'{page_number}'
        self.driver.get(base_url)

        # Locate the row display-flex class
        row_elements = self.driver.find_elements(By.CLASS_NAME, "row.display-flex")
        anime_hrefs = []

        # Iterate through each row element
        for row_element in row_elements:
            # Locate the col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding class within each row
            anime_elements = row_element.find_elements(By.CSS_SELECTOR, ".col-lg-2.col-md-4.col-sm-6.col-xs-6.col-no-padding.col-mobile-no-padding a.overlay")
            anime_hrefs.extend([element.get_attribute("href") for element in anime_elements])

        return anime_hrefs

    def scrape_anime_info(self, href):
        self.driver.get(href)
        try:
            # Wait for the anime details title to be present on the page
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.anime-details-title")))

            # Continue with scraping
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.anime-details-title").text
            genres = [genre.text for genre in self.driver.find_elements(By.CSS_SELECTOR, "ul.anime-genres li a")]
            story = self.driver.find_element(By.CSS_SELECTOR, "p.anime-story").text

            series_type_element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[1]/div[1]/div/a")
            series_type = series_type_element.text if series_type_element else None

            num_episodes_element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[1]/div[4]/div")
            num_episodes = num_episodes_element.text if num_episodes_element else None

            show_start_element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/div")
            show_start = show_start_element.text if show_start_element else None

            anime_info = {
                "title": title,
                "genres": ", ".join(genres),
                "story": story,
                "series_type": series_type,  # Add series_type to the result
                "num_episodes": num_episodes,  # Add num_episodes to the result
                "show_start": show_start,  # Add show_start to the result
                "picture": self.driver.find_element(By.CSS_SELECTOR, "div.anime-thumbnail img.thumbnail").get_attribute("src")
            }

            return anime_info
        except NoSuchElementException as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def save_to_csv(self, data_list):
        keys = data_list[0].keys()
        with open(f'{self.csv_file_path}', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data_list)

    def preprocess_anime_data(self):
        df = pd.read_csv(self.csv_file_path)

        df['show_start'] = df['show_start'].str.extract('(\d+)')
        df['num_episodes'] = df['num_episodes'].str.extract('(\d+)')

        df = df[['title', 'story', 'num_episodes', 'show_start', 'series_type', 'genres', 'picture']]

        df.to_csv(self.csv_file_path, index=False)

    def close_browser(self):
        self.driver.quit()


# if __name__ == "__main__":
    # base_url = "https://animeslayer.space/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%85%D9%8A/page/"
#     csv_file_path = "anime_info_all_pages_v3.csv"
#     scraper = AnimeScraper(csv_file_path, base_url)
#     scraper.scrape_anime_data()
#     scraper.close_browser()
















# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd

# class AnimeScraper:
#     def __init__(self, csv_file_path, base_url):
#         self.csv_file_path = csv_file_path
#         self.base_url = base_url
#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument("user-agent=")
#         self.driver = webdriver.Chrome(options=self.options)

#     def scrape_anime_data(self):
#         all_titles = []
#         all_images = []
#         all_types = []
#         all_contents = []

#         for page_number in range(1, 57):
#             url = f"{self.base_url}{page_number}"
#             self.driver.get(url)

#             anime_list = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, 'anime-card-container'))
#             )

#             titles = []
#             images = []
#             types = []
#             contents = []

#             for anime in anime_list:
#                 title = anime.find_element(By.CLASS_NAME, 'anime-card-title').text
#                 titles.append(title)

#                 image_url = anime.find_element(By.CLASS_NAME, 'img-responsive').get_attribute('src')
#                 images.append(image_url)

#                 anime_type = anime.find_element(By.CLASS_NAME, 'anime-card-type').text
#                 types.append(anime_type)

#                 content = anime.find_element(By.CLASS_NAME, 'anime-card-title').get_attribute('data-content')
#                 contents.append(content)

#             all_titles.extend(titles)
#             all_images.extend(images)
#             all_types.extend(types)
#             all_contents.extend(contents)

#         data = pd.DataFrame({
#             'Title': all_titles,
#             'Type': all_types,
#             'Content': all_contents,
#             'Image URL': all_images
#         })

#         print(data.head())
#         data.to_csv(self.csv_file_path, index=False)

#     def close_browser(self):
#         self.driver.quit()

# if __name__ == '__main__':
#     base_url = "https://animeslayer.space/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%85%D9%8A/page/"
#     csv_file_path = "anime_info_all_pages.csv"

#     scraper = AnimeScraper(csv_file_path=csv_file_path, base_url=base_url)
#     scraper.scrape_anime_data()
#     scraper.close_browser()















# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# from selenium.common.exceptions import NoSuchElementException

# class NoonScraper:
#     def __init__(self, csv_file_path, url):
#         self.csv_file_path = csv_file_path
#         self.url = url
#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument("user-agent=")
#         self.driver = webdriver.Chrome(options=self.options)

#     def get_product_info(self, product):
#         product_html = product.get_attribute('outerHTML')
#         product_soup = BeautifulSoup(product_html, 'html.parser')

#         product_container = product_soup.find('div', {'class': 'sc-d52968a7-7 EQtWK grid'})
        
#         if product_container:
#             classes_inside = product_container.find_all('span', {'class': 'sc-5c17cc27-0 eCGMdH wrapper productContainer'})
#             links = [span.find('a')['href'] for span in classes_inside]

#             return links

#         return []
#     def visit_links(self, links):
#         base_url = 'https://www.noon.com'  # Replace this with the actual base URL

#         # Lists to store product information
#         product_addresses = []
#         product_prices = []

#         for link in links:
#             full_url = f"{base_url}{link}"
#             print(f"Visiting link: {full_url}")
#             self.driver.get(full_url)

#             # Wait for the product container to load
#             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-e6ac681c-9.gYcwMr')))

#             # Extract information from the product container
#             product_container = self.driver.find_element(By.CSS_SELECTOR, 'div.sc-e6ac681c-9.gYcwMr')

#             try:
#                 # Extract product name
#                 product_name_element = product_container.find_element(By.CSS_SELECTOR, 'h1[data-qa="pdp-name-Z6A1A80199CFDA622EF85Z"]')
#                 product_name = product_name_element.text
#             except NoSuchElementException:
#                 product_name = "Product Name Not Found"

#             product_addresses.append(product_name)

#             # Extract product price
#             product_price = product_container.find_element(By.CSS_SELECTOR, 'div.priceNow[data-qa="div-price-now"]').text
#             product_prices.append(product_price)

#             # Perform any additional actions or scraping if needed

#         # Save the extracted information to a CSV file
#         product_data = pd.DataFrame({'Product Address': product_addresses, 'Product Price': product_prices})
#         product_data.to_csv("product_info.csv", index=False)


#     def scrape_noon_data(self):


#         self.driver.get(self.url)
        
#         for page_num in range(1, 4):
#             page_url = f"{self.url}&page={page_num}"
#             self.driver.get(page_url)

#             WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-d52968a7-7.EQtWK.grid')))

#             products = self.driver.find_elements(By.CSS_SELECTOR, 'div.sc-d52968a7-7.EQtWK.grid')
#             for product in products:
#                 links = self.get_product_info(product)
#                 for link in links:
#                     self.visit_links([link])

#         self.driver.quit()

# if __name__ == '__main__':
#     url = 'https://www.noon.com/saudi-ar/fashion-men/?limit=50&page=1&searchDebug=false&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc'
#     csv_file_path = "noon_data.csv"
#     scraper = NoonScraper(csv_file_path=csv_file_path, url=url)
#     scraper.scrape_noon_data()









# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# import logging  # Don't forget to import logging for logging.info and logging.error


# class NoonScraper:
#     def __init__(self, csv_file_path, url):
#         self.csv_file_path = csv_file_path
#         self.url = url
#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument("user-agent=")
#         self.driver = webdriver.Chrome(options=self.options)

#     def get_product_info(self, product):
#         product_html = product.get_attribute('outerHTML')
#         product_soup = BeautifulSoup(product_html, 'html.parser')

#         product_container = product_soup.find('div', {'class': 'sc-d52968a7-7 EQtWK grid'})

#         if product_container:
#             classes_inside = product_container.find_all('span', {'class': 'sc-5c17cc27-0 eCGMdH wrapper productContainer'})
#             links = [span.find('a')['href'] for span in classes_inside]

#             return links

#         return []

#     def get_product_name(self, product_container):
#         try:
#             product_name_element = product_container.find_element(By.CSS_SELECTOR, 'h1.sc-750eefb7-17.ftpDAI')
#             product_name = product_name_element.text.strip()
#             print(f"Product Name: {product_name}")
#         except TimeoutException:
#             product_name = "None"
#             print(product_name)

#         return product_name

#     def get_product_price(self, product_container):
#         try:
#             product_price_element = product_container.find_element(By.CSS_SELECTOR, 'div.priceNow[data-qa="div-price-now"]')
#             product_price = product_price_element.text
#             print(product_price)
#         except NoSuchElementException:
#             product_price = "None"
#             print(product_price)

#         return product_price

#     def get_product_overview(self, product_container):
#         try:
#             key_features_element = product_container.find_element(By.CSS_SELECTOR, 'div.sc-97eb4126-2.oPZpQ')
#             key_features = key_features_element.text
#             print("Key Features: ")
#             print(key_features)

#         except NoSuchElementException:
#             key_features ='None'
#             print("Key Features Not Found")

#         try:
#             overview_element = product_container.find_element(By.CSS_SELECTOR, 'span.sc-cdd75544-0.bHXbPt')
#             strong_element = overview_element.find_element(By.XPATH, './following-sibling::strong')
#             overview = strong_element.text
#             print("Overview: \n", overview)

#         except NoSuchElementException:
#             overview = 'None'
#             print("Overview Not Found")

#         return key_features, overview


#     def get_product_image(self, product_container):
#         try:
#             image_element = product_container.find_element(By.CSS_SELECTOR, 'div.sc-d8caf424-2.fJBKzl img')
#             image_url = image_element.get_attribute('src')
#             print("Image URL:", image_url)

#         except NoSuchElementException:
#             image_url = "Image Not Found"

#         return image_url



#     def save_to_csv(self, product_data):
#         if os.path.isfile(self.csv_file_path):
#             existing_noon_df = pd.read_csv(self.csv_file_path)
#         else:
#             existing_noon_df = pd.DataFrame(columns=["Product Name", "Product Price", "Key Features", "Overview", "Image URL"])

#         existing_noon_df = pd.concat([existing_noon_df, product_data], ignore_index=True)
#         existing_noon_df.drop_duplicates(subset=['Product Name'], keep='last', inplace=True)
#         existing_noon_df.to_csv(self.csv_file_path, header=True, index=False)

#     def scrape_noon_data(self):
#         self.driver.get(self.url)

#         for page_num in range(1, 4):
#             page_url = f"{self.url}&page={page_num}"
#             self.driver.get(page_url)

#             WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-d52968a7-7.EQtWK.grid')))

#             products = self.driver.find_elements(By.CSS_SELECTOR, 'div.sc-d52968a7-7.EQtWK.grid')
#             for product in products:
#                 links = self.get_product_info(product)

#         self.driver.quit()

# if __name__ == '__main__':
#     url = 'https://www.noon.com/saudi-ar/fashion-men/?limit=50&page=1&searchDebug=false&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc'
#     csv_file_path = "noon_data.csv"
#     scraper = NoonScraper(csv_file_path=csv_file_path, url=url)
#     scraper.scrape_noon_data()


















