#models.py

from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .base import Base



Base = declarative_base()



api_key_trading_pair_list = Table('api_key_trading_pair_list', Base.metadata,
    Column('api_key_id', Integer, ForeignKey('api_keys.id')),
    Column('trading_pair_list_id', Integer, ForeignKey('trading_pair_lists.id'))
)

api_key_bot = Table('api_key_bot', Base.metadata,
    Column('api_key_id', Integer, ForeignKey('api_keys.id')),
    Column('bot_id', Integer, ForeignKey('bots.id'))
)


# class ApiKeyBot(Base):
#     __tablename__ = 'api_key_bot'

#     api_key_id = Column(Integer, ForeignKey('api_keys.id'), primary_key=True)
#     bot_id = Column(Integer, ForeignKey('bots.id'), primary_key=True)
#     permissions = Column(Integer, nullable=False)

#     api_key = relationship('ApiKey', back_populates='api_key_bots')
#     bot = relationship('Bot', back_populates='api_key_bots')

api_key_wallet = Table('api_key_wallet', Base.metadata,
    Column('api_key_id', Integer, ForeignKey('api_keys.id')),
    Column('wallet_id', Integer, ForeignKey('wallet.id'))
)

bot_wallet = Table('bot_wallet', Base.metadata,
    Column('bot_id', Integer, ForeignKey('bots.id')),
    Column('wallet_id', Integer, ForeignKey('wallets.id'))
)

bot_trading_pair_list = Table('bot_trading_pair_list', Base.metadata,
    Column('bot_id', Integer, ForeignKey('bots.id')),
    Column('trading_pair_list_id', Integer, ForeignKey('trading_pair_lists.id'))
)


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    binance_key = Column(String, unique=True, index=True)
    binance_secret = Column(String, unique=True, index=True)
    __table_args__ = (UniqueConstraint("binance_key"), UniqueConstraint("binance_secret"),)

    #bots = relationship("Bot", secondary=api_key_bot, back_populates="api_keys")
    bots = relationship("Bot", secondary=api_key_bot,
                    primaryjoin="api_key_bot.c.api_key_id == api_keys.c.id",
                    secondaryjoin="api_key_bot.c.bot_id == bots.c.id",
                    back_populates="api_keys")
    # api_key_bots = relationship("ApiKeyBot", back_populates="api_key")
    # bots = relationship("Bot", secondary="api_key_bot", back_populates="api_keys")
    wallets = relationship("Wallet", back_populates="api_key")
    trading_pair_lists = relationship("TradingPairList", secondary=api_key_trading_pair_list, back_populates="api_keys")

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    #api_keys = relationship("ApiKey", secondary=api_key_bot, back_populates="bots")
    api_keys = relationship("ApiKey", secondary=api_key_bot,
                        primaryjoin="api_key_bot.c.bot_id == bots.c.id",
                        secondaryjoin="api_key_bot.c.api_key_id == api_keys.c.id",
                        back_populates="bots")
    # api_key_bots = relationship("ApiKeyBot", back_populates="bot")
    # api_keys = relationship("ApiKey", secondary="api_key_bot", back_populates="bots")                    
    #wallets = relationship("Wallet", secondary=bot_wallet, back_populates="bots")
    wallets = relationship("Wallet", secondary=bot_wallet,
                            primaryjoin="bot_wallet.c.bot_id == Bot.id",
                            secondaryjoin="bot_wallet.c.wallet_id == Wallet.id",
                            back_populates="bots")
    strategies = relationship("Strategy", back_populates="bot")
    #trading_pair_lists = relationship("TradingPairList", secondary=bot_trading_pair_list, back_populates="bots")
    trading_pair_lists = relationship("TradingPairList", secondary=bot_trading_pair_list,
                                       primaryjoin="bot_trading_pair_list.c.bot_id == Bot.id",
                                       secondaryjoin="bot_trading_pair_list.c.trading_pair_list_id == TradingPairList.id",
                                       back_populates="bots")
     


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    balance = Column(Float)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))

    api_key = relationship("ApiKey", back_populates="wallets")
    bots = relationship("Bot", secondary=bot_wallet, back_populates="wallets")



class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code_path = Column(String, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    bot2_id = Column(Integer, ForeignKey("bot2.id"))

    bot = relationship("Bot", back_populates="strategies")

# class Bot2(Base):
#     __tablename__ = "bot2"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     api_key_id = Column(Integer, ForeignKey("api_keys.id"))
#     wallet_id = Column(Integer, ForeignKey("wallets.id"))

#     strategies = relationship("Strategy", back_populates="bot2")
#     wallet = relationship("Wallet", back_populates="bot2")
   

class TradingPairList(Base):
    __tablename__ = 'trading_pair_lists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))    
    bot_id = Column(Integer, ForeignKey('bot.id'))

    trading_pairs = relationship("TradingPair", back_populates="trading_pair_list")
    api_keys = relationship("ApiKey", secondary=api_key_trading_pair_list, back_populates="trading_pair_lists")
    bots = relationship("Bot", secondary=bot_trading_pair_list, back_populates="trading_pair_lists")
    


class TradingPair(Base):
    __tablename__ = "trading_pairs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    base_asset = Column(String)
    quote_asset = Column(String)
    market = Column(String)
    volume = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    logo_url = Column(String(255))

    trading_pair_list_id = Column(Integer, ForeignKey("trading_pair_lists.id"))
    trading_pair_list = relationship("TradingPairList", back_populates="trading_pairs")
