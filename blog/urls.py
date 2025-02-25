from django.urls import path
from .views import * # ShowAllView, ArticleView, RandomArticleView

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'), 
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    # path('create_comment', CreateCommentView.as_view(), name ='create_comment'), ### FIRST (WITHOUT PK)
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
]