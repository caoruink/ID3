# -*- coding: utf-8 -*-
from enum import Enum


class Node(object):
    """
    定义节点的相关信息
    """
    def __init__(self,
                 data_set=None,
                 attributes=None,
                 parent=None,
                 type_node=None):
        """
        初始化节点内的税局
        :param data_set: 节点内数据集
        :param attributes: 当前节点内可分支属性
        :param parent: 父节点
        :param type_node: 节点类型
        """
        self.data_set = data_set
        self.attributes = attributes
        self.labels = self.find_labels()
        self.parent = parent
        # 当前节点将产生的子节点
        self.children = {}
        # 当前节点的类型，将用NodeType表示
        self.type_node = type_node
        # 如果是叶子节点，则这个就是该节点所代表的类别
        self.category = None
        # 如果当前节点是内部节点，则有分支条件
        self.split_condition = {"attr": None, "value": None}

    def find_labels(self):
        return list(set(self.data_set.values[:, -1]))

    def set_category(self, category):
        self.category = category


class NodeType(Enum):
    """
    某个节点的类型，分为叶子节点，内部节点，更特殊的是根节点
    """
    leaf_node = 1
    internal_node = 2
    root_node = 3
