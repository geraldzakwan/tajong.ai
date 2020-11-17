# Constants or whatever needed here in the root dir of ner

DATA_DIR = "ner/data"

TRAIN_DATA_1_PATH = "{}/train_data_1.txt".format(DATA_DIR)
TRAIN_DATA_2_PATH = "{}/train_data_2.txt".format(DATA_DIR)

SPACY_FORMATTED_TRAIN_DATA_PATH = "{}/spacy_formatted_train_data.pk".format(DATA_DIR)

EXAMPLE_DOCS_PATH = "{}/example_docs.txt".format(DATA_DIR)

MODEL_DIR = "ner/model"

MODEL_V0_PATH = "{}/model_v0_100".format(MODEL_DIR)
MODEL_V1_PATH = "{}/model_v1".format(MODEL_DIR)

DEFAULT_MODEL_PATH = MODEL_V0_PATH
