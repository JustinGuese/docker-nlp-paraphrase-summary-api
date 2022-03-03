from parrot import Parrot
import nltk

nltk.download("stopwords")
nltk.download("punkt")

PARROT_MODEL = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)