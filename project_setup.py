import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import spacy.cli


nlp = spacy.load("en_core_web_sm")

spacy.cli.download("en_core_web_sm")

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
