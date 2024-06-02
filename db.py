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
    sa.Column('company_id', sa.Integer, sa.ForeignKey("Company.company_id"), nullable=False),
)
placement_tbl = sa.Table(
    "Placement",
    metadata,
    sa.Column('placement_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('address', sa.String(45), unique=True, nullable=False),
    sa.Column('company_id', sa.Integer, sa.ForeignKey("Company.company_id"), nullable=False),
)
placement_tbl = sa.Table(
    "GasDetector",
    metadata,
    sa.Column('detector_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('ip_dns', sa.String(45)),
    sa.Column('name_', sa.String(45), nullable=False),
    sa.Column('placement_id', sa.Integer, sa.ForeignKey("Placement.placement_id"), nullable=False),
    sa.UniqueConstraint("name_", "placement_id", name="uc_detector")
)


def set_loop(loop_):
    loop = loop_


async def get_company():
    engine = await create_engine(
        user=data["mysql_user"], 
        db=data["db"],
        host=data["mysql_server"], 
        password=data["mysql_pass"], 
        loop=loop
    )
    async with engine.acquire() as conn:
        result = await conn.execute(company_tbl.select())
        result = await result.fetchall()
        print(result)

    engine.close()
    await engine.wait_closed()
