import random
from datetime import date
from random import randint
import nltk
import os
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from flask import Flask, request, jsonify, render_template

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('words')

wordList = words.words()

app = Flask(__name__)

validWords = set(word.lower() for word in wordList)

def dailyWord(listOfPossibleWords):
    today = date.today().toordinal()
    random.seed(today)
    wordToday = random.choice(list(validWords))
    return wordToday, definitions(wordToday)


def validate (word):
    if word.lower() in validWords:
        return True
    else:
        return False
def signalLetterDifference (word1, word2):
    if len(word1) != len(word2):
        return False
    return sum(a != b for a, b in zip(word1.lower(), word2.lower())) == 1
def suggestWords(word):
    word = word.lower()
    possiblities = []
    for i in validWords:
        if len(i) == len(word) and signalLetterDifference(word, i):
            possiblities.append(i)
    return possiblities[:10]
def autoComplete(halfDoneWord):
    prefix = halfDoneWord.lower()
    suggestions = [word for word in validWords if word.startswith(prefix)]
    return suggestions[:10]
def definitions(word):
    synsets = wn.synsets(word)
    if not synsets:
        return "No definitions found."

    result = []
    for syn in synsets[:3]:
        pos = syn.pos()
        definition = syn.definition()
        example = "; ".join(syn.examples())
        result.append(f"{pos.upper()}: {definition}")
        if example:
            result.append(f"Example: {example}\n")

    return "<br />".join(result)

@app.route("/", methods=["GET", "POST"])
def home():
    word = ""
    is_valid = False
    defs = ""
    suggestions = []
    autocomplete = []
    daily, dailyDef = dailyWord(wordList)

    if request.method == "POST":
        word = request.form["word"]
        is_valid = validate(word)
        defs = definitions(word)
        if is_valid:
            suggestions = suggestWords(word)
        else:
            autocomplete = autoComplete(word)

    return render_template("index.html",
        word=word,
        is_valid=is_valid,
        definitions=defs,
        suggestions=suggestions,
        autocomplete=autocomplete,
        daily = daily,
        dailyDef = dailyDef
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)