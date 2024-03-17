from django.db import models

# Create your models here.
from dvadmin.utils.models import CoreModel

class partyHistoryStudy(CoreModel):
    meeting_theme = models.CharField(max_length=255, verbose_name="会议主题")
    meeting_time = models.DateTimeField(verbose_name="会议时间") 
    meeting_place = models.CharField(max_length=255, verbose_name="会议地点")
    number_participants = models.IntegerField(verbose_name="参会人数")
    class_name = models.CharField(max_length=255,verbose_name="班级名称") 
    college_name = models.CharField(max_length=255, verbose_name="学院") 
    grade = models.IntegerField(verbose_name="年级") 
    metting_images = models.CharField(max_length=255, verbose_name="会议图片", help_text="会议图片")
    audit_results = models.IntegerField(default=-1, verbose_name="审核结果")

    class Meta:
        db_table = "party_history_study" 
        verbose_name = "党史学习记录表"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)