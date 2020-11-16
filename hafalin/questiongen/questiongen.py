# QuestionGen class

from hafalin.questiongen.__init__ import OUTPUT_EXAMPLE_1_SHORT_ANSWER_FILEPATH, OUTPUT_EXAMPLE_1_MULTIPLE_CHOICE_FILEPATH

class QuestionGen:

    def __init__(self, is_mock):
        self.is_mock = is_mock

    # Still a mock
    # Input: Document: String of any length.
    #        See /hafalin/data/input_example_1.txt for example.

    # Output: A dictionary. for example:
    #         See /hafalin/data/output_example_1_short_answer.txt
    #         and /hafalin/data/output_example_1_multiple_choice.txt for example.

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
    def generate(self, document, question_type):

        self.document = document
        self.question_type = question_type

        # Call appropriate function
        if question_type == "multiple_choice":
            return self.generate_multiple_choice()

        elif question_type == "short_answer":
            return self.generate_short_answer()

        else:
            raise Exception("Question type is not supported!")

    # Still a mock
    # Sample output:
    # {
    #
    #     "type": "short_answer",
    #
    #     "question": "Salah satu pelabuhan yang terdapat di Provinsi Sumatera Barat adalah Pelabuhan ....",
    #
    #     "answer": ["Teluk Bayur", "Selat Sunda"]
    # }
    def generate_short_answer(self):

        if self.is_mock:

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

        else:
            raise Exception("Not implemented yet!")

        # Built return object
        return {
            "type": self.question_type,
            "question": question,
            "answer": answer_candidates
        }

    # Still a mock
    # Sample output:
    # {
    #
    #     "type": "multiple_choice",
    #
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
    # }
    def generate_multiple_choice(self):

        if self.is_mock:

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

        else:
            raise Exception("Not implemented yet!")

        # Build return object
        return {
            "type": self.question_type,
            "question": question,
            "choices": choices,
            "answer": answer
        }
