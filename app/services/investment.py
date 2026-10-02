from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import FundingBase


def get_remaining_amount(obj: FundingBase) -> int:
    """Получить недостающую сумму проекта или остаток пожертвования."""
    return obj.full_amount - obj.invested_amount


def close_if_fully_invested(obj: FundingBase) -> None:
    """Закрыть объект, когда вся сумма распределена."""
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


def invest_money(new_obj: FundingBase, targets: list[FundingBase]) -> None:
    """Распределить деньги и закрыть объект, если достигли целевой суммы."""
    for target in targets:
        remaining = get_remaining_amount(new_obj)
        if remaining <= 0:
            return

        amount = min(remaining, get_remaining_amount(target))
        if amount <= 0:
            continue

        new_obj.invested_amount += amount
        target.invested_amount += amount

        close_if_fully_invested(new_obj)
        close_if_fully_invested(target)


async def process_investment(
    new_obj: FundingBase,
    func,
    session: AsyncSession
) -> FundingBase:
    """Получить объекты и распределить между ними средства."""
    targets = await func(session)
    invest_money(new_obj, targets)
    return new_obj
