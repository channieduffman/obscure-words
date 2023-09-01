from flask import Blueprint, render_template

from bs4 import BeautifulSoup
import requests

import random

from . import models
from obscurew.db import get_db

bp = Blueprint('words', __name__)


def get_words():

    url = 'https://phrontistery.info/mania.html'
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    results = soup.find('table', class_='words')
    words = results.find_all('td')

    # clean and further parse html data; none of the tags are closed in source code
    words = [str(word).split('<tr>') for word in words]
    words = [ls[0] for ls in words]
    words = [str(word).split('\r') for word in words]
    words = [ls[0].split('<td>') for ls in words]
    words = [ls[1] for ls in words]


    # split into seprate word, meaning lists
    x = [word for idx, word in enumerate(words) if idx % 2 == 0]
    y = [word for idx, word in enumerate(words) if idx % 2 != 0]


    # create a list of Word objects to be returned
    res = [] 
    for x, y in zip(x, y):
        word = models.Word(x, y)
        res.append(word)

    return res

    # return words


def add_to_db(words):
    db = get_db()
    
    for word in words:
        try:
            db.execute(
                'INSERT INTO words (word, meaning) VALUES (?, ?)',
                (word.term, word.meaning)
            )
            db.commit()
        except db.IntegrityError:
            pass


@bp.route('/', methods=('GET', 'POST'))
def index():

    words = get_words()
    # add_to_db(words)

    return render_template('words/index.html', words=words)