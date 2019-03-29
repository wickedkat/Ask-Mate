import data_manager as dm
from validation import form_validation as fv


def get_answers(question_id):
    try:
        return dm.get_answers(question_id)
    except ValueError as e:
        print(e)
    return []


def add_answer(answer):
    message = fv.remove_parentheses(answer['message'])
    message = fv.check_is_not_empty(message)
    user_id = answer['user_id']
    if message:
        answer_new = {
            'message': message,
            'user_id': user_id
        }
        answer.update(answer_new)
        dm.add_one_answer(answer)
        return True
    else:
        return False


def get_one_answer(answer_id):
    try:
        return dm.get_one_answer(answer_id)
    except ValueError as e:
        print(e)


def update_answer(answer):
    message = fv.remove_parentheses(answer['message'])
    message = fv.check_is_not_empty(message)
    if message:
        answer_new = {
            'message': message,
        }
        answer.update(answer_new)
        dm.update_answer(answer)
        return True
    else:
        return False


def delete_answer(answer_id):
    try:
        dm.delete_answer(answer_id)
    except ValueError as e:
        print(e)
