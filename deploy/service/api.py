# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api service

base_info:
    __author__ = "PyGo"
    __time__ = "2023/9/7 21:01"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python apis.py
# ------------------------------------------------------------
import json
import requests
import datetime


from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum


class ApiService(object):
    """
    api service
    """

    API_KEY = "R4uejriAnLKV8x1IghtNa7gQ"
    SECRET_KEY = "Dm0Y0SRwX4ccL7c9iNsYwwYmkCHXGFGH"

    # zlxcx_process
    zlxcx_process_params = [
        'xmbh',
        'year',
        'quarter'
    ]
    ZLXCX_PROCESS_YEAR_LIST = [2023, 2024]
    ZLXCX_PROCESS_QUARTER_LIST = {
        "第一季度": 0,
        "第二季度": 1,
        "第三季度": 2,
        "第四季度": 3,
    }

    def __init__(self):
        """
        ApisService class initialize
        """
        super(ApiService, self).__init__()

    def __str__(self):
        print("ApisService class.")

    def __repr__(self):
        self.__str__()

    def zlxcx_token(self) -> dict:
        token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjE3NCIsInVzZXJJZCI6IjIxMjEiLCJuYW1lIjoi6auY5piO5LquIiwicm9sZUlkcyI6IiIsInJvbGVDb2RlcyI6IiIsInNlc3Npb25JZCI6IkJEREMxODFDNEEzMzIwOEE5MUIxMEVCMzkwNjZDMjAwIiwib3JnSWQiOiIxOCIsImV4cCI6MTcyNDgwNTM3OH0.C4yX8xd8W480uoQ_UPNYiTtse39llGiEmZkBNzJh_XG2HwZIWwXDtZ9ZfXDmI0nLCE_xGdRDnMcg_ZG9lXOWdINEaaT_GM_nZX2R4faw0VKTqmJIla__g_hUH0onhyjbSIA5DKGK98xyXiwdJbrYgoFAkwP0PrZ_mnw4So4UCU9pqVdtX2omIg6LXp3JoWrdTEbY1GTzaIgs1YZbx1W_XqmyhQHOtQeweDNzNDy8HXKn3SSi5Wo0xRsFYPEIu_0JvECLwathVPWLTyFr82RI3EXqtTvcZaJYKi4B2RUQTsLqERSB_Due2kzyxeQAhehawiXofEoM4A50ZXUisEhV0A"
        return {"token": token}

    def zlxcx_process(self, params: dict) -> dict:
        """
        质量小程序: 过程检查
        :return: json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()

        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.zlxcx_process_params:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()

            if k == 'year' and int(v) not in self.ZLXCX_PROCESS_YEAR_LIST:
                # 年份参数
                return Status(
                    404, StatusEnum.FAILURE.value, '请求参数值%s不合法' % v, {}).json()
            elif k == 'quarter' and v not in self.ZLXCX_PROCESS_QUARTER_LIST.keys():
                # 季度参数
                return Status(
                    404, StatusEnum.FAILURE.value, '请求参数值%s不合法' % v, {}).json()

            new_params[k] = str(v)

        # 季度INDEX
        quarter_index = self.ZLXCX_PROCESS_QUARTER_LIST.get(new_params.get('quarter'))
        # 删除季度参数
        del new_params['quarter']
        other = {
            "gzsj": "",
            "zxjg": "",
            "jcpl": "",
            "zblx": "",
            "db": "dn0"
        }
        querystring = {**new_params, **other}
        url = "http://tmis.pasok.cn/tmis/pmp/zkgl/getZkjgList"
        token = self.zlxcx_token()
        if not token or not token.get('token'):
            return Status(
                903, StatusEnum.FAILURE.value, '质量API TOKEN初始化失败', {}).json()

        payload = {}
        headers = {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh,zh-CN;q=0.9,en;q=0.8,ru;q=0.7",
            'cache-control': "no-cache,no-cache",
            'connection': "keep-alive",
            # 'cookie': "JSESSIONID=BDDC181C4A33208A91B10EB39066C200",
            'host': "tmis.pasok.cn",
            'pragma': "no-cache",
            'referer': "http://tmis.pasok.cn/",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            'x-token': token.get('token'),
            'Postman-Token': "58d1a484-e8a6-4438-8cab-564f535f4dc2"
        }

        # 过程检查指标
        ZB = {
            44: "数据备份",
            26: "效果评估汇报",
            28: "效果评估评审",
            46: "效果评估咨询人员配置",
            54: "培训 / 调研 / 辅导 / 座谈会次数",
            52: "系统使用次数",
            25: "总调度跑批时长",
            22: "工资确认单",
            49: "一把手拜访",
            2: "阶段工作成果汇报",
            # ----------- 暂不展示 -----------
            # 36: "五结合评审",
            # 5: "制度评审",
            # 24: "价格测算",
            # 39: "咨询人员配置",
            # 50: "工资兑现流程",
            # 51: "当年首次按新办法兑现",
            # 6: "工资核对表",
            # 16: "效果自评",
            # 17: "成绩单规划清单",
            # 18: "成绩单一览表",
            # 19: "一把手认知评估",
            # 15: "续约汇报"
        }
        """
        zxqk为2长度指标:
            总调度跑批时长
        zxqk为3长度指标:
            效果评估汇报 效果评估评审 效果评估咨询人员配置
        zxqk为4长度指标:
            数据备份 系统使用次数 工资确认单
            培训/调研/辅导/座谈会次数 阶段工作成果汇报 一把手拜访
        """
        ZB_ZXQK_2 = [25]
        ZB_ZXQK_3 = [26, 28, 46]
        ZB_ZXQK_4 = [22, 44, 52, 54, 2, 49]

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        res = dict()
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("code") == 0:
                response_json_data_list = response_json.get('data').get('list')
                res['info'] = response_json.get('data').get('info')
                zb_list = list()
                for item in response_json_data_list:
                    if not item:
                        continue

                    # print("%s:%s" % (item.get('zbid'), item.get('zbmc')))
                    zb = dict()
                    # 指标ID
                    zb_id = item.get('zbid')
                    if int(zb_id) not in ZB.keys():
                        # 只统计展示指标
                        continue
                    zb['zbid'] = zb_id
                    # 指标名称
                    zb['zbmc'] = item.get('zbmc')
                    # 工作事件
                    zb['gzsj'] = item.get('gzsj')
                    # 检查频率
                    zb['jcpl'] = item.get('jcpl')
                    # 指标类型
                    zb['zblx'] = item.get('zblx')
                    # 质量标准
                    zb['zlbz'] = item.get('zlbz')
                    # 检查标准
                    zb['jcbz'] = item.get('jcbz')
                    # 扣罚标准
                    zb['kfbz'] = item.get('kfbz')
                    # 关联模型节点
                    zb['zjmx'] = item.get('zjmx')
                    # 手工指标SQL
                    # zb['sgzbsql'] = item.get('sgzbsql')
                    # 项目计划
                    zb['xmjh'] = item.get('xmjh')
                    # SF说明
                    zb['sfms'] = item.get('sfms')
                    # JMGZ
                    zb['jmgz'] = getattr(item, 'jmgz', "")
                    # 执行情况（是个list类型，并且根据月度/季度/年度数据长度不等，需要进行for循环）
                    # 只展示查询季度数据
                    zxqk_list = item.get('zxqk')
                    if zb_id in ZB_ZXQK_4:
                        zb['zxqk'] = zxqk_list[quarter_index].get('zxjgmc')
                    elif zb_id in ZB_ZXQK_3:
                        if quarter_index in [0, 1, 3]:
                            _index = 0
                        elif quarter_index in [4]:
                            _index = 1
                        else:
                            _index = 0
                        zb['zxqk'] = zxqk_list[_index].get('zxjgmc')
                    elif zb_id in ZB_ZXQK_2:
                        zb['zxqk'] = '/'
                    else:
                        zb['zxqk'] = '/'
                    zb_list.append(zb)
                res['list'] = zb_list

        return Status(
            100,
            StatusEnum.SUCCESS.value,
            StatusMsgs.get(100),
            res
        ).json()


