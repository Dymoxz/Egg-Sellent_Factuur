from api import getTransactions
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

getTransactions('dymowaltheer146@egg-sellent.nl', 'Dikketyfus94!', '2022-01-22', '2022-01-28')

kivy.require('1.9.0')

class MyRoot(BoxLayout):
    
    def __init__(self):
        super(MyRoot, self).__init__()
    
    def getTransactionee(self):
        self.totalGeld.text = getTransactions.totalGeld


class SumupFactuur(App):

    def build(self):
        return MyRoot()

SumupFactuur = SumupFactuur()
SumupFactuur.run()