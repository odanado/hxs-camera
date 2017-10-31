#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.ioloop import PeriodicCallback


import os
import base64
from PIL import Image
import cv2


try:
    import cStringIO as io
except ImportError:
    import io

from yolo import YOLO

ROOT = os.path.join(os.path.normpath(os.path.dirname(__file__)), 'client')
camera = cv2.VideoCapture(1)
config_file = './pytorch-yolo2/cfg/tiny-yolo-voc.cfg'
weight_file = 'weights/tiny-yolo-voc.weights'
yolo = YOLO(config_file, weight_file)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('../client/index.html', port=8080)


class WebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        print('message: ' + message)
        self.camera_loop = PeriodicCallback(self.loop, 10)
        self.camera_loop.start()

    def loop(self):
        """Sends camera images in an infinite loop."""
        sio = io.StringIO()

        _, frame = camera.read()
        if frame is None:
            return

        width, height, _ = frame.shape

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, draw_frame = yolo.detect(frame)
        draw_frame = cv2.resize(draw_frame, (height, width))

        img = Image.fromarray(draw_frame)
        img.save(sio, "JPEG")

        try:
            self.write_message(base64.b64encode(sio.getvalue()))
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocket),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'client'})
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
