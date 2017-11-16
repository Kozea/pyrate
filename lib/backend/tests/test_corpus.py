import json

from pyrate_api.tests.base import BaseTestCase
from pyrate_api.tests.utils import add_category, add_user, add_corpus_text


class TestCorpusService(BaseTestCase):
    """Tests for the Corpus Service."""

    def test_add_category(self):
        """=> Ensure a new category can be added to the database."""
        with self.client:
            response = self.client.post(
                '/categories',
                data=json.dumps(dict(
                    label='romans'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('"romans" was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_category_no_label(self):
        """=> Ensure error is thrown if a label is not provided."""
        with self.client:
            response = self.client.post(
                '/categories',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_category(self):
        """=> Ensure get a category behaves correctly."""
        cat = add_category('romans')

        with self.client:
            response = self.client.get(f'/categories/{cat.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('romans', data['data']['label'])

    def test_get_no_existing_category(self):
        """=> Ensure error is thrown if a category does not exist"""
        with self.client:
            response = self.client.get(f'/categories/99999999')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Category does not exist', data['message'])

    def test_delete_category(self):
        """=> Ensure delete a category behaves correctly."""
        cat = add_category('romans')

        with self.client:
            response = self.client.delete(f'/categories/{cat.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Category 1 deleted.', data['message'])

    def test_delete_not_exiting_category(self):
        """=> Ensure error is thrown if a category does not exist"""
        with self.client:
            response = self.client.delete('/categories/999999999')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Category 999999999 does not exist.', data['message'])


    def test_update_category(self):
        """=> Ensure an existing category can be updated in the database."""
        cat = add_category('romans')
        with self.client:
            response = self.client.put(
                f'/categories/{cat.id}',
                data=json.dumps(dict(
                    label='newspapers'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_category_invalid_json(self):
        """=> Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.put(
                '/categories/1',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_no_existing_category(self):
        """=> Ensure error is thrown if the category does not exist."""
        with self.client:
            response = self.client.put(
                '/categories/1',
                data=json.dumps(dict(
                    label='newspapers'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That category does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_text_in_corpus(self):
        """=> Ensure add a category behaves correctly."""
        add_user('test', 'test@test.com', 'test')
        add_category('romans')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

            response = self.client.post('/corpus',
                data=json.dumps(dict(
                    title='les miserables',
                    filename='les_miserables.txt',
                    category_id=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == f'Text "les miserables" was added!')
            self.assertEqual(response.status_code, 201)

    def test_delete_corpus(self):
        """=> Ensure delete a text from a corpus behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans')
        text = add_corpus_text('les miserables',
                               'les_miserables.txt',
                               cat.id,
                               user.id)

        with self.client:
            response = self.client.delete(f'/corpus/{text.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Corpus text 1 deleted.', data['message'])

    def test_delete_not_exiting_corpus(self):
        """=> Ensure error is thrown if a text does not exist"""
        with self.client:
            response = self.client.delete('/corpus/999999999')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Text 999999999 does not exist.', data['message'])
