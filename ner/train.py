import time
import random
import pickle

from spacy.util import minibatch, compounding
from spacy import load, displacy, blank

from __init__ import SPACY_FORMATTED_TRAIN_DATA_PATH, MODEL_V1_PATH
from __init__ import EXAMPLE_DOC_1_PATH, EXAMPLE_DOC_2_PATH, EXAMPLE_DOC_3_PATH

class Trainer:

    def __init__(self, train_data_filepath, saved_model_filepath, num_iters, print_freq, test_docs=[], verbose=False):
        self.train_data_filepath = train_data_filepath
        self.saved_model_filepath = saved_model_filepath

        self.num_iters = num_iters
        self.print_freq = print_freq

        self.nlp = blank("id")

        self.test_docs = test_docs

        self.verbose = verbose

        if self.verbose:
            print("Initialization finishes")

    def load_dataset(self):
        with open(self.train_data_filepath, "rb") as f:
            self.data = pickle.load(f)

        if self.verbose:
            print("Load dataset finishes")

    def setup_training(self):
        self.nlp.add_pipe(self.nlp.create_pipe("ner"))

        self.nlp.begin_training()

        self.ner = self.nlp.get_pipe("ner")

        self.pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

        self.unaffected_pipes = [pipe for pipe in self.nlp.pipe_names if pipe not in self.pipe_exceptions]

        for _, annotations in self.data:
            for ent in annotations.get("entities"):
                self.ner.add_label(ent[2])
                break

        if self.verbose:
            print("Setup training finishes")

    def train(self):
        start = time.time()

        with self.nlp.disable_pipes(*self.unaffected_pipes):
          for iteration in range(self.num_iters):
            random.shuffle(self.data)

            losses = {}
            batches = minibatch(self.data, size=compounding(4.0, 32.0, 1.001))

            for batch in batches:
                texts, annotations = zip(*batch)

                self.nlp.update(
                    texts,
                    annotations,
                    drop=0.5,
                    losses=losses
                )

            if self.verbose:
                if (iteration + 1) % self.print_freq == 0:
                    print("Iteration {}".format(iteration + 1))
                    print("Losses: {}".format(losses))
                    print("Time Elapsed: {} seconds".format(time.time()-start))

        for doc in self.test_docs
            pred_ents = self.nlp(doc)

            print("Entities: {}".format([(ent.text, ent.label_) for ent in pred_ents.ents]))

            displacy.render(pred_ents, style="ent")

            print("--------------------------------------------------")

    def save(self):
        self.nlp.to_disk(self.saved_model_filepath)

        if self.verbose:
            print("NER model is saved to: {}".format(self.saved_model_filepath))

if __name__ == '__main__':
    docs = []
    
    for filepath in [EXAMPLE_DOC_1_PATH, EXAMPLE_DOC_2_PATH, EXAMPLE_DOC_3_PATH]:
        with open(EXAMPLE_DOC_1_PATH, "r") as infile:
            docs.append(infile.read())

    trainer = Trainer(SPACY_FORMATTED_TRAIN_DATA_PATH, MODEL_V1_PATH, num_iters=100, print_freq=10, test_docs=docs, verbose=True)

    trainer.load_dataset()
    trainer.setup_training()
    trainer.train()
    trainer.save()
