def calculate(totaleEgg, totaleGeld, totaleFooi, besteldo, overeVWo, overNUo, kapotto):
    totalGeld = totaleGeld 
    totalEgg = totaleEgg
    totalEgg = round(totalEgg, 2) 
    totalFooi = totaleFooi

    eggPrijs = 0.28

    besteld = besteldo
    kapot = kapotto
    overVW = overeVWo
    overNU = overNUo

    verkocht = besteld + overVW - overNU - kapot

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

    totalProvis = verkocht * provisie
    teBetalen = (verkocht * provisie) + totalFooi - teKort
    teBetalen = round(teBetalen, 2)
    print(teBetalen)
    return besteld, overVW, overNU, kapot, verkocht, provisie, totalProvis, totalFooi, totalGeld, teKort
if __name__ == "__main__":
    calculate()