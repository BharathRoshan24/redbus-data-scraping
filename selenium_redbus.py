#!/usr/bin/env python
# coding: utf-8

# In[7]:


#importing libraries
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# # Kerala Routes

# In[12]:


#open the browser

driver=webdriver.Chrome()

#load the webpage

driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")

time.sleep(3)

driver.maximize_window()


# In[13]:


#10 states links
state_links=["https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile",
             "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile"
]


# In[14]:


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import time

def Kerala_link_route(driver, path):   
    wait = WebDriverWait(driver, 20)
    LINKS_KERALA = []
    ROUTE_KERALA = []
    
    for i in range(1, 3):  # Adjust this range as needed
        try:
            # Retrieve route links
            wait.until(EC.presence_of_all_elements_located((By.XPATH, path)))
            paths = driver.find_elements(By.XPATH, path)
            
            for link in paths:
                d = link.get_attribute("href")
                LINKS_KERALA.append(d)
                ROUTE_KERALA.append(link.text)  # Collect route names
            
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()="{i + 1}"]')
            
            # Scroll the button into view and wait
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Short delay to ensure the button is ready

            # Attempt to click the button with retries
            retries = 3
            for attempt in range(retries):
                try:
                    wait.until(EC.element_to_be_clickable(next_button))
                    next_button.click()
                    break  # Exit retry loop if successful
                except ElementClickInterceptedException:
                    print("Element click intercepted, retrying...")
                    time.sleep(2)  # Wait before retrying
                    # Re-fetch the button in case the DOM has changed
                    next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()="{i + 1}"]')

        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
        except TimeoutException:
            print("Timed out waiting for pagination element.")
            break

    return LINKS_KERALA, ROUTE_KERALA

# Example usage
LINKS_KERALA, ROUTE_KERALA = Kerala_link_route(driver, "//a[@class='route']")


# In[15]:


df_k=pd.DataFrame({"Route_name":ROUTE_KERALA,"Route_link":LINKS_KERALA})
df_k


# In[31]:


# change dataframe to csv
path=r"C:\Users\ajant\OneDrive\Desktop\redbus-data-scraping\Redbus\df_k.csv"
df_k.to_csv(path,index=False)


# # Andhra Pradesh Routes

# In[17]:


#open the browser

driver_A=webdriver.Chrome()

#load the webpage
driver_A.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile")

time.sleep(30)

driver_A.maximize_window()


# In[18]:


#retrive  bus links and route
wait = WebDriverWait(driver_A, 20)
def Andhra_link_route(path):   
    LINKS_ANDHRA=[]
    ROUTE_ANDHRA=[]
    # retrive the route links 
    for i in range(1,5):
        paths=driver_A.find_elements(By.XPATH,path)
        
        for links in paths:
            d = links.get_attribute("href")
            LINKS_ANDHRA.append(d)
            
        # retrive names of the routes
        for route in paths:
            ROUTE_ANDHRA.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            next_button.click()
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
        except TimeoutException:
            print("Timed out waiting for pagination element.")
            break
        except ElementClickInterceptedException:
            print("Element not clickable, trying to click using JavaScript")
            
    return LINKS_ANDHRA,ROUTE_ANDHRA

LINKS_ANDHRA,ROUTE_ANDHRA=Andhra_link_route("//a[@class='route']")


# In[19]:


df_A=pd.DataFrame({"Route_name":ROUTE_ANDHRA,"Route_link":LINKS_ANDHRA})
df_A


# In[32]:


# change dataframe to csv
path=r"C:\Users\ajant\OneDrive\Desktop\redbus-data-scraping\Redbus\df_A.csv"
df_A.to_csv(path,index=False)


# # Telugana Routes

# In[21]:


#open the browser

driver_T=webdriver.Chrome()

#load the webpage
driver_T.get("https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_T.maximize_window()


# In[22]:


#retrive bus links and route
wait = WebDriverWait(driver_T, 20)
def Telugana_link_route(path):   
    LINKS_TELUGANA=[]
    ROUTE_TELUGANA=[]
    
    for i in range(1,4):
        paths=driver_T.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            LINKS_TELUGANA.append(d)
            
        # retrive names of the routes
        for route in paths:
            ROUTE_TELUGANA.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            next_button.click()
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
        except TimeoutException:
            print("Timed out waiting for pagination element.")
            break
        except ElementClickInterceptedException:
            print("Element not clickable, trying to click using JavaScript")
            
    return LINKS_TELUGANA,ROUTE_TELUGANA

LINKS_TELUGANA,ROUTE_TELUGANA=Telugana_link_route("//a[@class='route']")


# In[23]:


df_T=pd.DataFrame({"Route_name":ROUTE_TELUGANA,"Route_link":LINKS_TELUGANA})
df_T


# In[33]:


# change dataframe to csv
path=r"C:\Users\ajant\OneDrive\Desktop\redbus-data-scraping\Redbus\df_T.csv"
df_T.to_csv(path,index=False)


# # Goa Routes

# In[26]:


#open the browser

driver_G=webdriver.Chrome()

#load the webpage
driver_G.get("https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile")

time.sleep(3)

driver_G.maximize_window()


# In[27]:


#retrive bus links and route
wait = WebDriverWait(driver_G, 20)
def Kadamba_link_route(path):   
    LINKS_KADAMBA=[]
    ROUTE_KADAMBA=[]
    
    for i in range(1,4):
        paths=driver_G.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            LINKS_KADAMBA.append(d)
            
        # retrive names of the routes
        for route in paths:
            ROUTE_KADAMBA.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            next_button.click()
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
        except TimeoutException:
            print("Timed out waiting for pagination element.")
            break
        except ElementClickInterceptedException:
            print("Element not clickable, trying to click using JavaScript")
            
    return LINKS_KADAMBA,ROUTE_KADAMBA

LINKS_KADAMBA,ROUTE_KADAMBA=Kadamba_link_route("//a[@class='route']")


# In[28]:


df_G=pd.DataFrame({"Route_name":ROUTE_KADAMBA,"Route_link":LINKS_KADAMBA})
df_G


# In[34]:


# change dataframe to csvp
path=r"C:\Users\ajant\OneDrive\Desktop\redbus-data-scraping\Redbus\df_G.csv"
df_G.to_csv(path,index=False)


# 
# # Rajastan routes
# 

# In[40]:


#open the browser

driver_R=webdriver.Chrome()

#load the webpage
driver_R.get("https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_R.maximize_window()


# In[41]:


#retrive bus links and route
wait = WebDriverWait(driver_R, 20)
def Rajastan_link_route(path):   
    LINKS_RAJASTAN=[]
    ROUTE_RAJASTAN=[]
    
    for i in range(1,4):
        paths=driver_R.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            LINKS_RAJASTAN.append(d)
            
        # retrive names of the routes
        for route in paths:
            ROUTE_RAJASTAN.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            next_button.click()
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
        except TimeoutException:
            print("Timed out waiting for pagination element.")
            break
        except ElementClickInterceptedException:
            print("Element not clickable, trying to click using JavaScript")
        
            
    return LINKS_RAJASTAN,ROUTE_RAJASTAN

LINKS_RAJASTAN,ROUTE_RAJASTAN=Rajastan_link_route("//a[@class='route']")


# In[42]:


df_R=pd.DataFrame({"Route_name":ROUTE_RAJASTAN,"Route_link":LINKS_RAJASTAN})
df_R


# In[43]:


# change dataframe to csv
path=r"C:\Users\ajant\OneDrive\Desktop\redbus-data-scraping\Redbus\df_R.csv"
df_R.to_csv(path,index=False)


# In[ ]:




