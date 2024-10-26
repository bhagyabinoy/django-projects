from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
    path('', views.studentview, name='studentview'),
    path('studentlist/', StudentList.as_view(),name='student-list'),
    path('studcreate/', views.studentcreateview, name='studentcreateview'),
    path('dashboard/', views.dashboardview, name='dashboard'),
    path('attendance/', views.attendanceview, name='attendanceview'),
    path('markattendance/', views.markattendanceview, name='markattendanceview'),
    path('student/create/', StudentCreate.as_view(),name='student-create'),
    path('student/detail/<int:pk>/', StudentDetail.as_view(),name='student-detail'),
    path('student/update/<int:pk>/', UpdateStudent.as_view(),name='student-update'),
    path('student/delete/<int:pk>/', DeleteStudent.as_view(),name='student-delete'),
    path('studentfilter/', views.StudentFilter.as_view(), name='filter-standard-class-bloodgroup'),
    path('student/total/', TotalStudentCounter.as_view(),name='total-counter'),
    path('student/active/', ActiveStudentCounter.as_view(),name='student-counter'),
    
    path('attendancelist/', AttendanceList.as_view(),name='attendance-list'),
    path('attendancefilter/', views.AttendanceFilter.as_view(), name='filter-attendance'),
    path('attendancecreate/', AttendanceCreate.as_view(),name='attendance-create'),
    path('attendanceupdate/<int:pk>/', AttendanceUpdate.as_view(),name='attendance-update'),
    path('attendancedelete/<int:pk>/', AttendanceDelete.as_view(),name='attendance-delete'),
]