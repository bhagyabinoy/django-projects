from django.urls import path
from .views import *



urlpatterns = [
    
    #----category-urls----
    path('category/list/', CategoryList.as_view(),name='Category_list'),
    path('category/create/', CategoryCreate.as_view(),name='Category_create'),
    path('category/detail/<int:pk>/', CategoryDetail.as_view(),name='Category_detail'),
    path('category/update/<int:pk>/', CategoryUpdate.as_view(),name='Category_update'),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(),name='Category_delete'),

    #----food-urls----
    path('list/', FoodList.as_view(),name='Food_list'),
    path('create/', FoodCreate.as_view(),name='Food_create'),
    path('detail/<int:pk>/', FoodDetail.as_view(),name='Food_detail'),
    path('update/<int:pk>/', FoodUpdate.as_view(),name='Food_update'),
    path('delete/<int:pk>/', FoodDelete.as_view(),name='Food_delete'),

    #----filter-urls----
    path('filter/category/', CategoryFilter.as_view(), name='CategoryFilter'),
    path('caloryless/', Caloryless.as_view(), name='CategoryFilter'),
    path('calorygt/', CaloryGt.as_view(), name='CategoryFilter'),
    path('calrange/', CaloryRange.as_view(), name='CategoryFilter'),
    path('searchbyname/', SearchFood.as_view(), name='Search name'),

    #----bulk create-urls----
    path('bulkcreate/', Bulkcreate.as_view(), name='bulkcreate'), 

    #----pdf-urls----
    path('pdf/', Convert_pdf_foodlist.as_view(), name='Convert_pdf_foodlist'),
    path('pdf/category/', Convert_pdf_by_category.as_view(), name='Convert_pdf_foodlist'),
    path('pdf/calorieless/', Convert_pdf_by_calorieless.as_view(), name='Convert_pdf_foodlist'),
    path('pdf/caloriegt/', Convert_pdf_by_caloriegt.as_view(), name='Convert_pdf_foodlist'),
    path('pdf/range/', Convert_pdf_by_calorierange.as_view(), name='Convert_pdf_foodlist'),  

    #----word document----
    path('word-document/', WordDocumentView.as_view(), name='word-document'),

    #----TEMPLATE URLS----
    path('listview/',foodlistpage, name='foodlistpage'),
    path('add/',addfoodpage, name='addfoodpage'),
    path('bulkcreatepage/',bulkcreatepage, name='bulkcreatepage'),

]
