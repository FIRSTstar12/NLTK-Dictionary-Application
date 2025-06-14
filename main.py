import nltk
import os
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from flask import Flask, request, jsonify
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('words')

wordList = words.words()

validWords = set(word.lower() for word in wordList)

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

    return "\n".join(result)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Word Explorer API!"

@app.route("/check", methods=["GET"])
def check_word():
    word = request.args.get("word", "")
    is_valid = validate(word)
    return jsonify({"word": word, "valid": is_valid})

@app.route("/define", methods=["GET"])
def define_word():
    word = request.args.get("word", "")
    defs = definitions(word)
    return jsonify({"word": word, "definitions": defs})

@app.route("/suggest", methods=["GET"])
def suggest():
    word = request.args.get("word", "")
    suggestions = suggestWords(word)
    return jsonify({"word": word, "suggestions": suggestions})

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    prefix = request.args.get("prefix", "")
    suggestions = autoComplete(prefix)
    return jsonify({"prefix": prefix, "suggestions": suggestions})

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
