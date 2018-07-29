#!/usr/bin/env python3
import svgwrite
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
import numpy as np

app = QApplication(sys.argv)
mainWindow = QMainWindow()
container = QWidget()
layout = QVBoxLayout()
container.setLayout(layout)

svgWidget = QSvgWidget()
svgWidget.setMinimumWidth(320)
svgWidget.setMinimumHeight(320)
layout.addWidget(svgWidget)

slider = QSlider(Qt.Horizontal)
slider.setMinimum(-100)
slider.setMaximum(100)
slider.setValue(10)
slider.valueChanged.connect(lambda x: set('scale', 0.01 * x))
layout.addWidget(QLabel('Scale factor'))
layout.addWidget(slider)

slider2 = QSlider(Qt.Horizontal)
slider2.setMinimum(0)
slider2.setMaximum(100)
slider2.setValue(100)
slider2.valueChanged.connect(lambda x: set('recursive', 0.01 * x))
layout.addWidget(QLabel('Recursive factor'))
layout.addWidget(slider2)

mainWindow.setCentralWidget(container)
mainWindow.show()

scale = recursive = 0

def set(param, val):
    globals()[param] = val
    timer.start(1000//24)

def render():
    global scale
    global recursive
    dwg = svgwrite.Drawing('tmp.svg', size=('15cm', '15cm'), profile='tiny')
    dwg.viewbox(width=1, height=1)
    color = '#000'
    a, b, c, d = (np.array(x, dtype=np.float) for x in ((0, 0), (0, 1), (1, 1), (1, 0)))
    w = scale
    aw = abs(w)
    for i in range(64):
        dwg.add(svgwrite.shapes.Polygon([a, b, c, d], fill=color))
        a1 = (1 - aw) * a + aw * (b if w >= 0 else d)
        b1 = (1 - aw) * b + aw * (c if w >= 0 else a)
        c1 = (1 - aw) * c + aw * (d if w >= 0 else b)
        d1 = (1 - aw) * d + aw * (a if w >= 0 else c)
        a, b, c, d = a1, b1, c1, d1
        color = '#fff' if color == '#000' else '#000'
        aw *= recursive
    dwg.save(pretty=True)
    svgWidget.load('tmp.svg')

timer = QTimer()
timer.setSingleShot(True)
timer.timeout.connect(render)

sys.exit(app.exec_())

