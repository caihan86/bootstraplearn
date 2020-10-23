from django.db import models

f_status_convert = {
    0: '新建',
    1: '已提交',
    2: '处理中',
    3: '已审批',
    4: '已退回',
    5: '已作废'
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
    _f_status = models.SmallIntegerField()

    @property
    def f_status(self):
        statusint = self._f_status
        return f_status_convert.get(statusint)

    @f_status.setter
    def f_status(self, input_value):
        self._f_status = input_value

    class Meta:
        db_table = 'imeiform'
