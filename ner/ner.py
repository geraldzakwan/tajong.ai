import sys
import time

from spacy import load, displacy

from __init__ import MODEL_DIR, MODEL_V0_PATH, MODEL_V1_PATH
from __init__ import EXAMPLE_DOC_1_PATH, EXAMPLE_DOC_2_PATH, EXAMPLE_DOC_3_PATH

class NER:

    def __init__(self, model_filepath, verbose=False):
        start = time.time()

        self.model_filepath = model_filepath
        self.verbose = verbose

        if self.verbose:
            print("Initialization finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    def load_model(self):
        start = time.time()

        self.nlp = load(self.model_filepath)

        if self.verbose:
            print("Model is loaded from: {}".format(self.model_filepath))
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    def predict(self, docs):
        start = time.time()

        self.pred_docs_ents = []

        for doc in docs:
            self.pred_docs_ents.append(self.nlp(doc))

        if self.verbose:
            self.display()
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

        return self.pred_docs_ents

    def display(self):
        for pred_ents in self.pred_docs_ents:
            print(pred_ents)
            print("--------------------------------------------------")

            print("Entities: {}".format([(ent.text, ent.label_) for ent in pred_ents.ents]))

            displacy.render(pred_ents, style="ent")
            print("--------------------------------------------------")

if __name__ == '__main__':
    docs = []

    for filepath in [EXAMPLE_DOC_1_PATH, EXAMPLE_DOC_2_PATH, EXAMPLE_DOC_3_PATH]:
        with open(filepath, "r") as infile:
            docs.append(infile.read())

    if sys.argv[1] == "default":
        ner = NER(model_filepath=MODEL_V0_PATH, verbose=True)
    else:
        ner = NER(model_filepath="{}/{}".format(MODEL_DIR, sys.argv[1]), verbose=True)

    ner.load_model()
    ner.predict(docs)
