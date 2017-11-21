import os

import markovify

from .. import app, appLog, db
from ..corpus.models import Corpus_category
from .custom.markovChain import MarkovChain


class Algorithm(db.Model):
    __tablename__ = "algorithms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(80), unique=True, nullable=False)
    last_train_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Text generation algorithm %r>' % self.label

    def __init__(self, label):
        self.label = label


class TrainException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class TextGeneration(object):
    def __init__(self, strategy):
        self.strategy = strategy
        self.generated_text = None

    def train(self, category_id):
        self.train = self.strategy.train(category_id)
        return self.train

    def generateText(self, category_id):
        self.generated_text = self.strategy.generateText(category_id)
        return self.generated_text


class TextGenerationStragegy(object):
    def train(self, category_id):
        raise NotImplementedError

    def generateText(self, category_id):
        raise NotImplementedError


class MarkovifyAlgo(TextGenerationStragegy):
    """Generate texts with 'markovify' package."""
    def __init__(self):
        self.name = "markovify"

    def train(self, category_id):
        category = Corpus_category.query.filter_by(id=category_id).first()
        if not category:
            raise TrainException("No text for this category.")

        corpus_texts = category.retrieve_corpus_text()
        text = ""
        try:
            for corpus_text in corpus_texts:
                with open(corpus_text) as f:
                    text = text + "\n\n" + f.read()

            # Build the model
            text_model = markovify.Text(text)

            # Export in JSON
            model_json = text_model.to_json()
            model_file = os.path.join(app.config['TRAINING_FOLDER'],
                                      "markovify",
                                      "markovify_{}_model.json"
                                      .format(category_id)
                                      )
            with open(model_file, 'w') as f:
                f.write(model_json)
                f.close()

            return True
        except Exception as e:
            appLog.error(e)
            return False

    def generateText(self, category_id, nb_sentences=5):
        result = ""

        try:
            model_file = os.path.join(app.config['TRAINING_FOLDER'],
                                      "markovify",
                                      "markovify_{}_model.json"
                                      .format(category_id)
                                      )

            with open(model_file) as f:
                model_json = f.read()
            text_model = markovify.Text.from_json(model_json)
            # Print five randomly-generated sentences
            for i in range(nb_sentences):
                result = result + (text_model.make_sentence()) + "\n\n"
            return result
        except Exception as e:
            appLog.error(e)
            return None


class MarkovChainAlgo(TextGenerationStragegy):
    """Generate texts with MarkovChain."""
    def __init__(self):
        self.name = "MarkovChain"

    def gen(self, m):
        return ''.join([w for w in m.generate_formatted(word_wrap=60,
                                                        soft_wrap=True,
                                                        start_with=None,
                                                        max_len=50,
                                                        verbose=True)])

    def train(self, category_id):
        mkv = MarkovChain()

        try:
            corpus_texts = os.path.join(app.config['UPLOAD_FOLDER'],
                                        str(category_id))

            parsed_files = mkv.bulk_train(corpus_texts + "/*.*")

            if parsed_files == 0:
                raise TrainException("No text for this category.")

            model_file = os.path.join(app.config['TRAINING_FOLDER'],
                                      "MarkovChain",
                                      "MarkovChain_cat-{}.model"
                                      .format(category_id)
                                      )
            mkv.save_training(model_file)
            return True
        except Exception as e:
            appLog.error(e)
            return False

    def generateText(self, category_id):
        mkv = MarkovChain()

        try:
            model_file = os.path.join(app.config['TRAINING_FOLDER'],
                                      "MarkovChain",
                                      "MarkovChain_cat-{}.model"
                                      .format(category_id)
                                      )
            mkv.load_training(model_file)

            return self.gen(mkv)
        except Exception as e:
            appLog.error(e)
            return None
