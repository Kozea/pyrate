import json
from ddt import ddt, data

from base import BaseTestCase
from utils import add_all, add_category, add_user

from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo


@ddt
class TestGeneratorService(BaseTestCase):
    """Tests for the Generator Service."""

    @data('markovify', 'MarkovChain')
    def test_train(self, value):
        """=> Ensure model can be trained."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo=value,
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn(f'Model "{value}" trained. You can now generate texts.', data['message'])

    def test_train_invalid_payload(self):
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

    @data('markovify', 'MarkovChain')
    def test_train_no_category(self, value):
        """=> Ensure error is thrown if no category is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo=value
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_train_no_algo(self):
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

    def test_train_invalid_model(self):
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

    @data('markovify', 'MarkovChain')
    def test_train_invalid_category(self, value):
        """=> Ensure error is thrown if category does not exist."""
        add_all()

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo=value,
                    category_id=99999999
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Selected category does not exist.', data['message'])

    @data('markovify', 'MarkovChain')
    def test_train_no_corpus_text(self, value):
        """=> Ensure error is thrown if there is no text in corpus."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no text exists

        with self.client:
            response = self.client.post(
                '/train',
                data=json.dumps(dict(
                    algo=value,
                    category_id=2
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Failed during model training. Please verify corpus texts.',
                          data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_text(self, value):
        """=> Ensure text can be generate without error."""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict(
                    algo=value,
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertNotEqual('', data['data']['text'])

    @data('markovify', 'MarkovChain')
    def test_generate_text_invalid_payload(self, value):
        """=> Ensure error is thrown if no category and model are provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_text_no_category(self, value):
        """=> Ensure error is thrown if no category is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict(
                    algo=value
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_generate_text_no_algo(self):
        """=> Ensure error is thrown if no model is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict(
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_generate_text_invalid_model(self):
        """=> Ensure error is thrown if model does not exist"""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
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

    @data('markovify', 'MarkovChain')
    def test_generate_text_invalid_category(self, value):
        """=> Ensure error is thrown if category does not exist."""
        add_all()

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict(
                    algo=value,
                    category_id=99999999
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Selected category does not exist.', data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_text_no_corpus_text(self, value):
        """=> Ensure error is thrown if there is no text in corpus."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no text exists

        with self.client:
            response = self.client.post(
                '/generate',
                data=json.dumps(dict(
                    algo=value,
                    category_id=2
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('No result, maybe the model is not trained.',
                          data['message'])
