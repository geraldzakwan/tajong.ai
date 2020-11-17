import sys
import time
import requests

from spacy import load, displacy

from ner.__init__ import EXAMPLE_DOCS_PATH
from ner.__init__ import MODEL_DIR, DEFAULT_MODEL_PATH

class NER:

    def __init__(self, ner_library, model_identifier, verbose=False):
        start = time.time()

        self.verbose = verbose

        self.ner_library = ner_library

        if self.ner_library == "kata":
            self.model_identifier = model_identifier

        elif self.ner_library == "spacy":
            if model_identifier == "default":
                self.model_identifier = DEFAULT_MODEL_PATH
            else:
                self.model_identifier = model_identifier

        else:
            raise Exception("NER library is not supported, use 'kata' or 'spacy'")

        self.load_model()

        if self.verbose:
            print("Initialization finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    def load_model(self):
        start = time.time()

        if self.ner_library == "kata":
            self.model_url, self.auth_token = self.model_identifier.strip("\n").split(";")
            self.request_headers = {
                "Authorization": "Bearer {}".format(self.auth_token)
            }

        elif self.ner_library == "spacy":
            self.nlp = load(self.model_identifier)

        if self.verbose:
            print("Model is loaded from: {}".format(self.model_identifier))

            if self.ner_library == "kata":
                print("Model URL: {}".format(self.model_url))
                print("Request headers: ")
                print(self.request_headers)

            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    def predict(self, docs):
        start = time.time()

        self.pred_docs_ents = []

        if self.ner_library == "kata":
            for doc in docs:
                payload = {
                    "text": doc
                }

                req = requests.post(self.model_url, json=payload, headers=self.request_headers)

                self.pred_docs_ents.append(req.json()["result"]["kata"])

            if self.verbose:
                self.display()
                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")

        elif self.ner_library == "spacy":
            for doc in docs:
                self.pred_docs_ents.append(self.nlp(doc))

            if self.verbose:
                self.display()
                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")

        return self.pred_docs_ents

    def display(self):
        start = time.time()

        if self.ner_library == "kata":
            for pred_ents in self.pred_docs_ents:
                print(pred_ents)
                print("--------------------------------------------------")

                print("Entities: {}".format([(ent["value"], ent["label"], ent["start"], ent["end"]) for ent in pred_ents]))

                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")

        elif self.ner_library == "spacy":
            for pred_ents in self.pred_docs_ents:
                print(pred_ents)
                print("--------------------------------------------------")

                print("Entities: {}".format([(ent.text, ent.label_) for ent in pred_ents.ents]))

                displacy.render(pred_ents, style="ent")
                print("--------------------------------------------------")

                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")
