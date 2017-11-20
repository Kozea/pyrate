import os
from pathlib import Path

from base import BaseTestCase
from utils import add_category, add_corpus_text, add_user

from lib.backend import app, db
from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo


def create_file():
    user = add_user('test', 'test@test.com', 'test')
    cat = add_category('romans', user.id)
    filename = 'les_miserables_markov.txt'
    dirpath = os.path.join(app.root_path, 'tests/files')
    filepath = os.path.join(dirpath, filename)
    txt = add_corpus_text('les_miserables_markov',
                          filepath,
                          cat.id,
                          user.id)


class TestGeneratorMarkovify(BaseTestCase):
    """Tests for the Generator Model."""

    def test_train(self):
        """=> Ensure a model file is generated (WIP)."""
        create_file()
        text_generator = TextGeneration(MarkovifyAlgo())
        text_generator.train(1)
        model_filepath = os.path.join(app.config['TRAINING_FOLDER'],
                                  "markovify/markovify_1_model.json")
        model_file = Path(model_filepath)
        self.assertTrue(model_file.is_file())

    def test_generate(self):
        """=> Ensure text generation is ok"""
        create_file()
        text_generator = TextGeneration(MarkovifyAlgo())
        result = text_generator.generateText(1)
        self.assertIsNotNone(result)
