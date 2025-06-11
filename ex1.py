'''
### Stage 1: Basic Order Book

- You will need to handle two types of orders: BUY and SELL.
- Each order will have a price and quantity.

__Input__:

You receive the following orders:

```
{"type": "BUY", "price": 102, "quantity": 5}
{"type": "SELL", "price": 104, "quantity": 2}
{"type": "BUY", "price": 101, "quantity": 3}
{"type": "SELL", "price": 103, "quantity": 4}
```

__Expected Output__:

After adding these orders, the state of the order book should be printed as follows:

```
BUY ORDERS:
Price: 102, Quantity: 5
Price: 101, Quantity: 3

SELL ORDERS:
Price: 103, Quantity: 4
Price: 104, Quantity: 2
```
'''
import heapq
import uuid

from abc import ABC, abstractmethod

from collections import defaultdict


class Order:
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type']
        self.instrument = order_dict['instrument'] if 'instrument' in order_dict else None
        self.order_id = str(uuid.uuid4())


class AbstractOrderBook(ABC):
    @abstractmethod
    def add_order(self, order: Order):
        pass

    @abstractmethod
    def cancel_order(self, order_id: str):
        pass

    @abstractmethod
    def get_orders(self):
        pass


class OrderBook(AbstractOrderBook):
    def __init__(self):
        self.order_map = {}
        self.buy_list = []
        self.sell_list = []

    def add_order(self, order: Order):
        self.orders[order.id] = order

    def cancel_order(self, order_id: str):
        return self.orders.pop(order_id, None)

    def get_orders(self):
        return self.orders


# class InstrumentOrderBook(AbstractOrderBook):
#     def __init__(self):
#
#         self.books = {}  # {instrument: {order_id: order}}
#
#     def add_order(self, order: Order):
#         instrument = order.instrument
#
#     if not instrument:
#         raise ValueError("Instrument is required for this order book.")
#
#     if instrument not in self.books:
#         self.books[instrument] = {}
#         self.books[instrument][order.id] = order
#
#     def cancel_order(self, order_id: str) -> Optional[Order]:
#         for instrument, book in self.books.items():
#             if order_id in book:
#             return book.pop(order_id)
#
#         return None
#
#     def get_orders(self) -> dict:
#         return self.books

# class OrderProcessor:
#     def __init__(
#         self,
#         generic_book: AbstractOrderBook,
#         instrument_book: AbstractOrderBook
#         ):
#         self.generic_book = generic_book
#         self.instrument_book = instrument_book
#         # self.matcher = matcher
#
#     def process_order(self, order: Order):
#         # Optional: Try matching first
#         # if self.matcher:
#         #     matched = self.matcher.match(order, self._get_target_book(order))
#         # if matched:
#         #     return # Match occurred, no need to store
#
#         self._get_target_book(order).add_order(order)
#
#     def cancel_order(self, order_id: str):
#         return self.generic_book.cancel_order(order_id) or \
#         self.instrument_book.cancel_order(order_id)
#
#     def _get_target_book(self, order: Order) -> AbstractOrderBook:
#         return self.instrument_book if order.instrument else self.generic_book
#
#     def get_all_orders(self) -> dict:
#         return {
#         "generic": self.generic_book.get_orders(),
#         "instrument": self.instrument_book.get_orders()
#         }


# Create system
generic = OrderBook()
# instrumented = InstrumentOrderBook()
# matcher = MatchingEngine()
processor = OrderProcessor(generic, instrumented)

# Add orders
processor.process_order(Order(id='1', price=100, quantity=10, side='buy'))
processor.process_order(Order(id='2', price=105, quantity=5, side='sell', instrument='AAPL'))

# Cancel
processor.cancel_order('1')

# View state
from pprint import pprint
pprint(processor.get_all_orders())