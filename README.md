## models
使用`filter`查询时 需要条件时 需要加两个下划线`__`进行查询

## views
1. `<slug:post>`则会被转换成一个名称为post，值为slug类型（仅有ASCII字符或数字，减号，下划线组成的字符串）的变量传给视图。
2. django2.0 反向解析就1.2 来说变化很大 需读官方文档

## 基于类视图CBV
1. 相比基于函数视图FBV
>可编写单独的方法对应不同的HTTP请求类型如GET，POST，PUT等请求，不像FBV一样需要使用分支
使用多继承创建可复用的类模块（也叫做mixins）

## 数据库查询
> 表之间的关系
1. many_to_one
2. one_to_many 
3. many_to_many

## 模板过滤器
1. pluralize 根据数据显示复数词尾
2. if for 
3. 也能自定义模板标签

## 发送邮件
1. QQ邮箱中端口号最好为587 这样不会和阿里云服务器冲突
2. 将TLS开启
3. 

## Django中的站点地图

## 搜索
1. 通过Search_Vector(name,weight='A')weight设置权重DCBA 对应0.1 0.2 0.4 1 
2. 三元相似性搜索