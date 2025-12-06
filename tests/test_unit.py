import os
import datetime
from models import Task, User
from app import multiple_of_2


def test_task_overdue():
    due_date = datetime.date.today() - datetime.timedelta(hours = 10)
    task = Task(title = "Test_date", due_date = due_date)
    
    assert task.is_overdue() is False
    
def test_password_hashing():
    user = User(username = "hugo")
    user.set_password("hugoefrei")

    assert user.check_password("hugoefrei") is True
    assert user.check_password("test_tp123") is False

def test_multiple_of_2():
    assert multiple_of_2(4) == True
    assert multiple_of_2(5) == False