import json

original_data = []


def cleanse_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        item['分区'] = [value.replace('"', '') for value in item['分区']]
        '''
    合并后面小类,分析json文件发现小类会成为单独的一行
    例如:
        "小类": "COMPUTER SCIENCE, HARDWARE & ARCHITECTURE 计算机：硬件",
        "COMPUTER SCIENCE, INFORMATION SYSTEMS 计算机：信息系统": "",
        "OPTICS 光学": "",
        "TELECOMMUNICATIONS 电信学": ""
    合并最后几项的key到小类的value中,用管道符'|'隔开
        '''
        while True:
            last_key = list(item.keys())[-1]
            if last_key != '小类':
                item.pop(last_key)
                item['小类'] += '|' + last_key
            else:
                break
        # 文件中json倒数第三个 为"": "学科",
        third_last_key = list(item.keys())[-3]
        # 倒数第四行为垃圾信息,其中有一项是否为top期刊,判读字符中是否含有字符'是'
        fourth_last_key = list(item.keys())[-4]
        if third_last_key == '':
            item.pop(third_last_key)
        if '是' in fourth_last_key:
            item['Top期刊'] = 1
        else:
            item['Top期刊'] = 0
        item.pop(fourth_last_key)
        original_data.append(item)
    # print(fourth_last_key + "\n*******\n")


if __name__ == '__main__':
    for i in range(11):
        cleanse_data('data{}.json'.format(i))
    with open('original_data.json', 'w', encoding='utf-8') as f:
        json.dump(original_data, f, ensure_ascii=False, indent=4)
    print(original_data)

    # 转化为excel
    import pandas as pd

    df = pd.read_json('original_data.json')
    df.to_excel('original_data.xlsx', index=False)
