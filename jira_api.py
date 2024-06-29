from jira import JIRA
import requests
import json
import configparser


# 获取飞书T_token：飞书API 2小时到期一次，这个函数是每次运行都获取一次。有时间可以将cookies和headers优化一下
def get_tenant_access_token():
    cookies = {
        'passport_web_did': '7319337147591655425',
        'QXV0aHpDb250ZXh0': '2a955715357d4851b7428f01ec861e40',
        'locale': 'en-US',
        'trust_browser_id': '2b7701d0-0333-4cb9-987d-7b942fd61aa3',
        'is_anonymous_session': '',
        'lang': 'zh',
        '__tea__ug__uid': '7319397282721465868',
        '_gcl_au': '1.1.1934240740.1712139071',
        'open_locale': 'zh-CN',
        'deviceId': 'clujnieub00002v6ljdbxl3ip',
        '_ga': 'GA1.3.941775451.1704165980',
        'session': 'XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA',
        'session_list': 'XN0YXJ0-d99ucdc8-bdbd-4722-a7c3-e82799315b83-WVuZA_XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA_XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA',
        'SLARDAR_WEB_ID': '0b97b54a-cb68-4ddc-90fc-08b921b14315',
        'Hm_lvt_e78c0cb1b97ef970304b53d2097845fd': '1712139071,1712932870',
        '_ga_R56B49X323': 'GS1.1.1714443471.1.0.1714443482.0.0.0',
        '_csrf_token': '3d6c17aaacc13ea820fd7a8db9e0ee5fe083051b-1718070750',
        'lark_oapi_csrf_token': 'sFA+e7YqI8gvvpz2OPhFQowNIpyjFTQTFmUrvy3Rn1g=',
        '_gid': 'GA1.3.941872876.1718763070',
        '_gid': 'GA1.2.941872876.1718763070',
        'open_csrf_token': '898eefb2-2abb-4953-bd2b-9d93cdb8a399',
        'passport_app_access_token': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg4OTI2MjMsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjciOnsiaWF0IjoxNzE4ODQ5NDIzLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiNThiZDYyYzM0N2I3MTIyYzhlM2Q0ODYwM2MyMzk5NDZmZTM4NTZiMjY4NWZjZWJkMzIxY2M3MGE1MTEwMGQ5YyJ9fQ.mawllGpMIyM9cXfexD0hgCr4AX6_29dAt8dgM9i_INEsa3RffIHR8Gs6W3XswNu9ooRM9zawSj-WuJWaFHlYPQ',
        'sl_session': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg4OTM4NDEsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXVGV5Q3lpVUFEWXlnYXdJMlpRQU5sazRKYk1ZV0FBV1dUZ2xzeGhZQUJaWk9DYkFyRGdBRUNLZ0VBUVVGQlFVRkJRVUZCUVVKc2F6UktjMGhWVGtGSVFUMDkiLCJzdW0iOiI1OGJkNjJjMzQ3YjcxMjJjOGUzZDQ4NjAzYzIzOTk0NmZlMzg1NmIyNjg1ZmNlYmQzMjFjYzcwYTUxMTAwZDljIiwibG9jIjoiZW5fdXMiLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4ODUwNjQxLCJzYWMiOnsiVXNlclR5cGUiOiI0MiIsIlVzZXJTdGFmZlN0YXR1cyI6IjEifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE5MzI5MTk5NzcxNjk3MTU1IiwibnNfdGlkIjoiNzE0NDk5MDIyMzEzNDk2NTc2MyIsIm90IjoyfX0.0BhlwpMsxu0AAzqn3KGOjwO_AL8PLLm1o-ZvR-ff3OE8EDCVwvV6ZUe9_ks7XTFqo7rNVxtDcQfHIKuJz0gOUQ',
        '_gat_UA-98246768-7': '1',
        '_ga': 'GA1.1.941775451.1704165980',
        '_ga_VPYRHN104D': 'GS1.1.1718849288.41.1.1718850642.59.0.0',
        'swp_csrf_token': '1610e1b9-bbc7-4c30-86c0-423de76aee3f',
        't_beda37': '27fa7838280ebec1ac98ab2e623f59122465478237f73ff5e97cb978fdedd078',
    }

    headers = {
        'authority': 'open.feishu.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'passport_web_did=7319337147591655425; QXV0aHpDb250ZXh0=2a955715357d4851b7428f01ec861e40; locale=en-US; trust_browser_id=2b7701d0-0333-4cb9-987d-7b942fd61aa3; is_anonymous_session=; lang=zh; __tea__ug__uid=7319397282721465868; _gcl_au=1.1.1934240740.1712139071; open_locale=zh-CN; deviceId=clujnieub00002v6ljdbxl3ip; _ga=GA1.3.941775451.1704165980; session=XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA; session_list=XN0YXJ0-d99ucdc8-bdbd-4722-a7c3-e82799315b83-WVuZA_XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA_XN0YXJ0-0dcre63c-d38b-4009-b7fe-f89126373d87-WVuZA; SLARDAR_WEB_ID=0b97b54a-cb68-4ddc-90fc-08b921b14315; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1712139071,1712932870; _ga_R56B49X323=GS1.1.1714443471.1.0.1714443482.0.0.0; _csrf_token=3d6c17aaacc13ea820fd7a8db9e0ee5fe083051b-1718070750; lark_oapi_csrf_token=sFA+e7YqI8gvvpz2OPhFQowNIpyjFTQTFmUrvy3Rn1g=; _gid=GA1.3.941872876.1718763070; _gid=GA1.2.941872876.1718763070; open_csrf_token=898eefb2-2abb-4953-bd2b-9d93cdb8a399; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg4OTI2MjMsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjciOnsiaWF0IjoxNzE4ODQ5NDIzLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiNThiZDYyYzM0N2I3MTIyYzhlM2Q0ODYwM2MyMzk5NDZmZTM4NTZiMjY4NWZjZWJkMzIxY2M3MGE1MTEwMGQ5YyJ9fQ.mawllGpMIyM9cXfexD0hgCr4AX6_29dAt8dgM9i_INEsa3RffIHR8Gs6W3XswNu9ooRM9zawSj-WuJWaFHlYPQ; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg4OTM4NDEsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXVGV5Q3lpVUFEWXlnYXdJMlpRQU5sazRKYk1ZV0FBV1dUZ2xzeGhZQUJaWk9DYkFyRGdBRUNLZ0VBUVVGQlFVRkJRVUZCUVVKc2F6UktjMGhWVGtGSVFUMDkiLCJzdW0iOiI1OGJkNjJjMzQ3YjcxMjJjOGUzZDQ4NjAzYzIzOTk0NmZlMzg1NmIyNjg1ZmNlYmQzMjFjYzcwYTUxMTAwZDljIiwibG9jIjoiZW5fdXMiLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4ODUwNjQxLCJzYWMiOnsiVXNlclR5cGUiOiI0MiIsIlVzZXJTdGFmZlN0YXR1cyI6IjEifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE5MzI5MTk5NzcxNjk3MTU1IiwibnNfdGlkIjoiNzE0NDk5MDIyMzEzNDk2NTc2MyIsIm90IjoyfX0.0BhlwpMsxu0AAzqn3KGOjwO_AL8PLLm1o-ZvR-ff3OE8EDCVwvV6ZUe9_ks7XTFqo7rNVxtDcQfHIKuJz0gOUQ; _gat_UA-98246768-7=1; _ga=GA1.1.941775451.1704165980; _ga_VPYRHN104D=GS1.1.1718849288.41.1.1718850642.59.0.0; swp_csrf_token=1610e1b9-bbc7-4c30-86c0-423de76aee3f; t_beda37=27fa7838280ebec1ac98ab2e623f59122465478237f73ff5e97cb978fdedd078',
        'origin': 'https://open.feishu.cn',
        'referer': 'https://open.feishu.cn/api-explorer/cli_a6878296023cd00d?apiName=query&project=sheets&resource=spreadsheet.sheet&state=undefined&version=v3',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-csrf-token': 'N5YDaHChxoDisaji977mLTmJZqpHbDOKQ06XJE7IebKHxj0TxovlSM0PNBTPRqNvtYRENuR5B5lVK7ybYxnm6g==',
        'x-timezone-offset': '-480',
    }

    json_data = {
        'appId': 'cli_a6878296023cd00d',
    }

    response = requests.post(
        'https://open.feishu.cn/api_explorer/v1/tenant/access_token',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    response = response.json()
    T_token = response['data']['tenantAccessToken']
    return T_token


# 配置文件路径，将获取的token更新到config.ini文件中
def update_tenant_access_token(token):
    config_file_path = (
        '/home/keningsun/work/ponyai/.sub-repos/common/experimental/keningsun/feishu/config.ini'
    )
    # 创建ConfigParser对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read(config_file_path)
    # 更新tenant_access_token值
    config.set('lark', 'tenant_access_token', token)  # 假设tenant_access_token在[DEFAULT]部分下
    # 写回配置文件
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)


# 读取配置文件，读取config.ini文件
def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    jira_url = config.get('jira', 'url')
    jira_url_RTI = config.get('jira', 'url_RTI')
    jira_username = config.get('jira', 'username')
    jira_password = config.get('jira', 'password')
    lark_access_token = config.get('lark', 'access_token')
    lark_spreadsheetToken = config.get('lark', 'spreadsheetToken')
    lark_tenant_access_token = config.get('lark', 'tenant_access_token')
    return (
        jira_url,
        jira_url_RTI,
        jira_username,
        jira_password,
        lark_access_token,
        lark_spreadsheetToken,
        lark_tenant_access_token,
    )


# 登录到 JIRA
def login_to_jira(server, username, password):
    options = {'server': server}
    jira = JIRA(options, basic_auth=(username, password))
    return jira


# 获取 JIRA 问题，这个解决飞书每页只能获取50条issues 目前设定可以获取1000条，超过这个数量可以修改max_results
def get_all_jira_issues(jira, jql_str):
    start_at = 0
    max_results = 1000
    total_issues = []

    while True:
        # 每次循环请求一定数量的问题
        issues = jira.search_issues(jql_str, startAt=start_at, maxResults=max_results)
        # 添加新获取的问题到总列表
        total_issues.extend(issues)
        # 更新起始位置
        start_at += len(issues)
        # 如果这次请求的问题数少于请求的最大值，说明已经获取了所有问题
        if len(issues) < max_results:
            break

    return total_issues


# 获得表格中Rows 并返回行数
def get_rows(lark_tenant_access_token, spreadsheetToken):
    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheetToken}/sheets/query'
    headers = {
        'Authorization': f'Bearer {lark_tenant_access_token}',
        'Content-Type': 'application/json',
    }
    response_rows = requests.get(url, headers=headers)
    if response_rows.status_code == 200:
        # 将JSON字符串转换为Python字典
        data_dict = response_rows.json()
        # 提取row_count
        row_count = data_dict['data']['sheets'][0]['grid_properties']['row_count']

        print('原表格行数为:', row_count)
        return row_count
    else:
        print(f'删除行列失败，状态码：{response_rows.status_code}')
        print(response_rows.text)


# 删除表内信息，如果不需要先删除表中内容 可以注释掉这个函数
def delete_all_rows_columns_in_sheet(lark_tenant_access_token, spreadsheetToken):
    # 获取工作表的总行数
    total_rows = get_rows(lark_tenant_access_token, spreadsheetToken)
    # 首先获取工作表的行数和列数
    url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/dimension_range'
    headers = {
        'Authorization': f'Bearer {lark_tenant_access_token}',
        'Content-Type': 'application/json',
    }

    # 准备删除所有行的payload
    payload_rows = {
        'dimension': {
            'sheetId': '2d4684',  # 填写自己的sheetId
            'majorDimension': 'ROWS',
            'startIndex': 1,  # 索引从1开始
            'endIndex': total_rows - 1,  # 减1是因为索引是从0开始的
        }
    }

    # 发送DELETE请求删除所有行
    response_rows = requests.delete(url, headers=headers, json=payload_rows)
    # 检查响应状态码
    if response_rows.status_code == 200:
        print('行列删除成功')
    else:
        print(f'删除行列失败，状态码：{response_rows.status_code}')
        print(response_rows.text)
    return response_rows.json()


# 插入数据到飞书表格
def insert_data_to_larksheet(lark_tenant_access_token, spreadsheetToken, data):
    print('Tenant Access Token:', lark_tenant_access_token)
    # 先清除表内数据
    delete_all_rows_columns_in_sheet(lark_tenant_access_token, spreadsheetToken)
    # 插入数据
    url = (
        f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values_prepend'
    )
    headers = {
        'Authorization': f'Bearer {lark_tenant_access_token}',
        'Content-Type': 'application/json',
    }
    # 应用序列化逻辑到数据
    serialized_data = [[serialize_custom_field(field) for field in row] for row in data]
    # 确保你获取的字段与表格字段一致
    body = {
        'valueRange': {
            'range': '2d4684!A:M',
            'values': [
                [
                    'Key',
                    'Issue_like',
                    'Labels',
                    'Summary',
                    'Type',
                    'Component',
                    'VOD_link',
                    'issue_replay',
                    'Is_Release_Blocker',
                    'RC',
                    '车号',
                    '车型',
                    'Operation Area',
                    'TripType',
                ]
            ]
            + serialized_data,
            'majorDimension': 'ROWS',
        }
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


# 自定义处理相关字段，根据需要直接调用
def serialize_custom_field(value):
    """处理自定义字段值，确保可JSON序列化"""
    if isinstance(value, list):
        # 如果是列表，递归处理每个元素
        return [serialize_custom_field(item) for item in value]
    elif hasattr(value, 'name'):  # 例如CustomFieldOption类型
        return value.name
    elif hasattr(value, 'id'):  # 或者如果它有ID属性
        return value.id
    else:
        # 对于其他未知类型，尝试转换为字符串
        return str(value)


def main():
    # 获取飞书Token
    new_token = get_tenant_access_token()
    # print(new_token)
    # 将Token更新.ini文件
    update_tenant_access_token(new_token)
    # 读取配置：填写你自己的config.ini地址
    config_path = (
        '/home/keningsun/work/ponyai/.sub-repos/common/experimental/keningsun/feishu/config.ini'
    )
    (
        jira_url,
        jira_url_RTI,
        jira_username,
        jira_password,
        lark_access_token,
        spreadsheetToken,
        lark_tenant_access_token,
    ) = read_config(config_path)
    # 登录 JIRA
    jira = login_to_jira(jira_url, jira_username, jira_password)
    # JQL 查询
    jql_str = str(input('请输入 JQL 查询语句: '))
    issues = get_all_jira_issues(jira, jql_str)
    print('让子弹飞一会！')
    # 转换数据格式以匹配 API 需求，下面字段可以选择你需要的
    data_to_insert = [
        [
            issue.key,  # Key
            jira_url_RTI + issue.key,  # issue_like
            ', '.join(issue.fields.labels),  # 获取多个labels
            issue.fields.summary,  # summary
            issue.fields.issuetype.name,  # Type
            ', '.join(
                [component.name for component in issue.fields.components[:]]
            ),  # 支持获取issue的多个component
            issue.fields.customfield_13800,  # issue_VOD
            issue.fields.customfield_14221.split('\n')[
                1
            ],  # 返回5个str类型URL选取第二个 issue_replay
            issue.fields.customfield_11976.value,  # 查看Is Release Blocker
            issue.fields.customfield_13904,  # RC
            issue.fields.customfield_10700,  # 车号
            issue.fields.customfield_16501[:] if issue.fields.customfield_16501 else '',  # 车型
            # 修改访问自定义字段的方式以避免NoneType错误
            issue.fields.customfield_14203[0]
            if issue.fields.customfield_14203
            else '',  # Operation Area
            issue.fields.customfield_10317.value,  # TripType
            # print(issue.key + ' 已添加到飞书表格'),
        ]
        for issue in issues
    ]
    # 插入数据到飞书：注意是先删除表内原数据再插入
    insert_data_to_larksheet(lark_tenant_access_token, spreadsheetToken, data_to_insert)
    print('输入已插入，请前往飞书查看')


if __name__ == '__main__':
    main()
