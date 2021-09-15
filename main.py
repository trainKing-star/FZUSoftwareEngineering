from words_search import IndexSearch
from data_preprocess import *

if __name__ == "__main__":
    s = "法轮功|flg|法lun功"
    test = "法轮功是一种邪教组织，简称flg，抵制法lun功"

    s = expand_keywords(s.split("|"))
    new_test, origin_index = characters_preprocess(test)
    search = IndexSearch()
    search.SetKeywords(s)
    message_list = search.FindAll(new_test)
    search_message_from_origin_text(test, message_list, origin_index)