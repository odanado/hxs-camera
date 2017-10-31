#!/bin/bash
mkdir -p weights
if [ ! -e weights/tiny-yolo-voc.weights ]; then
    wget https://pjreddie.com/media/files/tiny-yolo-voc.weights -P weights
fi

mkdir -p cfg
if [ ! -e cfg/tiny-yolo-voc.cfg ]; then
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/tiny-yolo-voc.cfg -P cfg
fi

mkdir -p data
if [ ! -e data/dog.jpg ]; then
    wget https://github.com/pjreddie/darknet/raw/master/data/dog.jpg -P data
fi
