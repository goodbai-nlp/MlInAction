#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: ML_0.py
@time: 17-3-26 上午10:02
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
fig = plt.figure()                      #建立一张图
ax = plt.axes(xlim=(0,2),ylim=(-2,2))   #坐标轴设置
line, = ax.plot([],[],lw=2)             #设置线条（颜色、线型、宽度等）和标记


def init():
    line.set_data([], [])
    return line,


# animation function.  this is called sequentially  #动画函数
def animate(i):                             # i 表示当前帧数
    x = np.linspace(0, 2, 1000)             #0-2间的等差数列，共1000项
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,


# call the animator.  blit=true means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)
if __name__ == "__main__":
    plt.show()
    anim.save('testImage.gif', fps=2, writer='imagemagick')