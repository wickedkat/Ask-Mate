import data_manager as dm
from validation import form_validation as fv


def get_all_comments_by_question(question_id):
    try:
        return dm.get_all_comments_by_question(question_id)
    except ValueError as e:
        print(e)
    return []


def add_comment(comment):
    message = fv.remove_parentheses(comment['message'])
    message = fv.check_is_not_empty(message)
    if message :
        comment_new = {
            'message': message
        }
        comment.update(comment_new)
        dm.add_one_comment(comment)
        return True
    else:
        return False


def get_one_comment(comment_id):
    try:
        return dm.get_comment_by_id(comment_id)
    except ValueError as e:
        print(e)


def update_comment(comment):
    message = fv.remove_parentheses(comment['message'])
    message = fv.check_is_not_empty(message)
    if message:
        comment_new = {
            'message': message,
        }
        comment.update(comment_new)
        dm.update_comment(comment)
        return True
    else:
        return False


def delete_comment(comment_id):
    try:
        dm.delete_comment(comment_id)
    except ValueError as e:
        print(e)
