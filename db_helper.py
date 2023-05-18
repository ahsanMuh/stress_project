from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(BigInteger)
    company = Column(String)

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    admin_id = Column(Integer)

class Stress(Base):
    __tablename__ = 'stress'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer)
    datetime = Column(DateTime, default=datetime.utcnow)
    stress_level = Column(Boolean)

class DBHelper:
    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        Base.metadata.create_all(bind=engine)
        self.SessionLocal = sessionmaker(bind=engine)

    def verify_admin_login(self, username: str, password: str) -> int:
        db = self.SessionLocal()
        admin = db.query(Admin).filter_by(username=username, password=password).first()
        if admin:
            return admin.id
        else:
            return -1

    def create_admin(self, name: str, username: str, password: str,
                    email: str, phone: str, company: str) -> int:
        db = self.SessionLocal()
        admin = Admin(name=name, username=username, password=password, email=email, phone=phone, company=company)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin.id

    def read_admin_profile(self, id: int) -> dict:
        db = self.SessionLocal()
        admin = db.query(Admin).filter_by(id=id).first()
        if admin:
            return {'username': admin.username, 'username': admin.username, 'email': admin.email, 'phone': admin.phone}
        else:
            return {}

    def get_stress_admin(self, admin_id: int) -> list:
        db = self.SessionLocal()
        employees = db.query(Employee).filter_by(admin_id=admin_id).all()
        stress_levels = []
        for employee in employees:
            stress = db.query(Stress).filter_by(id=employee.id).order_by(Stress.datetime.desc()).first()
            if stress:
                stress_levels.append({'name': employee.name, 'stress-status': stress.stress_level,
                                        'employee-id': employee.id, 'datetime': str(stress.datetime)})
        return stress_levels

    def get_stress_user(self, employee_id: str, start: datetime, end: datetime) -> list:
        db = self.SessionLocal()
        stresses = db.query(Stress).filter_by(id=employee_id).filter(
                    Stress.datetime >= start).filter(Stress.datetime <= end).all()
        stress_levels = []
        for stress in stresses:
            stress_levels.append((str(stress.datetime),
                                  stress.stress_level))
        return {'id': employee_id, 'List': stress_levels}
