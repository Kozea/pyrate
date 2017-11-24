import datetime

from flask import Blueprint, jsonify, request

from .. import appLog, db
from ..corpus.models import Corpus_category
from ..generator import models
from ..generator.models import Algorithm, Training

generator_blueprint = Blueprint('generator', __name__)


def verify_payload(request):
    response_object = {'status': 'fail', 'message': 'Invalid payload.'}
    post_data = request.get_json()
    if not post_data:
        return response_object, None, None
    algo_name = post_data.get('algo')
    category_id = post_data.get('category_id')

    if algo_name is None or category_id is None:
        return response_object, None, None

    algo = Algorithm.query.filter_by(label=algo_name).first()
    if not algo:
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


@generator_blueprint.route('/algorithmes', methods=['GET'])
def get_algorithm():
    """Get all corpus categories"""
    algos = Algorithm.query.all()
    algos_list = []
    for algo in algos:
        trainings_list = None
        for training in algo.trainings:
            trainings_list = {
                'category_id': training.category_id,
                'last_train': training.last_train_date
            }
        algo_object = {
            'id': algo.id,
            'label': algo.label,
            'training': trainings_list
        }
        algos_list.append(algo_object)
    response_object = {
        'status': 'success',
        'data': {
            'algorithmes': algos_list
        }
    }
    return jsonify(response_object), 200


@generator_blueprint.route('/train', methods=['POST'])
def train():
    """Train the selected model"""
    response_object, algo, category_id = verify_payload(request)

    # if response_object not None, an error was identified
    if response_object:
        return jsonify(response_object), 400

    # The others letters must keep capital letters
    algo_class = algo.label[0].capitalize() + algo.label[1:] + "Algo"
    try:
        text_generator = models.TextGeneration(getattr(models, algo_class)())
        trained_OK = text_generator.train(category_id)

        if not trained_OK:
            response_object = {
                'status': 'fail',
                'message': 'Failed during model training. '
                'Please verify corpus texts.'
            }
            return jsonify(response_object), 500

        # update date of the last training with the selected category
        training = Training.query.filter_by(algorithm_id=algo.id,
                                            category_id=category_id).first()
        if not training:
            training = Training()
            training.category_id = category_id
            # training.last_train_date = datetime.datetime.utcnow()
            algo.trainings.append(training)
        training.last_train_date = datetime.datetime.utcnow()
        db.session.commit()
    except Exception as e:
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error during model training. '
            'Please verify corpus texts.'
        }
        return jsonify(response_object), 500

    response_object = {
        'status': 'success',
        'message': f'Model "{algo.label}" trained. You can now generate texts.'
    }
    return jsonify(response_object), 200


@generator_blueprint.route('/generate', methods=['POST'])
def generate_text():
    """Generate text"""
    response_object, algo, category_id = verify_payload(request)

    # if response_object not None, an error was identified
    if response_object:
        return jsonify(response_object), 400

    print("=============")
    print(algo.label)
    print(category_id)
    print(algo.is_trained(category_id))
    print("=============")

    if not algo.is_trained(category_id):
        response_object = {
            'status': 'fail',
            'message': 'The model is not trained. Please train it and retry.'
        }
        return jsonify(response_object), 400

    # The others letters must keep capital letters
    algo_class = algo.label[0].capitalize() + algo.label[1:] + "Algo"
    text_generator = models.TextGeneration(getattr(models, algo_class)())
    result = text_generator.generateText(category_id)

    if not result:
        response_object = {
            'status': 'fail',
            'message': 'No result, maybe the model must be re-trained.'
        }
        return jsonify(response_object), 400

    response_object = {
        'status': 'success',
        'data': {
            'text': result
        }
    }
    return jsonify(response_object), 200
