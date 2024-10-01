#!/usr/bin/env python
# coding: utf-8
# In[1]:
import requests
from bs4 import BeautifulSoup
import pandas as pd
# In[67]:





# In[8]:



import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrape_yelp(url, num_pages):
    reviews_data = []
       
    for page in range(num_pages):
        start = page * 10  
        page_url = f"{url}&start={start}"  
       
        response = requests.get(page_url)  
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            continue 
       
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('li', {'class': 'y-css-mu4kr5'})
        restaurant_name = soup.find('h1', {'class':'y-css-olzveb'}).text.strip()
        total_reviews = soup.find('p', {'class': 'y-css-1g19ugt'}).text.strip()
   
        for review in reviews:
            reviewer_text_elem = review.find('span', {'class': 'raw__09f24__T4Ezm'})
            review_text = reviewer_text_elem.text.strip() if reviewer_text_elem else "No review text"
           
            reviewer_elem = review.find('a', {'class': 'y-css-12ly5yx'})
            reviewer = reviewer_elem.text.strip() if reviewer_elem else "Anonymous"
           
            rating = 0
            rating_elem = review.find('div', {'class': 'y-css-1jwbncq'})
            if rating_elem:
                paths = rating_elem.find_all('path')
                if paths:  
                    for path in paths:
                        opacity = path.get('opacity')
                        if opacity == '1':
                            rating += 1
                        elif opacity == '0.5':
                            continue
            reviews_data.append({
                'Review_Text': review_text,
                'Reviewer': reviewer,
                'Rating': int(rating / 2)  
            })
    df = pd.DataFrame(reviews_data)
   
    df['Restaurant_Name'] = restaurant_name
    df['Total_Reviews'] = total_reviews
    df = df[['Restaurant_Name', 'Total_Reviews', 'Reviewer', 'Rating', 'Review_Text']]
   
    df.to_csv('yelp_reviews_multiple.csv', index=False)
    print("Data has been saved to 'yelp_reviews_multiple.csv'.")
url = "https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants"
num_pages = 5  
scrape_yelp(url, num_pages)



# In[10]:



# In[ ]:







