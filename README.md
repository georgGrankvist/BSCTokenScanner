# Binance Smart Chain Contract Scraper + Contract Evaluator
Pulls Binance Smart Chain feed of newly-verified contracts every 30 seconds, then checks their contract code for links to socials.
Returns only those with socials information included, and then submits the contract address to TokenSniffer to evaluate contract legitimacy.  

Sample execution:  
![2b423cea3307c40b307fdfdfe2528592](https://user-images.githubusercontent.com/62744506/149968695-6a91dc12-be82-408b-9082-ff5796896391.png) 



Its common practice to include links to social media such as Telegram somewhere in the contract for added transparency, the idea of the scraper being to return new
contracts just as they come out that have websites, social media etc. that demonstrates some level of ambition - just a website is often enough for decently high market caps.  

Generally the contracts returned will never have high evaluation scores as they have just come out and TokenSniffers evaluation criteria is based on
factors like buying fees, contract ownership renouncals, liquidity locks etc. which in most cases are set some time after contract verification.

Upon startup you'll have to solve the captcha that appears in the ChromeDriver window to bypass TokenSniffer's bot protection.
Contracts returned with scores around 40-50 are ones to keep a look at generally as their overall evaluation is bound to be high if they decide to do those things mentioned
when launching. In general, I advise to trade these tokens returned by the scraper with caution, many of them are scams and will just lose you your funds.
However, as this scraper returns contracts when they just come out there is ample opportunity to be very early to good projects too. DYOR!

Future versions might implement frameworks like pupeteer to bypass the captcha so we can run the driver headlessly without that annoying chrome window. 

To run:   
1.Install Google Chrome.   
2.Import selenium, requests, time into a python3 environment of your choice  
3. Install the Chrome webdriver from: https://chromedriver.chromium.org/home    
4. Pass in the directory location of your chromedriver.exe as a String argument into the Service object on line 29   


![ce4e75df3c012907aee2c9559c250f30](https://user-images.githubusercontent.com/62744506/149964319-ce99bc2f-46ff-4cb7-8f89-c5791a8cb489.png)   

5.  Run Bsc_Contract_Scraper.py  


New contracts will be printed into the console, you can then go to the contract code to find the links to eventual social media/website.   



