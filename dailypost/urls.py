from django.conf.urls import url

from . import views


app_name='dailypost'
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'),
    url(r'^post/archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^post/category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^post/search/$',views.search,name='search'),
    url(r'^post/archives/(?P<year>[0-9]{4})/$',views.ArchivesYearView.as_view(),name='archives_year'),
    url(r'^post/hidden/$',views.HiddenIndexView.as_view(),name='hidden_index'),
    url(r'^post/hidden/(?P<pk>[0-9]+)/$',views.HiddenPostDetailView.as_view(),name='hidden_detail'),
]