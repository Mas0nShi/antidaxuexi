# anti daxuexi

一键生成通知模板以通知全体团支书，及时进行大学习任务

## 功能
 - 获取答案
 - 检测更新
 - 生成通知

## 原理

 解析网页元素

## TODO
 - 排序类题型

## 适用平台

- ✅ 青春浙江

## 使用方式

```shell
pip install antidxx -i https://pypi.org/simple

antidxx
```

## 预览

![img.png](screenshot.png)

## 自定义

antidxx的模板在`site-packages/antidxx/template`目录下


| 文件名          | 描述   | 格式                                               |
|--------------|------|--------------------------------------------------|
| message.txt  | 消息模板 | 格式化关键字：`{title}`、`{date}`、`{staffs}`、`{answers}` |
| sections.txt | 年级段  | 一行一个                                             |
| staffs.txt   | 人员列表 | 一行一个组合，最后一行为0   A\|B       |



## 更多
 ~~[Android下大学习摸鱼方案](https://blog.shi1011.cn/persummary/1614)~~ 微信版本更新后，x5内核已被删除