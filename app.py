import spacy
from spacypdfreader.spacypdfreader import pdf_reader
from services.format import clean, user_sort, auto_sort, grouping
from services.sentiment import SentimentAnalyzer

teams = [1710, 1678, 1880, 2383, 2438, 3473, 3794, 3937, 3990, 4253, 4400, 4481, 4607, 4788, 6014, 6431, 8159, 8557]

nlp = spacy.load("en_core_web_lg")
doc = nlp(pdf_reader('documents/'+str(teams[0])+'.pdf', nlp))

qna_collection = []

paragraphs = clean(doc, nlp)

qna, questions = user_sort(paragraphs) # qna is questions and answers

qna_collection.append(qna)

for team in teams:
    if team is not teams[0]:
        doc = nlp(pdf_reader('documents/'+str(team)+'.pdf', nlp))
        paragraphs = clean(doc, nlp)

        auto_qna = auto_sort(paragraphs, questions)

        qna_collection.append(auto_qna)

print('\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n')

for qna in qna_collection:
    for doc in qna:
        print(doc, '\n')
    print('\n', '\n', '\n')

grouped = grouping(qna_collection, questions)

polarity = []
subjectivity = []

for question in grouped:
    polarities = []
    subjectivities = []
    for answer in question:
        sentiment = SentimentAnalyzer(answer, nlp)
        polarities.append(sentiment.polarity())
        subjectivity.append(sentiment.subjectivity())
    polarity.append(polarities)
    subjectivity.append(subjectivities)

print(polarity)
print(subjectivity)