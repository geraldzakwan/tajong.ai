# Tajong.ai

A web app that could automatically generate academic questions (multiple choice and short answer) given a document in Indonesian, for example, an elementary school history lesson. Submitted for a Hackathon competition held by Kata.ai. More on the competition: https://blog.kata.ai/en/post/katahack-2-0-2/.

# How to Run

- Install all requirements

  `pip install -r requirements.txt`

- Run the web app

  `python3 app.py`

# How to use API

- Example Request using GET params

```
curl --location --request GET 'https://https://hafalin.herokuapp.com/generate_question?document=test&type=all&max_questions=1'
```

- Example Request using POST JSON

```
curl --location --request POST 'http://https://hafalin.herokuapp.com//generate_question/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document": "test",
    "type": "all",
    "max_questions": 1
}'
```

- Example Response in JSON

```
{
    "data": {
        "multiple_choice": [
            {
                "answer": "a",
                "choices": {
                    "a": "Selat Sunda dan Samudera Pasifik",
                    "b": "Selat Sunda dan Samudera Indonesia",
                    "c": "Selat Sunda dan Samudera Hindia",
                    "d": "Selat Sunda dan Samudera Arktik"
                },
                "question": "Pulau Sumatera sebelah selatan dan barat berbatasan dengan ...."
            }
        ],
        "short_answer": [
            {
                "answer": [
                    "Teluk Bayur",
                    "Selat Sunda"
                ],
                "question": "Salah satu pelabuhan yang terdapat di Provinsi Sumatera Barat adalah Pelabuhan ...."
            }
        ]
    }
}
```
