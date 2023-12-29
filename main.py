import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# Pycharm could not install dotenv for some reason. Run this command from the terminal.
# pip install python-dotenv
from dotenv import load_dotenv

load_dotenv(".env")
HOST_EMAIL = os.environ["HOST_EMAIL"]
FROM_ADDR = os.environ["FROM_ADDR"]
FROM_ADDR_APP_PASSWORD = os.environ["FROM_ADDR_APP_PASSWORD"]
TO_ADDR = os.environ["TO_ADDR"]
BEST_BUY_ITEM_URL = (
    "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-4090-gaming-x-slim-24g-24gb-ddr6x-pci-express-4-0"
    "-graphics-card-black/6560954.p?skuId=6560954"
)
# Use a url for an item that is in stock.
TEST_URL = (
    "https://www.bestbuy.com/site/pny-nvidia-geforce-rtx-4070-ti-12gb-gddr6x-pci-express-4-0-graphics-card-with"
    "-triple-fan-and-dlss-3-black/6528733.p?skuId=6528733"
)
# You will receive a 403 Forbidden Error is you do not provide a User-Agent in the header for Best Buy's pages.
BEST_BUY_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
}
MESSAGE = MIMEMultipart("alternative")
MESSAGE["Subject"] = "Item in stock"
MESSAGE["From"] = FROM_ADDR
MESSAGE["To"] = TO_ADDR
TEXT = f"MSI - NVIDIA GeForce RTX 4090 GAMING X SLIM is in stock!\r\n{BEST_BUY_ITEM_URL}"
HTML = f"""
<html>
  <head></head>
  <body>
    <p>MSI - NVIDIA GeForce RTX 4090 GAMING X SLIM is in stock!<br>
       <a href={BEST_BUY_ITEM_URL}>Product Page</a>
    </p>
  </body>
</html>
"""
PART1 = MIMEText(TEXT, 'plain')
PART2 = MIMEText(HTML, 'html')
MESSAGE.attach(PART1)
MESSAGE.attach(PART2)


def get_page_content():
    response = requests.get(url=TEST_URL, headers=BEST_BUY_HEADER)
    response.raise_for_status()
    return response.text


def parse_button_text():
    site_content = get_page_content()
    soup = BeautifulSoup(site_content, "html.parser")
    button_text = soup.select_one("button[data-button-state]").get_text()
    # print(button_text)
    return button_text


def send_email():
    with smtplib.SMTP(HOST_EMAIL, port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_ADDR, password=FROM_ADDR_APP_PASSWORD)
        connection.sendmail(
            from_addr=FROM_ADDR,
            to_addrs=TO_ADDR,
            msg=MESSAGE.as_string()
        )


item_state = parse_button_text()
if item_state == "Add to Cart":
    send_email()
