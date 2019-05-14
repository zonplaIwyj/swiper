import datetime

from django.db import models

# Create your models here.


class User(models.Model):
    """
    定义用户模型

    """
    SEX = (
        ('female', '女'),
        ('male', '男')
    )
    phonenum = models.CharField(max_length=20, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=100, verbose_name='昵称', unique=True)
    sex = models.CharField(choices=SEX,verbose_name='性别', max_length=10)
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=64, verbose_name='常居地')

    def __str__(self):
        return f'<User {self.nickname}>'

    @property
    def age(self):
        today = datetime.datetime.today()
        birthday = datetime.datetime(year=self.birth_year,
                                 month=self.birth_month, day=self.birth_day)
        return (today - birthday).days // 365

    def to_dict(self):
        return {
            "phonenum": self.phonenum,
            "nickname": self.nickname,
            "sex": self.sex,
            "age": self.age,
            "avatar": self.avatar,
            "location": self.location,
        }

    class Meta:
        db_table = 'user'
