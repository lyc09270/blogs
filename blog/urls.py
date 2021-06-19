from django.urls import path
from . import views
#from .views import IndexView

app_name='blogs'
urlpatterns = [
#    path('',views.index,name='index'),
#    path('posts/<int:pk>/',views.detail,name='detail'),
#    path('test',views.test,name='test'),
 #   path('archives/<int:year>/<int:month>',views.archive,name='archive'),
#    path('category/<int:pk>',views.category,name='category'),
 #   path('tags/<int:pk>',views.tag,name='tag'),
    path('', views.IndexView.as_view(), name='index'),
    path('categories/<int:pk>/',views.CategoryView.as_view(),name='category'),
    path('tags/<int:pk>',views.TagView.as_view(),name='tag'),
    path('archives/<int:year>/<int:month>',views.ArchiveView.as_view(),name='archive'),
    path('posts/<int:pk>/', views.PostDetaiView.as_view(), name='detail'),
    path('search/',views.search, name='search'),
]