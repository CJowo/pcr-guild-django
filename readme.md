### 公主连结ReDive公会战系统
公主连结ReDive公会战系统，旨在使公会管理更加简洁高效。

功能列表:

已实现

- [x] 多公会共用
- [x] 成员BOX收集（截图自动识别BOX测试中）
- [x] 公会成员Box过滤
- [x] 公会战报刀，每日出刀统计

目前正在开发

- [ ] 公会战作业轴上传查看
- [ ] 公会战出刀结果完全统计
- [ ] 报错信息优化

欢迎提出任何建议或意见

### 将编译后的前端文件放入后端vue文件夹中

使用django自带的开发服务器并非最好的选择，推荐使用其他专业服务器


### 安装依赖

`> pip install -r requirements.txt`



### 迁移数据库

`> python manage.py makemigrations`

`> python manage.py migrate`



### 启动后端

`> python manage.py runserver 0.0.0.0:80`


默认管理密码 administrator

### 重置管理密码(需要安装sqlite)

`> python manage.py dbshell`

`sqlite> UPDATE admin_admin SET password = '新密码';`

`sqlite> .quit`


### 游戏截图识别BOX(测试)

RANK识别功能需要使用百度OCR，在[百度AI开放平台](https://ai.baidu.com/tech/ocr/general)创建通用文字识别应用，并将`APP_ID`, `API_KEY`, `SECRET_KEY`填入管理页面。

不填则只进行星级和角色识别，RANK默认为0。

目前人物列表不全，数量约为国服人物数量。

暂未对除国服以外的其他服截图进行测试，效果不确定。