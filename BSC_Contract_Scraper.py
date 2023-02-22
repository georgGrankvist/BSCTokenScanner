#! python3
#
# Pulls BSC Scan feed of newly-verified contracts every 30 seconds, then checks their contract code for links to socials
# Returns only those with socials information included, and then submits the contract address to TokenSniffer to evaluate contract legitimacy
# Its common practice to include links to social media such as Telegram somewhere in the contract for added transparency, the idea of the scraper being to return new
# contracts just as they come out that have websites, social media etc. that demonstrates some level of ambition - just a website is often enough for decently high market caps.
# Generally the contracts returned will never have high evaluation scores as they have just come out and TokenSniffers evaluation criteria is based on
# factors like buying fees, contract ownership renouncals, liquidity locks etc. which in most cases are set some time after contract verification.

# Upon startup you'll have to solve the captcha that appears in the ChromeDriver window to bypass TokenSniffer's bot protection.
# Contracts returned with scores around 40-50 are ones to keep a look at generally as their overall evaluation is bound to be high if they decide to do those things mentioned
# when launching. In general, I advise to trade these tokens returned by the scraper with caution, many of them are scams and will just lose you your funds.
# However, as this scraper returns contracts when they just come out there is ample opportunity to be very early to good projects too. DYOR!
# author Greek, GG

import requests
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service


URL = "https://bscscan.com/"
contractsFeedURL = URL + "contractsVerified"

options = uc.ChromeOptions()
options.add_argument('--headless')

#service = uc.chrome("C:\\Users\quant\Downloads\chromedriver.exe")
browser = uc.Chrome(use_subprocess=True,options=options)

payload = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/83.0.4103.116 Safari/537.36'}

addresses = []  # To store all the addresses pulled from the contracts feed
leadAddresses = []  # To store only those addresses whose contracts include socials information
keywords = ["t.me/", "twitter.com", "medium.com", ".finance"]  # Keywords being scraped for in smart contract headers, can include any keyword you want to query for


def FeedScan():  # Update the BSC Scan verified contracts feed and scrape the addresses of new additions

    res = requests.get(contractsFeedURL, headers=headers, data=payload)  # Load the BSC Scan new verified contracts page
    contractsFeed = res.text.split("<tbody>")[1]  # Break out the table of contracts from the page
    for i in range(1, 26):  # Iterate over each entry in the table, i.e. newest 25 records
        addrSplit = contractsFeed.split("href=\'/address/")[i].split("#code\'")[
            0]  # Break out the address of each individual token
        if not addrSplit in addresses:  # Check if the address has already been parsed or not
            addresses.append(addrSplit)


def ContractCheck(address):  # Check the contract code of a given token address and see if it contains links to socials

    contractURL = URL + "address/" + address + "#code"


    tokenSnifferUrl = "https://tokensniffer.com/token/bsc/" + address
    bscScanRequest = requests.get(contractURL, headers=headers, data=payload)

    try:
     contractText = bscScanRequest.text.split("id=\'editor\' style=\'margin-top: 5px;\'>")[1].split("</pre><br><script>")[0]
     tokenName = bscScanRequest.text.split("Contract Name:</div>")[1].split("mb-0\">")[1].split("</span>")[0]

     for kw in keywords:
        if kw in contractText and address not in leadAddresses:

            time.sleep(3)
            browser.get(tokenSnifferUrl)

            delay = 40

            try:
                element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[1]/table[1]/tbody/tr[1]/td/h2/span'))
                WebDriverWait(browser, delay).until(element_present)
                element = browser.find_element(By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[1]/table[1]/tbody/tr[1]/td/h2/span')
                tokenSnifferEval = element.text

                if not tokenSnifferEval:
                    print("Token: " + tokenName + ", URL: " + contractURL)
                    print("")


                else:
                    print("Token: " + tokenName + ", URL: " + contractURL + ", TokenSniffer evaluation score: " + tokenSnifferEval)
                    print("")
                    time.sleep(3)

            except TimeoutException:
                print("Token: " + tokenName + ", URL: " + contractURL)
                print("Couldn't load TokenSniffer for token " + tokenName + ", " + contractURL + ", took too much time or too many requests")
                print("")
            leadAddresses.append(address)
        else:
            continue

    except IndexError:
        pass


print("Checking BSCScan for new contracts with socials...")
while 1 == 1:  # Infinite loop checking for new contracts every 60 seconds
    FeedScan()
    counter = 0
    for i in addresses:
        if counter == 5:  # BSCScan rate limited at 5 requests per second
            time.sleep(3)
            counter = 0
        ContractCheck(i)
        counter += 1
    # print(leadAddresses)
    time.sleep(60)
    print("Refreshing new contract list...")
