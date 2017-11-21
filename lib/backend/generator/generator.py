from flask import Blueprint, jsonify, request

from .. import appLog
from ..corpus.models import Corpus_category
from ..generator import models

generator_blueprint = Blueprint('generator', __name__)


algos = {
    'markovify': 'MarkovifyAlgo',
    'MarkovChain': 'MarkovChainAlgo'
}


def verify_paylaod(request):
    response_object = {'status': 'fail', 'message': 'Invalid payload.'}
    post_data = request.get_json()
    if not post_data:
        return response_object, None, None
    algo = post_data.get('algo')
    category_id = post_data.get('category_id')

    if algo is None or category_id is None:
        return response_object, None, None

    if algo not in algos:
        response_object = {
            'status': 'error',
            'message': 'Selected algorithm does not exist.'
        }
        return response_object, None, None

    category = Corpus_category.query.filter_by(id=category_id).first()
    if not category:
        response_object = {
            'status': 'error',
            'message': 'Selected category does not exist.'
        }
        return response_object, None, None
    return None, algo, category_id


@generator_blueprint.route('/train', methods=['POST'])
def train():
    """Train the selected model"""
    response_object, algo, category_id = verify_paylaod(request)

    # if response_object not None, an error was identified
    if response_object:
        return jsonify(response_object), 400

    try:
        text_generator = models.TextGeneration(getattr(models, algos[algo])())
        trained = text_generator.train(category_id)
    except Exception as e:
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error during model training. '
            'Please verify corpus texts.'
        }
        return jsonify(response_object), 500

    if not trained:
        response_object = {
            'status': 'fail',
            'message': 'Failed during model training. '
            'Please verify corpus texts.'
        }
        return jsonify(response_object), 400

    response_object = {
        'status': 'success',
        'message': f'Model "{algo}" trained. You can now generate texts.'
    }
    return jsonify(response_object), 200


@generator_blueprint.route('/generate', methods=['POST'])
def generate_text():
    """Generate text"""
    response_object, algo, category_id = verify_paylaod(request)

    # if response_object not None, an error was identified
    if response_object:
        return jsonify(response_object), 400

    text_generator = models.TextGeneration(getattr(models, algos[algo])())
    result = text_generator.generateText(category_id)

    if not result:
        response_object = {
            'status': 'fail',
            'message': 'No result, maybe the model is not trained.'
        }
        return jsonify(response_object), 400

    response_object = {
        'status': 'success',
        'data': {
            'text': result
        }
    }
    return jsonify(response_object), 200
