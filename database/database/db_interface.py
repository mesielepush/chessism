from typing import Any

from .engine import DBSession
from .models import Base, to_dict
from sqlalchemy import exists
DataObject = dict[str, Any]


class DBInterface:
    def __init__(self, db_class: type[Base]):
        self.db_class = db_class

    def read_by_id(self, id: int) -> DataObject:
        session = DBSession()
        data: Base = session.query(self.db_class).get(id)
        session.close()
        return to_dict(data)
    def read_by_name(self, player_name: str)->DataObject:
        session = DBSession()
        data: Base = session.query(self.db_class).get(player_name)
        session.close()
        print('===================')
        print(data)
        print(data == None)
        print('===================')
        if data == None:
            return None
        return to_dict(data)

    def read_all(self) -> list[DataObject]:
        session = DBSession()
        data: list[Base] = session.query(self.db_class.player_name).all()
        session.close()
        return [item[0] for item in data]

    def create(self, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = self.db_class(**data)
        session.add(item)
        session.commit()
        result = to_dict(item)
        session.close()
        return result
    def create_all(self, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = [self.db_class(**game) for game in data]
        session.add_all(item)
        session.commit()
        session.close()
        return True

    def update(self, id: int, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = session.query(self.db_class).get(id)
        for key, value in data.items():
            setattr(item, key, value)
        session.commit()
        session.close()
        return to_dict(item)

    def delete(self, id: int) -> DataObject:
        session = DBSession()
        item: Base = session.query(self.db_class).get(id)
        result = to_dict(item)
        session.delete(item)
        session.commit()
        session.close()
        return result
    def player_exists(self, player_name: str) -> DataObject:
        session = DBSession()
        item: Base = session.query(exists().\
        where(self.db_class.player_name==player_name)).scalar()
        if str(item) == 'True':
            return True
        else:
            return False
    def game_exists(self, game_id: int) -> DataObject:
        session = DBSession()
        item: Base = session.query(exists().\
        where(self.db_class.id==game_id)).scalar()
        if str(item) == 'True':
            return True
        else:
            return False
    def read_oponents(self, player_name:str) -> list:
        session = DBSession()        
        white: Base  = session.query(
            self.db_class
        ).where(self.db_class.white ==player_name).all()
        black = session.query(
            self.db_class
        ).where(self.db_class.black ==player_name).all()
        black = [game.white for game in black]
        white = [game.black for game in white]
        return white + black
