# coding=UTF-8
import random
import math
from utils import *

S = list()  # 非终止状态
S2 = list()  # 所有状态
SS = list()  # 系统状态
SE = list()  # 环境状态
SV = dict()  # 状态自身附带的价值
A = list()  # 动作列表
AToS = dict()  # 每个状态下可供选择的动作

# 这两个字典是有特殊方法的，因为获取值时比较特殊，需要(状态1，动作，状态2)和(状态，动作)作为键对应
P = dict()  # 状态转移概率（每个状态下，执行相应的动作后，可能到达的后继状态对应的概率）
R = dict()  # s,a对应的奖励r

Result_Dict = dict()  # 保存结果的字典

Threshold = 0.01  # 阈值


class CalculateValue():
    def __init__(self, Document, Document2):
        self.Document = Document
        self.Document2 = Document2

    def initialize(self):
        with open(self.Document) as file:
            for line in file:
                line = line.split()
                # 这里要注意，mdp文件千万不能有空白行，如果有的话，print会打印出[]，并且下面会出现index out of range错误
                print("line:", line)
                # 设置状态转移字典P
                set_prob(P, line[0], line[1], line[2], float(line[3]))
                # 设置奖励字典R
                set_reward(R, line[0], line[1], float(line[4]))
                # 设置列表S
                if (line[0] not in S):
                    S.append(line[0])
                S.sort()
                # 设置列表S2
                if (line[0] not in S2):
                    S2.append(line[0])
                if (line[2] not in S2):
                    S2.append(line[2])
                S2.sort()
                # 设置列表A
                if (line[1] not in A):
                    A.append(line[1])
            # 设置列表SS和列表SE
            for i in range(len(S2)):
                if (i % 2 == 0):
                    SE.append(S2[i])
                else:
                    SS.append(S2[i])
        # 设置字典SV
        with open(self.Document2) as file:
            for line in file:
                line = line.split()
                SV[line[0]] = line[1]

        self.set_atos_dict()

        # 打印
        print()
        print("非终止状态：", S)
        print("所有状态：", S2)
        print("系统状态：", SS)
        print("环境状态：", SE)
        print("所有动作：", A)
        print()
        print("状态自身附带的价值:")
        print(SV.items())
        print("每个状态下可供选择的动作:")
        print(AToS.items())
        print("状态转移概率字典：")
        display_dict(P)
        print("奖励字典：")
        display_dict(R)

    # 该函数用于设置字典AToS
    def set_atos_dict(self):
        for i in range(len(S)):
            AToS.setdefault(S[i])

        for i in AToS.keys():
            AToS[i] = []

        with open(self.Document) as file:
            for line in file:
                line = line.split()
                if (line[1] not in AToS[line[0]]):
                    AToS[line[0]].append(line[1])

    # 计算状态价值
    def computer_v(self, s):
        if (s in S2 and s not in S):
            return 0
        action_list = AToS[s]
        action_value = dict()
        for i in range(len(action_list)):
            action_value[action_list[i]] = self.computer_q(s, action_list[i])
        # 奇数，系统状态，取大
        if (s in SS):
            v_s = float(SV[s]) + max(action_value.values())
        # 偶数，环境状态，取小
        elif (s in SE):
            v_s = float(SV[s]) + min(action_value.values())
        return v_s

    # 计算状态-动作价值
    def computer_q(self, s, a):
        q = get_reward(R, s, a)
        for i in range(len(S2)):
            prob = get_prob(P, s, a, S2[i])
            if (prob != 0):
                q += prob * Result_Dict[S2[i]]
        return q

    def result(self):
        # 先初始化为0
        for i in range(len(S2)):
            Result_Dict[S2[i]] = 0
        # 设置迭代轮数
        for i in range(5):
            # result_help用于暂存状态价值，但是先不覆盖Result_Dict中的值
            result_help = list()
            for j in range(len(S2)):
                result_help.append(cv.computer_v(S2[j]))
            for k in range(len(result_help)):
                Result_Dict[S2[k]] = result_help[k]
        print(Result_Dict.items())

    def result2(self):
        for i in range(len(S2)):
            Result_Dict[S2[i]] = 0
        episode = 0  # 记录迭代轮数
        while (True):
            result_help = list()
            flag = True
            for j in range(len(S2)):
                result_help.append(cv.computer_v(S2[j]))
                if (abs(result_help[j] - Result_Dict[S2[j]]) > Threshold):
                    flag = False
            if (flag == True):
                break
            for k in range(len(result_help)):
                Result_Dict[S2[k]] = result_help[k]
            episode += 1
        print("迭代了%d轮后收敛" % episode)
        print(Result_Dict.items())


if __name__ == "__main__":
    cv = CalculateValue("mdp", "mdp_value")
    cv.initialize()
    cv.result2()
