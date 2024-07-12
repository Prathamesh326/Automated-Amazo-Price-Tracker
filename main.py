import os

import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
target_price = 100

response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-US"})
data = response.text
soup = BeautifulSoup(data, "html.parser")
print(soup.prettify())

whole_price = soup.find(class_="a-price-whole").getText()
fraction_price = soup.find(class_="a-price-fraction").getText()
final_price = float(whole_price + fraction_price)

title = soup.find(id="productTitle").get_text().strip()
print(title)

if final_price < target_price:
    message = f"{title} is on sale for {final_price}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")

        )
