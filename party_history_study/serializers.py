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
        
    def get_queryset(self):
        # 调用父类的 get_queryset 方法获取基础查询集
        queryset = super().get_queryset()
        # 获取当前请求的用户
        user = self.context['request'].user
        print(user)

        # 如果用户是超级用户，则不应用任何过滤
        if user.is_superuser:
            return queryset

        # 假设每个 PartyHistoryStudy 对象都有一个 'department' 字段
        # 这里我们使用自定义的查询来限制查询集
        # 只包含用户所在部门及以下的记录
        department = user.department  # 假设用户有一个 'department' 属性
        subquery = Department.objects.filter(id__in=department.get_descendants(include_self=True)).values('id')

        # 使用 Subquery 来过滤 PartyHistoryStudy 对象
        return queryset.filter(department__in=subquery)


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