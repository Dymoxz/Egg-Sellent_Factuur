from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import requests
from requests.structures import CaseInsensitiveDict
import time
import json
import sys, os

clientID = 'ZK3NWDD0xencY-DFAJ6Ulg'
clientSecret = '56a987f382d00f80b93d2d318f85d75d'
redirectURL = 'https://sumuppy.ddns.net:420'


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
    username = email
    password = pswd

    getClientID = f'https://api.sumup.com/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURL}'

    driver.get(getClientID)

    time.sleep(2)
    #Enter the username and password for authentication
    inputElement = driver.find_element_by_id("username")
    inputElement.send_keys(username)
    print('Username entered...')
    time.sleep(.5)
    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(password)
    print('Password entered...')
    time.sleep(.5)
    confirm = driver.find_element_by_id("login-button")
    confirm.click()
    print('Logging in complete.')
    time.sleep(.5)
    try:
        machtig = driver.find_element_by_xpath("//button[text()=' Machtigen ']")
        machtig.click()
        print('Authorization Complete.')
    except NoSuchElementException:
        print('Already Authorized.')
        pass

    time.sleep(4)
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
    for trans in allTrans:
        if trans["status"] != "FAILED":
            allTransGet =  requests.get('https://api.sumup.com/v0.1/me/transactions',headers=headers, params={ "id": trans["id"]})
            allTransComplete.append(allTransGet.json())
        else:
            pass

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
            if "eieren" in item["name"]:
                curEgg += item["total_with_vat"]
            if "Fooi" in item["name"]: 
                curFooi += item["total_with_vat"]
        curTotal = curEgg + curFooi
        totalGeld += curTotal
        totalEgg += curEgg
        totalFooi += curFooi
        aasjdkn += 1
    return totalEgg, totalGeld, totalFooi

if __name__ == "__main__":
   getTransactions()