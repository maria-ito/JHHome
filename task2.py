'''
### Stage 2: Order Matching

Following from stage 1, orders may now match. A match occurs when a buy order's price is equal to or higher than a sell order's price.

- Implement order matching logic: when an order is added, check if it matches with any existing order in the book.
- If a match is found, reduce the quantities of the matched orders, remove any order with 0 quantity, and print the match details.
- Ensure the order book is updated accordingly.

__Input__:

```
{"type": "SELL", "price": 102, "quantity": 1}
```

__Expected Output__:

This order matches with one of the BUY orders. The state of the order book after this match and addition of the new order (if any quantity remains) should be:

```
Match: BUY 5@102 with SELL 1@102

BUY ORDERS:
Price: 102, Quantity: 4
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
        self.type = order_dict['type']
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
        if order.type.lower() == 'buy':
            heapq.heappush(self.buy_list, (order.price, order.quantity))
            print(f'Buy list: {self.buy_list}')
        elif order.type.lower() == 'sell':
            heapq.heappush(self.sell_list, (order.price, order.quantity))
            print(f'Sell list: {self.sell_list}')
        else:
            raise KeyError('Order type not available.')
        self.order_map[order.order_id] = order
        # print(f'Order map: {self.order_map}')

    def estimate_match(self):
        pass

    def process_order(self, order):
        if order.type.lower() == 'buy' and self.sell_list:
            best_sell_order = heapq.nsmallest(1, self.sell_list)[0][0]
            if order.price >= best_sell_order:
                self.estimate_match()
            else:
                self.add_order()
        elif order.type.lower() == 'sell' and self.buy_list:
            best_buy_order = heapq.nlargest(1, self.buy_list)[0][0]
            if order.price <= best_buy_order:
                self.estimate_match()
            else:
                self.add_order(order)

    def cancel_order(self, order_id):
        if order_id in self.order_map:
            print(f'Order_map: {self.order_map}')
            order = self.order_map.pop(order_id)
            order.quantity = 0
            print(f'Order {order_id} cancelled.')
            print(f'Order_map: {self.order_map}')
        else:
            raise KeyError('Order ID unavailable.')

    def print_order_book(self):
        print('BUY ORDERS:')
        for price, quantity in sorted(self.buy_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')
        print('SELL ORDERS:')
        for price, quantity in sorted(self.sell_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')


if __name__ == '__main__':
    # Single instrument
    book = OrderBook()

    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 5}))
    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 6}))
    book.add_order(Order({"type": "SELL", "price": 104, "quantity": 2}))
    book.add_order(Order({"type": "BUY", "price": 101, "quantity": 3}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 4}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 3}))
    book.process_order(Order({"type": "SELL", "price": 1000, "quantity": 3}))
    book.cancel_order(list(book.order_map.keys())[0])
    book.cancel_order(list(book.order_map.keys())[-1])
    book.print_order_book()
