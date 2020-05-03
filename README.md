# 《公主连结Re:Dive》(国服)公会战排刀系统 - 后端

方便公会里的排刀人~~工具人~~排刀的系统。目前为预览版，更多功能等待后续添加。
[前端地址](https://github.com/CJowo/pcr-guild-vue)

### 使用方法

安装依赖：

`pip install -r requirements.txt`

数据库迁移:

`python manage.py makemigrations`
`python manage.py migrate`

关闭调试模式:

```python
# /pcr/settings.py

...

DEBUG = False

...
```

设置其他服务器或使用开发服务器 `python manage.py runserver 0.0.0.0:80`