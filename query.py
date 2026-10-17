
query_create_quiz_type = '''
    CREATE TABLE IF NOT EXISTS quiz (
        id      INTEGER PRIMARY KEY,
        name    VARCHAR
    )    
'''

query_create_quiz_question = '''
    CREATE TABLE IF NOT EXISTS questions(
    id          INTEGER PRIMARY KEY,
    question    VARCHAR,
    answer      VARCHAR,
    wrong1      VARCHAR,
    wrong2      VARCHAR,
    wrong3      VARCHAR
    )
'''

enable_foreign_key = '''
    PRAGMA foreign_keys=on
'''

query_create_quiz_content = '''
  CREATE TABLE IF NOT EXISTS quiz_content(
    id          INTEGER   PRIMARY KEY,
    quiz_id     INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
  )
'''



query_add_quiz = '''
    INSERT INTO QUIZ(name) VALUES (?)

'''

query_add_questions = '''
    INSERT INTO questions(question, answer, wrong1, wrong2, wrong3)
    VALUES (?, ?, ?, ?, ?)
'''

query_create_link = '''INSERT INTO quiz_content(quiz_id, question_id) VALUES (?, ?)'''

query_get_question = '''
    SELECT quiz_content.id,
            questions.question,
            questions.answer,
            questions.wrong1,
            questions.wrong2,
            questions.wrong3
    FROM questions, quiz_content
    WHERE quiz_content.question_id == questions.id
    AND quiz_content.id > ?
    AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
'''