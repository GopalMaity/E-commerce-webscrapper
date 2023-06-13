from bs4 import BeautifulSoup
import requests

def tickerDataScrapper(prod_type) :

    def get_enterprise_value_ticker(soup) :
        try:
            enterprise_value = soup.find("span", attrs={"id":"mainContent_ltrlEntValue"}).find("span", attrs={"class":"number"}).string.strip()

        except AttributeError:
            enterprise_value = "Details Not Available"
        
        return enterprise_value

    def get_sector_ticker(soup) :
        try:
            sector = soup.find("a", attrs={"class":"font-weight-bold"}).text.strip()

        except AttributeError:
            sector = "Details Not Available"
        
        return sector


    def get_name_ticker(soup) :
        try:
            name = soup.find("span", attrs={"id":"mainContent_ltrlCompName"}).text.strip()

        except AttributeError:
            name = "Details Not Available"

        return name


    def get_title_ticker(soup) :
        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"id":'mainContent_ltrlCompName'}).text.strip()
            
        except AttributeError:
            title = ""	
            
        return title


    # Code calling begins here.....	
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language' : 'en-US'
    }

    # The webpage URL
    url = f"https://ticker.finology.in/company/{prod_type}"

    # HTTP Request
    webpage = requests.get(url, headers=headers)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    title=get_title_ticker(soup)

    product_details_ticker = []

    # Extract product details
    name = get_name_ticker(soup)
    sector = get_sector_ticker(soup)
    enterprise_value = get_enterprise_value_ticker(soup)
    rating = get_title_ticker(soup)
    review_count = get_title_ticker(soup)
    availability = get_title_ticker(soup)

    # Append details to the list
    product_details_ticker.append({
        "name": name,
        "sector": sector,
        "enterprise_value": enterprise_value,
        "rating": rating,
        "review_count": review_count,
        "availability": availability
    })

    return product_details_ticker
