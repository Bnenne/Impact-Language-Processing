from spacytextblob.spacytextblob import SpacyTextBlob
import spacy

class SentimentAnalyzer:
    def __init__(self, paragraph, nlp):
        nlp.add_pipe('spacytextblob')
        self.doc = nlp(paragraph)

    def polarity(self):
        pol = self.doc._.blob.polarity
        if pol != 0:
            return pol

    def subjectivity(self):
        sub = self.doc._.blob.subjectivity
        if sub != 0:
            return sub