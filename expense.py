import datetime
from dataclasses import dataclass


@dataclass
class Expense:
    name: str
    category: str
    amount: float
    date: datetime.date

    def __repr__(self):
        return (
            f"<Expense: {self.name}, {self.category},"
            f"${self.amount:.2f}, {self.date.strftime('%Y-%m-%d')} >"
        )
