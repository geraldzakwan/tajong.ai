import time
import string

import numpy as np

from random import randint, sample

from hafalin.questiongen.__init__ import OUTPUT_EXAMPLE_1_SHORT_ANSWER_FILEPATH, OUTPUT_EXAMPLE_1_MULTIPLE_CHOICE_FILEPATH
from hafalin.questiongen.__init__ import CHOICES, MIN_CHOICES, MAX_CHOICES

from ner.ner import NER

class QuestionGen:

    def __init__(self, ner, verbose):
        start = time.time()

        self.ner = ner

        self.verbose = verbose
        if self.verbose:
            print("Initialization finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    # Input: Document: String of any length.
    #        See /hafalin/data/examples/input_example_1.txt.

    # Output: A list of dictionary
    #         See generate_short_answer() and generate_multiple_choice() below

    # Outputs explanation per key:

    # 1. "type": One of ["multiple_choice", "short_answer"].

    # 2. "question": String of any length.

    # 3. "choices": Applicable only for type="multiple_choice".
    #     A dictionary with letter option as key: "a", "b", "c", ...

    # 4. "answer": The correct answer, denoted by:
    #    - The key, e.g. "a", if type="multiple_choice".
    #    - List of String of any length, e.g. ["Teluk Bayur", "Selat Sunda"].
    #    Case doesn't matter because we will lowercase both student's answer and reference answer.
    #    Student's answer is correct if it matches one of the List element.
    #    We will also use edit distance so minor typo won't be deemed as incorrect.
    def generate(self, document, question_type, max_questions):
        self.document = document
        self.question_type = question_type
        self.max_questions = max_questions

        # Call appropriate function
        if question_type == "multiple_choice":
            return self.generate_multiple_choice()

        elif question_type == "short_answer":
            return self.generate_short_answer()

        else:
            raise Exception("Question type is not supported, use 'short_answer' or 'multiple_choice'")

    # Sample output:
    # [{
    #     "question": "Salah satu pelabuhan yang terdapat di Provinsi Sumatera Barat adalah Pelabuhan ....",
    #
    #     "answer": ["Teluk Bayur", "Selat Sunda"]
    # }]
    def generate_short_answer(self):
        start = time.time()

        # List of questions generated
        generated_questions = []

        self.identify_entities()

        iteration = 0

        for (sentence, ents) in self.sentence_ents:
            if self.verbose:
                print("Sentence: {}".format(sentence))
                print("--------------------------------------------------")
                print("Ents:")
                print(ents)
                print("--------------------------------------------------")

            if len(ents) > 0:
                rand_ent_idx = int(np.random.uniform(0, len(ents)))

                word, word_idx, label = ents[rand_ent_idx]

                if word_idx == 0:
                    question = "... " + sentence[len(word):]
                elif word_idx + len(word) == len(sentence):
                    question = sentence[:word_idx] + "..."
                else:
                    question = sentence[:word_idx] + " ... " + sentence[word_idx + len(word):]

                generated_questions.append({
                    "question": question,
                    "answer": [word]
                })

                iteration += 1
                if iteration > self.max_questions:
                    break

        if self.verbose:
            print("Generate short answer finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

        return generated_questions

    # Sample output:
    # [{
    #     "question": "Pulau Sumatera sebelah selatan dan barat berbatasan dengan ....",
    #
    #     "choices": {
    #         "a": "Selat Sunda dan Samudera Pasifik",
    #         "b": "Selat Sunda dan Samudera Indonesia",
    #         "c": "Selat Sunda dan Samudera Hindia",
    #         "d": "Selat Sunda dan Samudera Arktik"
    #     },
    #
    #     "answer": "a"
    # }]
    def generate_multiple_choice(self):
        start = time.time()

        # List of questions generated
        generated_questions = []

        self.identify_entities()

        iteration = 0

        entity_pool = {}

        for (_, ents) in self.sentence_ents:
            for ent in ents:
                word, _, label = ent

                if label not in entity_pool:
                    entity_pool[label] = set([])

                entity_pool[label].add(word)

        for label in entity_pool:
            if self.verbose:
                print(entity_pool[label])

            entity_pool[label] = list(entity_pool[label])

        for (sentence, ents) in self.sentence_ents:
            if self.verbose:
                print("Sentence: {}".format(sentence))
                print("--------------------------------------------------")
                print("Ents:")
                print(ents)
                print("--------------------------------------------------")

            if len(ents) > 0:
                rand_ent_idx = int(np.random.uniform(0, len(ents)))

                word, word_idx, label = ents[rand_ent_idx]

                if word_idx == 0:
                    question = "... " + sentence[len(word):]
                elif word_idx + len(word) == len(sentence):
                    question = sentence[:word_idx] + "..."
                else:
                    question = sentence[:word_idx] + " ... " + sentence[word_idx + len(word):]

                entity_candidates = entity_pool[label]

                try:
                    entity_candidates.remove(word)
                except:
                    pass

                num_candidates = len(entity_candidates)
                if num_candidates < MIN_CHOICES:
                    break

                if num_candidates > MAX_CHOICES:
                    num_candidates = MAX_CHOICES

                random_entity_idxes = sample(range(0, len(entity_candidates)), num_candidates)

                right_choice = CHOICES[randint(0, num_candidates - 1)]

                choices = {}
                idx = 0

                for choice in CHOICES[:num_candidates]:

                    if choice == right_choice:
                        choices[choice] = word
                    else:
                        choices[choice] = entity_candidates[random_entity_idxes[idx]]
                        idx = idx + 1

                generated_questions.append({
                    "question": question,
                    "choices": choices,
                    "answer": right_choice
                })

                iteration += 1
                if iteration > self.max_questions:
                    break

        if self.verbose:
            print("Generate multiple choice finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

        return generated_questions

    # Sample input:
    # Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di Pulau Sumatera. Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur. Sebelum pulang, supir bus sengaja membawa mereka mampir ke Pelabuhan Teluk Bayur yang merupakan salah satu dari lima pelabuhan terbesar dan tersibuk di Indonesia. Mereka juga melewati Provinsi Bengkulu, Sumatera Selatan, dan Lampung karena searah dengan jalan pulang menuju Jakarta.
    #
    # --------------------------------------------------
    # Entities: [('Roro', 'PERSON'), ('Sumatera Barat', 'LOCATION'), ('Pulau Sumatera', 'LOCATION'), ('Teluk Benggala', 'LOCATION'), ('Selat Sunda', 'LOCATION'), ('Selat Malaka', 'LOCATION'), ('Pelabuhan Teluk Bayur', 'LOCATION'), ('Indonesia', 'LOCATION'), ('Bengkulu', 'LOCATION'), ('Sumatera Selatan', 'LOCATION'), ('Jakarta', 'LOCATION')]

    # Sample output:
    #
    def identify_entities(self):
        start = time.time()

        self.pred_ents = self.ner.predict([self.document])[0]
        self.sentence_ents = []

        if self.ner.ner_library == "kata":
            for sentence, sent_ents in self.pred_ents:
                self.ents = []

                for ent in sent_ents:
                    word, word_idx, label = ent["value"], ent["start"], ent["label"]
                    word = word.translate(str.maketrans('', '', string.punctuation))

                    self.ents.append((word, word_idx, label))

                self.sentence_ents.append((sentence, self.ents))

            if self.verbose:
                print(self.sentence_ents)
                print("--------------------------------------------------")
                print("Identify entities finishes")
                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")

        elif self.ner.ner_library == "spacy":
            for sentence, sent_ents in self.pred_ents:
                self.ents = []

                for ent in sent_ents.ents:
                    word, label = ent.text, ent.label_
                    word = word.translate(str.maketrans('', '', string.punctuation))

                    word_idx = sentence.find(word)

                    self.ents.append((word, word_idx, label))

                self.sentence_ents.append((sentence, self.ents))

            if self.verbose:
                print(self.sentence_ents)
                print("--------------------------------------------------")
                print("Identify entities finishes")
                print("Time elapsed: {} seconds".format(time.time() - start))
                print("--------------------------------------------------")

if __name__ == "__main__":
    question_gen = QuestionGen(
        ner=NER(
            ner_library="kata",
            model_identifier="https://geist.kata.ai/nlus/tajong:hafalin/predict;fccfb733-1dfc-4f48-a42b-1db3bd7ef9ba\n",
            verbose=True
        ),
        verbose=True
    )

    # question_gen = QuestionGen(
    #     ner=NER(
    #         ner_library="spacy",
    #         model_identifier="default",
    #         verbose=True
    #     ),
    #     verbose=True
    # )

    question_gen.generate(
        document="Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di Pulau Sumatera. Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur. Sebelum pulang, supir bus sengaja membawa mereka mampir ke Pelabuhan Teluk Bayur yang merupakan salah satu dari lima pelabuhan terbesar dan tersibuk di Indonesia. Mereka juga melewati Provinsi Bengkulu, Sumatera Selatan, dan Lampung karena searah dengan jalan pulang menuju Jakarta.",
        question_type="short_answer",
        max_questions=5
    )
