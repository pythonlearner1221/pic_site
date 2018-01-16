from django.conf.urls import url

from .views import IndexView,ArchivesView,CategoryView,search,HiddenView,ArchivesYearView,PrettyView,random_post,PrettyCategoryView,random_category,choose,choose_tag


app_name='pics'
urlpatterns=[
    url(r'^pics/$', IndexView.as_view(),name='pics'),
    url(r'^pics/archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',ArchivesView.as_view(),name='archives'),
    url(r'^pics/search/$',search,name='search'),
    url(r'^pics/category/(?P<category>[a-z]+)/$',CategoryView.as_view(),name='category'),
    url(r'^pics/hidden/$',HiddenView.as_view(),name='hidden'),
    url(r'^pics/archives/(?P<year>[0-9]{4})/$',ArchivesYearView.as_view(),name='archives_year'),
    url(r'^pics/pretty/$', PrettyView.as_view(), name='pretty'),
    url(r'^pics/pretty/category/(?P<category>[a-z]+)/$',PrettyCategoryView.as_view(),name='pretty_category'),
    url(r'^pics/random/$',random_post,name='random'),
    url(r'^pics/random/category/(?P<category>[a-z]+)/$',random_category,name='random_category'),
    url(r'^pics/choose/(?P<tag>[0-9]+)/$', choose_tag, name='choose_tag'),
    url(r'^pics/choose/$',choose,name='choose'),

]