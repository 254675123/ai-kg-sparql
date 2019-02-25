#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from  parse.regulation.syntacticNode import *
from  parse.dict.lexicon import *
from  parse.nlentity import *
class StatementStructure:
    "descrip the nl structure after parse"

    def __init__(self):
        # 输入的自然语言串
        self.input_origin = None
        # 对自然语言的原始分段
        # 每个node的类型有：标点符号，虚词，图谱词类，未知分类
        self.segments_full = []

        # 去掉标点符号和虚词的分类
        self.segments_imp = []

        # 仅保留图谱词类
        self.segments_graph = []

        # 对self.segments_graph处理结果
        self.segments_standard = []

        # 对自然语言处理结果
        self.result = None

        # 对自然语言处理结果的评价
        self.result_desc = None



class StatementSegment:
    "对语句分词"

    # 反向最大匹配算法
    def reverseMaxSegmentation(self):

        if self.input_origin is None:
            return
        ""
        # 获取词典
        lex = Lexicon()
        lex_common = lex.lex_common
        lex_sign = lex.lex_sign
        lex_graph = lex.lex_graph

        # 获取输入的字符串
        statement = self.input_origin
        # 未知分词
        unknown_segment = []
        # 先计算输入串的长度
        stat_length = len(statement)
        while stat_length > 0:
            # 切词成功标记
            cut_flag = False
            for i in range(stat_length):
                candidate_word = statement[i:]

                # 逐个词典查看是否有该候选词
                # 先看图谱中是否有该词
                if (candidate_word in lex_graph) or (candidate_word in lex_common):
                    # 如果未知词列表中有词，则标记为未知词
                    length = len(unknown_segment)
                    if length > 0:
                        unknown_word = ""
                        for x in range(length)[::-1]:
                            unknown_word += x
                        n_entity = NLEntity()
                        n_entity.setValue(unknown_word, unknown_word)
                        self.segments_full.append(n_entity)
                        unknown_segment.clear()

                    # 将当前分词，加入到分词结果列表中
                    standard_val = lex_graph.get(candidate_word)
                    n_entity = NLEntity()
                    n_entity.setValue(candidate_word, standard_val)
                    self.segments_full.append(n_entity)

                    # 裁掉当前词
                    statement = statement[:i]
                    stat_length = len(statement)
                    cut_flag = True

                    break
                else:
                    i += 1

            # 如果循环一遍，没有找到合适的词
            if cut_flag == False:
                last_word = statement[stat_length - 1:]
                unknown_segment.append(last_word)

                # 去掉最后一个词
                statement = statement[:stat_length - 1]
                stat_length = len(statement)
