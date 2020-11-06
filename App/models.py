from django.contrib.auth.hashers import make_password, check_password
from django.db import models

f_status_convert = {
    0: '新建',
    1: '已提交',
    2: '已审批',
    3: '已退回',
    4: '已作废'
}


# Create your models here.
class ImeiForm(models.Model):
    f_title = models.CharField(max_length=128)
    f_content = models.CharField(max_length=500)
    f_createman = models.CharField(max_length=16)
    f_createtime = models.DateTimeField(auto_now_add=True)
    f_lastmodifytime = models.DateTimeField(auto_now=True)
    f_lastdealman = models.CharField(max_length=16)
    f_dealman = models.CharField(max_length=16, default="", blank=True)
    f_type = models.CharField(max_length=16, null=True)
    _f_status = models.SmallIntegerField(default=0)

    @property
    def f_status(self):
        statusint = self._f_status
        return f_status_convert.get(statusint)

    @f_status.setter
    def f_status(self, input_value):
        self._f_status = input_value

    class Meta:
        db_table = 'imeiform'


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    mobile_number = models.IntegerField()
    _password = models.CharField(max_length=500)

    @property
    def password(self):
        raise Exception("cant access")

    @password.setter
    def password(self, password_value):
        self._password = make_password(password_value)

    def check_password(self, password_value):
        return check_password(password_value, self._password)

    class Meta:
        db_table = 'user'


class DealRecorde(models.Model):
    dealman = models.CharField(max_length=32)
    dealtime = models.DateTimeField(auto_now_add=True)
    dealcontent = models.CharField(max_length=500)
    form = models.ForeignKey(ImeiForm, related_name='form_dealrec', on_delete=models.CASCADE)

    class Meta:
        db_table = 'deal_recorde'


class Attachment(models.Model):
    uploadman = models.CharField(max_length=32)
    uploadfile = models.FileField(upload_to='attach/%Y/%m/%d/')
    uploadtime = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(ImeiForm, related_name='form_attach', on_delete=models.CASCADE, default='')

    @property
    def filename(self):
        filename = self.uploadfile.__str__()
        filename = filename.split('/')
        return filename[-1]

    class Meta:
        db_table = 'attachments'
