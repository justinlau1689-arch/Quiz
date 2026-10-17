import sqlite3
from query import *

db_name = 'quiz.sqlite'

conn = None
cursor = None

#=== ULTILITY START ===
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def do(query):
    cursor.execute(query)
    conn.commit()

def close():
    cursor.close()
    conn.close()
#=== ULTILITY END ===


def create():
    open()
    do(enable_foreign_key)
    print('Foreign Key Enabled Successfully')
    do(query_create_quiz_question)
    print('Quiz Table Created')
    do(query_create_quiz_type)
    print('Question Table Created!')
    do(query_create_quiz_content)
    print('Quiz Content Table Created!')

    close()


def add_quiz():
    quizes = [
        ('Math',),
        ('P.E',),
        ('Economics',)
    ]
    open()
    cursor.executemany(query_add_quiz, quizes)
    conn.commit()
    print('Sucessfully Insert Quiz Type')
    close()

questions_list = [
    # 4 questions of Math
    ('10+11', '21', '13', '22', '45'),
    ('5x5', '25', '10', '15', '20'),
    ('20-7', '13', '12', '14', '15'),
    ('12x3', '36', '24', '30', '42'),

    # 4 questions of P.E
    ('How many players are on a basketball team?', '5', '6', '7', '8'),
    ('Which sport uses a racket?', 'Badminton', 'Football', 'Basketball', 'Swimming'),
    ('How many minutes is a football match?', '90', '60', '70', '80'),
    ('Which sport is played in a swimming pool?', 'Swimming', 'Football', 'Badminton', 'Basketball'),

    # 4 questions of Economics
    ('What is the meaning of demand?', 'Desire to buy', 'Selling goods', 'Making goods', 'Saving money'),
    ('What is an example of a need?', 'Food', 'Gaming PC', 'Luxury watch', 'Sports car'),
    ('What happens when price increases?', 'Demand decreases', 'Demand increases', 'Demand doubles', 'Demand stays equal'),
    ('What is money used for?', 'Buying goods and services', 'Playing games', 'Exercising', 'Sleeping')
]

def add_questions():
    open()
    cursor.executemany(query_add_questions, questions_list)
    conn.commit()
    close()
    print('Successfully Insert Question')

def add_links(): #create relation between question and quiz category
    link = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),

        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),

        (3,9),
        (3, 10),
        (3, 11),
        (3, 12),
    ]
    open()
    cursor.execute(enable_foreign_key)
    cursor.executemany(query_create_link, link)
    conn.commit()
    close()
    print('Sucessfully linked the question and quiz category!')

def get_question_after(question_id = 0, quiz_id=1):
    open()
    cursor.execute(query_get_question, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def clear_db():
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def get_quizes():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def check_answer(q_id, ans_text):
    query = '''
        SELECT question.answer
        FROM quiz_content, question
        WHERE quiz_content.id = ?
        AND quiz_content.question_id = question.id
    '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()

    if result is None:
        return False
    else:
        if result[0] == ans_text:
            return True # The answer matched
        else:
            return False # Found the answer but it didnt matched or it's wrong

def main():
    clear_db()
    create()
    add_quiz()
    add_questions()
    add_links()

if __name__ == "__main__":
    main()

