## 任务
links.json中有501条链接,每条所耗费的时间大概为20s-30s,
将links.json中的链接分成三段,即501/3=167条数据


```python
#读取links.json文件
with open('links.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
```

```python
# 这是循环迭代的代码,需要改的是data的迭代位置,例如1-167 ,168-334, 334-501
 for idx, (link, journal) in tqdm(enumerate(data.items()), total=len(data), desc="Processing links"):
        print(link, journal)
        get_Collection(driver, link)
        if idx % 50 == 0:
            name = int(idx / 50)
            with open('data/data{}.json'.format(name), 'w', encoding='utf-8') as f:
                json.dump(original_data, f, ensure_ascii=False, indent=4)
            # 重置original_data,每50条重置一次,防止占用内存
            original_data = []
```
运行过程中在data文件夹中生成data0.json、data1.json....
> 函数Login_operation()执行登录操作并返回driver
> 

> 函数get_Collection()是主要获取页面内容

这段代码耗时最长,是用来获取html中隐式表达
```python
    script = f"""
    return window.getComputedStyle(document.querySelector('span.{class_value}'), '::before').getPropertyValue('content');
    """
    pseudo_element_content = driver.execute_script(script)
    partition.append(pseudo_element_content)
```


