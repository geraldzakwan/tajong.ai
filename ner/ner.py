import sys
import time

from spacy import load, displacy

from ner.__init__ import MODEL_DIR, DEFAULT_MODEL_PATH
from ner.__init__ import EXAMPLE_DOCS_PATH

class NER:

    def __init__(self, model_filepath, verbose=False):
        start = time.time()

        if model_filepath == "default":
            self.model_filepath = DEFAULT_MODEL_PATH
        else:
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
    with open(EXAMPLE_DOCS_PATH, "r") as infile:
        docs = infile.readlines()

    if sys.argv[1] == "default":
        ner = NER(model_filepath=DEFAULT_MODEL_PATH, verbose=True)
    else:
        ner = NER(model_filepath="{}/{}".format(MODEL_DIR, sys.argv[1]), verbose=True)

    ner.load_model()
    ner.predict(docs)
