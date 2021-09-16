from simplified_translate import Translate

# 输入文本
origin_text = "福州大學，拼音稱呼fuzhou大學，首字母簡稱fz大學，全簡稱FZDX。" \
              "zhd現在正在做的這個項目是爲了在fz大學的軟件工程課上更happy的學習！"
# 测试标准结果
target_text = "福州大学，拼音称呼fuzhou大学，首字母简称fz大学，全简称FZDX。" \
              "zhd现在正在做的这个项目是为了在fz大学的软件工程课上更happy的学习！"


class TestSimplified:

    def test_Simplified(self):
        global origin_text
        global target_text
        print("测试全局搜索")
        translate = Translate()
        text = translate.ToSimplifiedChinese(origin_text)
        assert text == target_text
        print("全局搜索正常")
