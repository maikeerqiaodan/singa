#!/usr/bin/env python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from singa.model import *
from examples.datasets import cifar10

X_train, X_test, workspace = cifar10.load_data()

m = Sequential('cifar10-cnn', sys.argv)

parw = Parameter(init='gaussian', std=0.0001)
parb = Parameter(init='constant')
m.add(Convolution2D(32, 5, 1, 2, w_param=parw, b_param=parb, b_lr=2))
m.add(MaxPooling2D(pool_size=(3,3), stride=2))
m.add(Activation('relu'))
m.add(LRN2D(3, alpha=0.00005, beta=0.75))

parw.update(std=0.01)
m.add(Convolution2D(32, 5, 1, 2, w_param=parw, b_param=parb))
m.add(Activation('relu'))
m.add(AvgPooling2D(pool_size=(3,3), stride=2))
m.add(LRN2D(3, alpha=0.00005, beta=0.75))

m.add(Convolution2D(64, 5, 1, 2, w_param=parw, b_param=parb, b_lr=1))
m.add(Activation('relu'))
m.add(AvgPooling2D(pool_size=(3,3), stride=2))

m.add(Dense(10, w_param=parw, w_wd=250, b_param=parb, b_lr=2, b_wd=0, activation='softmax'))

sgd = SGD(decay=0.004, lr_type='manual', step=(0,60000,65000), step_lr=(0.001,0.0001,0.00001))
topo = Cluster(workspace)
m.compile(loss='categorical_crossentropy', optimizer=sgd, cluster=topo)
m.fit(X_train, nb_epoch=100, with_test=True)
result = m.evaluate(X_test, test_steps=10, test_freq=300)
