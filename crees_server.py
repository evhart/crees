#! /usr/bin/env python
from __future__ import print_function
import os
import sys
import io
import csv
from optparse import OptionParser

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from tensorflow.contrib import learn

import data_helpers
from flask_restplus import Api, Resource, fields, marshal_with, reqparse
from text_cnn import TextCNNModel

from werkzeug.datastructures import FileStorage



# Create event type model
def __load_models():
    mod = "models/event-types/model.ckpt"
    vocab = "models/event-types/vocabulary.voc"
    data_helpers.merge_model_file(mod, remove=True)
    type_classifier = TextCNNModel.restore(
        mod, vocab, sequence_length=32, num_classes=14, vocab_size=44345)
    type_classifier.labels = ["bombings", "collapse", "crash", "derailment", "earthquake",
                              "explosion", "fire", "floods", "haze", "meteorite",
                              "none", "shootings", "typhoon", "wildfire"]

    # Create related event type model:
    mod = "models/event-related/model.ckpt"
    vocab = "models/event-related/vocabulary.voc"
    data_helpers.merge_model_file(mod, remove=True)
    related_classifier = TextCNNModel.restore(
        mod, vocab, sequence_length=43, num_classes=2, vocab_size=87420)
    related_classifier.labels = ["non-related", "related"]

    # Create related info type model:
    mod = "models/info-types/model.ckpt"
    vocab = "models/info-types/vocabulary.voc"
    data_helpers.merge_model_file(mod, remove=True)
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

    parser.add_option('-d', '--debug', action="store_true", dest='debug', default=False,
                      help="show debugging information")

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

        post_arguments = reqparse.RequestParser()
        post_arguments.add_argument(
            'texts', required=True, type=list, location='json', help="The JSON array containning the strings to be analysed.")

        # Output arguments:
        model2_inner = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
        })
        model2 = api.model('Categories', {
            'labels': fields.List(fields.Nested(model2_inner)),
            'classifier': fields.String,
            'version': fields.Float
        })


        @api.doc(id='textEventType')
        @api.expect(post_arguments, validate=False)
        @api.marshal_with(model2, description='Event Type')
        def post(self):
            """Identifies the type of events associated with multiple posts."""
            data = request.get_json()

            resp = []
            for text in data:
                results = type_classifier.predict(text) 
                resp.append({'input': text, 'label': results})
            
            return {'labels': resp, 'classifier': "CNN", 'version': 0.3}

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


        post_arguments = reqparse.RequestParser()
        post_arguments.add_argument(
            'texts', required=True, type=list, location='json', help="The JSON array containning the strings to be analysed.")

        # Output arguments:
        model2_inner = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
        })
        model2 = api.model('Categories', {
            'labels': fields.List(fields.Nested(model2_inner)),
            'classifier': fields.String,
            'version': fields.Float
        })


        @api.doc(id='textInfoType')
        @api.expect(post_arguments, validate=False)
        @api.marshal_with(model2, description='Info Type')
        def post(self):
            """Identifies the type of information associated with multiple posts'"""
            data = request.get_json()

            resp = []
            for text in data:
                results = info_classifier.predict(text) 
                resp.append({'input': text, 'label': results})
            
            return {'labels': resp, 'classifier': "CNN", 'version': 0.3}

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

        post_arguments = reqparse.RequestParser()
        post_arguments.add_argument(
            'texts', required=True, type=list, location='json', help="The JSON array containning the strings to be analysed.")

        # Output arguments:
        model2_inner = api.model('Category', {
            'input': fields.String,
            'label': fields.String,
        })
        model2 = api.model('Categories', {
            'labels': fields.List(fields.Nested(model2_inner)),
            'classifier': fields.String,
            'version': fields.Float
        })


        @api.doc(id='textEventRelated')
        @api.expect(post_arguments, validate=False)
        @api.marshal_with(model2, description='Event relations')
        def post(self):
            """Identifies if multiple posts are talking about an event."""
            data = request.get_json()

            resp = []
            for text in data:
                results = related_classifier.predict(text) 
                resp.append({'input': text, 'label': results})
            
            return {'labels': resp, 'classifier': "CNN", 'version': 0.3}


    # Start App:
    app.run(host='0.0.0.0', port=options.port, debug=options.debug)


if __name__ == "__main__":
    main(sys.argv)
