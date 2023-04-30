#coinlist_manager.py

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from jinja2 import Template

from .database import Base, engine
from . import models, schemas
from .models import ApiKey, TradingPairList, TradingPair

from binance import Client

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from typing import List
from . import schemas, crud
from .database import get_db



app = FastAPI()
router = APIRouter()



def get_available_pairs(api_key: str, api_secret: str, market: str, base_asset: str):
    client = Client(api_key, api_secret)
    if market == 'stock':
        exchange_info = client.get_exchange_info()
        pairs = [p['symbol'] for p in exchange_info['symbols'] if p['quoteAsset'] == base_asset]
    elif market == 'futures':
        exchange_info = client.futures_exchange_info()
        pairs = [p['symbol'] for p in exchange_info['symbols'] if p['quoteAsset'] == base_asset]
    else:
        raise ValueError('Invalid market')
    return pairs



# class TradingPairList(Base):
#     __tablename__ = 'trading_pair_list'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), index=True)
#     api_key_id = Column(Integer, ForeignKey('api_key.id'))
#     api_key = relationship("ApiKey", back_populates="trading_pair_lists")
#     bot_id = Column(Integer, ForeignKey('bot.id'))
#     bot = relationship("Bot", back_populates="trading_pair_list")
#     trading_pairs = relationship("TradingPair", back_populates="trading_pair_list")
#     # wallets = relationship("Wallet", back_populates="trading_pair_list")
#     strategies = relationship("Strategy", back_populates="trading_pair_list")

#     def __repr__(self):
#         return f'<TradingPairList {self.name}>'



def create_trading_pair_list_table(name: str, api_key_id: int, bot_id: int):
    table_name = f'trading_pair_list_{name.lower().replace(" ", "_")}'
    metadata = Base.metadata
    trading_pair_list_table = Table(
        table_name,
        metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trading_pair_id', sa.Integer, sa.ForeignKey('trading_pair.id')),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, onupdate=datetime.utcnow),
    )
    trading_pair_list_table.create(bind=engine, checkfirst=True)
    TradingPairList.__table__.create(bind=engine, checkfirst=True)

    with Session(bind=engine) as session:
        api_key = session.query(ApiKey).filter_by(id=api_key_id).first()
        bot = session.query(Bot).filter_by(id=bot_id).first()

        trading_pair_list = TradingPairList(name=name, api_key=api_key, bot=bot)
        # trading_pair_list.wallets = [Wallet(name=f"{name} Wallet", trading_pair_list=trading_pair_list)]
        trading_pair_list.strategies = [Strategy(name=f"{name} Strategy", trading_pair_list=trading_pair_list)]
        session.add(trading_pair_list)
        session.commit()

# Получаем список доступных монет с биржи (например, через вызов функции get_available_pairs)
available_pairs = ['BTC/USDT', 'ETH/USDT', 'LTC/USDT', ...]

# Создаем экземпляр TradingPairList
trading_pair_list = TradingPairList()

# Добавляем каждую торговую пару в TradingPairList
for pair in available_pairs:
    trading_pair = TradingPair(market='example_market', pair=pair)
    trading_pair_list.trading_pairs.append(trading_pair)

# Добавляем TradingPairList в сессию базы данных и сохраняем изменения
session.add(trading_pair_list)
session.commit()

@router.get("/trading_pairs/", response_model=List[schemas.TradingPair])
async def read_trading_pairs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trading_pairs = crud.get_trading_pairs(db, skip=skip, limit=limit)
    return trading_pairs

@router.post("/trading_pairs/", status_code=status.HTTP_201_CREATED)
async def create_trading_pair(trading_pair: schemas.TradingPairCreate, db: Session = Depends(get_db)):
    db_trading_pair = crud.get_trading_pair_by_symbol(db, symbol=trading_pair.symbol)
    if db_trading_pair:
        raise HTTPException(status_code=400, detail="Trading pair already exists")
    return crud.create_trading_pair(db=db, trading_pair=trading_pair)
