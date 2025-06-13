import nltk
import tkinter as tk
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from tkinter import messagebox, scrolledtext
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
            result.append(f"Example: {example}")

    return "\n".join(result)



def main():
    print("Welcome to the NLTK dictionary app!\nType a word in to see if it is a valid English word.\nType exit to exit the program.\n")
    while True:
        word = input("Enter your word: ")
        if word == "exit":
            print("Thank You for using the NLTK dictionary!")
            break
        if validate(word):
            print(str(word)+" is a valid English word")

            print("Definition:\n"+definitions(word))

            if len(suggestWords(word)) > 0:
                print("Here are some similar words(One letter difference):")
                print(", ".join(suggestWords(word)))
            else:
                print("No suggestions found")
        else:
            print("Not a valid English word")
            options = autoComplete(word)
            if len(options) > 0:
                print("Did you mean?: ")
                print(" ,".join(options))
            else:
                print("No suggestions found")

if __name__ == "__main__":
    main()

