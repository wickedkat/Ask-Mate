import database_connection as db_connect
import psycopg2
from psycopg2.extensions import AsIs


@db_connect.connection_handler
def get_all_questions(cursor):
    try:
        cursor.execute("""
                SELECT q.id, q.submission_time, q.title, q.message, u.username as username
                FROM question AS q
                LEFT JOIN users AS u
                ON q.user_id = u.id
                ORDER BY submission_time DESC;
                           """)
        all_question = cursor.fetchall()
        return all_question
    except psycopg2.DatabaseError as e:        #błędy lepiej obsługiwać w logice
        print(e)
        return []


@db_connect.connection_handler
def add_one_question(cursor, question):
    try:
        cursor.execute("""
                    INSERT INTO question (submission_time, title, message, user_id)
                    VALUES (NOW()::timestamp(0), %(title)s, %(message)s, %(user_id)s)
                    ON CONFLICT(id) DO NOTHING
                    RETURNING id ;
                               """,
                       {'title': question['title'],
                        'message': question['message'],
                        'user_id': question['user_id']
                        })
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_question(cursor, question_id):
    try:
        cursor.execute("""
                    SELECT id, submission_time, title, message
                    FROM question
                    WHERE id = %(question_id)s;
                        """,
                       {'question_id': question_id})
        question = cursor.fetchone()
        return question
    except psycopg2.Error as e:
        print(e)
        return []


@db_connect.connection_handler
def get_all_comments(cursor):
    try:
        cursor.execute("""
                SELECT *
                FROM comment
                ORDER BY submission_time DESC;
                """)
        all_comments = cursor.fetchall()
        return all_comments
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_comment_by_id(cursor, id):
    try:
        cursor.execute("""
                SELECT *
                FROM comment
                WHERE id = %(id)s;
                """,
                       {'id': id})
        comment = cursor.fetchone()
        return comment
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def add_one_comment(cursor, comment):
    try:
        cursor.execute("""
                    INSERT INTO comment (submission_time, question_id, answer_id, message, user_id)
                    VALUES (NOW()::timestamp(0), %(question_id)s, %(answer_id)s, %(message)s, %(user_id)s)
                    ON CONFLICT(id) DO NOTHING
                    RETURNING id;
                               """,
                       {'question_id': comment['question_id'],
                        'answer_id': comment['answer_id'],
                        'message': comment['message'],
                        'user_id': comment['user_id']
                        })
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_all_comments_by_question(cursor, question_id):
    try:
        cursor.execute("""
                SELECT  c.id, c.submission_time, c.question_id, c.answer_id, c.message, u.username AS username
                FROM comment AS c 
                LEFT JOIN users AS u
                ON c.user_id = u.id
                WHERE question_id = %(question_id)s 
                ORDER BY submission_time DESC;
                """,
                       {'question_id': question_id
                        })
        all_comments = cursor.fetchall()
        return all_comments
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def add_one_answer(cursor, answer):
    try:
        cursor.execute("""
                        INSERT INTO answer (submission_time, question_id, message, user_id)
                        VALUES (NOW()::timestamp(0) , %(question_id)s, %(message)s, %(user_id)s)
                        ON CONFLICT(id) DO NOTHING;
                                   """,
                       {'question_id': answer['question_id'],
                        'message': answer['message'],
                        'user_id': answer['user_id']
                        })
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_answers(cursor, question_id):
    try:
        cursor.execute("""
                        SELECT a.id, a.submission_time, a.question_id, a.message, u.username AS username
                        FROM answer AS a
                        LEFT JOIN users AS u
                        ON a.user_id = u.id
                        WHERE question_id = %(question_id)s 
                        ORDER BY submission_time ASC;
                                   """,
                       {'question_id': question_id})
        answers = cursor.fetchall()
        return answers
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def sort_questions(cursor, conditions):
    try:
        cursor.execute("""
                            SELECT id, submission_time, title, message
                            FROM question
                            ORDER BY %(col_name)s %(order)s; 
                                       """,
                       {'col_name': AsIs(conditions['attribute']), 'order': AsIs(conditions['order'])})
        questions = cursor.fetchall()
        return questions
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_one_answer(cursor, id):
    try:
        cursor.execute("""
                        SELECT id, submission_time, question_id, message, user_id
                        FROM answer
                        WHERE id = %(id)s ;
                                   """,
                       {'id': id})
        answer = cursor.fetchone()
        return answer
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def update_answer(cursor, answer):
    try:
        cursor.execute("""                   
                           UPDATE answer 
                           SET message = %(message)s 
                           WHERE id = %(id)s;
                           """,
                       {'id': answer['id'], 'message': answer['message']})
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def update_comment(cursor, comment):
    try:
        cursor.execute("""                   
                           UPDATE comment 
                           SET message = %(message)s 
                           WHERE id = %(id)s;
                           """,
                       {'id': comment['id'], 'message': comment['message']})
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def get_one_user(cursor, username):
    try:
        cursor.execute("""
                        SELECT id, submission_time, username, password
                        FROM users
                        WHERE username = %(username)s ;
                                   """,
                       {'username': username})
        user = cursor.fetchone()
        return user
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def add_one_user(cursor, user):
    try:
        cursor.execute("""
                    INSERT INTO users (submission_time, username, password)
                    VALUES (NOW()::timestamp(0), %(username)s, %(password)s)
                    ON CONFLICT(id) DO NOTHING
                    RETURNING id ;
                               """,
                       {'username': user['username'],
                        'password': user['password']
                        })
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def delete_question(cursor, question_id):
    try:
        cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(question_id)s;
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
                    DELETE FROM question
                    WHERE id = %(question_id)s;    
                            """,
                       {'question_id': question_id})
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def delete_answer(cursor, answer_id):
    try:
        cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s;
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;                       
                            """,
                       {'answer_id': answer_id})
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def delete_comment(cursor, comment_id):
    try:
        cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                            """,
                       {'comment_id': comment_id})
    except psycopg2.Error as e:
        print(e)


@db_connect.connection_handler
def search_questions_by_expression(cursor, expression):
    cursor.execute("""
                    SELECT id, submission_time, title, message
            FROM question 
            LEFT JOIN answer a on question.id = a.question_id
            WHERE title LIKE '%%'|| %(expression)s || '%%'
            OR question.message LIKE  '%%'|| %(expression)s || '%%'
            OR answer.message LIKE '%%'|| %(expression)s || '%%'
            """,
         )


    searched_questions = cursor.fetchall()
    return searched_questions
