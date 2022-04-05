from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import time
import json

time.sleep(1)

def factuur(eggBesteld, eggOverVW, eggOverNu, eggKapot, eggVerkocht, provisieEi, loon, fooiPin, opbrengstR, teKort, weekNummer, zaterdag, vrijdag, teKortB):
    img = Image.open("Images/Factuur.jpg")
    draw = ImageDraw.Draw(img)

    info = json.load(open(('Data/info.json'), 'r'))
    # font = ImageFont.truetype(<font-file>, <font-size>)

    font = ImageFont.truetype("Data/calibri-bold.ttf", 50)

    #Add the personal info
    draw.text((850, 490),str(info["name"]),(70,70,70),font=font)
    draw.text((850, 590),str(info["adress"]),(70,70,70),font=font)
    draw.text((850, 690),str(info["postcode/wp"]),(70,70,70),font=font)
    draw.text((850, 790),str(info["rekening"]),(70,70,70),font=font)


    font = ImageFont.truetype("Data/calibri-bold.ttf", 60)
    #week
    draw.text((1040, 980),str(weekNummer),(70,70,70),font=font)
    draw.text((1120, 980),str(zaterdag) + ' /',(70,70,70),font=font)
    draw.text((1120, 1025),str(vrijdag),(70,70,70),font=font)

    font = ImageFont.truetype("Data/calibri-bold.ttf", 75)

    loon = round(loon, 2)
    fooiPin = round(fooiPin, 2)
    teKort = round(teKort, 2)
    opbrengstR = round(opbrengstR, 2)

    draw.text((270, 1215),str(eggBesteld),(70,70,70),font=font)
    draw.text((875, 1215),str(eggOverVW),(70,70,70),font=font)
    draw.text((2060, 1215),str(eggBesteld + eggOverVW),(70,70,70),font=font)
    draw.text((1550, 1215),str(eggKapot),(70,70,70),font=font)
    draw.text((1060, 1375),str(eggOverNu),(70,70,70),font=font)
    draw.text((575, 1575),str(eggVerkocht),(70,70,70),font=font)
    font = ImageFont.truetype("Data/calibri-bold.ttf", 70)
    draw.text((965, 1580),str(provisieEi),(70,70,70),font=font)
    draw.text((2100, 1565),str(loon),(70,70,70),font=font)
    draw.text((2100, 1640),str(fooiPin),(70,70,70),font=font)

    draw.text((1190, 1800),str(opbrengstR),(70,70,70),font=font)

    lastLine = str(round(loon + fooiPin, 2)) + '  -  ' + str(teKort) + '  =  ' + str(round(loon + fooiPin - teKort, 2))
    draw.text((1175, 1905),lastLine,(70,70,70),font=font)
    if teKort > 0:
        cashUitleg = str(teKort) + f'  =  {teKortB}'
        draw.text((1600, 1792),cashUitleg,(70,70,70),font=font)
    img.save(f'Facturen/Week-{str(weekNummer)}.jpg')

if __name__ == "__main__":
    factuur()