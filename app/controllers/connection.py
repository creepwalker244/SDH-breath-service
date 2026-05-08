from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.configs.configs import settings

USER = settings.POSTGRESQL_USER
PASSWORD = settings.POSTGRESQL_PASSWORD
HOST = settings.POSTGRESQL_HOST
PORT = settings.POSTGRESQL_PORT
DATABASE = settings.POSTGRESQL_DBNAME


DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class SingletoneMetaClass(type):

    _instances = {}


    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
   

class SingletoneDBConnection(metaclass=SingletoneMetaClass):

    #TODO: класс проперти не принят в 3.13
    def _create_connection(self):
        """
        Пример использования:
        async def select(dbcon:SingletoneDBConnection)-> list[dict]:
            async with dbcon.start_session() as session:
                query = select(Table.title, Table.description)
                result = await session.execute(query)
                return result.mapping().all()
        """
        self._engine = create_async_engine(DATABASE_URL, echo=True)
        self._async_session = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)
        return self._async_session()

DBCONN = SingletoneDBConnection()
DBCONN._create_connection()

