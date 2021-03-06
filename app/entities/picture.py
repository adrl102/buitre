from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .entity import Entity, Base, session
from marshmallow import Schema, fields


class Picture(Entity, Base):
    __tablename__ = 'Picture'

    opportunity_id = Column("opportunity_id", Integer,
                            ForeignKey('Opportunity.id'), nullable=False)
    path = Column("path", String)

    opportunity = relationship("Opportunity", back_populates="pictures")

    def __init__(self, opportunity_id, path, created_by=None):
        super().__init__(created_by)
        self.opportunity_id = opportunity_id
        self.path = path

    def to_dict(self):
        return {
            'opportunity_id': self.opportunity_id,
            'path': self.path
        }


class PictureSchema:
    id = fields.Integer()
    opportunity_id = fields.Integer()
    path = fields.Str()


class PictureRepository:

    @staticmethod
    def get_by_opportunity_id(opportunity_id):
        pictures = session.query(Picture).filter_by(opportunity_id=opportunity_id).all()
        return pictures

    @staticmethod
    def add_to_opportunity(path, opportunity):
        picture = Picture(opportunity.id, path, opportunity.user_id)
        picture.persist()
