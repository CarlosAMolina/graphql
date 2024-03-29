from models import engine, db_session, Base, Department, Employee


def run():
    Base.metadata.create_all(bind=engine)

    engineering = Department(name="Engineering")
    hr = Department(name="Human Resources")

    peter = Employee(name="Peter", department=engineering)
    roy = Employee(name="Roy", department=engineering)
    tracy = Employee(name="Tracy", department=hr)

    db_session.add(engineering)
    db_session.add(hr)
    db_session.add(peter)
    db_session.add(roy)
    db_session.add(tracy)
    db_session.commit()


if __name__ == "__main__":
    run()
