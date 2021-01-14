from math import ceil


class Pager:
    def __init__(self, query, per_page: int = 30, page: int = 1):
        """
        初始化分页参数
        :param query: 查询对象
        :param per_page: 一页多少内容
        :param page: 第几页 1起
        """
        self.query = query
        self.per_page = per_page
        self.page = page

    @property
    def items(self):
        """
        得到分页后的内容
        :return: [model row / Model]
        """
        print(self.page, self.pages)
        if self.page > self.pages:
            return []
        offset_num = (self.page - 1) * self.per_page
        return self.query.offset(offset_num).limit(self.per_page).all()

    @property
    def counts(self):
        """
        总数据量
        :return: int
        """
        return self.query.count()

    @property
    def pages(self):
        """
        总页数
        :return: int
        """
        return ceil(self.counts / self.per_page)

    @property
    def next_num(self):
        """下一页"""
        next_num = self.page + 1
        if self.pages < next_num:
            return None
        return next_num

    @property
    def prev_num(self):
        """上一页"""
        prev_num = self.page - 1
        if prev_num < 1:
            return None
        return prev_num

    def iter_pages(self, left=2, right=2):
        length = left + right + 1
        # 页数大于
        if self.page > self.pages:
            range_start = self.pages - length
            if range_start <= 0:
                range_start = 1
            return range(range_start, self.pages + 1)

        # 页数小于最少分页数
        if self.pages < length:
            return range(1, self.pages + 1)

        # 页数正常的情况下,至少大于 length 长度
        l_boundary, r_boundary = left + 1, self.pages - right + 1
        if l_boundary < self.page < r_boundary:
            return range(self.page - left, self.page + right + 1)
        if self.page <= left:
            return range(1, length + 1)
        return range(self.pages - length, self.pages + 1)
