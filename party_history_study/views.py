'''
Author: sky-eve-yang
Date: 2023-03-09 19:08:24
LastEditTime: 2023-03-12 15:36:38
LastEditors: sky 1326906378@qq.com
Description: 视图逻辑
FilePath: \django-vue-admin\backend\party_history_study\views.py
 
'''
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from party_history_study.models import partyHistoryStudy
from party_history_study.serializers import PartyHistoryStudyStatisticsSerializer,partyHistoryStudyExportSerializer,partyHistoryStudySerializer, partyHistoryStudyCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.db import connection
from rest_framework.views import APIView
from dvadmin.utils.permission import AnonymousUserPermission
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.system.models import Dept
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class partyHistoryStudyViewSet(viewsets.ModelViewSet):
    """
    list: 查询
    create: 新增
    update: 更新
    retrieve: 单例
    destroy: 删除
    approve: 审核通过
    reject: 审核驳回
    """

    queryset = partyHistoryStudy.objects.all()
    serializer_class = partyHistoryStudySerializer
    create_serializer_class = partyHistoryStudyCreateUpdateSerializer
    update_serializer_class = partyHistoryStudyCreateUpdateSerializer
    filter_fields = ['meeting_theme', 'class_name', 'college_name', 'grade']
    search_fields = ['meeting_theme', 'class_name', 'college_name', 'grade']
    export_field_label = [
        '会议主题', '会议时间', '会议地点', '参会人数', '班级名称', '学院', '年级', '会议图片', '审核结果'
    ]
    export_serializer_class = partyHistoryStudyExportSerializer

    def get_queryset(self):
        # 调用父类的 get_queryset 方法获取基础查询集
        queryset = super().get_queryset()

        # 获取当前请求的用户
        user = self.request.user
        print("user", user)

        # 如果用户是超级用户，则不应用任何过滤
        if user.is_superuser:
            return queryset

        # 假设每个 PartyHistoryStudy 对象都有一个 'department' 外键
        # 这里我们使用自定义的查询来限制查询集
        # 只包含用户所在部门及以下的记录
        department_id = user.dept.id  # 假设用户有一个 'department' 属性
        print("department_id", department_id)
        
        
        # 根据用户部门过滤查询集
        # 这里需要根据你的实际模型和数据库结构来编写过滤逻辑
        # 以下是一个示例，可能需要根据你的具体情况进行调整
        # 假设 Department 模型有一个递归的 'descendants' 方法
        department_ids = Dept.recursion_dept_info(department_id)
        print("department_ids", department_ids)

        # 应用过滤
        print(queryset[0].__dict__)
        return queryset.filter(dept_belong_id__in=department_ids)

    @action(methods=['put'], detail=True, permission_classes=[AnonymousUserPermission])
    def approve(self, request, pk=None):
        post = self.get_object()
        post.audit_results = 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, permission_classes=[AnonymousUserPermission])
    def reject(self, request, pk=None):
        post = self.get_object()
        post.audit_results = 0
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

# 原始的，不加部门过滤器的
# class partyHistoryStudyViewSet(CustomModelViewSet):
#     """
#     list: 查询
#     create: 新增
#     update: 更新
#     retrieve: 单例
#     destory: 删除
#     approve: 审核通过
#     reject: 审核驳回
#     """

#     queryset = partyHistoryStudy.objects.all()
#     serializer_class = partyHistoryStudySerializer
#     create_serializer_class = partyHistoryStudyCreateUpdateSerializer
#     update_serializer_class = partyHistoryStudyCreateUpdateSerializer
#     filter_fields = ['meeting_theme', 'class_name', 'college_name', 'grade']
#     search_fields = ['meeting_theme', 'class_name', 'college_name', 'grade']


#     #导出
#     export_field_label = ['会议主题', '会议时间','会议地点', '参会人数', '班级名称', '学院', '年级', '会议图片', '审核结果']
#     export_serializer_class = partyHistoryStudyExportSerializer

#     @action(methods=['put'], detail=True, permission_classes=[AnonymousUserPermission])
#     def approve(self, request, pk=None):
#         post = self.get_object()
#         post.audit_results = 1
#         post.save()
#         serializer = self.get_serializer(post)
#         return Response(serializer.data)

#     @action(methods=['put'], detail=True, permission_classes=[AnonymousUserPermission])
#     def reject(self, request, pk=None):
#         post = self.get_object()
#         post.audit_results = 0
#         post.save()
#         serializer = self.get_serializer(post)
#         return Response(serializer.data)
    
    

class partyHistoryStudyStatisticsViewSet(CustomModelViewSet):
    """
    list: 查询
    """

    filter_fields = ['meeting_time', 'meeting_theme', 'class_name', 'college_name', 'grade']
    search_fields = ['meeting_time', 'meeting_theme', 'class_name', 'college_name', 'grade']


    queryset = partyHistoryStudy.objects.all()
    serializer_class = PartyHistoryStudyStatisticsSerializer

    
    def list(self, request, *args, **kwargs):
        # 如果懒加载，则只返回父级
        params = request.query_params
        year_month = params.get('year_month', '2000-01')
        college_name = params.get('college_name', Dept.objects.get(id=request.user.dept_id).name)
        search_grade = params.get('grade', '')
        class_name = params.get('class_name', '')
        
        # 1. 获取指定月份、年级、学院的所有“存在数据”，并将数据序列化，转化为JSON格式
        # 2. 获取当前用户的所有子部门
        if search_grade:
            queryset = self.queryset.filter(meeting_time__contains=year_month, college_name=college_name, grade=search_grade)
            dept_children_queryset = Dept.objects.filter(parent_id=request.user.dept_id, key__contains=search_grade).values('name')
        else:
            queryset = self.queryset.filter(meeting_time__contains=year_month, college_name=college_name)
            dept_children_queryset = Dept.objects.filter(parent_id=request.user.dept_id).values('name')
        
        serializer = PartyHistoryStudyStatisticsSerializer(queryset, many=True, request=request)
        
        if(len(serializer.data) == 0):
            return DetailResponse(data={'data': []}, msg='无数据')
        
        dept_children_name = [i['name'] for i in dept_children_queryset]
        exits_data = serializer.data



        # 遍历子部门列表，查看“存在数据”中是否有该子部门的数据，
        # 有则将对应子部门的“存在数据项”的is_submitted字段置为True
        # 无则将对应子部门的“存在数据项”的is_submitted字段置为False

        for class_name in dept_children_name:
            filtered_data = [data for data in exits_data if data['class_name'] == class_name]

            if filtered_data:
                filtered_data[0]['is_submitted'] = True
            else:
                exits_data.append({
                    'meeting_time': '',
                    'meeting_theme': '',
                    'class_name': class_name,
                    'college_name': college_name,
                    'grade': class_name[:4],
                    'is_submitted': False
                })
                

        
        print(exits_data)
        return DetailResponse(data={'data': exits_data}, msg='获取成功')

