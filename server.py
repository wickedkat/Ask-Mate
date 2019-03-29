from flask import Flask, render_template, request, redirect, url_for, session, flash

from logic import question_logic as ql
from logic import answer_logic as al
from logic import comment_logic as cl
from logic import user_logic as ul
import data_manager

app = Flask(__name__)
app.secret_key = "waw"

@app.route('/')
@app.route('/list')
def route_list():
    all_questions = ql.get_all_question()
    if not all_questions:
        flash('No data')
    return render_template('list.html',
                           all_questions=all_questions
                           )


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        user_id = session['id']
        question = {
            'title': title,
            'message': message,
            'user_id': user_id
        }
        result = ql.add_one_question(question)
        if result:
            return redirect('/')
        else:
            flash("Please, fill in form correctly")
    return render_template('edit.html',
                           form_url=url_for('route_add_question'),
                           page_title='Add Question',
                           button_title='Submit question'
                           )


@app.route('/question/<question_id>', methods=['GET'])
def route_question(question_id):
    question = ql.get_question(question_id)
    answers = al.get_answers(question_id)
    all_comments = cl.get_all_comments_by_question(question_id)
    return render_template('question.html',
                           question=question,
                           form_url=url_for('route_question', question_id=question_id),
                           page_title='Question',
                           answers=answers,
                           all_comments=all_comments
                           )


@app.route('/question/new-answer/<question_id>', methods=['GET', 'POST'])
def route_add_answer(question_id):
    question = ql.get_question(question_id)
    if request.method == 'POST':
        message = request.form.get('message')
        user_id = session['id']
        answer = {
            'message': message,
            'question_id': question_id,
            'user_id': user_id
        }
        result = al.add_answer(answer)
        if result:
            return redirect('/question/{}'.format(question_id))
        else:
            flash("Please, fill in form correctly")
    return render_template('answer.html',
                           page_title='Add Answer',
                           button_title='Submit answer',
                           form_url=url_for('route_add_answer', question_id=question_id),
                           question_id=question_id,
                           question=question
                           )


@app.route('/list/sorted')
def route_list_sorted():
    attribute = request.args.get('attribute')
    order = request.args.get('order')
    conditions = {
        'attribute': attribute,
        'order': order
    }
    sorted_data = ql.sorting_questions(conditions)
    if not sorted_data:
        return redirect(url_for('route_list'), code=302, Response=None)
    else:
        return render_template('list.html',
                               all_questions=sorted_data
                               )


@app.route('/edit-answer/<id>', methods=['GET', 'POST'])
def route_edit_answer(id):
    answer = al.get_one_answer(id)
    question_id = answer['question_id']
    question = ql.get_question(question_id)
    if request.method == "POST":
        message = request.form.get('message')
        answer = {
            'id': id,
            'message': message,
            'question_id': question_id
        }
        if al.update_answer(answer):
            return redirect('/question/{}'.format(question_id))
        else:
            flash("Please, fill in form correctly")
    return render_template('answer.html',
                           page_title='Add Answer',
                           button_title='Submit answer',
                           edit_answer=answer,
                           question=question
                           )


@app.route('/answer/new-comment/<answer_id>', methods=['GET', 'POST'])
def route_add_comment(answer_id):
    answer = al.get_one_answer(answer_id)
    question_id = answer['question_id']
    user_id = session['id']
    if request.method == 'POST':
        message = request.form.get('message')
        comment = {
            'message': message,
            'question_id': question_id,
            'answer_id': answer_id,
            'user_id': user_id
        }
        result = cl.add_comment(comment)
        if result:
            return redirect('/question/{}'.format(comment['question_id']))
        else:
            flash("Please, fill in form correctly")
    return render_template('comment.html',
                           page_title='Add comment',
                           button_title='Submit Comment',
                           form_url=url_for('route_add_comment', answer_id=answer_id),
                           answer_id=answer_id,
                           answer=answer
                           )


@app.route('/edit-comment/<comment_id>', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    comment = cl.get_one_comment(comment_id)
    question_id = comment['question_id']
    if request.method == "POST":
        message = request.form.get('message')
        comment = {
            'id': comment_id,
            'message': message,
            'question_id': question_id
        }
        if cl.update_comment(comment):
            return redirect('/question/{}'.format(question_id))
        else:
            flash("Please, fill in form correctly")
    return render_template('comment.html',
                           page_title='Edit comment',
                           button_title='Submit comment',
                           edit_comment=comment
                           )

@app.route('/list/search/', methods= ['GET'])
def route_list_search():
    expression = request.form.get('expression')

    searched_questions = data_manager.search_questions_by_expression(expression)

    return render_template ('list.html',
                            all_questions = searched_questions)


@app.route('/registration', methods=['GET', 'POST'])
def route_registration():
    if request.method == "POST":
        new_user = {
            'username': request.form.get('username'),
            'password': ul.hash_password(request.form.get('password'))
        }
        if ul.add_new_user(new_user):
            session['username'] = new_user['username']
            user_data = ul.get_user(session.get('username'))
            session['id'] = user_data['id']
            return redirect('/')
        flash("User already exists")
    return render_template('register_form.html')


@app.route('/login', methods=['POST'])
def route_login():
    login_user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }
    if ul.check_pass(login_user):
        session['username'] = login_user['username']
        user_data = ul.get_user(session.get('username'))
        session['id'] = user_data['id']
        return redirect('/')
    if ul.check_exist_user(username=login_user['username']):
        flash("Incorrect password")
        return redirect('/')
    flash("User is not in base. Please sign up.")
    return render_template('register_form.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/question/<question_id>/delete', methods=['POST'])
def route_delete_question(question_id):
    ql.delete_question(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def route_delete_answer(answer_id):
    answer = al.get_one_answer(answer_id)
    question_id = answer['question_id']
    al.delete_answer(answer_id)
    return redirect('/question/{}'.format(question_id))


@app.route('/comment/<comment_id>/delete', methods=['POST'])
def route_delete_comment(comment_id):
    comment = cl.get_one_comment(comment_id)
    question_id = comment['question_id']
    cl.delete_comment(comment_id)
    return redirect('/question/{}'.format(question_id))


if __name__ == '__main__':
    app.secret_key = "some_key"
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True
    )
