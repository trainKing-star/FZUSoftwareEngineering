from words_search import IndexSearch
from data_preprocess import *
import sys
import os
import psutil
mem = psutil.virtual_memory()

'''
 数据加载和数据处理，包括读入数据，预处理数据，写入数据
 
 :param input_file:输入数据文件路径
 :param keyword_file:关键词文件路径
 :param output_file:输出文件路径
'''
def data_load_process(input_file, keyword_file, output_file):
    # 加载输入和关键词文件
    with open(keyword_file, "r", encoding="utf8") as f:
        keyword_list = f.read().splitlines()
    with open(input_file, "r", encoding="utf8") as f:
        text_list = f.read().splitlines()
    # 扩展关键词
    new_keywords, keywords_dict = expand_keywords(keyword_list)
    # 初始化搜索类
    search = IndexSearch()
    search.SetKeywords(new_keywords)
    # 初始化总数
    total = 0
    # 初始化处理结束的信息列表
    message_line_list = []
    for index, text in enumerate(text_list):
        # 行为空则跳过循环
        if not text:
            continue
        # 处理输入文本行
        new_text, origin_index = characters_preprocess(text, keyword_list)
        # 搜索文本
        message_list = search.FindAll(new_text)
        # 返回处理后的搜索信息
        target_message = search_message_from_origin_text(text, new_text, message_list, origin_index, keywords_dict)
        # 没有搜索信息则跳过循环
        if not target_message:
            continue
        # 总数自增
        total += len(target_message)
        # 信息格式处理
        for t_message in target_message:
            message = "Line{}: <{}> {}\n".format(index + 1, t_message["Keyword"], t_message["Search"])
            message_line_list.append(message)
    # 插入总数信息
    message_line_list.insert(0, "Total: {}\n".format(total))
    # 写入文件
    output = open(output_file, "w", encoding="utf8")
    output.writelines(message_line_list)
    print("结束")

    # print('A：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    # print('B：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


if __name__ == "__main__":
    data_load_process("text/org.txt", "text/words.txt", "text/ans.txt")