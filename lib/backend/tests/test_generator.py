import json
from ddt import ddt, data, unpack

from base import BaseTestCase
from utils import add_all, add_category, add_user

from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo


@ddt
class TestGeneratorService(BaseTestCase):
    """Tests for the Generator Service."""

    @data('markovify', 'MarkovChain')
    def test_train(self, value):
        """=> Ensure a model can be trained."""
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

    @data('markovify', 'MarkovChain')
    def test_generate_text(self, value):
        """=> Ensure text can be generate without error."""
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

    @data('/train', '/generate')
    def test_generator_invalid_payload(self, value):
        """=> Ensure error is thrown if no category or model are provided."""
        add_all()

        with self.client:
            response = self.client.post(
                value,
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    @data(('markovify', '/train'),
          ('markovify', '/generate'),
          ('MarkovChain', '/train'),
          ('MarkovChain', '/generate'))
    @unpack
    def test_generator_no_category(self, algo, route):
        """=> Ensure error is thrown if no category is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                route,
                data=json.dumps(dict(
                    algo=algo
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    @data('/train', '/generate')
    def test_generator_no_algo(self, value):
        """=> Ensure error is thrown if no model is provided."""
        add_all()

        with self.client:
            response = self.client.post(
                value,
                data=json.dumps(dict(
                    category_id=1
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    @data('/train', '/generate')
    def test_generator_invalid_model(self, value):
        """=> Ensure error is thrown if model does not exist"""
        add_all()

        with self.client:
            response = self.client.post(
                value,
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

    @data(('markovify', '/train'),
          ('markovify', '/generate'),
          ('MarkovChain', '/train'),
          ('MarkovChain', '/generate'))
    @unpack
    def test_generator_invalid_category(self, algo, route):
        """=> Ensure error is thrown if category does not exist."""
        add_all()

        with self.client:
            response = self.client.post(
                route,
                data=json.dumps(dict(
                    algo=algo,
                    category_id=99999999
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Selected category does not exist.', data['message'])

    @data(('markovify', '/train'),
          ('markovify', '/generate'),
          ('MarkovChain', '/train'),
          ('MarkovChain', '/generate'))
    @unpack
    def test_generator_no_file(self, algo, route):
        """
            => Ensure error is thrown if there is no text in corpus or
               pre-trained models.
        """
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no file exist

        with self.client:
            response = self.client.post(
                route,
                data=json.dumps(dict(
                    algo=algo,
                    category_id=2
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])

            if route == '/train':
                self.assertIn('Failed during model training. Please verify corpus texts.',
                              data['message'])
            else:  # no train in this case (not a test on fil existence)
                self.assertIn('No result, maybe the model must be re-trained.',
                              data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_text_no_file(self, value):
        """
            => Ensure error is thrown if there is no text in corpus or
               pre-trained models.
        """
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no file exist

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
            self.assertIn('No result, maybe the model must be re-trained.',
                          data['message'])
