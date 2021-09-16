# 树节点类
class TrieNode:
    def __init__(self):
        # 节点索引
        self.Index = 0
        # 节点所在的树层数
        self.Layer = 0
        # 关键词结束标识
        self.End = False
        # 字符代表的十进制整数
        self.Char = ''
        # 对应的关键词列表
        self.Results = []
        # 子节点列表
        self.m_values = {}
        # 重复值需要链接的属性
        self.Failure = None
        # 父节点
        self.Parent = None

    # 插入节点函数
    # c——输入的字符十进制整数
    # 一个十进制整数对应一个节点
    def Add(self, c):
        # 如果该整数在该节点的子节点列表中，返回原来子节点列表
        if c in self.m_values:
            return self.m_values[c]
        # 生产一个新节点
        node = TrieNode()
        # 将新节点作为当前节点的子节点
        node.Parent = self
        # 设置新节点代表的值
        node.Char = c
        # 将新节点加入到该节点的子节点列表
        self.m_values[c] = node
        # 返回新生成的节点
        return node

    def SetResults(self, index):
        # 标识叶节点
        if self.End is False:
            self.End = True
        # 设置一条路径对应的关键词索引
        self.Results.append(index)


# 广搜节点类
class TrieNode2:
    def __init__(self):
        # 关键词结束标识
        self.End = False
        # 对应的关键词列表
        self.Results = []
        # 子节点列表
        self.m_values = {}
        # 子节点列表中的最小十进制整数值
        self.minflag = 0xffff
        # 子节点列表中的最大十进制整数值
        self.maxflag = 0

    # 插入节点函数
    def Add(self, c, node3):
        # 在插入过程中记录下插入节点十进制整数的最大最小值
        if self.minflag > c:
            self.minflag = c
        if self.maxflag < c:
            self.maxflag = c
        # 加入到本节点的子节点列表中
        self.m_values[c] = node3

    # 标识叶节点
    def SetResults(self, index):
        if self.End is False:
            self.End = True
        # 设置一条路径对应的关键词索引
        if not (index in self.Results):
            self.Results.append(index)

    # 判断子节点中有无该键值
    def HasKey(self, c):
        return c in self.m_values

    # 尝试获取到输入字符对应的子孙节点
    def TryGetValue(self, c):
        # 判断c是否在该节点的子孙节点值范围中
        if self.minflag <= c <= self.maxflag:
            if c in self.m_values:
                # 如果存在就返回该子孙节点
                return self.m_values[c]
        return None
