import time
import random
import pickle

from spacy.util import minibatch, compounding
from spacy import load, displacy, blank

from __init__ import MODEL_V1_PATH, EXAMPLE_DOC

class NER:

    def __init__(self, model_filepath, verbose=False):
        self.model_filepath = model_filepath
        self.verbose = verbose
        self.nlp = None

    def load_model(self):
        self.nlp = load(self.model_filepath)

        if self.verbose:
            print("Model is loaded from: {}".format(self.model_filepath))

    def predict(self, docs):
        pred_docs_ents = []

        for doc in docs:
            pred_ents = self.nlp(doc)
            pred_docs_ents.append(pred_ents)

            if self.verbose:
                print("Entities: {}".format([(ent.text, ent.label_) for ent in pred_ents.ents]))

                displacy.render(pred_ents, style="ent")

                print("--------------------------------------------------")

        return pred_docs_ents


if __name__ == '__main__':
    docs = []
    
    for filepath in [EXAMPLE_DOC_1_PATH, EXAMPLE_DOC_2_PATH, EXAMPLE_DOC_3_PATH]:
        with open(EXAMPLE_DOC_1_PATH, "r") as infile:
            docs.append(infile.read())

    ner = NER(model_filepath=MODEL_V1_PATH, verbose=True)

    ner.load_model()
    ner.predict(docs)
