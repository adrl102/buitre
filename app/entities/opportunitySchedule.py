from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class OpportunitySchedule(Entity, Base):
    __tablename__ = 'OpportunitySchedule'

    start_time = Column("start_time", Time, nullable=False)
    end_time = Column("end_time", Time, nullable=False)
    monday = Column("monday", Boolean)
    tuesday = Column("tuesday", Boolean)
    wednesday = Column("wednesday", Boolean)
    thursday = Column("thursday", Boolean)
    friday = Column("friday", Boolean)
    saturday = Column("saturday", Boolean)
    sunday = Column("sunday", Boolean)
    opportunity_id = Column("opportunity_id", Integer,
                            ForeignKey('Opportunity.id'), nullable=False)

    opportunity = relationship("Opportunity", back_populates="schedules")

    def __init__(self, user_id, opportunity_id, start_time, end_time,
                 mo=True, tu=True, we=True, th=True, fr=True, sa=True, su=True):
        Entity.__init__(self, user_id)
        self.start_time = start_time
        self.end_time = end_time
        self.monday = mo
        self.tuesday = tu
        self.wednesday = we
        self.thursday = th
        self.friday = fr
        self.saturday = sa
        self.sunday = su
        self.opportunity_id = opportunity_id

    def to_dict(self):
        return {
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday,
        }


class OpportunityScheduleSchema(Schema):
    id = fields.Integer()
    opportunity_id = fields.Integer()
    start_time = fields.Time()
    end_time = fields.Time()
    monday = fields.Boolean()
    tuesday = fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()
    saturday = fields.Boolean()
    sunday = fields.Boolean()
