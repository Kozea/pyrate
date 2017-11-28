import datetime
import json
from ddt import ddt, data, unpack

from base import BaseTestCase
from utils import add_all, add_category, add_user

from lib.backend import db
from lib.backend.generator.models import TextGeneration, MarkovifyAlgo, MarkovChainAlgo, Training, Algorithm


@ddt
class TestGeneratorService(BaseTestCase):
    """Tests for the Generator Service."""

    @data('markovify', 'MarkovChain')
    def test_train(self, value):
        """=> Ensure a model can be trained."""
        add_all()

        with self.client:
            response = self.client.post(
                '/api/train',
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
                '/api/train',
                data=json.dumps(dict(
                    algo=value,
                    category_id=1
                    )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/generate',
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
                '/api' + value,
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
                '/api' + route,
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
                '/api' + value,
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
                '/api' + value,
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
                '/api' + route,
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

    @data('markovify', 'MarkovChain')
    def test_train_no_file(self, value):
        """
            => Ensure error is thrown if there is no text in corpus or
               pre-trained models.
        """
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no file exists

        with self.client:
            response = self.client.post(
                '/api/train',
                data=json.dumps(dict(
                    algo=value,
                    category_id=2
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 500)
            self.assertIn('fail', data['status'])
            self.assertIn('Failed during model training. Please verify corpus texts.',
                          data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_no_train(self, value):
        """
            => Ensure error is thrown if the model is not trained.
        """
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no file exists

        with self.client:
            response = self.client.post(
                '/api/generate',
                data=json.dumps(dict(
                    algo=value,
                    category_id=2
                    )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('The model is not trained. Please train it and retry.',
                          data['message'])

    @data('markovify', 'MarkovChain')
    def test_generate_no_file(self, value):
        """
            => Ensure error is thrown if there is no pre-trained models.
        """
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('test', user.id)
        cat = add_category('romans', user.id)  # to be sure no file exists

        algo = Algorithm.query.filter_by(label=value).first()
        training = Training()
        training.category_id = cat.id
        training.last_train_date = datetime.datetime.utcnow()
        algo.trainings.append(training)
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/api/generate',
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
