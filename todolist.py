from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    task_input = input("Enter task\n")
    deadline_input = datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d')
    new_row = Table(task=task_input, deadline=datetime.date(deadline_input))
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def todays_task():
    print("Today", datetime.today().day, datetime.today().strftime('%b') + ":")
    result = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if not result:
        print("Nothing to do!")
    else:
        for i, row in enumerate(result, 1):
            print(i, '.', row, sep="")


def weeks_task():
    for x in range(0, 7):
        date = datetime.today().date() + timedelta(days=x)
        print("\n" + date.strftime('%A'), date.day, date.strftime('%b'), end=":\n")
        result = session.query(Table).filter(Table.deadline == date).all()
        if not result:
            print("Nothing to do!")
        else:
            for i, row in enumerate(result, 1):
                print(i, '. ', row, sep="")


def all_tasks():
    result = session.query(Table).order_by(Table.deadline).all()
    if result:
        for i, row in enumerate(result, 1):
            print(i, '. ', row, '. ', row.deadline.day, ' ', row.deadline.strftime('%b') + ".", sep="")
    else:
        print("Nothing to do!")


def missed_task():
    print("Missed tasks:")
    result = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if result:
        for i, row in enumerate(result, 1):
            print(i, '. ', row, '. ', row.deadline.day, ' ', row.deadline.strftime('%b') + '.', sep="")
    else:
        print("Nothing is missed!")


def delete_task():
    result = session.query(Table).order_by(Table.deadline).all()
    if result:
        print("Choose the number of the task you want to delete:")
        numbered_result = enumerate(result, 1)
        for i, row in numbered_result:
            print(i, '. ', row, '. ', row.deadline.day, ' ', row.deadline.strftime('%b') + ".", sep="")
        choice = int(input())
        session.delete(result[choice-1])
        session.commit()
    else:
        print("Nothing to do!")


def main():
    while True:
        user_input = int(input(("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")))
        if user_input == 1:
            todays_task()
        elif user_input == 2:
            weeks_task()
        elif user_input == 3:
            print("All tasks:")
            all_tasks()
        elif user_input == 4:
            missed_task()
        elif user_input == 5:
            add_task()
        elif user_input == 6:
            delete_task()
        else:
            print("Bye!")
            return 0


main()
session.close()
