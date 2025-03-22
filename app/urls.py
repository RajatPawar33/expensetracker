
from django.urls import path
from app.views import index, deleteTransaction, registration, login_page, logout_page

urlpatterns = [
    path('', login_page , name="login_page"),
    path('index/', index, name="index"),
    path('registration/', registration , name="registration"),
    path('logout/', logout_page , name="logout_page"),
    path('delete-tranaction/<uuid>', deleteTransaction, name="deleteTransaction")
]