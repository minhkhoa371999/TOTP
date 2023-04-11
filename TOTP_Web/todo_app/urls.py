# todo_list/todo_app/urls.py
from django.urls import path
# todo_list/todo_app/urls.py
from todo_app import views

app_name = 'todo_app'
urlpatterns = [
    path("todo_list/",
         views.ListListView.as_view(), name="todo_list"),
    path("list/<int:list_id>/",
         views.ItemListView.as_view(), name="list"),
    # CRUD patterns for ToDoLists
    path("list/add/", views.ListCreate.as_view(), name="list_add"),
    path(
        "list/<int:pk>/delete/", views.ListDelete.as_view(), name="list_delete"
    ),
    # CRUD patterns for ToDoItems
    path(
        "list/<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name="item_add",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name="item_update",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name="item_delete",
    ),
]
