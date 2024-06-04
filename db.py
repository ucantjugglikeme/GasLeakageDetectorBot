import asyncio
import sqlalchemy as sa
from aiomysql.sa import create_engine

from config import data


loop: asyncio.AbstractEventLoop | None = None
metadata = sa.MetaData()

company_tbl = sa.Table(
    "Company",
    metadata,
    sa.Column('company_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('name_', sa.String(45), unique=True, nullable=False),
    sa.Column('email', sa.String(45)),
    sa.Column('phone', sa.String(45))
)
chat_tbl = sa.Table(
    "Chat",
    metadata,
    sa.Column('chat_id', sa.BigInteger, primary_key=True),
    sa.Column('name_', sa.String(45), nullable=False),
    sa.Column('company_id', sa.Integer, sa.ForeignKey("Company.company_id"), nullable=False)
)
placement_tbl = sa.Table(
    "Placement",
    metadata,
    sa.Column('placement_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('address', sa.String(45), unique=True, nullable=False)
)
chat_placement_tbl = sa.Table(
    "ChatPlacement",
    metadata,
    sa.Column('chat_id', sa.BigInteger, nullable=False),
    sa.Column('placement_id', sa.Integer, nullable=False),
    sa.UniqueConstraint("chat_id", "placement_id", name="uc_chat_placement")
)
detector_tbl = sa.Table(
    "GasDetector",
    metadata,
    sa.Column('detector_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('name_', sa.String(45), nullable=False),
    sa.Column('placement_id', sa.Integer, sa.ForeignKey("Placement.placement_id"), nullable=False),
    sa.UniqueConstraint("name_", "placement_id", name="uc_detector")
)


async def get_placement_by_address(address: str) -> list: 
    engine_ = await create_engine(
        user=data["mysql_user"], 
        db=data["db"],
        host=data["mysql_server"], 
        password=data["mysql_pass"], 
        loop=loop
    )
    async with engine_.acquire() as conn:
        result = await conn.execute(placement_tbl.select().where(placement_tbl.c.address == address))
        result = await result.fetchall()

    engine_.close()
    await engine_.wait_closed()
    return result


async def get_detector_by_name_placement(name: str, placement_id: int) -> list:
    engine_ = await create_engine(
        user=data["mysql_user"], 
        db=data["db"],
        host=data["mysql_server"], 
        password=data["mysql_pass"], 
        loop=loop
    )
    async with engine_.acquire() as conn:
        result = await conn.execute(
            detector_tbl.select().where(
                detector_tbl.c.name_ == name and 
                detector_tbl.c.placement_id == placement_id
            )
        )
        result = await result.fetchall()

    engine_.close()
    await engine_.wait_closed()
    return result


async def get_companies_chats_by_placementd_id(placement_id: str) -> list:
    engine_ = await create_engine(
        user=data["mysql_user"], 
        db=data["db"],
        host=data["mysql_server"], 
        password=data["mysql_pass"], 
        loop=loop
    )

    select_stmt = sa.select(company_tbl.c.name_, chat_tbl.c.chat_id).join(
        chat_tbl, company_tbl.c.company_id == chat_tbl.c.company_id
    ).where(chat_tbl.c.chat_id.in_(
        sa.select(chat_placement_tbl.c.chat_id).where(
            chat_placement_tbl.c.placement_id == placement_id
        )
    ))
    async with engine_.acquire() as conn:
        result = await conn.execute(select_stmt)
        result = await result.fetchall()

    engine_.close()
    await engine_.wait_closed()
    return result
