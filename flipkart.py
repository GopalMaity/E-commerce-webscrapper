from bs4 import BeautifulSoup
import requests

def flipkartDataScrapper(prod_type, prod_count) :

    def get_title_flipkart(soup):
        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"class":'B_NuCI'})
            print(title.text)
            # Inner NavigatableString Object
            # title_value = title.string
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()
            print(title_string)
            
        except AttributeError:
            title_string = ""	
            
        return title_string
    
    # Function to extract Product Price
    def get_price_flipkart(soup):
        try:
            price = soup.find("div", attrs={"class": "_25b18c"}).find(
                    "div", attrs={"class": "_30jeq3 _16Jk6d"}
                ).text.strip()
            if len(price) >= 10 :
                price = "NA"
        except AttributeError:

            try:
                # If there is some deal price
                price = soup.find("span", attrs={"class": "a-offscreen"}).string.strip()
                if len(price) >= 10 :
                    price = "NA"
            except:
                price = ""

        return price
    
    # Function to extract Product Rating
    def get_rating_flipkart(soup):
        try:
            rating = soup.find("span", attrs={'class':'_2_R_DZ'}).find("span").find("span").string.strip()
            
            # print(rating)
        except AttributeError:
            
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""	

        return rating
    
    # Function to extract Number of User Reviews
    def get_review_count_flipkart(soup):
        try:
            review_count = soup.find("span", attrs={'class':'_2_R_DZ'}).find("span").find_all("span")[2].string.strip()
            
        except AttributeError:
            review_count = ""	

        return review_count
    
    # Function to extract Availability Status
    def get_availability_flipkart(soup):
        try:
            available = soup.find("span", attrs={'class': '_1TPvTK'}).string.strip()
            # available = available.find("span").string.strip()

        except AttributeError:
            available = "Not Available"	

        return available

    # Code calling begins here.....	
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language' : 'en-US'
    }

    # The webpage URL
    url = f"https://www.flipkart.com/search?q={prod_type}"

    # HTTP Request
    webpage = requests.get(url, headers=headers)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': '_1fQZEK'})
    # print(links[0])

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))
    
    # print(links_list[0])

    product_details_flipkart = []

    # Loop for extracting product details from each link
    for link in links_list[:prod_count]:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=headers)
        
        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        # Extract product details
        title = get_title_flipkart(new_soup)
        price = get_price_flipkart(new_soup)
        rating = get_rating_flipkart(new_soup)
        review_count = get_review_count_flipkart(new_soup)
        availability = get_availability_flipkart(new_soup)

        # Append details to the list
        product_details_flipkart.append({
            "title": title,
            "price": price,
            "rating": rating,
            "review_count": review_count,
            "availability": availability
        })

    return product_details_flipkart
