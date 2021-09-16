import re
from simplified_translate import Translate
from pin_yin_translate import Pinyin
import enchant
import itertools

# 加载繁简体转换实例
translate = Translate()
# 加载拼音转换实例
pinyin = Pinyin()

'''
 从原输入文本中搜索查找到的敏感词信息
 
 :param origin_text:原输入文本
 :param new_text:经过处理的新文本
 :param message_list:搜索类实例搜索返回的信息列表
 :param origin_index: 处理后文本对应原输入文本的索引列表
 :param keywords_target:扩充后的关键词对应原输入关键词的字典
 :return target_message:保存搜索的文本对应的关键词
'''


def search_message_from_origin_text(origin_text, new_text, message_list, origin_index, keywords_target):
    # 保存搜索的文本对应的关键词
    target_message = []
    # 索引字典，用于获取到同开始索引但是结束索引更大的值
    index_dict = {}
    for message in message_list:
        # 获取开始索引
        state = message["Start"]
        if state not in index_dict:
            # 开始索引不在字典里就加入
            index_dict[state] = message
        elif index_dict[state]["End"] < message["End"]:
            # 只有新信息的开始索引大于旧信息的开始索引才会覆盖原来的值
            index_dict[state] = message
    # 遍历信息列表
    for k, message in index_dict.items():
        # 获取信息中对应的敏感词
        keyword = message["Keyword"]
        # 获取新文本中消息
        new_word = "".join(new_text[message["Start"]:message["End"] + 1])
        # 原文本中的搜索文本开始索引
        start = origin_index[message["Start"]]
        # 原文本中的搜索文本结束索引
        end = origin_index[message["End"]] + 1
        # 根据索引获取原文本
        target_word = origin_text[start:end]
        # 根据搜索到的文本是英文还是中文，返回不同的结果
        target_word = judge_chinese_english(target_word, new_word)
        # 筛选后没有信息则跳过此次循环
        if target_word is None:
            continue
        # 设置成字典加入保存列表
        target_message.append({"Keyword": keywords_target[keyword], "Search": target_word})
    # 返回对应信息
    return target_message


'''
 根据搜索的文本段是英文还是中文返回不同的信息
 
 :param origin_text:原输入文本搜索后切割出来的文本
 :param target_text:处理后文本搜索后切割出来的文本
'''


def judge_chinese_english(origin_text, target_text):
    judge = enchant.Dict("en_US")
    if judge.check(target_text) is False:
        # 是中文，就判断文本段里是否有数字
        flag = re.search(r'[0-9]', origin_text)
        if flag is None:
            # 没有数字就返回输入西悉尼
            return origin_text
        # 中文中有数字则不是敏感词，返回None
        return None
    # 是英文，直接返回
    return origin_text


'''
 字符预处理函数
 将输入文本中字母转化为小写，删除所有字母、汉字、换行符以外的字符
 将输入文本中与关键词中字谐音的字转化为与该字谐音的关键字
 返回一个处理后的字符列表以及一个字符列表对应原输入文本索引的索引列表
 
 :param text:输入文本
 :param keywords:敏感词列表
 :return new_text:新文本列表
 :return new_text_index:对应原输入文本的索引列表
'''


def characters_preprocess(text, keywords):
    # new_text:处理后将要返回的新输入文本列表
    # new_text_index：处理后新输入文本对应原输入文本的索引列表
    new_text, new_text_index = [], []
    # 输入文本转换成简体
    text = translate.ToSimplifiedChinese(text)
    # 大写字母转换成小写
    text = text.lower()
    # 链接关键词成为文本
    keywords_text = "".join(keywords)
    # 获取关键词文本每个字符的拼音
    keyword_pinyin_list = pinyin.GetPinyinList(keywords_text)
    # 对文本中的每个字符进行过滤
    # 除了字母、数字、汉字、换行符之外全部过滤掉
    for index, word in enumerate(text):
        flag = re.search(r'[^a-z\u4e00-\u9fff]', word)
        if flag is None:
            # 获取输入文本单个字的拼音
            word_pinyin = pinyin.GetPinyinList(word)[0]
            if word_pinyin is not None and word_pinyin in keyword_pinyin_list:
                # 把这个字转化为敏感词中的同拼音的关键字
                word = keywords_text[keyword_pinyin_list.index(word_pinyin)]
            # 如果是字母、数字、汉字、换行符则加入设定的两个列表
            new_text.append(word)
            new_text_index.append(index)
    # 返回新文本列表和对应原输入文本的索引列表
    return new_text, new_text_index


'''
 扩充敏感词
 包括扩充谐音替代、拼音替代、拼音首字母代替

 :param keywords:输入的关键词列表
 :return new_keywords:扩充后的关键词列表
 :return new_keywords_target:扩充后的关键词对应原输入关键词的字典
'''


def expand_keywords(keywords):
    # 关键词转换成简体与输入文本处理统一成简体
    keywords = translate.ToSimplifiedChinese("|".join(keywords)).split("|")
    # 设置一个集合，保证集合中的每个关键词唯一
    new_keywords = set(keywords[:])
    # 扩充后的关键词对应原关键词字典
    new_keywords_target = {}
    # 遍历关键词列表
    for keyword in keywords:
        # 如果扩充对应字典中没有该键值，则键值加入字典
        if keyword not in new_keywords_target:
            new_keywords_target[keyword] = keyword
        # 获取关键词对应的拼音列表
        keyword_pinyin_list = pinyin.GetPinyinList(keyword)
        # 初始化拼音列表对应的索引列表
        index_pinyin_list = list(range(len(keyword_pinyin_list)))
        # 遍历将拼音和关键词字符替换，包括拼音首字母替换、拼音替换、谐音替换
        for i in range(1, len(index_pinyin_list) + 1):
            # 获取长度为i的索引组合
            iter_list = itertools.combinations(index_pinyin_list, i)
            # 迭代索引组合
            for one_iter in iter_list:
                # 设置两个列表，分别用于关键词的拼音替换、拼音首字母替换
                random_pinyin_total = list(keyword)
                random_pinyin_head = list(keyword)
                random_pinyin_pinyin_head = keyword_pinyin_list[:]
                # 遍历替换
                for one in one_iter:
                    # 字符对应的拼音存在则替换
                    if keyword_pinyin_list[one] is not None:
                        # 关键词列表拼音替换字符
                        random_pinyin_total[one] = keyword_pinyin_list[one]
                        # 关键词列表拼音首字母替换字符
                        random_pinyin_head[one] = keyword_pinyin_list[one][0]
                        # 关键词拼音列表首字母替换拼音
                        if None not in random_pinyin_pinyin_head:
                            random_pinyin_pinyin_head[one] = keyword_pinyin_list[one][0]
                # 列表链接成词，字母转小写加入新关键词列表中并对应原关键词
                pinyin_total = "".join(random_pinyin_total).lower()
                pinyin_head = "".join(random_pinyin_head).lower()
                new_keywords.add(pinyin_total)
                new_keywords_target[pinyin_total] = keyword
                new_keywords.add(pinyin_head)
                new_keywords_target[pinyin_head] = keyword
                # 拼音和拼音首字母的组合
                if None not in random_pinyin_pinyin_head:
                    pinyin_pinyin_head = "".join(random_pinyin_pinyin_head).lower()
                    new_keywords.add(pinyin_pinyin_head)
                    new_keywords_target[pinyin_pinyin_head] = keyword
    # 返回关键词列表
    new_keywords = list(new_keywords)
    return new_keywords, new_keywords_target
