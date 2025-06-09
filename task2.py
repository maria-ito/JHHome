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

class Order:
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type']
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
            heapq.heappush(self.buy_list, (order.price, order.order_id, order))
            print(f'Buy list: {self.buy_list}')
        elif order.type.lower() == 'sell':
            heapq.heappush(self.sell_list, (order.price, order.order_id, order))
            print(f'Sell list: {self.sell_list}')
        else:
            raise KeyError('Order type not available.')
        self.order_map[order.order_id] = order
        # print(f'Order map: {self.order_map}')

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
        for price, _, order in sorted(self.buy_list):
            if order.quantity > 0:
                print(f'Price: {price}, Quantity: {order.quantity}')
        print('SELL ORDERS:')
        for price, _, order in sorted(self.sell_list):
            if order.quantity > 0:
                print(f'Price: {price}, Quantity: {order.quantity}')

if __name__ == '__main__':
    book = OrderBook()

    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 5}))
    book.add_order(Order({"type": "BUY", "price": 102, "quantity": 6}))
    book.add_order(Order({"type": "SELL", "price": 104, "quantity": 2}))
    book.add_order(Order({"type": "BUY", "price": 101, "quantity": 3}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 4}))
    book.add_order(Order({"type": "SELL", "price": 103, "quantity": 3}))
    book.cancel_order(list(book.order_map.keys())[0])
    book.cancel_order(list(book.order_map.keys())[-1])


    book.print_order_book()