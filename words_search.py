from trie_node_model import *


# 能返回索引信息的搜索类
class IndexSearch:
    def __init__(self):
        # 头节点
        self._first = {}
        # 关键词列表
        self._keywords = []
        # 关键词索引列表
        self._indexs = []

    # 设置关键字函数
    # 通过输入的关键字列表，建立树
    def SetKeywords(self, keywords):
        # 将输入的关键字列表赋值给类属性
        self._keywords = keywords
        # 建立关键字索引列表
        self._indexs = []
        for i in range(len(keywords)):
            self._indexs.append(i)
        # 创建一个节点
        root = TrieNode()
        # 表示节点层数以及节点信息的列表
        allNodeLayer = {}
        # 遍历关键字列表
        # 建立节点树，对每一个关键词都建立一条节点路径
        for i in range(len(self._keywords)):  # for (i = 0; i < _keywords.length; i++)
            # 获取索引i的关键字
            p = self._keywords[i]
            # 创建临时变量，引用根节点
            nd = root
            # 遍历关键字中每个字符， 生成节点树
            # 例子：敏感词，将生成root->敏->感->词的树路径
            for j in range(len(p)):  # for (j = 0; j < p.length; j++)
                # ord(p[j])返回字符对应的十进制整数
                # 将这个整数生成一个新节点，加入到树的根节点下
                # nd.Add()将返回新生成节点，这个新生成的节点是上一节点的子节点
                nd = nd.Add(ord(p[j]))
                # 层数为0，代表是根节点
                if (nd.Layer == 0):
                    # 因为上一步nd.Add()返回的是上一个节点的子节点
                    # 所以到这里需要将该节点的层数设置为j+1
                    nd.Layer = j + 1
                    # 设置一个节点层数与节点的对应列表字典
                    # 在节点层对应列表中加入节点
                    # 表示每一层都有哪些节点
                    if nd.Layer in allNodeLayer:
                        allNodeLayer[nd.Layer].append(nd)
                    else:
                        allNodeLayer[nd.Layer] = []
                        allNodeLayer[nd.Layer].append(nd)
            # 表示叶节点
            nd.SetResults(i)

        # 获取一个包含所有节点的列表
        allNode = []
        allNode.append(root)
        for key in allNodeLayer.keys():
            for nd in allNodeLayer[key]:
                allNode.append(nd)

        # 遍历所有节点列表
        # 对每一个节点建立他与下一个节点的联系，将节点链接起来
        for i in range(len(allNode)):  # for (i = 0; i < allNode.length; i++)
            # 索引0为根节点
            if i == 0:
                continue
            # 获取索引i的节点
            nd = allNode[i]
            # 设置节点Index属性为i
            nd.Index = i
            # 获取该节点的父节点的Failure属性
            # Failure属性表示下一节点
            # 这一步是找到其父节点的下一节点，也就是这个nd本身
            r = nd.Parent.Failure
            # 获取该节点代表的字符二进制整数值
            c = nd.Char

            # r存在且r的子节点中没有c
            # 父节点的下一节点存在，且该节点中c并不是它的子节点值
            while (r != None and (c in r.m_values) == False):
                # 获取到下一节点
                r = r.Failure
            # r不存在
            if (r == None):
                # 设置nd的下一节点是root
                nd.Failure = root
            else:
                # 设置nd的下一节点为r的节点值为c的子节点，也就是重复值会进入这里，比如:天天
                # 把重复出现的节点链接到一起
                nd.Failure = r.m_values[c]
                for key2 in nd.Failure.Results:
                    nd.SetResults(key2)
        # 根节点的下一节点还是root
        root.Failure = root
        # 创建一个节点列表
        allNode2 = []
        # 加入与allNode列表同数量的TrieNode2节点
        for i in range(len(allNode)):
            allNode2.append(TrieNode2())

        for i in range(len(allNode2)):
            # 获取节点树对应索引i节点
            oldNode = allNode[i]
            # 获取新树节点
            newNode = allNode2[i]
            # 遍历节点的所有子节点
            for key in oldNode.m_values:
                # 获取子节点的索引
                index = oldNode.m_values[key].Index
                # 插入节点以及记录节点最大最小值
                newNode.Add(key, allNode2[index])
            # 设置叶节点信息
            for index in range(len(oldNode.Results)):
                item = oldNode.Results[index]
                newNode.SetResults(item)
            # 获取下一节点
            oldNode = oldNode.Failure
            # 以头节点为推出循环条件
            # 将这遍历得到的oldNode下所有子孙节点接入netNode
            while oldNode != root:
                # 遍历子节点
                for key in oldNode.m_values:
                    if (newNode.HasKey(key) == False):
                        # 如果新节点的信息没在newNode中
                        # 则把该节点信息加入newNode子节点
                        index = oldNode.m_values[key].Index
                        newNode.Add(key, allNode2[index])
                # 设置叶节点信息
                for index in range(len(oldNode.Results)):
                    item = oldNode.Results[index]
                    newNode.SetResults(item)
                # 获取下一节点
                oldNode = oldNode.Failure
        # 设置成头节点
        self._first = allNode2[0]

    # 发现输入文本中的第一个关键字
    def FindFirst(self, text):
        ptr = None
        # 遍历输入文本中是每一个字符
        for index in range(len(text)):  # for (index = 0; index < text.length; index++)
            # 字符转化为十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 进行基于当前节点的下一次广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 如果这次广搜没有对应的节点值，则返回首节点进行第一次广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 如果该节点存在结束标志，返回关键字信息字典
                    item = tn.Results[0]
                    keyword = self._keywords[item]
                    return {"Keyword": keyword, "Success": True, "End": index, "Start": index + 1 - len(keyword),
                            "Index": self._indexs[item]}
            ptr = tn
        # 没有找到关键字就返回None
        return None

    # 发现输入文本中所有的关键字
    def FindAll(self, text):
        ptr = None
        # 将要返回的关键字列表
        list = []
        # 遍历输入文本中的每个字符
        for index in range(len(text)):  # for (index = 0; index < text.length; index++)
            # 获取到字符的十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 进行基于当前节点的广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 没有搜索结果，则返回首节点进行广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 遍历得到该搜索路径下的所有关键词
                    for j in range(len(tn.Results)):  # for (j = 0; j < tn.Results.length; j++)
                        item = tn.Results[j]
                        keyword = self._keywords[item]
                        list.append(
                            {"Keyword": keyword, "Success": True, "End": index, "Start": index + 1 - len(keyword),
                             "Index": self._indexs[item]})
            ptr = tn
        # 返回关键词列表
        return list

    # 判断关键词是否在文本中
    def ContainsAny(self, text):
        ptr = None
        for index in range(len(text)):
            # 获取到字符的十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 基于当前节点进行下一次广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 没有搜索结果则返回首节点进行下一次广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 有关键词返回True
                    return True
            ptr = tn
        # 没有关键词返回False
        return False

    # 将文本中关键词替换
    def Replace(self, text, replaceChar='*'):
        result = list(text)

        ptr = None
        for i in range(len(text)):  # for (i = 0; i < text.length; i++)
            # 获取到字符的十进制整数
            t = ord(text[i])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 基于当前节点进行下一次广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 没有搜索结果则返回首节点进行下一次广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 获取替换长度
                    maxLength = len(self._keywords[tn.Results[0]])
                    start = i + 1 - maxLength
                    for j in range(start, i + 1):  # for (j = start; j <= i; j++)
                        # 进行替换
                        result[j] = replaceChar
            ptr = tn
        # 返回替换结果
        return ''.join(result)


# 直接返回列表的搜索类
class DirectSearch():
    def __init__(self):
        # 头节点
        self._first = {}
        # 关键字列表
        self._keywords = []

    # 设置关键字函数
    # 通过输入的关键字列表，建立树
    def SetKeywords(self, keywords):
        # 将输入的关键字列表赋值给类属性
        self._keywords = keywords
        # 创建一个节点
        root = TrieNode()
        # 表示节点层数以及节点信息的列表
        allNodeLayer = {}
        # 遍历关键字列表
        # 建立节点树，对每一个关键词都建立一条节点路径
        for i in range(len(self._keywords)):  # for (i = 0; i < _keywords.length; i++)
            # 获取索引i的关键字
            p = self._keywords[i]
            # 创建临时变量，引用根节点
            nd = root
            # 遍历关键字中每个字符， 生成节点树
            # 例子：敏感词，将生成root->敏->感->词的树路径
            for j in range(len(p)):  # for (j = 0; j < p.length; j++)
                # ord(p[j])返回字符对应的十进制整数
                # 将这个整数生成一个新节点，加入到树的根节点下
                # nd.Add()将返回新生成节点，这个新生成的节点是上一节点的子节点
                nd = nd.Add(ord(p[j]))
                # 层数为0，代表是根节点
                if (nd.Layer == 0):
                    # 因为上一步nd.Add()返回的是上一个节点的子节点
                    # 所以到这里需要将该节点的层数设置为j+1
                    nd.Layer = j + 1
                    # 设置一个节点层数与节点的对应列表字典
                    # 在节点层对应列表中加入节点
                    # 表示每一层都有哪些节点
                    if nd.Layer in allNodeLayer:
                        allNodeLayer[nd.Layer].append(nd)
                    else:
                        allNodeLayer[nd.Layer] = []
                        allNodeLayer[nd.Layer].append(nd)
            # 表示叶节点
            nd.SetResults(i)

        # 获取一个包含所有节点的列表
        allNode = []
        allNode.append(root)
        for key in allNodeLayer.keys():
            for nd in allNodeLayer[key]:
                allNode.append(nd)
        # 遍历所有节点列表
        # 对每一个节点建立他与下一个节点的联系，将节点链接起来
        for i in range(len(allNode)):  # for (i = 0; i < allNode.length; i++)
            # 索引0为根节点
            if i == 0:
                continue
            # 获取索引i的节点
            nd = allNode[i]
            # 设置节点Index属性为i
            nd.Index = i
            # 获取该节点的父节点的Failure属性
            # Failure属性表示下一节点
            # 这一步是找到其父节点的下一节点，也就是这个nd本身
            r = nd.Parent.Failure
            # 获取该节点代表的字符二进制整数值
            c = nd.Char

            # r存在且r的子节点中没有c
            # 父节点的下一节点存在，且该节点中c并不是它的子节点值
            while (r != None and (c in r.m_values) == False):
                # 获取到下一节点
                r = r.Failure
            # r不存在
            if (r == None):
                # 设置nd的下一节点是root
                nd.Failure = root
            else:
                # 设置nd的下一节点为r的节点值为c的子节点，也就是重复值会进入这里，比如:天天
                # 把重复出现的节点链接到一起
                nd.Failure = r.m_values[c]
                for key2 in nd.Failure.Results:
                    nd.SetResults(key2)
        # 根节点的下一节点还是root
        root.Failure = root
        # 创建一个节点列表
        allNode2 = []
        # 加入与allNode列表同数量的TrieNode2节点
        for i in range(len(allNode)):
            allNode2.append(TrieNode2())

        for i in range(len(allNode2)):
            # 获取节点树对应索引i节点
            oldNode = allNode[i]
            # 获取新树节点
            newNode = allNode2[i]
            # 遍历节点的所有子节点
            for key in oldNode.m_values:
                # 获取子节点的索引
                index = oldNode.m_values[key].Index
                # 插入节点以及记录节点最大最小值
                newNode.Add(key, allNode2[index])
            # 设置叶节点信息
            for index in range(len(oldNode.Results)):
                item = oldNode.Results[index]
                newNode.SetResults(item)
            # 获取下一节点
            oldNode = oldNode.Failure
            # 以头节点为推出循环条件
            # 将这遍历得到的oldNode下所有子孙节点接入netNode
            while oldNode != root:
                # 遍历子节点
                for key in oldNode.m_values:
                    if (newNode.HasKey(key) == False):
                        # 如果新节点的信息没在newNode中
                        # 则把该节点信息加入newNode子节点
                        index = oldNode.m_values[key].Index
                        newNode.Add(key, allNode2[index])
                # 设置叶节点信息
                for index in range(len(oldNode.Results)):
                    item = oldNode.Results[index]
                    newNode.SetResults(item)
                # 获取下一节点
                oldNode = oldNode.Failure
        # 设置成头节点
        self._first = allNode2[0]

    # 发现输入文本中的第一个关键字
    def FindFirst(self, text):
        ptr = None
        # 遍历输入文本中是每一个字符
        for index in range(len(text)):  # for (index = 0; index < text.length; index++)
            # 字符转化为十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 进行基于当前节点的下一次广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 如果这次广搜没有对应的节点值，则返回首节点进行第一次广搜
                    tn = self._first.TryGetValue(t)
            if (tn != None):
                if (tn.End):
                    # 如果该节点存在结束标志，返回关键字索引
                    return self._keywords[tn.Results[0]]
            ptr = tn
        # 没有找到关键字就返回None
        return None

    # 发现输入文本中所有的关键字
    def FindAll(self, text):
        ptr = None
        # 将要返回的关键字列表
        list = []
        # 遍历输入文本中的每个字符
        for index in range(len(text)):  # for (index = 0; index < text.length; index++)
            # 获取到字符的十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 进行基于当前节点的广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 没有搜索结果，则返回首节点进行广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 遍历得到该搜索路径下的所有关键词
                    for j in range(len(tn.Results)):  # for (j = 0; j < tn.Results.length; j++)
                        item = tn.Results[j]
                        list.append(self._keywords[item])
            ptr = tn
        # 返回关键词列表
        return list

    # 判断关键词是否在文本中
    def ContainsAny(self, text):
        ptr = None
        for index in range(len(text)):  # for (index = 0; index < text.length; index++)
            # 获取到字符的十进制整数
            t = ord(text[index])  # text.charCodeAt(index)
            if (ptr == None):
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 基于当前节点进行下一次广搜
                tn = ptr.TryGetValue(t)
                if (tn == None):
                    # 没有搜索结果则返回首节点进行下一次广搜
                    tn = self._first.TryGetValue(t)

            if (tn != None):
                if (tn.End):
                    # 有关键词返回True
                    return True
            ptr = tn
        # 没有关键词返回False
        return False

    # 将文本中关键词替换
    def Replace(self, text, replaceChar='*'):
        result = list(text)

        ptr = None
        for i in range(len(text)):  # for (i = 0; i < text.length; i++)
            # 获取到字符的十进制整数
            t = ord(text[i])  # text.charCodeAt(index)
            if ptr is None:
                # 进行第一次广搜
                tn = self._first.TryGetValue(t)
            else:
                # 基于当前节点进行下一次广搜
                tn = ptr.TryGetValue(t)
                if tn is None:
                    # 没有搜索结果则返回首节点进行下一次广搜
                    tn = self._first.TryGetValue(t)

            if tn is not None:
                if tn.End:
                    # 获取替换长度
                    maxLength = len(self._keywords[tn.Results[0]])
                    start = i + 1 - maxLength
                    for j in range(start, i + 1):  # for (j = start; j <= i; j++)
                        # 进行替换
                        result[j] = replaceChar
            ptr = tn
        # 返回替换结果
        return ''.join(result)
