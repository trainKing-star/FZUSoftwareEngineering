import re
from simplified_translate import Translate
from pin_yin_translate import Pinyin
import itertools

# 加载繁简体转换实例
translate = Translate()
# 加载拼音转换实例
pinyin = Pinyin()


def search_message_from_origin_text(origin_text, message_list, origin_index):
    for message in message_list:
        print("keywords:", message["Keyword"])
        print(origin_text[origin_index[message["Start"]]:origin_index[message["End"]] + 1])



# 字符预处理函数
# 将输入文本中字母转化为小写，删除所有字母、汉字、换行符以外的字符
# 返回一个处理后的字符列表以及一个字符列表对应原输入文本索引的索引列表
def characters_preprocess(text):
    # new_text:处理后将要返回的新输入文本列表
    # new_text_index：处理后新输入文本对应原输入文本的索引列表
    new_text, new_text_index = [], []
    # 输入文本转换成简体
    text = translate.ToSimplifiedChinese(text)
    # 大写字母转换成小写
    text = text.lower()
    # 对文本中的每个字符进行过滤
    # 除了字母、数字、汉字、换行符之外全部过滤掉
    for index, word in enumerate(text):
        flag = re.search(r'[^a-z0-9\u4e00-\u9fff\n]', word)
        if flag is None:
            # 如果是字母、数字、汉字、换行符则加入设定的两个列表
            new_text.append(word)
            new_text_index.append(index)
    # 返回新文本列表和对应原输入文本的索引列表
    return new_text, new_text_index


# 扩充敏感词
# 包括扩充谐音替代、拼音替代、拼音首字母代替
def expand_keywords(keywords):
    # 关键词转换成简体与输入文本处理统一成简体
    keywords = translate.ToSimplifiedChinese("|".join(keywords)).split("|")
    # 设置一个集合，保证集合中的每个关键词唯一
    new_keywords = set(keywords[:])
    # 遍历关键词列表
    for keyword in keywords:
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
                # 遍历替换
                for one in one_iter:
                    # 字符对应的拼音存在则替换
                    if keyword_pinyin_list[one] is not None:
                        # 拼音替换字符
                        random_pinyin_total[one] = keyword_pinyin_list[one]
                        # 拼音首字母替换字符
                        random_pinyin_head[one] = keyword_pinyin_list[one][0]
                # 列表链接成词，字母转小写加入新关键词列表中
                new_keywords.add("".join(random_pinyin_total).lower())
                new_keywords.add("".join(random_pinyin_head).lower())
    # 返回关键词列表
    return list(new_keywords)




