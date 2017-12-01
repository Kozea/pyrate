import os
from pathlib import Path

from base import BaseTestCase
from utils import add_all

from lib.backend import app
from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo



class TestGeneratorMarkovify(BaseTestCase):
    """Tests for markovify."""

    def test_train(self):
        """=> Ensure a model file is generated (WIP)."""
        add_all()
        text_generator = TextGeneration(MarkovifyAlgo())
        text_generator.train(1)
        model_filepath = os.path.join(app.config['TRAINING_FOLDER'],
                                  "markovify/markovify_1_model.json")
        model_file = Path(model_filepath)
        self.assertTrue(model_file.is_file())

    def test_generate(self):
        """=> Ensure text generation is ok"""
        add_all()
        text_generator = TextGeneration(MarkovifyAlgo())
        result = text_generator.generateText(1, 5)
        self.assertIsNotNone(result)


class TestGeneratorMarkovChain(BaseTestCase):
    """Tests for markovChain."""

    def test_train(self):
        """=> Ensure a model file is generated (WIP)."""
        add_all()
        text_generator = TextGeneration(MarkovChainAlgo())
        text_generator.train(1)
        model_filepath = os.path.join(app.config['TRAINING_FOLDER'],
                                  "markovify/markovify_1_model.json")
        model_file = Path(model_filepath)
        self.assertTrue(model_file.is_file())

    def test_generate(self):
        """=> Ensure text generation is ok"""
        add_all()
        text_generator = TextGeneration(MarkovChainAlgo())
        result = text_generator.generateText(1, 50)

        self.assertIsNotNone(result)
