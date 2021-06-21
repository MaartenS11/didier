from database import Base
from sqlalchemy import Column, String, Integer
from typing import List


class TestTable(Base):

    __tablename__ = "test_table"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)


# A list of all models in this file, this is used to
# create all tables later on
all_models: List[Base] = [TestTable]
