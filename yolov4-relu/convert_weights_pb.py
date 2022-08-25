# -*- coding: utf-8 -*-

import tensorflow as tf
import yolo_v4
import yolo_v4_tiny

from utils import load_weights, load_coco_names, detections_boxes, freeze_graph

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
    'class_names', 'coco.names', 'File with class names')
tf.app.flags.DEFINE_string(
    'weights_file', 'yolov4.weights', 'Binary file with detector weights')
tf.app.flags.DEFINE_string(
    'data_format', 'NCHW', 'Data format: NCHW (gpu only) / NHWC')
tf.app.flags.DEFINE_string(
    'output_graph', 'frozen_darknet_yolov4_model.pb', 'Frozen tensorflow protobuf model output path')

tf.app.flags.DEFINE_bool(
    'tiny', False, 'Use tiny version of YOLOv4')
tf.app.flags.DEFINE_integer(
    'height', 480, 'Image height')
tf.app.flags.DEFINE_integer(
    'width', 640, 'Image width')



def main(argv=None):
    if FLAGS.tiny:
        model = yolo_v4_tiny.yolo_v4_tiny
    else:
        model = yolo_v4.yolo_v4

    classes = load_coco_names(FLAGS.class_names)

    # placeholder for detector inputs
    inputs = tf.placeholder(tf.float32, [None, FLAGS.height, FLAGS.width, 3], "inputs")

    with tf.variable_scope('detector'):
        detections = model(inputs, len(classes), data_format=FLAGS.data_format)
        load_ops = load_weights(tf.global_variables(scope='detector'), FLAGS.weights_file)

    # Sets the output nodes in the current session
    boxes = detections_boxes(detections)

    with tf.Session() as sess:
        sess.run(load_ops)
        freeze_graph(sess, FLAGS.output_graph)

if __name__ == '__main__':
    tf.app.run()
