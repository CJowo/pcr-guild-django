### 公主连结ReDive公会战系统
公主连结ReDive公会战系统，旨在使公会管理更加简洁高效。

功能列表:

已实现

- [x] 多公会共用
- [x] 成员BOX收集（截图自动识别BOX测试中）
- [x] 公会成员Box过滤
- [x] 公会战报刀，每日出刀统计

目前正在开发

- [ ] BOX角色排序
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
