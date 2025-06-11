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

from collections import defaultdict

class Order:
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type'].lower()
        self.instrument = order_dict['instrument'] if 'instrument' in order_dict else None
        self.order_id = str(uuid.uuid4())


class OrderBook:
    def __init__(self):
        self.buy_list = []
        self.sell_list = []
        self.order_map = {}

    def add_order(self, order):
        if order.price < 0:
            raise ValueError('Price must be positive.')
        if order.type == 'buy':
            heapq.heappush(self.buy_list, (order.price, order.order_id, order.quantity))
            print(f'Buy list: {self.buy_list}')
        elif order.type == 'sell':
            heapq.heappush(self.sell_list, (order.price, order.order_id, order.quantity))
            print(f'Sell list: {self.sell_list}')
        else:
            raise KeyError('Order type not available.')
        self._add_to_map(order)

    def _add_to_map(self, order):
        self.order_map[order.order_id] = order
        print('')

    def cancel_order(self, order_id):
        if order_id in self.order_map:
            print(f'Order_map: {self.order_map}')
            order = self.order_map.pop(order_id)
            # order.quantity = 0
            self._delete_from_map(order, order_id)
            print(f'Order {order_id} cancelled.')
            print(f'Order_map: {self.order_map}')

        else:
            raise KeyError('Order ID unavailable.')

    def _delete_from_map(self, order, order_id):
        if order.type == 'buy':
            self.buy_list = [x for x in self.buy_list if x[1] != order_id]
        else:
            self.sell_list = [x for x in self.sell_list if x[1] != order_id]

    def print_order_book(self):
        print('BUY ORDERS:')
        for price, _, quantity in sorted(self.buy_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')
        print('SELL ORDERS:')
        for price, _, quantity in sorted(self.sell_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')


class InstrumentOrderBook(OrderBook):
    def __init__(self):
        super().__init__()
        self.instrument_order_map = {}

    def add_order_instrument(self, order):
        if not order.instrument:
            raise KeyError('Missing instrument type in order.')
        super().add_order(order)
        if order.instrument not in self.instrument_order_map:
            self.instrument_order_map[order.instrument] = {}
        self.instrument_order_map[order.instrument][order.order_id] = self.order_map[order.order_id]

    def cancel_order_instrument(self, order_id):
        for instrument in (self.instrument_order_map.keys()):

            if order_id in self.instrument_order_map[instrument]:
                print(f'Instrument_order_map: {self.order_map}')
                order = self.instrument_order_map[instrument].pop(order_id)
                self._delete_from_map(order, order_id)
                print(f'Order {order_id} cancelled.')
                print(f'Instrument_order_map: {self.order_map}')
                return
        raise KeyError('Order ID unavailable.')


if __name__ == '__main__':
    print('Single Instrument')
    # Single instrument
    book = OrderBook()

    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 5}))
    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 6}))
    book.add_order(Order({"type": "BUY", "price": 101, "quantity": 3}))
    book.add_order(Order({"type": "SELL", "price": 104, "quantity": 2}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 4}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 3}))
    book.cancel_order(list(book.order_map.keys())[0])
    book.cancel_order(list(book.order_map.keys())[-1])
    book.print_order_book()

    print('Multiple instrument')
    # Multiple instruments
    book = InstrumentOrderBook()
    book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 1}))
    book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 5}))
    book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 6}))
    book.add_order_instrument(Order({"type": "BUY", "instrument": "FX", "price": 101, "quantity": 3}))
    book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 3}))
    book.add_order_instrument(Order({"type": "SELL", "instrument": "EQ", "price": 104, "quantity": 2}))
    book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 4}))
    book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 7}))
    book.cancel_order_instrument(list(book.instrument_order_map['EQ'].keys())[0])
    book.cancel_order_instrument(list(book.instrument_order_map['FX'].keys())[0])
    book.print_order_book()

