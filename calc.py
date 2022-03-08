totalGeld = 142.34 
totalEgg = 139.44000000000003
totalEgg = round(totalEgg, 2) 
totalFooi = 2.9

eggPrijs = 0.28

besteld = 480
overVW = 176
overNU = 132

verkocht = besteld + overVW - overNU

if verkocht < 500:
    provisie = 0.035
elif verkocht >= 500 and verkocht <= 999:
    provisie = float(0.03 + (int(str(verkocht)[0]) + 1) / 1000)
else:
    provisie = 0.03 + int(str(verkocht)[:2]) / 1000
provisie = round(provisie, 3)

eggVerkocht = round(totalEgg / eggPrijs)
needGeld = round(verkocht * eggPrijs, 2)

teKort = needGeld - totalEgg
teKort = round(teKort, 2)

print(totalEgg, needGeld, teKort)

teBetalen = (verkocht * provisie) + totalFooi - teKort
teBetalen = round(teBetalen, 2)
print(teBetalen)