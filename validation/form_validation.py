from flask import Flask, request
import re

app = Flask(__name__)


def check_conditions_of_sorting(conditions):
    attribute_list = ['submission_time', 'title']
    order_list = ['asc', 'desc']
    attribute = conditions['attribute']
    order = conditions['order']
    if attribute in attribute_list and order in order_list:
        return True
    else:
        return False


def remove_parentheses(string):
    string = re.sub('\<|\>|\{|\}|\[|\]', '', string)
    return string


def check_is_not_empty(string):
    if len(string) == 0 or string.isspace():
        return False
    return string
