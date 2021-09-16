from words_search import IndexSearch
from data_preprocess import *
import argparse
import psutil

mem = psutil.virtual_memory()

'''
 数据加载和数据处理，包括读入数据，预处理数据，写入数据
 
 :param input_file:输入数据文件路径
 :param keyword_file:关键词文件路径
 :param output_file:输出文件路径
'''


def data_load_process(keyword_file, input_file, output_file):
    # 加载输入和关键词文件
    print("开始加载输入文本和关键词文件, 输入文本路径：{}， 关键词文件路径：{}".format(input_file, keyword_file))
    with open(keyword_file, "r", encoding="utf8") as f:
        keyword_list = f.read().splitlines()
    with open(input_file, "r", encoding="utf8") as f:
        text_list = f.read().splitlines()
    print("完成加载输入文本和关键词文件")
    # 扩展关键词
    print("开始扩展关键词")
    new_keywords, keywords_dict = expand_keywords(keyword_list)
    print("完成扩展关键词")
    # 初始化搜索类
    print("开始初始化搜索类")
    search = IndexSearch()
    search.SetKeywords(new_keywords)
    print("完成初始化搜索类")
    # 初始化总数
    total = 0
    # 初始化处理结束的信息列表
    message_line_list = []
    print("开始处理文本行信息")
    for index, text in enumerate(text_list):
        # 行为空则跳过循环
        if not text:
            continue
        if (index + 1) % 10 == 0:
            print("正在处理第{}行信息".format(index + 1))
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
        if (index + 1) % 10 == 0:
            print("完成处理第{}行信息".format(index + 1))
    # 插入总数信息
    message_line_list.insert(0, "Total: {}\n".format(total))
    # 写入文件
    print("开始写入文件，文件路径：{}".format(output_file))
    output = open(output_file, "w", encoding="utf8")
    output.writelines(message_line_list)
    print("完成写入文件，文件路径：{}".format(output_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword_file_path", help="请填入敏感词文件路径")
    parser.add_argument("input_file_path", help="请填入待检测文件路径")
    parser.add_argument("output_file_path", help="请填入答案文件路径")
    args = parser.parse_args()
    # 执行函数
    data_load_process(args.keyword_file_path, args.input_file_path, args.output_file_path)
