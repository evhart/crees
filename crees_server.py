#! /usr/bin/env python
import os
import sys
from optparse import OptionParser

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from tensorflow.contrib import learn

import data_helpers
from flask_restplus import Api, Resource, fields, marshal_with, reqparse
from text_cnn import TextCNNModel


# Create event type model
def __load_models():
    mod = "models/event-types/model.ckpt"
    vocab = "models/event-types/vocabulary.voc"
    type_classifier = TextCNNModel.restore(
        mod, vocab, sequence_length=32, num_classes=14, vocab_size=44345)
    type_classifier.labels = ["bombings", "collapse", "crash", "derailment", "earthquake",
                              "explosion", "fire", "floods", "haze", "meteorite",
                              "none", "shootings", "typhoon", "wildfire"]

    # Create related event type model:
    mod = "models/event-related/model.ckpt"
    vocab = "models/event-related/vocabulary.voc"
    related_classifier = TextCNNModel.restore(
        mod, vocab, sequence_length=43, num_classes=2, vocab_size=87420)
    related_classifier.labels = ["non-related", "related"]

    # Create related info type model:
    mod = "models/info-types/model.ckpt"
    vocab = "models/info-types/vocabulary.voc"
    info_classifier = TextCNNModel.restore(
        mod, vocab, sequence_length=32, num_classes=8, vocab_size=44345)
    info_classifier.labels = ["affected_individuals", "caution_and_advice", "donations_and_volunteering",
                              "infrastructure_and_utilities", "not_applicable", "not_labeled",
                              "other_useful_information", "sympathy_and_support"]

    return (type_classifier, related_classifier, info_classifier)


def main(argv):

    # Parse command line arguments:
    parser = OptionParser()
    parser.add_option('-p', '--port', type='int', dest='port', default=80,
                      help="the API port for serving CREES [default: %default]")

    parser.add_option('-n', '--namespace', type='string', dest='api_namespace', default="comrades",
                      help="the API namespace for CREES [default: %default]")

    (options, args) = parser.parse_args()

    # Use environment variables if available:
    if os.environ.get('CREES_PORT') is not None and options.port is 80:
        options.port = int(os.environ.get('CREES_PORT'))
    if os.environ.get('CREES_NAMESPACE') is not None and options.api_namespace is 'comrades':
        options.api_namespace = str(os.environ.get('CREES_NAMESPACE'))

    # Web App:
    app = Flask(__name__, static_url_path='')
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.config['APPLICATION_ROOT'] = '/' + options.api_namespace
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    api = Api(app, version='0.3', title='COMRADES Event API',
              description='A set of tools for analysing short textual documents (e.g. tweets).',
              doc='/' + options.api_namespace + '/',
              endpoint='/' + options.api_namespace
              )

    ns = api.namespace(options.api_namespace,
                       description='Event detection tools.')

    # Load models:
    type_classifier, related_classifier, info_classifier = __load_models()

    # Routes:
    @ns.route('/')
    class RootController(Resource):
        def get(self):
            return app.send_static_file('index.html')

    @ns.route('/events/eventType')
    class EventClassifierController(Resource):
        """
        Performs event detection on short piece of text (e.g. tweets).
        """

        # API arguments:
        get_arguments = reqparse.RequestParser()
        get_arguments.add_argument(
            'text', required=True, help="The text to be analysed.")

        # Output arguments:
        model = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
            'classifier': fields.String,
            'version': fields.Float
        })

        @api.doc(id='textEventType')
        @api.expect(get_arguments, validate=True)
        @api.marshal_with(model, description='Event type')
        def get(self):
            """Obtains the type of event associated with a post."""
            args = self.get_arguments.parse_args()
            text = args['text']
            results = type_classifier.predict(text)

            return {'input': text, 'label': results, 'classifier': "CNN", 'version': 0.3}

    @ns.route('/events/infoType')
    class InfoTypeClassifierController(Resource):
        """
        Identifies the type of information associated with a post.
        """

        # API arguments:
        get_arguments = reqparse.RequestParser()
        get_arguments.add_argument(
            'text', required=True, help="The text to be analysed.")

        # Output arguments:
        model = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
            'classifier': fields.String,
            'version': fields.Float
        })

        @api.doc(id='textInfoType')
        @api.expect(get_arguments, validate=True)
        @api.marshal_with(model, description='Info type')
        def get(self):
            """Identifies the type of information associated with a post."""
            args = self.get_arguments.parse_args()
            text = args['text']
            results = info_classifier.predict(text)

            return {'input': text, 'label': results, 'classifier': "CNN", 'version': 0.3}

    @ns.route('/events/eventRelated')
    class RelatedClassifierController(Resource):
        """
        Identifies if a post is talking about an event.
        """

        # API arguments:
        get_arguments = reqparse.RequestParser()
        get_arguments.add_argument(
            'text', required=True, help="The text to be analysed.")

        # Output arguments:
        model = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
            'classifier': fields.String,
            'version': fields.Float
        })

        @api.doc(id='textEventRelated')
        @api.expect(get_arguments, validate=True)
        @api.marshal_with(model, description='Event relation')
        def get(self):
            """Identifies if a post is talking about an event."""
            args = self.get_arguments.parse_args()
            text = args['text']
            results = related_classifier.predict(text)

            return {'input': text, 'label': results, 'classifier': "CNN", 'version': 0.3}

    # Start App:
    app.run(host='0.0.0.0', port=options.port, debug=False)


if __name__ == "__main__":
    main(sys.argv)
