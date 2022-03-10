from __future__ import print_function, unicode_literals
from calendar import SUNDAY, week
import re
import datetime
from api import getTransactions
from calc import calculate
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from email_validator import validate_email, EmailNotValidError
from PyInquirer import Validator, ValidationError
from Factuur import factuur
import json


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

def weekDates(weeko):
    week = weeko
    d1 = "2022-W" + str(int(week) - 1)
    d2 = "2022-W" + str(week)
    r1 = datetime.datetime.strptime(d1 + '-6', "%Y-W%W-%w")
    saturday = str(r1).split(' ')[0]
    r2 = datetime.datetime.strptime(d2 + '-5', "%Y-W%W-%w")
    friday = str(r2).split(' ')[0]
    return saturday, friday

creds = json.load(open('creds.json', "r"))
account1 = creds["account1"]["email"]
account2 = creds["account2"]
account3 = creds["account3"]
print(creds)

accountQuestion = [
    {
        'type': 'list',
        'name': 'account',
        'message': 'Selecteer uw Sumup account',
        'choices': [
            account1,
            account2,
            account3,
            'Nieuw'
        ]
    }
]

accountAnswers = prompt(accountQuestion, style=style)

loginQuestions = [
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
]
weekQuestion =[
    {
        'type': 'input',
        'name': 'week',
        'message': 'Voer hier het weeknummer in: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    }
]
print(accountAnswers)
if accountAnswers["account"] == 'Nieuw':
    loginAnswers = prompt(loginQuestions, style=style)
    emailAdded = False 
    pswdAdded = False
    print(type(creds))
    for account in creds:
        acc = creds[account]
        if emailAdded == False and pswdAdded == False:
            if acc["email"] == "":
                acc["email"] = loginAnswers["email"]
                emailAdded = True
            if acc["pswd"] == "":
                acc["pswd"] = loginAnswers["password"]
                pswdAdded = True
    creds = json.dump(creds, open('creds.json', "w"))

weekAnswers = prompt(weekQuestion, style=style)
saturday = list(weekDates(weekAnswers["week"]))[0]
friday = list(weekDates(weekAnswers["week"]))[1]
totals = list(getTransactions(loginAnswers["email"], loginAnswers["password"], saturday, friday)) # [egg, total, fooi]


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
        'name': 'kapot',
        'message': 'Aantal kapotte eieren: ',
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
        'name': 'overNU',
        'message': 'Aantal eieren over nu: ',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    }
]

eggAnswers = prompt(eggQuestions, style=style)
print(eggAnswers)

calcList = list(calculate(totals[0], totals[1], totals[2], eggAnswers["besteld"], eggAnswers["overVW"], eggAnswers["overNU"], eggAnswers["kapot"]))



factuur(calcList[0], calcList[1], calcList[2], calcList[3], calcList[4], calcList[5], calcList[6], calcList[7], calcList[8], calcList[9], weekAnswers["week"], saturday, friday)
