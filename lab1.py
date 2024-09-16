from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import date

# Базовий клас для моделі
Base = declarative_base()

# Модель Пацієнт (зберігається в центральній базі)
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    medical_record_number = Column(String)
    email = Column(String)
    phone = Column(String)

# Модель Етап евакуації (може бути розподілена між вузлами)
class EvacuationStage(Base):
    __tablename__ = 'evacuation_stages'
    id = Column(Integer, primary_key=True)
    stage_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    patient_id = Column(Integer, ForeignKey('patients.id'))

# Підключення до центральної бази даних (наприклад, для пацієнтів)
central_engine = create_engine('postgresql://user:password@central_server/central_db')
CentralSession = sessionmaker(bind=central_engine)
central_session = CentralSession()

# Підключення до локальної бази даних (наприклад, для стабілізаційного пункту)
local_engine = create_engine('postgresql://user:password@local_server/local_db')
LocalSession = sessionmaker(bind=local_engine)
local_session = LocalSession()

# Створення таблиць в обох базах даних
Base.metadata.create_all(central_engine)  # Створення в центральній базі
Base.metadata.create_all(local_engine)    # Створення в локальній базі

# Приклад роботи з даними
new_patient = Patient(
    first_name="Іван",
    last_name="Петров",
    age=30,
    gender="Чоловік",
    medical_record_number="12345",
    email="ivan.petrov@example.com",
    phone="+380123456789"
)

# Додаємо пацієнта до центральної бази даних
central_session.add(new_patient)
central_session.commit()

# Додаємо етап евакуації до локальної бази даних
new_stage = EvacuationStage(
    stage_name="Стабілізаційний пункт",
    start_date=date(2024, 9, 10),
    end_date=date(2024, 9, 12),
    patient_id=new_patient.id  # Використовуємо ID з центральної бази
)

local_session.add(new_stage)
local_session.commit()
