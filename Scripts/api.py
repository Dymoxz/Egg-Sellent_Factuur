from matplotlib.pyplot import magma
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import requests
from requests.structures import CaseInsensitiveDict
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys, os
from datetime import datetime
import aiohttp
import asyncio
from tqdm import tqdm
clientID = 'cc_classic_0kJ7gzKMcbtqpQMDmoegJTScAv75z'
clientSecret = 'cc_sk_classic_QnEiqnA4VQR2UPWpJtbOuPJWwzcYbo9hV8dvGsSl7q1DfbuKWs'
redirectURL = 'https://cakeeatergames.github.io/ThisButtonDoesNothing/index.html'


#Chrome driver options
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
if getattr(sys, 'frozen', False): 
    # executed as a bundled exe, the driver is in the extracted folder
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")

    driver = webdriver.Chrome(chromedriver_path, options=options)
else:
    driver = webdriver.Chrome('Scripts\chromedriver.exe', options=options)

def getTransactions(email, pswd, start_date, end_date):


    startTime = datetime.now()
    username = email
    password = pswd

    getClientID = f'https://api.sumup.com/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURL}'

    driver.get(getClientID)
    print()
    print('Ingloggen..')
    with tqdm(total=4, colour='cyan',  bar_format='{l_bar}{bar:25}{r_bar}{bar:-10b}') as loginBar:
        #Enter the username and password for authentication
        
        inputElement = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        inputElement.send_keys(username)
        loginBar.update(1)
        loginBar.set_postfix({'actie': 'Email invoeren'})

        inputElement = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        inputElement.send_keys(password)
        loginBar.update(1)
        loginBar.set_postfix({'actie': 'Wachtwoord invoeren'})

        confirm = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "login-button")))
        confirm.click()
        loginBar.update(1)
        loginBar.set_postfix({'actie': 'Inloggen'})

        try:
            machtig = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//button[text()=' Machtigen ']")))
            machtig.click()
        except TimeoutException:
            pass

        # try:
        #     machtig = driver.find_element_by_xpath("//button[text()=' Machtigen ']")
        #     machtig.click()
        #     print('Authorization Complete.')
        # except NoSuchElementException:
        #     print('Already Authorized.')
        #     pass

        try:
            uselessButton = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "button")))
            uselessButton.click()
            loginBar.update(1)
            loginBar.set_postfix({'actie': 'Authoriseren'})

        except TimeoutException:
            print('Inloggen mislukt..')
            exit()

    url = driver.current_url
    code = url.split('code=')[1]

    #Post the access token and recieve an authorization code
    accesTokenPost = requests.post('https://api.sumup.com/token', json={"grant_type": "authorization_code",
                                                                        "client_id": clientID,
                                                                        "client_secret": clientSecret,
                                                                        "code": code})
    postJson = accesTokenPost.json()
    accessToken = postJson['access_token']



    # AUTHORIZATION DONE 





    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {accessToken}"

    #Get a dictonary with all transactions between start_date & end_date
    transListGet =  requests.get('https://api.sumup.com/v0.1/me/transactions/history',headers=headers, params={
                                                                                                "oldest_time": start_date,
                                                                                                "newest_time": end_date,
                                                                                                "limit": 1000                                                                       
                                                                                                })

    transJson = transListGet.json()
    # print(transJson)
    # print(transListGet.status_code)

    # #Remove the failed transactions from the dict
    # i=0
    # for item in transJson["items"]:
    #     if item["status"] == "FAILED":
    #         transJson["items"].pop(i)
    #     i+=1

    Oldsummary = transJson

    allTrans = [x for x in Oldsummary["items"]]

    allTransComplete = []

    nonoStatus = []

    #Get a more detailed transaction for everythin in dict
    realTransLen = 0
    for trans in allTrans:
        if trans["status"] != "FAILED":
            realTransLen += 1
        else:
            pass

    


    start_time = time.time()
    print()
    print('Transacties Ophalen..')

    async def main():
        # apigetter = Progress().add_task("[cyan]Cooking...", total=realTransLen)
        async with aiohttp.ClientSession() as session:
            transWprogress = tqdm(allTrans, bar_format='{l_bar}{bar:25}{r_bar}{bar:-10b}', colour='cyan')
            for trans in transWprogress:
                transWprogress.set_postfix({'transaction code': trans["transaction_code"]})
                pokemon_url = 'https://api.sumup.com/v0.1/me/transactions'
                if trans["status"] != "FAILED":
                    async with session.get(pokemon_url, headers=headers, params={ "id": trans["id"]}) as resp:
                        detailTrans = await resp.json()
                        allTransComplete.append(detailTrans)
                    # Progress().update(apigetter, advance=1)
                else:
                    pass
    
    asyncio.get_event_loop().run_until_complete(main())













    # for trans in allTrans:
    #     if trans["status"] != "FAILED":
    #         allTransGet =  requests.get('https://api.sumup.com/v0.1/me/transactions',headers=headers, params={ "id": trans["id"]})
    #         allTransComplete.append(allTransGet.json())
    #     else:
    #         pass

    json_string = {"items": allTransComplete}

    with open('Data/CompleteTrans.json', 'w') as outfile:
       json.dump(json_string, outfile)


    # API COMPLETE

    totalGeld = 0
    totalEgg = 0
    totalFooi = 0
    aasjdkn = 0

    for transaction in allTransComplete:
        curTotal = 0
        curEgg = 0
        curFooi = 0
        for item in transaction["products"]:
            if "eieren" in item["name"] or "Eieren" in item["name"]:
                curEgg += item["total_with_vat"]
            if "Fooi" in item["name"] or 'fooi' in item["name"]: 
                curFooi += item["total_with_vat"]
        curTotal = curEgg + curFooi
        totalGeld += curTotal
        totalEgg += curEgg
        totalFooi += curFooi
        aasjdkn += 1
    return totalEgg, totalGeld, totalFooi

if __name__ == "__main__":
   getTransactions()