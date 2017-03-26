#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: Perceptron.py
@time: 17-3-26 下午2:51
"""
import copy
from matplotlib import pyplot as plt
from matplotlib import animation

training_set = [[(3, 3), 1], [(4, 3), 1], [(1, 1), -1]]
w = [0, 0]
b = 0
eta = 1.0       #学习率
history = []   #存放记录

def update(item,eta):
    '''
    随机梯度下降法更新参数w(t+1)=w(t)+ eta*item[1]*item[0];b(t+1) = b(t)+ eta*item[1]
    :param item: item的结构[(3, 3), 1],第一个元组是x,第二个是分类
    :param eta: 学习率
    :return: NULL
    '''
    global w,b,history
    for i in range(len(w)):
        w[i]+=eta*item[1]*item[0][i]
    b += eta * item[1]
    print w, b
    history.append([copy.copy(w), b])

def calc(item):
    '''
    计算 (w*x+b)*y
    :param item: item的结构[(3, 3), 1],第一个元组是x,第二个是分类 
    :return: (w*x+b)*y
    '''
    res =0
    for i in range(len(item[0])):
        res+=w[i]*item[0][i]
    res+=b
    res*=item[1]
    return res


def Judge():
    flag = False
    for item in training_set:
        if calc(item) <= 0:
            flag = True
            update(item,eta)
    if not flag:
        print "Result: w = "+str(w)+" b = "+str(b)
    return flag


def draw():
    '''
    画出感知器参数调整的过程图
    :return: 
    '''
    # 初始化
    global line,label
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
    line, = ax.plot([], [], 'g', lw=2)
    label = ax.text([], [], '')

    def init():
        line.set_data([], [])   #感知机超平面，这里是直线
        x, y, x_, y_ = [], [], [], []   #两类点
        for p in training_set:
            if p[1] > 0:
                x.append(p[0][0])
                y.append(p[0][1])
            else:
                x_.append(p[0][0])
                y_.append(p[0][1])

        plt.plot(x, y, 'bo', x_, y_, 'rx')  #画点
        plt.axis([-6, 6, -6, 6])    #数轴
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Perceptron Algorithm')
        return line, label

    def animate(i):
        '''
        每一帧的画面
        :param i: 帧号
        '''
        global history, ax, line, label

        w = history[i][0]
        b = history[i][1]
        if w[1] == 0: return line, label
        # 画线的两个端点
        x1 = -7
        y1 = -(b + w[0] * x1) / w[1]
        x2 = 7
        y2 = -(b + w[0] * x2) / w[1]
        line.set_data([x1, x2], [y1, y2])
        # label的坐标
        x1 = 0
        y1 = -(b + w[0] * x1) / w[1]
        label.set_text(history[i])
        label.set_position([x1, y1])
        return line, label

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(history), interval=1000, repeat=True,
                                   blit=True)
    plt.show()
    anim.save('perceptron.gif', fps=2, writer='imagemagick')
if __name__ == "__main__":
    for i in range(1000):
        if not Judge(): break
    draw()