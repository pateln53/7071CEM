from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.font as font
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ujson

stemmer = PorterStemmer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()

with open('publication_list_stemmed.json', 'r') as a: pub_list_first_stem = ujson.load(a)
with open('publication_indexed_dictionary.json', 'r') as a: pub_index = ujson.load(a)
with open('pub_name.json', 'r') as a: pub_name = ujson.load(a)
with open('pub_url.json', 'r') as a: pub_url = ujson.load(a)
with open('pub_cu_author.json', 'r') as a: pub_cu_author = ujson.load(a)
with open('pub_date.json', 'r') as a: pub_date = ujson.load(a)


def pub_qp_data(a=0, ):
    outputData.delete(1.0, END)
    outcome.delete(0, END)
    inputText = inputBar.get()
    abc = {}
    if operator.get() == 2:
        outputData.configure(fg='blue')
        inputText = inputText.lower().split()
        pointer = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo(title="Hello!!!", message="Please enter atleast 2 words to apply operator.")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            stem_temp = ""
            stem_word_file = []
            temp_file = []
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)
            if pub_index.get(stem_word_file[0].strip()):
                pointer = pub_index.get(stem_word_file[0].strip())

            else:
                # stem_word_file = []
                if (len(inputText) == 1):
                    pointer = []
            if (len(pointer) == 0):
                abc = {}
            else:
                for j in pointer:
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                if pub_index.get(stem_word_file[0].strip()):
                    for j in pointer:
                        abc[j] = cosine_output[pointer.index(j)]

    else:
        outputData.configure(fg='brown')
        inputText = inputText.lower().split()
        pointer = []
        match_word = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo("Error!!!", "Please enter atleast 2 words to apply operator.")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            temp_file = []
            set2 = set()
            stem_word_file = []
            word_list = word_tokenize(token)
            stem_temp = ""
            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)
            if pub_index.get(stem_word_file[0].strip()):
                set1 = set(pub_index.get(stem_word_file[0].strip()))
                pointer.extend(list(set1))

                if match_word == []:
                    match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                else:
                    match_word.extend(list(set1))
                    match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})
            else:
                pointer = []

        if (len(inputText) > 1):
            match_word = {z for z in match_word if z in set2 or (set2.add(z) or False)}

            if (len(match_word) == 0):
                abc = {}
            else:
                for j in list(match_word):
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in list(match_word):
                    abc[j] = cosine_output[list(match_word).index(j)]
        else:

            if (len(pointer) == 0):
                abc = {}
            else:
                for j in pointer:
                    temp_file.append(pub_list_first_stem[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in pointer:
                    abc[j] = cosine_output[pointer.index(j)]

    aa = 0
    rank_sorting = sorted(abc.items(), key=lambda z: z[1], reverse=True)
    for a in rank_sorting:
        outputData.insert(INSERT, "Rank: ")
        outputData.insert(INSERT, "{:.2f}".format(a[1][0]))
        outputData.insert(INSERT, "\n")
        outputData.insert(INSERT, 'Title: ' + pub_name[a[0]] + "\n")
        outputData.insert(INSERT, 'URL: ' + pub_url[a[0]] + "\n")
        outputData.insert(INSERT, 'Date: ' + pub_date[a[0]] + "\n")
        outputData.insert(INSERT, 'Cov_Uni_Author: ' + pub_cu_author[a[0]] + "\n")
        outputData.insert(INSERT, "\n")

        aa = aa + 1
    if aa == 0:
        messagebox.showinfo("Error!!!", "No results found. TRY AGAIN!!!")
    outcome.insert(END, aa)


# GUI build steps
window = Tk()
window.configure(bg='#263543')
window.geometry('1000x750')
label = Label(window, text="PPoogle", bg="#263543", fg="white", font="'Arial' 24 bold")
label.config(anchor=CENTER)
label.pack()
apply = Label(window, text='APPLY :')
count = Label(window, text='COUNT :')
outcome = Entry(window, width=10)
inputBar = Entry(window, width=50)
inputBar.pack()
inputBar.place(x=50, y=70)
count.place(x=620, y=80)
outcome.place(x=680, y=80)
outputData = scrolledtext.ScrolledText(window, width=110, height=37)
outputData.place(x=50, y=120)
search = Button(window, text='SEARCH', bg="#D4D7D9", fg="#263543", font="'Arial' 10", command=pub_qp_data).place(x=370, y=70)
operator = IntVar()
operator.set(2)
rb_and = Radiobutton(window, text='AND', value=1, variable=operator, command=pub_qp_data)
rb_or = Radiobutton(window, text='OR', value=2, variable=operator, command=pub_qp_data)
apply.place(x=620, y=50)
rb_and.place(x=680, y=50)
rb_or.place(x=750, y=50)
window.bind('<Return>', pub_qp_data)
window.mainloop()
