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