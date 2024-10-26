from django.urls import path
from .views import ApplyLeaveView, ApproveLeaveView

urlpatterns = [
    path('apply/', ApplyLeaveView.as_view(), name='apply-leave'),
    path('approve/<int:leave_id>/', ApproveLeaveView.as_view(), name='approve-leave'),
]
