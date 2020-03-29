from django.db import models


# Create your models here.

# 存储用户上传图片的信息
class Image(models.Model):
    img_url = models.CharField(max_length=128, unique=True)
    hash_code = models.CharField(max_length=128)
    upload_date = models.DateTimeField('upload time')
    # d_hamming = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.img_url

    '''
    class Meta:
        ordering = ['d_hamming']
    '''
