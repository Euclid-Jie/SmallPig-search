# 爬取小猪民宿信息

此工作基本实现小猪网页版https://m.xiaozhu.com/，基本信息的获取，包括民宿的房东信息和民宿的评价信息，需要使用到`selenium`方法

## 代码结构

```python
获取民宿列表.py # 获取指定城市的民宿列表（后两个流程的基础）
获取房东信息.py # 获取民宿的房客评价信息
获取评价信息.py # 获取民宿的房东自我介绍
```

## 输出参数

只要在执行第一个流程时，需要输入参数；

两个参数一一对应，可以在小猪网页版尝试搜索某城市后，观测网址获得，网址示例：

```tex
https://m.xiaozhu.com/#/result?cityId=272&city=揭阳市&landmark=&timeZone=&checkInDay=2022-10-27&checkOutDay=2022-10-28
```

- 城市名称，格式为`str`

  ```python
  city = '揭阳市'
  ```

- 城市编码，格式为`str`

  ```python 
  cityId = '272'
  ```

## 调用方式

修改参数后直接运行即可调用，输入保存为`csv`文件

## 输出内容

三个流程各有一个输出，输出文件的列名在此一起进行说明

| 名称                     | 含义                                             |
| ------------------------ | ------------------------------------------------ |
| `id`、`luid`、`roomLuid` | 小猪民宿编号，每个民宿编号唯一，不同文件列名不同 |
| `title`                  | 民宿名称                                         |
| 个性描述                 | 房东对民宿的描述（为空即为没有描述，下同）       |
| 内部情况                 | 房东对民宿的内部情况描述                         |
| 交通情况                 | 房东对民宿的交通情况描述                         |
| `content`                | 房客对民宿的评价内容                             |
| `time`                   | 房客对民宿的评价时间                             |

## 注意事项

- 数据采集过程中，请勿关闭弹出浏览器窗口
- 各民宿信息主页可以访问https://m.xiaozhu.com/#/detail?luId=152118827297访问，修改`luid`即可

- 此工作无需设置`header`，但请务必保证网速良好
- 此项目较为成熟，如有问题欢迎`Issues`