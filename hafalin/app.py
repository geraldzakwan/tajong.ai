# Main web app: Use Flask/Django or whatever
# CC: Lerps

# Example of using QuestionGen module

from questiongen.__init__ import INPUT_EXAMPLE_1_FILEPATH

from questiongen.questiongen import QuestionGen

question_gen = QuestionGen(is_mock=True)

# Read input example and replace newline with space
with open(INPUT_EXAMPLE_1_FILEPATH) as infile:
    document = infile.read().replace("\n", " ")

short_answer = question_gen.generate(document=document, question_type="short_answer")

multiple_choice = question_gen.generate(document=document, question_type="multiple_choice")

print(short_answer)

print(multiple_choice)
