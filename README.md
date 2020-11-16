# Tajong.ai

A web app that could automatically generate academic questions (multiple choice and short answer) given a document in Indonesian, for example, an elementary school history lesson. Submitted for a Hackathon competition held by Kata.ai. More on the competition: https://blog.kata.ai/en/post/katahack-2-0-2/.

# How to Run

- Install all requirements

  `pip install -r requirements.txt`

- Run the web app

  `python3 app.py`

# How to use API

- Example Request using POST JSON

```
curl --location --request POST 'http://127.0.0.1:5001/generate_question/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document": "Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di Pulau Sumatera. Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur. Sebelum pulang, supir bus sengaja membawa mereka mampir ke Pelabuhan Teluk Bayur yang merupakan salah satu dari lima pelabuhan terbesar dan tersibuk di Indonesia. Mereka juga melewati Provinsi Bengkulu, Sumatera Selatan, dan Lampung karena searah dengan jalan pulang menuju Jakarta.",
    "type": "all",
    "max_questions": 5
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
                    "a": "Roro",
                    "b": "dummy",
                    "c": "dummy",
                    "d": "dummy"
                },
                "question": "... , Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di Pulau Sumatera"
            },
            {
                "answer": "d",
                "choices": {
                    "a": "dummy",
                    "b": "dummy",
                    "c": "dummy",
                    "d": "Sumatera Barat"
                },
                "question": "Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke  ...  yang terletak di Pulau Sumatera"
            },
            {
                "answer": "c",
                "choices": {
                    "a": "dummy",
                    "b": "dummy",
                    "c": "Pulau Sumatera",
                    "d": "dummy"
                },
                "question": "Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di ..."
            },
            {
                "answer": "d",
                "choices": {
                    "a": "dummy",
                    "b": "dummy",
                    "c": "dummy",
                    "d": "Teluk Benggala"
                },
                "question": " Pulau ini berbatasan dengan  ...  pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur"
            },
            {
                "answer": "a",
                "choices": {
                    "a": "Selat Sunda",
                    "b": "dummy",
                    "c": "dummy",
                    "d": "dummy"
                },
                "question": " Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara,  ...  pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur"
            },
            {
                "answer": "a",
                "choices": {
                    "a": "Selat Malaka",
                    "b": "dummy",
                    "c": "dummy",
                    "d": "dummy"
                },
                "question": " Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan  ...  pada sebelah timur"
            }
        ],
        "short_answer": [
            {
                "answer": [
                    "Roro"
                ],
                "question": "... , Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di Pulau Sumatera"
            },
            {
                "answer": [
                    "Sumatera Barat"
                ],
                "question": "Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke  ...  yang terletak di Pulau Sumatera"
            },
            {
                "answer": [
                    "Pulau Sumatera"
                ],
                "question": "Roro, Guntur, dan Kanguru baru saja selesai melakukan karya wisata ke Sumatera Barat yang terletak di ..."
            },
            {
                "answer": [
                    "Teluk Benggala"
                ],
                "question": " Pulau ini berbatasan dengan  ...  pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur"
            },
            {
                "answer": [
                    "Selat Sunda"
                ],
                "question": " Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara,  ...  pada sebelah selatan, Samudera Hindia pada sebelah barat, dan Selat Malaka pada sebelah timur"
            },
            {
                "answer": [
                    "Selat Malaka"
                ],
                "question": " Pulau ini berbatasan dengan Teluk Benggala pada sebelah utara, Selat Sunda pada sebelah selatan, Samudera Hindia pada sebelah barat, dan  ...  pada sebelah timur"
            }
        ]
    }
}
```
