import json

from base import BaseTestCase
from utils import add_all, add_category, add_user

from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo



class TestGeneratorService(BaseTestCase):
    """Tests for the Generator Service."""

    def test_train_markovify(self):
        """=> Ensure model can be trained."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo='markovify',
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Model "markovify" trained. You can now generate texts.', data['message'])


    def test_train_markovify_invalid_payload(self):
        """=> Ensure error is thrown if no category and model are provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])


    def test_train_markovify_no_category(self):
        """=> Ensure error is thrown if no category is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo='markovify'
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_train_markovify_no_algo(self):
        """=> Ensure error is thrown if no model is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_train_markovify_invalid_model(self):
        """=> Ensure error is thrown if model does not exist"""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo='no-model',
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Selected algorithm does not exist.', data['message'])

    def test_train_markovify_invalid_category(self):
        """=> Ensure error is thrown if category does not exist."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo='markovify',
                    category_id=99999999
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Selected category does not exist.', data['message'])

    def test_train_markovify_no_corpus_text(self):
        """=> Ensure error is thrown if there is no text in corpus."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo='markovify',
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Failed during model training. Please verify corpus texts.',
                          data['message'])
