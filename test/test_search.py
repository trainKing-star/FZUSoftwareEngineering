from words_search import IndexSearch

test_search = IndexSearch()
# 输入测试关键词案例
test_keyword = ["福州大学", "软件工程", "FZDX", "zhd", "happy", "fz大学", "fuzhou大学"]
# 输入测试文本
test_text = "福州大学，拼音称呼fuzhou大学，首字母简称fz大学，全简称FZDX。" \
            "zhd现在正在做的这个项目是为了在fz大学的软件工程课上更happy的学习！"

class TestSearch:

    def test_set_keyword(self):
        global test_search
        global test_keyword
        print("测试初始化搜索类")
        test_search.SetKeywords(test_keyword)
        print("初始化搜索类正常")

    def test_find_all(self):
        global test_search
        global test_text
        print("测试全局搜索")
        all = test_search.FindAll(test_text)
        assert all[0]["Keyword"] == "福州大学"
        assert all[1]["Keyword"] == "fuzhou大学"
        assert all[2]["Keyword"] == "fz大学"
        assert all[3]["Keyword"] == "FZDX"
        assert all[4]["Keyword"] == "zhd"
        assert all[5]["Keyword"] == "fz大学"
        assert all[6]["Keyword"] == "软件工程"
        assert all[7]["Keyword"] == "happy"
        assert len(all) == 8
        print("全局搜索正常")
