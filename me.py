import JobSpider

spider = JobSpider.JobSpider()
R = spider.go('郑州')

# 输出职位详情
# spider.details(R)

# 输出薪资情况
# spider.salary(R)

# 输出技术要求情况
# spider.technology(R)

# 输出公司待遇情况
spider.labels(R)
