from flask import Flask, redirect, url_for, url_for, session, render_template, request
from random import randint
from database import get_question_after, get_quizes, check_answer
import os
from random import shuffle


quiz = 0
last_question = 0

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)

def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return redirect(url_for('test'))
    
    #return '<a href="/test">Start The Quiz!!!</a>'

def question_form(question):
    # Get the row from the database (quiz_content) corresponding to
    # the question, and after that return the html wgat uts form
    answer_list = [
        question[2], # answer
        question[3], # wrong1
        question[4], # wrong2
        question[5], # wrong3
    ]
    shuffle(answer_list)
    return render_template(
        'test.html',
        question=question[1],
        quest_id=question[0],
        answer_list= answer_list
    )

def save_answer():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')

    # this question has already been asked
    session['last_question'] = quest_id

    # increase the question counter
    session['total'] += 1

    # check if the answer matches the correct one for this id
    if check_answer(quest_id, answer):
        session['answers'] += 1

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # if we receieved data, we need to read it and update the information
        if request.method == 'POST':
            save_answer()
            # save the answer
        next_question = get_question_after(session['last_question'],session['quiz'])
        if next_question is None or len(next_question) == 0:
            # the quiz is over
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

    # result = get_question_after (session['last_question'], session['quiz'])
    # if result is None or len(result) == 0:
    #     return redirect(url_for('result'))
    # else:
    #     session['last_question'] = result[0]
    #     return f"<h1> {session['quiz']} <br> {str(result)} </h1>"

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html


# Routes
folder = os.getcwd()
app = Flask(__name__, template_folder=folder)
app.add_url_rule('/', 'index', index, methods=['get', 'post'])
app.add_url_rule('/test', 'test', test, methods=['get', 'post'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'holiday'

if __name__ == '__main__':
    app.run()
