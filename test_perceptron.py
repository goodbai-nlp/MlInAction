#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: test_perceptron.py
@time: 17-4-8 下午5:25
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from Perceptron import Perceptron
from Perceptron import DualPerceptron


def showPic(history):

    fig = plt.figure()
    ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
    line, = ax.plot([], [], 'g', lw=2)
    label = ax.text([], [], '')

    def init():
        line.set_data([], [])
        x, y, x_, y_ = [], [], [], []
        for p in training_set:
            if p[1] > 0:
                x.append(p[0][0])
                y.append(p[0][1])
            else:
                x_.append(p[0][0])
                y_.append(p[0][1])

        plt.plot(x, y, 'bo', x_, y_, 'rx')
        plt.axis([-6, 6, -6, 6])
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Perceptron Algorithm 2')
        return line, label


    def animate(i):

        w = history[i][0]
        b = history[i][1]
        if w[1] == 0: return line, label
        x1 = -7.0
        y1 = -(b + w[0] * x1) / w[1]
        x2 = 7.0
        y2 = -(b + w[0] * x2) / w[1]
        line.set_data([x1, x2], [y1, y2])
        x1 = 0.0
        y1 = -(b + w[0] * x1) / w[1]
        label.set_text(str(history[i][0]) + ' ' + str(b))
        label.set_position([x1, y1])
        return line, label


    # call the animator.  blit=true means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(history), interval=1000, repeat=True,
                                   blit=True)
    plt.show()
    anim.save('perceptron.gif', fps=2, writer='imagemagick')

if __name__ == "__main__":
    print "test Normal Perceptron\n"
    training_set = np.array([[[3, 3], 1], [[4, 3], 1], [[1, 1], -1], [[5, 2], -1]])
    per1 = Perceptron(1.0)
    w,b,history=per1.train(training_set)
    showPic(history)
    print "test DualPerceptron\n"
    training_set = np.array(([[[3, 3], 1], [[4, 3], 1], [[1, 1], -1]]))
    per2 = DualPerceptron(1.0)
    w2,b2,history2 = per2.train(training_set)
    showPic(history2)