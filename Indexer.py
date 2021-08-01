import ujson
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

#Preprosessing data before indexing
with open('scraper_results.json', 'r') as doc: scraper_results=doc.read()

pubName = []
pubURL = []
pubCUAuthor = []
pubDate = []
data_dict = ujson.loads(scraper_results)
array_length = len(data_dict)
print(array_length)

#Seperate name, url, date, author in different file
for item in data_dict:
    pubName.append(item["name"])
    pubURL.append(item["pub_url"])
    pubCUAuthor.append(item["cu_author"])
    pubDate.append(item["date"])
with open('pub_name.json', 'w') as f:ujson.dump(pubName, f)
with open('pub_url.json', 'w') as f:ujson.dump(pubURL, f)
with open('pub_cu_author.json', 'w') as f:ujson.dump(pubCUAuthor, f)
with open('pub_date.json', 'w') as f: ujson.dump(pubDate, f)

#nltk.download()
#Downloading libraries to use its methods
nltk.download('stopword')
nltk.download('punkt')

#Open a file with publication names in read mode
with open('pub_name.json','r') as f:publication=f.read()

#Load JSON File
pubName = ujson.loads(publication)

#Predefined stopwords in nltk are used
stop_words = stopwords.words('english')
stemmer = PorterStemmer()
pub_list_first_stem = []
pub_list = []
pub_list_wo_sc = []
print(len(pubName))

for file in pubName:
    #Splitting strings to tokens(words)
    words = word_tokenize(file)
    stem_word = ""
    for i in words:
        if i.lower() not in stop_words:
            stem_word += stemmer.stem(i) + " "
    pub_list_first_stem.append(stem_word)
    pub_list.append(file)

#Removing all below characters
special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
for file in pub_list:
    word_wo_sc = ""
    if len(file.split()) ==1 : pub_list_wo_sc.append(file)
    else:
        for a in file:
            if a in special_characters:
                word_wo_sc += ' '
            else:
                word_wo_sc += a
        #print(word_wo_sc)
        pub_list_wo_sc.append(word_wo_sc)

#Stemming Process
pub_list_stem_wo_sw = []
for name in pub_list_wo_sc:
    words = word_tokenize(name)
    stem_word = ""
    for a in words:
        # if len(w) > 4:
        #     temp += stemmer.stem(w[0:5].lower()) + ' '
        #     print(w, "temp1", temp)
        if a.lower() not in stop_words:
            stem_word += stemmer.stem(a) + ' '
            #print(w, "temp2", stem_word)
    pub_list_stem_wo_sw.append(stem_word.lower())

data_dict = {}

# Indexing process
for a in range(len(pub_list_stem_wo_sw)):
    for b in pub_list_stem_wo_sw[a].split():
        if b not in data_dict:
             data_dict[b] = [a]
        else:
            data_dict[b].append(a)


print(len(pub_list_wo_sc))
print(len(pub_list_stem_wo_sw))
print(len(pub_list_first_stem))
print(len(pub_list))


# with open('publication_filter_without_stopwords.json', 'w') as f:
#     ujson.dump(pub_list_stem_wo_sw, f)
with open('publication_list_stemmed.json', 'w') as f:
    ujson.dump(pub_list_first_stem, f)

# with open('publication_list.json', 'w') as f:
#     ujson.dump(pub_list, f)
with open('publication_indexed_dictionary.json', 'w') as f:
    ujson.dump(data_dict, f)