#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: Perceptron.py
@time: 17-4-8 下午4:21
"""
import copy
import numpy as np

class BasePerceptron(object):
    '''Class BasePerceptron'''
    def __init__(self,learnRate):
        '''
        :param learnRate: 学习率
        :param Dual: 是否使用对偶形式
        '''
        self.learnRate = learnRate
        self.History=[]

class Perceptron(BasePerceptron):
    '''An implementation of Perceptron
    Attributes:
        trainData: 训练数据
        learnRate: 感知器学习率
    Results:
        w:超平面参数w
        b:超平面截距b
        History: 超平面变动过程记录
    '''
    def train(self,trainData):
        self.Data = trainData
        self.y = np.array(trainData[:, 1])
        self.x = np.empty((len(trainData), 2), np.float)
        for i in range(len(trainData)):
            self.x[i] = trainData[i][0]
        self.w = np.zeros(len(self.x[0]), np.float)
        self.b = 0.0
        for i in range(1000):
            if not self.Judge():
                # print "Can't find a result within 1000 iterations!\n"
                break
        return self.w,self.b,self.History

    def Judge(self):
        flag = False
        for i in range(len(self.Data)):
            if self.calc(i) <= 0:
                flag = True
                self.update(i)
        if not flag:
            print "Result: w = " + str(self.w) + " b = " + str(self.b)
        return flag

    def calc(self,i):
        '''
        计算 (w*x+b)*y
        :param i 第i组元素
        :return: (w*x+b)*y
        '''
        res = np.dot(self.w,self.x[i])
        res += self.b
        res *= self.y[i]
        return res
    def update(self,i):
        '''
        更新超平面
        w = w + eta*x[i]*y[i]
        b = b+ eta*y[i]
        :param i: 第i组元素
        '''
        self.w += self.learnRate * self.y[i]*self.x[i]
        self.b += self.learnRate * self.y[i]
        self.History.append([copy.copy(self.w), self.b])

class DualPerceptron(BasePerceptron):
    '''An implementation of Dual Perceptron 
    Attributes:
        trainData: 训练数据
        learnRate: 感知器学习率
    Results:
        w:超平面参数w
        b:超平面截距b
        History: 超平面变动过程记录
    '''
    def train(self,trainData):
        self.Data = trainData
        self.y = np.array(trainData[:, 1])
        self.x = np.empty((len(trainData), 2), np.float)
        for i in range(len(trainData)):
            self.x[i] = trainData[i][0]
        self.n = np.zeros(len(trainData), np.float)
        self.b = 0.0
        self.Gram = self.calGram(self.Data)
        for i in range(1000):
            if not self.Judge():
                # print "Can't find a result within 1000 iterations!\n"
                break
        a = self.learnRate * self.n
        w = np.dot(a * self.y, self.x)
        return w,self.b,self.History

    def calGram(self,data):
        """
            calculate the Gram matrix
            :return:
            """
        g = np.empty((len(data), len(data)), np.float)
        for i in range(len(data)):
            for j in range(len(data)):
                g[i][j] = np.dot(data[i][0], data[j][0])
        return g

    def Judge(self):
        '''
        判断是否存在误分类的点
        :return: boolean 
        '''
        flag = False
        for i in range(len(self.Data)):
            if self.calc(i) <= 0:
                flag = True
                self.update(i)
        if not flag:
            a = self.learnRate * self.n
            w = np.dot(a * self.y, self.x)
            b = np.dot(a, self.y)
            print "Result: w = " + str(w) + " b = " + str(b)
        return flag
    def calc(self,i):
        '''
            计算y*(w*x+b)是否<=0
            :param i: 
            '''
        a = self.learnRate * self.n
        res = np.dot(a * self.y, self.Gram[i])
        res = (res + self.b) * self.y[i]
        return res

    def update(self,i):
        '''
        更新操作
        如果误分类，则该项的累加次数+1
        :param i:第i个对象 
        '''
        global n, b
        self.n[i] += 1
        a = self.learnRate * self.n  # a = n*eta
        self.b = np.dot(a, self.y)  # b = a*y
        self.History.append([np.dot(a * self.y, self.x), self.b])  # w = a*y*x