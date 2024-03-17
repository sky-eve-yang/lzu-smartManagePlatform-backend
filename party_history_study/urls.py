'''
Author: sky-eve-yang
Date: 2023-03-09 20:04:35
LastEditTime: 2023-03-12 15:36:55
LastEditors: sky 1326906378@qq.com
Description: 配置路由文件


''' 
from django.urls import path, re_path

from rest_framework.routers import SimpleRouter
from .views import partyHistoryStudyViewSet, partyHistoryStudyStatisticsViewSet

router = SimpleRouter()
router.register("api/party_history_study", partyHistoryStudyViewSet)
router.register("api/party_history_study_statistics", partyHistoryStudyStatisticsViewSet)

urlpatterns = [
    re_path('user/export/', partyHistoryStudyViewSet.as_view({'get': 'export_data', })),
]

urlpatterns += router.urls

