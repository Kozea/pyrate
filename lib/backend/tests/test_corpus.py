import json

from base import BaseTestCase
from io import BytesIO
from utils import add_category, add_user

from lib.backend import db


class TestCorpusService(BaseTestCase):
    """Tests for the Corpus Service."""

    def test_add_category(self):
        """=> Ensure a new category can be added to the database."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/categories',
                data=json.dumps(dict(label='romans')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('"romans" was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_duplicate_category(self):
        """=> Ensure error is thrown if a category is a duplicate (label)."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/categories',
                data=json.dumps(dict(label='romans')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            response = self.client.post(
                '/categories',
                data=json.dumps(dict(label='romans')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn(
                'Sorry. The category "romans" already exists.', data['message']
            )

    def test_add_category_no_label(self):
        """=> Ensure error is thrown if a label is not provided."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/categories',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_category(self):
        """=> Ensure get a category behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

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
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.delete(
                f'/categories/{cat.id}',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Category 1 deleted.', data['message'])

    def test_delete_category_admin(self):
        """=> Ensure delete a category by admin behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        admin = add_user('admin', 'admin@admin.com', 'admin')
        admin.admin = True
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='admin@admin.com', password='admin')
                ),
                content_type='application/json'
            )

            response = self.client.delete(
                f'/categories/{cat.id}',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Category 1 deleted.', data['message'])

    def test_delete_category_no_admin(self):
        """=> Ensure delete a category by admin behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        user2 = add_user('another', 'another@another.com', 'another')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='another@another.com', password='another')
                ),
                content_type='application/json'
            )

            response = self.client.delete(
                f'/categories/{cat.id}',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 401)
            self.assertIn('error', data['status'])
            self.assertIn(
                'You do not have permission to delete this category.',
                data['message']
            )

    def test_delete_not_exiting_category(self):
        """=> Ensure error is thrown if a category does not exist"""
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.delete(
                '/categories/999999999',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn(
                'Category 999999999 does not exist.', data['message']
            )

    def test_update_category(self):
        """=> Ensure an existing category can be updated in the database."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.put(
                f'/categories/{cat.id}',
                data=json.dumps(dict(label='newspapers')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_category_admin(self):
        """=> Ensure an existing category can be updated in the database."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        admin = add_user('admin', 'admin@admin.com', 'admin')
        admin.admin = True
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='admin@admin.com', password='admin')
                ),
                content_type='application/json'
            )
            response = self.client.put(
                f'/categories/{cat.id}',
                data=json.dumps(dict(label='newspapers')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_category_no_admin(self):
        """=> Ensure an existing category can't be updated in the database."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        user2 = add_user('another', 'another@another.com', 'another')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='another@another.com', password='another')
                ),
                content_type='application/json'
            )
            response = self.client.put(
                f'/categories/{cat.id}',
                data=json.dumps(dict(label='newspapers')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You do not have permission to update this category.',
                data['message']
            )
            self.assertIn('error', data['status'])

    def test_update_category_invalid_json(self):
        """=> Ensure error is thrown if the JSON object is empty."""
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.put(
                '/categories/1',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_no_existing_category(self):
        """=> Ensure error is thrown if the category does not exist."""
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.put(
                '/categories/1',
                data=json.dumps(dict(label='newspapers')),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Category 1 does not exist.', data['message'])
            self.assertIn('error', data['status'])

    def test_add_text_in_corpus(self):
        """=> Ensure add a text in corpus behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == f'Text "les miserables" was added!'
            )
            self.assertEqual(response.status_code, 201)

    def test_add_duplicate_text_in_corpus(self):
        """=> Ensure error is thrown if a duplicate text is added."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] ==
                f'Sorry. A text with the same title already exists.'
            )
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_unallowed_file(self):
        """=> Ensure error is thrown if text file extension is not allowed."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.aaaa'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'File extension not allowed.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_empty_file(self):
        """=> Ensure error is thrown if text file is empty."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(), ""),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'No selected file.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_no_file(self):
        """=> Ensure error is thrown if no text file is provided."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    file="",
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'No file part.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_no_file2(self):
        """=> Ensure error is thrown if no text file is provided."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'No file part.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_no_data(self):
        """=> Ensure error is thrown if text details are not provided."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )

            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt')
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_no_form(self):
        """=> Ensure error is thrown if the payload is not valid."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_without_title(self):
        """=> Ensure error is thrown if text title not provided."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_add_text_in_corpus_without_category(self):
        """=> Ensure error is thrown if text category not provided."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "Les miserables"}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == f'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_delete_corpus(self):
        """=> Ensure delete a text from a corpus behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            response = self.client.delete(
                f'/corpus/1',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Corpus text 1 deleted.', data['message'])

    def test_delete_corpus_admin(self):
        """=> Ensure delete a text from a corpus behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        admin = add_user('admin', 'admin@admin.com', 'admin')
        admin.admin = True
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='admin@admin.com', password='admin')
                ),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            response = self.client.delete(
                f'/corpus/1',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Corpus text 1 deleted.', data['message'])

    def test_delete_corpus_no_admin(self):
        """=> Ensure delete a text from a corpus behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        cat = add_category('romans', user.id)

        user2 = add_user('another', 'another@another.com', 'another')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    dict(email='another@another.com', password='another')
                ),
                content_type='application/json'
            )
            response = self.client.post(
                '/corpus',
                data=dict(
                    file=(BytesIO(b'les miserables'), 'les_miserables.txt'),
                    data='{"title": "les miserables", "category_id": 1}'
                ),
                headers=dict(
                    content_type='multipart/form-data',
                    authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            response = self.client.delete(
                f'/corpus/1',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 401)
            self.assertIn('error', data['status'])
            self.assertIn(
                'You do not have permission to delete this text.',
                data['message']
            )

    def test_delete_not_exiting_corpus(self):
        """=> Ensure error is thrown if a text does not exist"""
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            response = self.client.delete(
                '/corpus/999999999',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Text 999999999 does not exist.', data['message'])
