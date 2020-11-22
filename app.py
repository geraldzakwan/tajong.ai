# Main web app: Use Flask/Django or whatever

from flask import Flask, request

from hafalin.questiongen.__init__ import INPUT_EXAMPLE_1_FILEPATH
from hafalin.questiongen.questiongen import QuestionGen

from ner.__init__ import EXAMPLE_DOCS_PATH
from ner.ner import NER

from config import configs
from helper import reply_success, reply_error

from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

deploy_env = environ.get("DEPLOY_ENV")
ner_library = environ.get("NER")

if ner_library == "kata":
    model_url = environ.get("MODEL_URL")
    auth_token = environ.get("AUTH_TOKEN")

    model_identifier = "{};{}".format(model_url, auth_token)

elif ner_library == "spacy":
    model_identifier = "default"

else:
    raise Exception("NER library is not supported, use 'kata' or 'spacy'")

app = Flask(__name__)

app.question_gen = QuestionGen(
    ner=NER(
        ner_library=ner_library,
        model_identifier=model_identifier,
        verbose=True
    ),
    verbose=True
)

@app.route("/")
def index():
    return "<h1>HAFALIN 1.0 API</h1>"

@app.route("/generate_question/", methods=["GET", "POST"])
def generate_question():
    if request.method == "GET":
        document = request.args.get("document", None)
        type = request.args.get("type", None)
        max_questions = int(request.args.get("max_questions", None))

    elif request.method == "POST":
        json_req = request.get_json()

        document = json_req["document"]
        type = json_req["type"]
        max_questions = int(json_req["max_questions"])

    else:
        return reply_error(code=400, message="Supported method is 'GET' and 'POST'")

    if document:
        if type:
            if max_questions:
                if type == "short_answer":
                    return reply_success(data=app.question_gen.generate(document=document, question_type="short_answer", max_questions=max_questions))

                elif type == "multiple_choice":
                    return reply_success(data=app.question_gen.generate(document=document, question_type="multiple_choice", max_questions=max_questions))

                elif type == "all":
                    return reply_success(data={
                        "short_answer": app.question_gen.generate(document=document, question_type="short_answer", max_questions=max_questions),
                        "multiple_choice": app.question_gen.generate(document=document, question_type="multiple_choice", max_questions=max_questions)
                    })

                else:
                    return reply_error(code=400, message="Supported type is 'short_answer', 'multiple_choice', and 'all'")

            else:
                return reply_error(code=400, message="Max num is not specified")

        else:
            return reply_error(code=400, message="Type is not specified")

    else:
        return reply_error(code=400, message="Document is not specified")

if __name__ == "__main__":
    app.run(threaded=True, port=configs["DEPLOY_ENV"][deploy_env]["PORT"], debug=configs["DEPLOY_ENV"][deploy_env]["DEBUG"])
