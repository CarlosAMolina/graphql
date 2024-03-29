from models import engine, db_session, Base, Department, Employee


def run():
    Base.metadata.create_all(bind=engine)

    departments = {
        "engineering": Department(name="Engineering"),
        "hr": Department(name="Human Resources"),
    }
    employees = [
        Employee(name="Peter", department=departments["engineering"]),
        Employee(name="Roy", department=departments["engineering"]),
        Employee(name="Tracy", department=departments["hr"]),
    ]
    for department in departments.values():
        db_session.add(department)
    for employee in employees:
        db_session.add(employee)
    db_session.commit()


if __name__ == "__main__":
    run()
