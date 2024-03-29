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
    rows_to_insert = list(departments.values()) + employees
    for row in rows_to_insert:
        db_session.add(row)
    db_session.commit()


if __name__ == "__main__":
    run()
