from pin_yin_translate import Pinyin
# 输入测试文本
origin_text = "福州大学，拼音称呼fuzhou大学，首字母简称fz大学，全简称FZDX。" \
              "zhd现在正在做的这个项目是为了在fz大学的软件工程课上更happy的学习！"
# 输入测试标准文本
target_text = "FuZhouDaXue，PinYinChengHufuzhouDaXue，ShouZiMuJianChengfzDaXue，QuanJianChengFZDX。" \
              "zhdXianZaiZhengZaiZuoDiZheGeXiangMuShiWeiLeZaifzDaXueDiRuanJianGongChengKeShangGenghappyDiXueXi！"


class TestPinyin:

    def test_pinyin(self):
        global origin_text
        global target_text
        print("测试拼音替换")
        pinyin = Pinyin()
        text = pinyin.GetPinyin(origin_text)
        assert text == target_text
        print("拼音替换正常")
