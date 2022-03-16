from __future__ import print_function, unicode_literals
import datetime

from api import getTransactions
from calc import calculate
from Factuur import factuur

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from email_validator import validate_email, EmailNotValidError
from PyInquirer import Validator, ValidationError



style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class EmailValidator(Validator):
    def validate(self, document):
        try:
            valid = validate_email(document.text)
        #ok = re.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        except EmailNotValidError as e:
            raise ValidationError(
                message='Please enter a valid email adress',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


print('Hallo, welkom bij de Egg-Sellent auto factuur')


#krijg de data van zaterdag/vrijdag aan de hand van het weeknummer
def weekDates(weeko):
    week = weeko
    d1 = "2022-W" + str(int(week) - 1)
    d2 = "2022-W" + str(week)
    r1 = datetime.datetime.strptime(d1 + '-6', "%Y-W%W-%w")
    saturday = str(r1).split(' ')[0]
    r2 = datetime.datetime.strptime(d2 + '-5', "%Y-W%W-%w")
    friday = str(r2).split(' ')[0]
    return saturday, friday


sumupQuestions = [
    {
        'type': 'input',
        'name': 'email',
        'message': 'Voer hier uw Sumup email adres in: ',
        'validate': EmailValidator
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Voer hier uw Sumup wachtwoord in: '
    },
    {
        'type': 'input',
        'name': 'week',
        'message': 'Voer hier het weeknummer in: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    }
]

sumupAnswers = prompt(sumupQuestions, style=style)
saturday = list(weekDates(sumupAnswers["week"]))[0]
friday = list(weekDates(sumupAnswers["week"]))[1]
totals = list(getTransactions(sumupAnswers["email"], sumupAnswers["password"], saturday, friday)) # [egg, total, fooi]


print('-----Sumup Complete-----')


eggQuestions = [
    {
        'type': 'input',
        'name': 'besteld',
        'message': 'Aantal bestelde eieren: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'overVW',
        'message': 'Aantal eieren over van vorige week: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'kapot',
        'message': 'Aantal kapotte eieren: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'overNU',
        'message': 'Aantal eieren over nu: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    }
]

eggAnswers = prompt(eggQuestions, style=style)
#print(eggAnswers)


#bereken de loon, provisie etc.
calcList = list(calculate(totals[0], totals[1], totals[2], eggAnswers["besteld"], eggAnswers["overVW"], eggAnswers["overNU"], eggAnswers["kapot"]))
print()
print('-----Gegevens berenkend-----')
print()

teKortQuestions = [
    {
        'type': 'list',
        'name': 'teKortBeschrijving',
        'message': f'Er is een te kort van €{calcList[9]}, geef een beschrijving: ',
        'choices': [
            'Cash',
            'Tikkie',
            'Cash/Tikkie',
            {
                'name': 'Custom',
                'disabled': 'Niet beschikbaar'
            },
            'Exit'
        ]
    }
]   
#   teKort
if calcList[9] > 0: 
    teKortAnswers = prompt(teKortQuestions, style=style)
#print((teKortAnswers))

if teKortAnswers["teKortBeschrijving"] == 'Exit':
    exit()


#zet alle data op het factuur
#       eggBesteld,  eggOverVW,    eggOverNu,   eggKapot,   eggVerkocht, provisieEi,    loon,       fooiPin,    opbrengstR,   teKort,         weekNummer,       zaterdag, vrijdag
factuur(calcList[0], calcList[1], calcList[2], calcList[3], calcList[4], calcList[5], calcList[6], calcList[7], calcList[8], calcList[9], sumupAnswers["week"], saturday, friday, teKortAnswers["teKortBeschrijving"])
print()
print('-----Factuur gegenereerd-----')
print()
print(f'Locatie:  "Facturen/Week-{str(sumupAnswers["week"])}.jpg"')
input()