import time

from random import randint

from hafalin.questiongen.__init__ import OUTPUT_EXAMPLE_1_SHORT_ANSWER_FILEPATH, OUTPUT_EXAMPLE_1_MULTIPLE_CHOICE_FILEPATH
from hafalin.questiongen.__init__ import CHOICES

from ner.ner import NER

class QuestionGen:

    def __init__(self, is_mock, ner, verbose):
        start = time.time()

        self.verbose = verbose

        self.is_mock = is_mock

        self.ner = None
        if not self.is_mock:
            self.ner = ner

        if self.verbose:
            print("Initialization finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

    # Still a mock
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
            raise Exception("Question type is not supported!")

    # Still a mock
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

        if self.is_mock:

            # Generate question max_questions times
            for _ in range(self.max_questions):

                # Read output example
                with open(OUTPUT_EXAMPLE_1_SHORT_ANSWER_FILEPATH, "r") as infile:
                    data = infile.readlines()

                # The first line is the question
                question = data[0].strip("\n")
                del(data[0])

                answer_candidates = []

                # The remaining lines are the answer candidates
                for answer in data:
                    answer_candidates.append(answer.strip("\n"))

                # Append dict object
                generated_questions.append({
                    "question": question,
                    "answer": answer_candidates
                })

        else:
            self.identify_entities()

            iteration = 0

            for (sentence, ents) in self.sentence_ents:
                if self.verbose:
                    print("Sentence: {}".format(sentence))
                    print("--------------------------------------------------")
                    print("Ents:")
                    print(ents)
                    print("--------------------------------------------------")

                for ent in ents:
                    word, word_idx, label = ent

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

                if iteration > self.max_questions:
                    break


        if self.verbose:
            print("Generate short answer finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

        return generated_questions

    # Still a mock
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

        if self.is_mock:

            # Generate question max_questions times
            for _ in range(self.max_questions):

                # Read output example
                with open(OUTPUT_EXAMPLE_1_MULTIPLE_CHOICE_FILEPATH, "r") as infile:
                    data = infile.readlines()

                # The first line is the question
                question = data[0].strip("\n")
                del(data[0])

                choices = {}

                # The remaining lines, except the last line, are the answer choices
                for i, line in enumerate(data):

                    if i == len(data) - 1:
                        break

                    # Choice line example:
                    # a;Selat Sunda dan Samudera Pasifik
                    line_tuple = line.split(";")

                    letter_choice = line_tuple[0]

                    answer = line_tuple[1]
                    answer = answer.strip("\n")

                    choices[letter_choice] = answer

                # The last line is the correct choice
                answer = data[-1].strip("\n")

                # Append dict object
                generated_questions.append({
                    "question": question,
                    "choices": choices,
                    "answer": answer
                })

        else:
            iteration = 0

            for (sentence, ents) in self.sentence_ents:
                if self.verbose:
                    print("Sentence: {}".format(sentence))
                    print("--------------------------------------------------")
                    print("Ents:")
                    print(ents)
                    print("--------------------------------------------------")

                for ent in ents:
                    word, word_idx, label = ent

                    if word_idx == 0:
                        question = "... " + sentence[len(word):]
                    elif word_idx + len(word) == len(sentence):
                        question = sentence[:word_idx] + "..."
                    else:
                        question = sentence[:word_idx] + " ... " + sentence[word_idx + len(word):]

                    right_choice = CHOICES[randint(0, len(CHOICES) - 1)]

                    choices = {}
                    for choice in CHOICES:
                        if choice == right_choice:
                            choices[choice] = word
                        else:
                            # TO BE IMPLEMENTED
                            choices[choice] = "dummy"

                    generated_questions.append({
                        "question": question,
                        "choices": choices,
                        "answer": right_choice
                    })

                    iteration += 1
                    if iteration > self.max_questions:
                        break

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

        for sentence in self.document.split("."):
            self.ents = []

            for ent in self.pred_ents.ents:
                word, label = ent.text, ent.label_
                word_idx = sentence.find(word)

                if word_idx > -1:
                    self.ents.append((word, word_idx, label))

            self.sentence_ents.append((sentence, self.ents))

        if self.verbose:
            print(self.sentence_ents)
            print("--------------------------------------------------")
            print("Identify entities finishes")
            print("Time elapsed: {} seconds".format(time.time() - start))
            print("--------------------------------------------------")

if __name__ == '__main__':
    question_gen = QuestionGen(
        is_mock=False,
        ner=NER(model_filepath="default", verbose=True),
        verbose=True
    )

    with open(EXAMPLE_DOCS_PATH, "r") as infile:
        docs = infile.readlines()

    for doc in docs:
        doc = doc.strip("\n")

        if len(doc) > 0:
            app.question_gen.generate(doc, "short_answer", 1)
