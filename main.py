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


def search_word():
    word = entry.get().strip()
    output.delete('1.0', tk.END)

    if not word:
        messagebox.showinfo("Input Needed", "Please enter a word.")
        return

    if validate(word):
        output.insert(tk.END, f"✅ '{word}' is a valid English word.\n\n")
        output.insert(tk.END, "📚 Definitions:\n")
        output.insert(tk.END, definitions(word) + "\n\n")

        suggestions = suggestWords(word)
        if suggestions:
            output.insert(tk.END, "💡 Similar words (1-letter off):\n")
            output.insert(tk.END, ", ".join(suggestions) + "\n")
    else:
        output.insert(tk.END, f"❌ '{word}' is not a valid English word.\n\n")
        options = autoComplete(word)
        if options:
            output.insert(tk.END, "Did you mean:\n")
            output.insert(tk.END, ", ".join(options) + "\n")
        else:
            output.insert(tk.END, "No suggestions found.")

root = tk.Tk()
root.title("Word Explorer")
root.geometry("600x500")

label = tk.Label(root, text="Enter a word:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.pack()

search_button = tk.Button(root, text="Search", command=search_word, font=("Arial", 12))
search_button.pack(pady=5)

output = scrolledtext.ScrolledText(root, height=20, width=70, font=("Consolas", 11))
output.pack(pady=10)

root.mainloop()
