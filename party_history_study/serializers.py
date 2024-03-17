'''
Author: sky-eve-yang
Date: 2023-03-09 19:52:53
LastEditTime: 2023-03-12 15:35:31
LastEditors: sky 1326906378@qq.com
Description: 
FilePath: \django-vue-admin\backend\party_history_study\serializers.py

'''

from party_history_study.models import partyHistoryStudy
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework import serializers

 
class partyHistoryStudySerializer(CustomModelSerializer):
    """
    序列化器
    """
    
    class Meta:
        fields = "__all__"
        model = partyHistoryStudy
        


class partyHistoryStudyCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的序列化器
    """
    

    class Meta:
        fields = '__all__'
        model = partyHistoryStudy


class partyHistoryStudyExportSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    # last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # dept__deptName = serializers.CharField(source='dept.deptName', default='')
    # dept__owner = serializers.CharField(source='dept.owner', default='')
    # gender = serializers.CharField(source='get_gender_display',read_only=True)

    class Meta:
        model = partyHistoryStudy
        fields = ( 'meeting_theme', 'meeting_time', 'meeting_place', 'number_participants', 'class_name', 'college_name', 'grade', 'metting_images', 'audit_results')


class PartyHistoryStudyStatisticsSerializer(serializers.ModelSerializer):
    """
    统计序列化器
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = partyHistoryStudy
        fields = ('meeting_theme', 'meeting_time', 'meeting_place', 'number_participants', 'class_name', 'college_name', 'grade', 'metting_images', 'audit_results')
        read_only_fields = ('meeting_theme', 'meeting_time', 'meeting_place', 'number_participants', 'class_name', 'college_name', 'grade', 'metting_images', 'audit_results')
        # 依据grade进行降序排列
        ordering = ['-grade', '-meeting_time']