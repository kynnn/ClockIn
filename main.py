import json
import time
import random
import requests


# 输入Secrets
stu_name = input()
stu_id = input()
dept_text = input()
sc_url = input()


def main():
    """
    主函数
    """
    # 获取deptId
    class_id = 80035

    # 时间判断 Github Actions采用国际标准时
    hms = update_time()
    if (hms[0] >= 18) & (hms[0] < 22):
        customer_app_type_rule_id = 148
    else:
        print("现在是%d点%d分，将打卡早间档测试" % (hms[0], hms[1]))
        customer_app_type_rule_id = 146

    # 随机温度(36.2~36.5)
    a = random.uniform(36.2, 36.5)
    temperature = round(a, 1)

    check_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

    check_json = {
        "businessType": "epmpics",
        "method": "submitUpInfo",
        "jsonData": {
            "deptStr": {
                "text": dept_text,
                "deptid": class_id
            },
            "areaStr": {"streetNumber": "", "street": "X242", "district": "仙游县", "city": "莆田市", "province": "福建省",
                        "town": "", "pois": "仙游度尾艺龙阁古典家具馆", "lng": 118.588836 + random.random() / 10000,
                        "lat": 25.399884 + random.random() / 10000, "address": "仙游县X242仙游度尾艺龙阁古典家具馆",
                        "text": "福建省-莆田市", "code": ""},
            "reportdate": round(time.time() * 1000),
            "customerid": 786,
            "deptid": class_id,
            "source": "app",
            "templateid": "pneumonia",
            "stuNo": stu_id,
            "username": stu_name,
            "userid": 6778027,
            "updatainfo": [
                {
                    "propertyname": "temperature",
                    "value": temperature
                },
                {
                    "propertyname": "symptom",
                    "value": "无症状"
                },
                {
                    "propertyname": "isConfirmed",
                    "value": "否"
                },
                {
                    "propertyname": "isdefinde",
                    "value": "否.未隔离"
                },
                {
                    "propertyname": "isGoWarningAdress",
                    "value": "否"
                },
                {
                    "propertyname": "isTouch",
                    "value": "否"
                },
                {
                    "propertyname": "isFFHasSymptom",
                    "value": "没有"
                },
                {
                    "propertyname": "isContactFriendIn14",
                    "value": "没有"
                },
                {
                    "propertyname": "xinqing",
                    "value": "健康"
                },
                {
                    "propertyname": "bodyzk",
                    "value": "否"
                },
                {
                    "propertyname": "cxjh",
                    "value": "否"
                },
                {
                    "propertyname": "isleaveaddress",
                    "value": "否"
                },
                {
                    "propertyname": "gtjz0511",
                    "value": "否"
                },
                {
                    "propertyname": "medicalObservation",
                    "value": "绿色"
                },
                {
                    "propertyname": "ownPhone",
                    "value": "13789098759"
                },
                {
                    "propertyname": "emergencyContact",
                    "value": "吴金梅"
                },
                {
                    "propertyname": "mergencyPeoplePhone",
                    "value": "15260945412"
                },
                {
                    "propertyname": "assistRemark",
                    "value": ""
                }
            ],
            "gpsType": 1,
            "token": "53793692-b7a8-4238-9e34-0a27c14a6bb3",
            "customerAppTypeRuleId": customer_app_type_rule_id,
            "clockState": 0
        },
    }

    # 提交打卡与结果判定
    flag = 0
    for i in range(1, 10):
        hms = update_time()
        response = requests.post(check_url, json=check_json)
        if response.status_code == 200:
            flag = 1
            break
        else:
            time.sleep(60)
    print(response.text)
    time_msg = str(hms[0]) + '时' + str(hms[1]) + '分' + str(hms[0]) + '秒'
    if flag == 1:
        if response.json()["msg"] == '成功':
            msg = time_msg + '时' + "打卡成功"
        else:
            msg = time_msg + "打卡异常"
    else:
        msg = time_msg + "网络错误打卡失败"

    print(msg)

    # 微信通知
    title = msg
    result = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    content = f"""
    ```
    {result}
    ```
    """
    data = {
        "text": title,
        "desp": content
    }
    requests.post(sc_url, data=data)


def print_info_error():
    """
    打印 个人信息错误
    """
    print('请检查你填写的学院、专业、班级信息！')
    print('见完美校园健康打卡页面')
    print('如 理学院-应用物理学-应物1901')


def update_time():
    return [(time.localtime().tm_hour + 8) % 24,
            time.localtime().tm_min,
            time.localtime().tm_sec]


if __name__ == '__main__':
    main()