# -*- coding: utf-8 -*-
import pandas as pd


class Samples(object):
    """
    读入样本文件，划分属性
    """
    def __init__(self, filename):
        """
        读入文件，区分数据（data）和属性（attribute），并统计每个属性可取的值（factor）
        :param filename: 样本文件名，含列名
        """
        self.factors = {}
        self.data = pd.read_csv(filename)
        self.attributes = self.data.columns.values.tolist()[:-1]
        for i in self.attributes:
            self.factors[i] = []
            temp = list(self.data[i].drop_duplicates())
            self.factors[i] = temp
        # self.data = tuple(self.data.values)
        self.category = list(set(self.data.values[:, -1]))


if __name__ == "__main__":
    samples = Samples("samples.csv")
    print(samples.factors)
    print(samples.data[samples.data["Outlook"] == "Sunny"])
