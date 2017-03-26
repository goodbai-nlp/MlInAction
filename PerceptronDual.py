#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: PerceptronDual.py
@time: 17-3-26 下午4:57
"""
import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

training_set = np.array([[[3, 3], 1], [[4, 3], 1], [[1, 1], -1], [[5, 2], -1]])

n = np.zeros(len(training_set), np.float)
eta = 1.0       #学习率
b = 0.0
Gram = None
y = np.array(training_set[:, 1])
x = np.empty((len(training_set), 2), np.float)
for i in range(len(training_set)):
    x[i] = training_set[i][0]

history = []   #存放记录
def cal_gram():
    """
    calculate the Gram matrix
    :return:
    """
    g = np.empty((len(training_set), len(training_set)), np.int)
    for i in range(len(training_set)):
        for j in range(len(training_set)):
            g[i][j] = np.dot(training_set[i][0], training_set[j][0])
    return g

def update(i,eta):
    '''
    更新操作
    :param i:第i个对象 
    '''
    global n, b
    n[i] += 1
    a = eta*n           # a = n*eta
    b = np.dot(a,y)     # b = a*y
    history.append([np.dot(a * y, x), b])   # w = a*y*x
def calc(i):
    '''
    计算y*(w*x+b)是否<=0
    :param i: 
    '''
    global b, n, x, y
    a = eta*n
    res = np.dot(a * y, Gram[i])
    res = (res + b) * y[i]
    return res
def Judge():
    global b, n, x, y
    flag = False
    for i in range(len(training_set)):
        if calc(i)<=0:
            flag=True
            update(i,eta)
    if not flag:
        a = eta*n
        w = np.dot(a * y, x)
        b = np.dot(a,y)
        print "Result: w = "+str(w)+" b = "+str(b)
    return flag

if __name__ == "__main__":
    Gram = cal_gram()
    for i in range(1000):
        if not Judge(): break
    global line,label
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
        global history, ax, line, label

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
    anim.save('perceptron2.gif', fps=2, writer='imagemagick')