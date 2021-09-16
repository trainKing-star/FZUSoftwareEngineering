from data_preprocess import *
from words_search import IndexSearch
from main import data_load_process

class TestDataPreprocess:

    def test_expand_keywords(self):
        global keywords
        global keywords_expand_results
        print("开始测试扩展敏感词")
        for index, keyword in enumerate(keywords):
            test_keywords, test_expand_results = expand_keywords([keyword])
            for test_k in test_keywords:
                assert test_k in keywords_expand_results[index][0]
            for test_k, test_v in test_expand_results.items():
                assert test_expand_results[test_k] == keywords_expand_results[index][1][test_k]
        print("扩展敏感词正常")

    def test_characters_preprocess(self):
        global keywords
        global char_text
        global char_text_result_1
        global char_text_result_2
        print("开始测试输入文本预处理")
        test_text, test_index = characters_preprocess(char_text, keywords)
        test_text = "".join(test_text)
        assert test_text == char_text_result_1
        assert test_index == char_text_result_2

    def test_judge_c_z(self):
        global judge_test
        print("开始测试中英文区分判断")
        for i in range(len(judge_test)):
            assert judge_test[i][2] == judge_chinese_english(judge_test[i][0], judge_test[i][1])
        print("测试中英文区分判断正常")

    def test_data_load_process(self):
        global keywords_file
        global input_file
        global output_file
        global compare_file
        data_load_process(keywords_file, input_file, output_file)
        with open(output_file, "r", encoding="utf8") as f:
            output_list = f.read().splitlines()
        with open(compare_file, "r", encoding="utf8") as f:
            compare_list = f.read().splitlines()
        for i in range(len(output_list)):
            assert output_list[i] == compare_list[i]


keywords = ["福州大学", "happy"]
keywords_expand_results = [
(['fuzhoudxue', 'fuzhoudaxue', 'fuzhou大xue', '福州大学', '福州dx', 'fzhoudxue', 'fu州大学',
  'fuzdxue', 'fzhoudaxue', 'fuzhouda学', '福zhou大学', '福zhou大xue', 'fu州da学', '福州da学',
  'fzd学', '福州daxue', 'f州dx', 'fu州大xue', '福zdx', 'fuzhoudx', 'fzdx', 'fuzdax', 'fzhoudax',
  '福zd学', 'fzdax', '福zhoudaxue', 'fuzhou大学', 'fzdxue', 'fzhoudx', 'fu州daxue', 'f州大x', 'fz大学',
  'fuzdx', 'fuzhoudax', 'f州d学', 'fz大x', '福州大x', 'f州大学', '福z大x', '福zhouda学', '福州d学', '福州大xue',
  'fzdaxue', '福z大学', 'fuzdaxue'],
 {'福州大学': '福州大学', 'fu州大学': '福州大学', 'f州大学': '福州大学', 'fzhoudaxue': '福州大学', '福zhou大学': '福州大学',
  '福z大学': '福州大学', 'fuzdaxue': '福州大学', '福州da学': '福州大学', '福州d学': '福州大学', 'fuzhoudxue': '福州大学',
  '福州大xue': '福州大学', '福州大x': '福州大学', 'fuzhoudax': '福州大学', 'fuzhou大学': '福州大学', 'fz大学': '福州大学',
  'fzdaxue': '福州大学', 'fu州da学': '福州大学', 'f州d学': '福州大学', 'fzhoudxue': '福州大学', 'fu州大xue': '福州大学',
  'f州大x': '福州大学', 'fzhoudax': '福州大学', '福zhouda学': '福州大学', '福zd学': '福州大学', 'fuzdxue': '福州大学',
  '福zhou大xue': '福州大学', '福z大x': '福州大学', 'fuzdax': '福州大学', '福州daxue': '福州大学', '福州dx': '福州大学',
  'fuzhoudx': '福州大学', 'fuzhouda学': '福州大学', 'fzd学': '福州大学', 'fzdxue': '福州大学', 'fuzhou大xue': '福州大学',
  'fz大x': '福州大学', 'fzdax': '福州大学', 'fu州daxue': '福州大学', 'f州dx': '福州大学', 'fzhoudx': '福州大学',
  '福zhoudaxue': '福州大学', '福zdx': '福州大学', 'fuzdx': '福州大学', 'fuzhoudaxue': '福州大学', 'fzdx': '福州大学'}),
(['happy'], {'happy': 'happy'})
]

char_text = "抚州大学，富洲大雪，辅轴搭薛，拼音称呼fuzhou大学，首字母简称fz大学，全简称FZDX。" \
            "zhd现在正在做的这个项目是为了在fz大学的软件工程课上更happy的学习！"
char_text_result_1 = "福州大学福州大学福州大学拼音称呼fuzhou大学首字母简称fz大学全简称fzdx" \
                   "zhd现在正在做的这个项目是为了在fz大学的软件工程课上更happy的学习"
char_text_result_2 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                      24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 46,
                      47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                      67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82]

judge_test = [
    ("ha132468492^$^%%&%&ap48548&^%py", "happy", "ha132468492^$^%%&%&ap48548&^%py"),
    ("福5465州456%……&大……%%￥……学", "福州大学", None),
    ("￥%……#@￥福%…………&州%…………大%……#@#￥&&*学", "福州大学", "￥%……#@￥福%…………&州%…………大%……#@#￥&&*学")
]

keywords_file = "test/words.txt"
input_file = "test/org.txt"
output_file = "test/ans.txt"
compare_file = "test/compare.txt"

