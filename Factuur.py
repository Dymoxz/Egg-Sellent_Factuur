from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import time

time.sleep(1)

# from main import eggBesteld, eggOverVW, eggOverNu, eggKapot, eggVerkocht, provisieEi, loon, fooiPin, opbrengstR, teKort
def factuur(eggBesteld, eggOverVW, eggOverNu, eggKapot, eggVerkocht, provisieEi, loon, fooiPin, opbrengstR, teKort, weekNummer, zaterdag, vrijdag):
    img = Image.open("Factuur.jpg")
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("calibri-bold.ttf", 60)
    #week
    draw.text((1040, 980),str(weekNummer),(70,70,70),font=font)
    draw.text((1120, 980),str(zaterdag) + ' /',(70,70,70),font=font)
    draw.text((1120, 1025),str(vrijdag),(70,70,70),font=font)

    font = ImageFont.truetype("calibri-bold.ttf", 75)

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((270, 1215),str(eggBesteld),(70,70,70),font=font)
    draw.text((875, 1215),str(eggOverVW),(70,70,70),font=font)
    draw.text((2060, 1215),str(eggBesteld + eggOverVW),(70,70,70),font=font)
    draw.text((1550, 1215),str(eggKapot),(70,70,70),font=font)
    draw.text((1060, 1375),str(eggOverNu),(70,70,70),font=font)
    draw.text((575, 1575),str(eggVerkocht),(70,70,70),font=font)
    font = ImageFont.truetype("calibri-bold.ttf", 70)
    draw.text((965, 1580),str(provisieEi),(70,70,70),font=font)
    draw.text((2100, 1565),str(round(loon, 2)),(70,70,70),font=font)
    draw.text((2100, 1640),str(round(fooiPin, 2)),(70,70,70),font=font)

    draw.text((1190, 1800),str(round(opbrengstR, 2)),(70,70,70),font=font)

    lastLine = str(round(loon, 2) + round(fooiPin, 2)) + '  -  ' + str(teKort) + '  =  ' + str((round(loon, 2) + round(fooiPin, 2)) - teKort)
    draw.text((1175, 1905),lastLine,(70,70,70),font=font)
    if teKort > 0:
        cashUitleg = str(teKort) + '  =   Cash / Tikkie'
        draw.text((1600, 1792),cashUitleg,(70,70,70),font=font)
    img.save('Factuur-out.jpg')

if __name__ == "__main__":
    factuur()