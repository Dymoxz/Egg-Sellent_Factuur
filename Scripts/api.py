from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import requests
from requests.structures import CaseInsensitiveDict
import time
import json

clientID = 'ZK3NWDD0xencY-DFAJ6Ulg'
clientSecret = '56a987f382d00f80b93d2d318f85d75d'
redirectURL = 'https://sumuppy.ddns.net:420'


options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('Scripts\chromedriver.exe', options=options)

def getTransactions(email, pswd, start_date, end_date):
    username = email
    password = pswd

    getClientID = f'https://api.sumup.com/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURL}'

    driver.get(getClientID)

    time.sleep(2)

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
    #print(url)
    #print('code:  ', code)


    accesTokenPost = requests.post('https://api.sumup.com/token', json={"grant_type": "authorization_code",
                                                                        "client_id": clientID,
                                                                        "client_secret": clientSecret,
                                                                        "code": code})
    postJson = accesTokenPost.json()
    accessToken = postJson['access_token']
    #print('Access token:  ', accessToken)




    # AUTHORIZATION DONE 





    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {accessToken}"

    transListGet =  requests.get('https://api.sumup.com/v0.1/me/transactions/history',headers=headers, params={ "oldest_time": start_date,
                                                                                                "newest_time": end_date,
                                                                                                "limit": 500
                                                                                                })

    transJson = transListGet.json()

    i=0
    for item in transJson["items"]:
        if item["status"] == "FAILED":
            transJson["items"].pop(i)
        i+=1
    #print(transListGet.status_code)
    #print(transJson)

    Oldsummary = transJson
    # i=0
    # for item in summary["items"]:
    #     try:
    #         print(item["product_summary"])
    #     except:
    #         noSummary.update(item)
    #         summary["items"].pop(i)
    #     i+=1

    summary = [x for  x in Oldsummary["items"] if "product_summary" in x]
    noSummary = [x for  x in Oldsummary["items"] if "product_summary" not in x]
    noSummaryFixed = []

    allTrans = [x for x in Oldsummary["items"]]

    allTransComplete = []

    for trans in allTrans:
        allTransGet =  requests.get('https://api.sumup.com/v0.1/me/transactions',headers=headers, params={ "id": trans["id"]})
        allTransComplete.append(allTransGet.json())

    #print(allTransComplete)
    json_string = {"items": allTransComplete}

    with open('Data\CompleteTrans.json', 'w') as outfile:
        json.dump(json_string, outfile)


   #print('kasjdkas',len(allTransComplete))

    # API SHIT COMPLETE


    totalGeld = 0
    totalEgg = 0
    totalFooi = 0
    aasjdkn = 0

    for transaction in allTransComplete:
        curTotal = 0
        curEgg = 0
        curFooi = 0
        for item in transaction["products"]:
            #print(item["name"], item["total_with_vat"])
            if "eieren" in item["name"]:
                curEgg += item["total_with_vat"]
            if "Fooi" in item["name"]: 
                curFooi += item["total_with_vat"]
        curTotal = curEgg + curFooi
        #print(curEgg, curFooi, curTotal)
        #print('---------------------')
        totalGeld += curTotal
        totalEgg += curEgg
        totalFooi += curFooi
        aasjdkn += 1
    return totalEgg, totalGeld, totalFooi
    #print(aasjdkn)
    #print(totalGeld, totalEgg, totalFooi)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   getTransactions()