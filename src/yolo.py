from darkflow.net.build import TFNet
import cv2


class YOLO(object):

    def __init__(self, config_file, weight_file, threshold=0.5):
        options = {"model": config_file,
                   "load": weight_file, "threshold": threshold}
        self.tfnet = TFNet(options)
        self.colors = self.tfnet.meta['colors']
        self.labels = self.tfnet.meta['labels']

    def draw_bbox(self, img, bboxes):
        for box in bboxes:
            label = box['label']
            topleft = box['topleft']
            bottomright = box['bottomright']
            color = self.colors[self.labels.index(label)]
            cv2.putText(img, label, (topleft['x'], topleft['y']),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)
            cv2.rectangle(img, (topleft['x'], topleft['y']),
                          (bottomright['x'], bottomright['y']), color, 2)

        return img

    def detect(self, img):
        bboxes = self.tfnet.return_predict(img)
        draw_img = self.draw_bbox(img, bboxes)

        return bboxes, draw_img


if __name__ == '__main__':
    config_file = './pytorch-yolo2/cfg/tiny-yolo-voc.cfg'
    weight_file = 'weights/tiny-yolo-voc.weights'
    img_file = './pytorch-yolo2/data/dog.jpg'
    yolo = YOLO(config_file, weight_file)

    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(img.shape)
    # print(img)
    bboxes, draw_img = yolo.detect(img)
    print(bboxes)
    print(draw_img)
