# -*- coding: utf-8 -*-
import math
from Sample import Samples
from Node import Node, NodeType
from queue import *


class DecisionTree(object):
    def __init__(self, all_sample):
        self.root = Node(data_set=all_sample.data, attributes=all_sample.attributes, type_node=NodeType.root_node)

    def train(self, tree_node=None):
        """
        构建决策树
        :param tree_node: 一个节点，基于Node
        :return: 分支结束的节点
        """
        # 如果还没有建树，则建立一颗树
        if tree_node is None:
            tree_node = self.root
        # 如果数据集为空，返回一个只有单个节点(Failure)的决策树
        if tree_node.data_set is None:
            tree_node.type_node = NodeType.leaf_node
            tree_node.set_category("failure to construct the tree")
            return
        # 如果类别都相同，返回一个带有该值的节点
        elif len(tree_node.labels) <= 1:
            tree_node.type_node = NodeType.leaf_node
            tree_node.set_category(tree_node.labels[0])
            return
        # 如果属性集合为空，返回一个单节点，其值为出现频率最高的类别属性值
        elif not tree_node.attributes:
            decision_label = self.find_majority(tree_node.data_set, tree_node.labels)
            tree_node.type_node = NodeType.leaf_node
            tree_node.set_category(decision_label)
            return
        else:
            tree_node.type_node = NodeType.internal_node
            # 选择当前节点中最优的划分属性
            best_attr = self.find_best_attr(tree_node)
            tree_node.split_condition['attr'] = best_attr
            # 对已经选定的最优划分属性的所有可能取值分裂子节点
            values_best_attr = list(set(tree_node.data_set[best_attr]))
            for value in values_best_attr:
                # 创建新的子节点
                examples = tree_node.data_set[tree_node.data_set[best_attr] == value]
                temp_attr = tree_node.attributes[:]
                temp_node = Node(data_set=examples, attributes=temp_attr, parent=tree_node)
                temp_node.attributes.remove(best_attr)
                temp_node.split_condition['value'] = value

                tree_node.children[value] = temp_node
                # 递归建立新的节点
                self.train(temp_node)
                # del temp_node
            return

    @staticmethod
    def find_majority(temp_data_set, label):
        """
        找出当前节点中所属类别最多的标签
        :param temp_data_set: 当前节点的样本
        :param label: 所有类别标签可能的取值
        :return: 出现次数做多的类别
        """
        targets = temp_data_set[:, -1]
        frequency = {}
        for each in label:
            frequency[each] = 0
        for each in targets:
            frequency[each] += 1
        return max(frequency, key=frequency.get)

    def find_best_attr(self, tree_node):
        """
        找到当前节点的最优分支属性
        :param tree_node:
        :return:
        """
        best_attr = tree_node.attributes[0]
        max_gain = 0
        entropy = self.entropy(tree_node.data_set, tree_node.labels)
        for attr in tree_node.attributes:
            new_gain = self.gain(tree_node, attr, entropy)
            if new_gain > max_gain:
                max_gain = new_gain
                best_attr = attr
        return best_attr

    @staticmethod
    def entropy(data_set, label):
        """
        计算一个样本空间的熵
        :param data_set: 样本集合
        :param label: 类别标签
        :return:
        """
        frequency = {}
        for each_label in label:
            frequency[each_label] = 0
        targets = data_set.iloc[:, -1]
        for each_label in targets:
            frequency[each_label] += 1
        entropy = 0.0
        for freq in frequency.values():
            prob = freq/targets.size
            entropy += (-prob) * math.log2(prob)
        return entropy

    def gain(self, node, attr, entropy):
        """
        计算某属性在当前节点内的增益
        :param node: 当前节点
        :param attr: 某属性
        :param entropy: 当前节点的熵
        :return: 增益
        """
        frequency = {}
        subset_entropy = 0.0
        num_all_sample_in_node = len(node.data_set)
        # 当前属性所有可能的取值
        all_values_attr = list(set(node.data_set[attr]))
        # 每个取值生成的子集合
        for value in all_values_attr:
            examples = node.data_set[node.data_set[attr] == value]
            new_label = list(set(examples.values[:, -1]))
            a = len(examples)
            temp = self.entropy(examples, new_label)
            subset_entropy += (len(examples)/num_all_sample_in_node) * self.entropy(examples, new_label)
        return entropy - subset_entropy

    def traverse(self):
        """
        广度遍历建立的决策树，输出每个节点和相关信息
        :return:
        """
        print("***************广度遍历******************\n")
        if self.root is None:
            return None
        index_node = 1
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            print("\n-----------------第" + str(index_node) + "个节点------------------\n")
            node = queue.get()
            self.print_info(node)
            for key, child in node.children.items():
                if child is not None:
                    queue.put(child)
            index_node += 1
        return

    @staticmethod
    def print_info(node):
        if node.type_node != NodeType.leaf_node:
            if node.split_condition['value'] is not None:
                print("上一节点的分支属性为:" + node.parent.split_condition['attr'])
                print("本节点属性值为:" + node.split_condition['value'])
            print("\n内部节点分支属性为：" + node.split_condition["attr"])

        else:
            if node.split_condition['value'] is not None:
                print("上一节点的分支属性为:" + node.parent.split_condition['attr'])
                print("本节点属性值为:" + node.split_condition['value'])
            print("\n叶子节点的类别:" + node.category)


if __name__ == "__main__":
    print("\n##############第一棵树###############\n")
    samples = Samples("samples.csv")
    tree = DecisionTree(samples)
    tree.train()
    tree.traverse()
    print("\n##############第二棵树###############\n")
    samples_2 = Samples("samples_2.csv")
    tree_2 = DecisionTree(samples_2)
    tree_2.train()
    tree_2.traverse()
    del tree, tree_2
