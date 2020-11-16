# Tajong.ai

A web app that could automatically generate academic questions (multiple choice and short answer) given a document in Indonesian, for example, an elementary school history lesson. Submitted for a Hackathon competition held by Kata.ai. More on the competition: https://blog.kata.ai/en/post/katahack-2-0-2/.

# How to Run

- Install all requirements

  `pip install -r requirements.txt`

- Run the web app

  `python3 app.py`

# How to use API (Using GET params or POST JSON)

- Example Request to Get Short Answer Question

```
curl --location --request GET 'https://hafalin.herokuapp.com/generate_question?document=test&type=short_answer'
```

```
curl --location --request POST 'https://hafalin.herokuapp.com/generate_question' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document": "test",
    "type": "short_answer"
}'
```

- Example Request to Get Multiple Choice Question

```
curl --location --request GET 'https://hafalin.herokuapp.com/generate_question?document=test&type=multiple_choice'
```

```
curl --location --request POST 'https://hafalin.herokuapp.com/generate_question' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document": "test",
    "type": "multiple_choice"
}'
```
