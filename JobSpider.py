'''
    定义一个包
'''
import re
import requests
import matplotlib.pyplot as plt


class JobSpider():

    ''' 定义一个类 '''
    # 请求头
    page_header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_?px=new&city=%E5%85%A8%E5%9B%BD',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3\
        6 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    }

    def __fetch_content__(self, city):
        ''' 获取数据 '''
        datas_box = []
        first = 'true'
        for count in range(1, 4):
            if count > 1:
                first = 'false'
            r = requests.post(
                'https://www.lagou.com/jobs/positionAjax.json',
                params={'px': 'default', 'city': city,
                        'needAddtionalResult': 'false', 'isSchoolJob': 0},
                data={'first': first, 'pn': count, 'kd': '前端'},
                headers=JobSpider.page_header
            )
            res = r.json()['content']['positionResult']['result']
            datas_box += res
        return datas_box

    def __analysis__(self, datas_box):
        ''' 整理数据 '''
        job_box = []
        for rank in range(0, len(datas_box)):
            job = {
                '公司': datas_box[rank]['companyFullName'],
                '薪资': datas_box[rank]['salary'],
                '技术': datas_box[rank]['positionLables'],
                '标签': datas_box[rank]['companyLabelList'],
                '阶段': datas_box[rank]['financeStage']
            }
            job_box.append(job)
        return job_box

    def go(self, city):
        ''' 抓取特定城市数据'''
        datas_box = self.__fetch_content__(city)
        job_box = self.__analysis__(datas_box)
        return job_box

    def details(self, arr):
        ''' 显示所有职位详情 '''
        for items in arr:
            for key, value in items.items():
                print(key, ':', value)
            print('~~~~~~~~')

    def salary(self, arr):
        ''' 工资最大值，最小值，平均值，饼图 '''
        salaries = []
        ave_salaries = []
        for rank in range(0, len(arr)):
            salary_range = arr[rank]['薪资']
            min_salary = re.findall(r'([\d]{1,2})', salary_range)[0]
            max_salary = re.findall(r'([\d]{1,2})', salary_range)[1]
            salaries.append(int(min_salary))
            salaries.append(int(max_salary))
            ave_salaries.append((int(min_salary) + int(max_salary)) / 2)
        min_salary = min(salaries)
        max_salary = max(salaries)
        ave_salary = round(sum(salaries) / (len(salaries)), 2)
        print('最低工资:' + str(min_salary) + 'k')
        print('最高工资:' + str(max_salary) + 'k')
        print('平均工资:' + str(ave_salary) + 'k')
        salary_dic = {
            '5k': 0,
            '10k': 0,
            '15k': 0,
            '20k': 0,
            '25k': 0,
            '30k': 0,
            '35k': 0
        }
        for item in ave_salaries:
            if item < 5:
                salary_dic['5k'] += 1
            elif item < 10:
                salary_dic['5k'] += 1
            elif item < 15:
                salary_dic['15k'] += 1
            elif item < 20:
                salary_dic['20k'] += 1
            elif item < 25:
                salary_dic['25k'] += 1
            elif item < 30:
                salary_dic['30k'] += 1
            else:
                salary_dic['35k'] += 1

        labels = ['0-5k', '5k-10k', '10k-15k',
                  '15k-20k', '20k-25k', '25k-30k', '>35k']
        salary_count = []
        for key, value in salary_dic.items():
            salary_count.append(int(value))
        sizes = salary_count
        plt.pie(sizes, labels=labels, shadow=True,
                autopct='%1.1f%%', startangle=50)
        plt.axis('equal')
        plt.show()

    def technology(self, arr):
        ''' 技术要求 排序 '''
        technology_dict = {}
        for rank in range(0, len(arr)):
            technologies = arr[rank]['技术']
            for technology in technologies:
                technology = technology.lower()
                if technology == 'js':
                    technology = 'javascript'
                if technology == 'web前端':
                    technology = 'web'
                if technology in technology_dict:
                    technology_dict[technology] += 1
                else:
                    technology_dict[technology] = 1
        technology_dict = sorted(
            technology_dict.items(), key=lambda e: e[1], reverse=True)
        for item in technology_dict:
            print(item[0], ':', item[1])

    def labels(self, arr):
        ''' 招聘公司标签 排序'''
        labels_dict = {}
        for rank in range(0, len(arr)):
            labels = arr[rank]['标签']
            for label in labels:
                label = label.lower()
                if label in labels_dict:
                    labels_dict[label] += 1
                else:
                    labels_dict[label] = 1
        labels_dict = sorted(labels_dict.items(),
                             key=lambda e: e[1], reverse=True)
        for item in labels_dict:
            print(item[0], ':', item[1])
