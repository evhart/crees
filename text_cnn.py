import numpy as np
import tensorflow as tf
from tensorflow.contrib import learn

from data_helpers import clean_str


class TextCNNModel(object):
    """
    A CNN for multiclass text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    Code based on https://github.com/dennybritz/cnn-text-classification-tf
    Please cite http://oro.open.ac.uk/49639/
    """

    def __init__(self, sequence_length, num_classes, vocab_size,
                 embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0,
                 sess=None, vocab=None, labels=None):

        # Define session context (not needed when trainning the model so the defaults should be fine)
        self.sess = sess if sess is not None else tf.Session()
        sess.vocab = vocab
        self.vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
            vocab) if vocab is not None else None

        self.labels = labels
        if not self.labels or self.labels is None:  # Generate labels if no labels are supplied
            self.labels = list(range(0, num_classes))

        # Define model
        self.__build_cnn(sequence_length, num_classes, vocab_size,
                         embedding_size, filter_sizes, num_filters, l2_reg_lambda)

    @classmethod
    def restore(cls, model_ckpt, vocab, sequence_length, num_classes, vocab_size,
                embedding_size=300, filter_sizes=[3, 4, 5], num_filters=128,
                labels=[], l2_reg_lambda=0.0):

        g = tf.Graph()
        with g.as_default():
            model = cls(sequence_length=sequence_length,
                        num_classes=num_classes,
                        vocab_size=vocab_size,
                        embedding_size=embedding_size,
                        filter_sizes=filter_sizes,
                        num_filters=num_filters,
                        l2_reg_lambda=l2_reg_lambda,
                        sess=tf.Session(),
                        vocab=vocab,
                        labels=labels)

            tf.global_variables_initializer()
            saver = tf.train.Saver()
            saver.restore(model.sess, model_ckpt)

        return model

    def __build_cnn(self, sequence_length, num_classes, vocab_size,
                    embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):

        # Placeholders for input, output and dropout
        self.input_x = tf.placeholder(
            tf.int32, [None, sequence_length], name="input_x")
        self.input_y = tf.placeholder(
            tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(
            tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            self.W = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W")
            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)
            self.embedded_chars_expanded = tf.expand_dims(
                self.embedded_chars, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):

                # Convolution Layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(
                    filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(
                    0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                    self.embedded_chars_expanded,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")

                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")

                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(3, pooled_outputs)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

        # Add dropout
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(
                self.h_pool_flat, self.dropout_keep_prob)

        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # Calculate Mean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(
                self.scores, self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

    def predict(self, text):
        text = clean_str(text)
        x = list(self.vocab_processor.transform([text]))

        feed_dict = {
            self.input_x: x,
            self.input_y: [[0] * len(self.labels)],
            self.dropout_keep_prob: 1.0
        }
        classification = self.labels[self.sess.run(
            self.predictions, feed_dict)[0]]
        return classification
