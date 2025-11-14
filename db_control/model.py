from sqlalchemy import (
    Column, String, Date, Integer, Float, ForeignKey, TIMESTAMP, Text, UUID
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, DOUBLE_PRECISION
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db_control.db_connect import Base
import uuid

# class File(Base):
#     __tablename__ = "files"

#     id_name_file = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name_file = Column(String(255), nullable=False)
#     created_at = Column(Date, server_default=func.current_date())

#     # Relasi ke race_telematry
#     race_telematry = relationship("RaceTelematry", back_populates="file", cascade="all, delete")

class ProjectName(Base):
    __tablename__ = "project_name"

    # Kolom ID (UUID sebagai Primary Key)
    # Menggunakan default=uuid.uuid4 untuk membuat UUID secara otomatis saat insert
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Kolom Data
    project_name = Column(String(255), nullable=False)
    circuit = Column(String(255))
    note = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    # Relasi ke tabel RaceTelematry
    # 'race_telematry' adalah nama back_populates di model RaceTelematry
    race_telemetries = relationship("RaceTelematry", back_populates="project_details")

    def __repr__(self):
        return f"<ProjectName(nama_project='{self.nama_project}', id='{self.id}')>"
    
class RaceTelematry(Base):
    __tablename__ = "race_telematry"

    id = Column(Integer, primary_key=True, index=True)
    id_project = Column(UUID(as_uuid=True), ForeignKey("project_name.id", ondelete="CASCADE"))

    timestamp = Column(Text)
    meta_session = Column(Text)
    original_vehicle_id = Column(Text)
    outing = Column(Integer)
    vehicle_id = Column(Text)
    vehicle_number = Column(Integer)
    lap = Column(Integer)

    Laptrigger_lapdist_dls = Column(DOUBLE_PRECISION)
    Steering_Angle = Column(DOUBLE_PRECISION)
    VBOX_Lat_Min = Column(DOUBLE_PRECISION)
    VBOX_Long_Minutes = Column(DOUBLE_PRECISION)
    accx_can = Column(DOUBLE_PRECISION)
    accy_can = Column(DOUBLE_PRECISION)
    aps = Column(DOUBLE_PRECISION)
    ath = Column(DOUBLE_PRECISION)
    gear = Column(DOUBLE_PRECISION)
    nmot = Column(DOUBLE_PRECISION)
    pbrake_f = Column(DOUBLE_PRECISION)
    pbrake_r = Column(DOUBLE_PRECISION)
    speed = Column(DOUBLE_PRECISION)
    timestamp_dt = Column(TIMESTAMP(timezone=True))

    AIR_TEMP = Column(DOUBLE_PRECISION)
    TRACK_TEMP = Column(Integer)
    HUMIDITY = Column(DOUBLE_PRECISION)
    PRESSURE = Column(DOUBLE_PRECISION)
    WIND_SPEED = Column(DOUBLE_PRECISION)
    WIND_DIRECTION = Column(Integer)
    RAIN = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relasi ke tabel File
    project_details = relationship("ProjectName", back_populates="race_telemetries")