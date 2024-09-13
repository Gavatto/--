from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import date  # Імпорт класу date

# Базовий клас для моделі
Base = declarative_base()

# Модель Пацієнт
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

    evacuation_stages = relationship('EvacuationStage', back_populates='patient')

# Модель Етап евакуації
class EvacuationStage(Base):
    __tablename__ = 'evacuation_stages'
    id = Column(Integer, primary_key=True)
    stage_name = Column(String)
    start_date = Column(Date)  # Поле дати
    end_date = Column(Date)    # Поле дати
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship('Patient', back_populates='evacuation_stages')
    documents = relationship('Documentation', back_populates='evacuation_stage')

# Модель Документація
class Documentation(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    doc_type = Column(String)
    created_date = Column(Date)  # Поле дати
    description = Column(String)
    evacuation_stage_id = Column(Integer, ForeignKey('evacuation_stages.id'))

    evacuation_stage = relationship('EvacuationStage', back_populates='documents')

# Підключення до бази даних SQLite
engine = create_engine('sqlite:///evacuation.db')
Base.metadata.create_all(engine)

# Створення сесії для взаємодії з базою даних
Session = sessionmaker(bind=engine)
session = Session()

# Приклад додавання нового пацієнта, етапу та документа
new_patient = Patient(
    first_name="Іван",
    last_name="Петров",
    age=30,
    gender="Чоловік",
    medical_record_number="12345",
    email="ivan.petrov@example.com",
    phone="+380123456789"
)

new_stage = EvacuationStage(
    stage_name="Стабілізаційний пункт",
    start_date=date(2024, 9, 10),  # Використовуємо об'єкт date
    end_date=date(2024, 9, 12),    # Використовуємо об'єкт date
    patient=new_patient
)

new_document = Documentation(
    doc_type="Огляд",
    created_date=date(2024, 9, 10),  # Використовуємо об'єкт date
    description="Первинний огляд пораненого",
    evacuation_stage=new_stage
)

# Збереження даних в базі
session.add(new_patient)
session.add(new_stage)
session.add(new_document)
session.commit()

# Закриття сесії
session.close()
