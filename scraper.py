import requests
from bs4 import BeautifulSoup
import smtplib # allows you to send emails
import time 

# Insert your product's URL here
URL = "https://www.amazon.ca/Acer-CB272-bmiprx-FreeSync-Technology/dp/B07WMTLW2R/ref=sr_1_8?crid=FYI9L1R1IK54&keywords=acer+monitor&qid=1692073193&sprefix=acer+moni%2Caps%2C342&sr=8-8&ufe=app_do%3Aamzn1.fos.d0e27fc4-6417-4b26-97cb-f959a9930752"
DESIRED_PRICE = 200 # Insert your own desired price here
EMAIL = "test.scraperpython@gmail.com" # Insert your email address here
PASSKEY = "uejsycslxgkayrfq" # Insert your password here

# Gives information about the user's browser
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

def check_price():
    # Call the webpage?
    page = requests.get(URL, headers=headers)

    # Excracts the content inside the page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get title and price of product on website
    title = soup.find(id="productTitle").get_text()
    price = soup.find(class_="a-price-whole").get_text()
    # Convert price from string to float
    converted_price = float(price)

    # Send a notification if current price is lower than old price
    if (converted_price < DESIRED_PRICE):
        send_mail()
    
    print(title.strip() + "\n")
    print("Current price: " + str(converted_price))

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() # A command used by the email server to identify itself when connecting to another server
    server.starttls() # Encrypts the connection
    server.ehlo()

    server.login(EMAIL, PASSKEY)

    # Create subject and body of email
    subject = "Price fell down!"

    body = 'Link to the product: ' + URL
    
    msg = f"Subject: {subject}\n\n{body}"

    # Send email
    server.sendmail(
        EMAIL,
        EMAIL,
        msg
    )
    print("EMAIL HAS BEEN SENT! \n")

    server.quit()

# Check the price once a day
while (True):
    check_price()
    time.sleep(60 * 60 * 24) 