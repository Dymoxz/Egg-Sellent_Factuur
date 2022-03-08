from __future__ import print_function, unicode_literals
from calendar import week
import re
import datetime
from api import getTransactions
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


print('Hi, welcome to Python Pizza')

def weekDates(weeko):
    week = weeko
    d1 = "2022-W" + str(int(week) - 1)
    d2 = "2022-W" + str(week)
    r1 = datetime.datetime.strptime(d1 + '-6', "%Y-W%W-%w")
    saturday = str(r1).split(' ')[0]
    r2 = datetime.datetime.strptime(d2 + '-5', "%Y-W%W-%w")
    friday = str(r2).split(' ')[0]
    return saturday, friday


questions = [
    {
        'type': 'input',
        'name': 'email',
        'message': 'Voer hier uw Sumup email adres in.',
        'validate': EmailValidator
    },
    {
        'type': 'input',
        'name': 'password',
        'message': 'Voer hier uw Sumup wachtwoord in.'
    },
    {
        'type': 'input',
        'name': 'week',
        'message': 'Voer hier het weeknummer in.',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    # {
    #     'type': 'list',
    #     'name': 'size',
    #     'message': 'What size do you need?',
    #     'choices': ['Large', 'Medium', 'Small'],
    #     'filter': lambda val: val.lower()
    # },
    # {
    #     'type': 'input',
    #     'name': 'quantity',
    #     'message': 'How many do you need?',
    #     'validate': NumberValidator,
    #     'filter': lambda val: int(val)
    # },
    # {
    #     'type': 'expand',
    #     'name': 'toppings',
    #     'message': 'What about the toppings?',
    #     'choices': [
    #         {
    #             'key': 'p',
    #             'name': 'Pepperoni and cheese',
    #             'value': 'PepperoniCheese'
    #         },
    #         {
    #             'key': 'a',
    #             'name': 'All dressed',
    #             'value': 'alldressed'
    #         },
    #         {
    #             'key': 'w',
    #             'name': 'Hawaiian',
    #             'value': 'hawaiian'
    #         }
    #     ]
    # },
    # {
    #     'type': 'rawlist',
    #     'name': 'beverage',
    #     'message': 'You also get a free 2L beverage',
    #     'choices': ['Pepsi', '7up', 'Coke']
    # },
    # {
    #     'type': 'input',
    #     'name': 'comments',
    #     'message': 'Any comments on your purchase experience?',
    #     'default': 'Nope, all good!'
    # },
    # {
    #     'type': 'list',
    #     'name': 'prize',
    #     'message': 'For leaving a comment, you get a freebie',
    #     'choices': ['cake', 'fries'],
    #     'when': lambda answers: answers['comments'] != 'Nope, all good!'
    # }
]

answers = prompt(questions, style=style)
saturday = list(weekDates(answers["week"]))[0]
friday = list(weekDates(answers["week"]))[1]
getTransactions(answers["email"], answers["password"], saturday, friday)

print('Order receipt:')
pprint(answers)