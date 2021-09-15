from WordsSearch import IndexSearch

if __name__ == "__main__":
    s = "法轮功|flg|法lun功"
    test = "法轮功是一种邪教组织，简称flg，抵制法lun功"

    search = IndexSearch()
    search.SetKeywords(s.split('|'))
    print("搜索信息：", search.FindAll(test))
    print("关键词替换：", search.Replace(test))