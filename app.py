# Main web app: Use Flask/Django or whatever

from questiongen.__init__ import INPUT_EXAMPLE_1_FILEPATH
from questiongen.questiongen import QuestionGen

from flask import Flask, request, jsonify

app = Flask(__name__)
app.question_gen = QuestionGen(is_mock=True)

@app.route("/")
def index():
    return "<h1>HAFALIN 1.0 API</h1>"

@app.route("/generate_question/", methods=["GET", "POST"])
def post_something():
    if request.method == "GET":
        document = request.args.get("document", None)
        type = request.args.get("type", None)

    elif request.method == "POST":
        document = request.form.get("document", None)
        type = request.form.get("type", None)

    if document:
        if type:
            if app.question_gen.is_mock:
                with open(INPUT_EXAMPLE_1_FILEPATH) as infile:
                    document = infile.read().replace("\n", " ")

            if type == "short_answer":
                return jsonify({
                    "data": question_gen.generate(document=document, question_type="short_answer")
                })

            elif type == "multiple_choice"
                return jsonify({
                    "data": question_gen.generate(document=document, question_type="multiple_choice")
                })

            else:
                return jsonify({
                    "error": {
                        "code": 400,
                        "message": "Supported type is 'short_answer', 'multiple_choice', and 'all'"
                    }
                })

        else:
            return jsonify({
                "error": {
                    "code": 400,
                    "message": "Type is not specified"
                }
            })

    else:
        return jsonify({
            "error": {
                "code": 400,
                "message": "Document is not specified"
            }
        })

if __name__ == '__main__':
    app.run(threaded=True, port=5000)