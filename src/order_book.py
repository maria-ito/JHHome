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

from datetime import date
from collections import OrderedDict
from settings import *

class Order:
    '''
    Order with price, quantity, type, instrument, and optional contract details.
    '''
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type'].lower()
        self.instrument = order_dict.get('instrument', None)
        self.order_id = str(uuid.uuid4())

        contract = order_dict.get('contract', None)
        if contract:
            contract = contract.split()
            self.product = product_mapping[contract[0][:-2].upper()]
            self.exp_date = date(int(f'202{contract[0][-1]}'), month_mapping[contract[0][-2].upper()], 1)
            self.market = contract[1]
        else:
            self.product = self.exp_date = self.market = None


class OrderBook:
    '''
    Represents an order book to manage and match buy/sell orders for financial instruments.
    '''
    def __init__(self):
        self.buy_list = []
        self.sell_list = []
        self.order_map = OrderedDict()
        self.trade_map = OrderedDict()

    def add_order(self, order, match_bool=False):
        '''
        Adds an order to the book.
        If `match_bool` is True, attempts to match it first.
        Otherwise, it will simply add the order to the book.
        '''
        if match_bool:
            order = self.match_order(order, True)

        if order.price < 0:
            raise ValueError('Price must be positive.')
        if order.quantity < 0:
            raise ValueError('Quantity must be positive.')
        if order.type == 'buy':
            heapq.heappush(self.buy_list,
                           [order.price,
                            order.order_id,
                            order.quantity,
                            order.product,
                            order.exp_date,
                            order.instrument])
        elif order.type == 'sell':
            heapq.heappush(self.sell_list,
                           [-order.price,
                            order.order_id,
                            order.quantity,
                            order.product,
                            order.exp_date,
                            order.instrument])
        else:
            raise KeyError('Order type not available.')

        self._add_to_map(order)

    def _add_to_map(self, order):
        '''
        Adds the order to the internal order_map.
        '''
        if order.type == 'sell':
            order.price *= -1
        self.order_map[order.order_id] = order

    def cancel_order(self, order_id):
        '''
        Cancels an existing order if no trade has occurred with it.
        '''
        if order_id in self.order_map:
            order = self.order_map.pop(order_id)
            self._check_trade(order)
            self._delete_from_list(order, order_id)
            print(f'Order {order_id} cancelled.')


        else:
            raise KeyError('Order ID unavailable.')

    def _check_trade(self, order):
        '''
        Checks if the order has already been involved in a trade.
        '''
        for local_trade in self.trade_map:
            if order.order_id in list(self.trade_map[local_trade].values()):
                raise Warning('Not possible to cancel, trade has taken place.')

    def _delete_from_list(self, order, order_id):
        '''
        Removes the order from the corresponding list.
        '''
        if order.type == 'buy':
            self.buy_list = [x for x in self.buy_list if x[1] != order_id]
        else:
            self.sell_list = [x for x in self.sell_list if x[1] != order_id]

    def _execute_match(self, order, add_bool):
        '''
        Core matching logic. Matches orders based on price, instrument, product.
        Returns updated temp list and unmatched portion of the input order.
        The variable `add_bool` defines whether the order should be added to the book or not.
        '''
        temp = []
        if order.type == 'buy':
            temp_list = self.sell_list
        else:
            temp_list = self.buy_list
        while temp_list and order.quantity > 0:
            best_order = heapq.heappop(temp_list)
            if order.type == 'buy':
                multiplier = -1
                buy_key = order.order_id
                sell_key = best_order[1]
            else:
                multiplier = 1
                buy_key = best_order[1]
                sell_key = order.order_id
            # A match occurs when a buy order's price is equal to or higher than a sell order's price.
            if (best_order[0] >= multiplier * order.price) or \
                    ((best_order[0] >= multiplier * order.price) and
                    (best_order[5] == order.instrument)) or \
                    ((best_order[0] >= multiplier * order.price)  and
                    (best_order[3] == order.product) and
                    (best_order[4] == order.exp_date)):

                local_quantity = min(best_order[2], order.quantity)
                if best_order[2] >= order.quantity:
                    best_order[2] -= order.quantity
                    order.quantity = 0

                    temp.append(best_order)
                    self.order_map[best_order[1]].quantity = best_order[2]
                elif best_order[2] < order.quantity:
                    order.quantity -= best_order[2]
                    best_order[2] = 0
                trade_id = str(uuid.uuid4())
                local_trade = {
                    'buy': buy_key,
                    'sell': sell_key,
                    'quantity': local_quantity
                }
                self.trade_map[trade_id] = local_trade
            else:
                temp.append(best_order)
        if not add_bool:
            heapq.heappush(temp_list, [-order.price, order.order_id, order.quantity])
            self._add_to_map(order)
        return temp_list, temp, order

    def match_order(self, order, from_add=False):
        '''
        Tries to match a given order against the existing orders in the book.
        The variable `from_add` defines whether the match is executed before adding an order to a book.
        '''
        if order.type == 'buy':
            self.sell_list, temp, order = self._execute_match(order, from_add)
            while temp:
                heapq.heappush(self.sell_list, temp.pop())
        else:
            self.buy_list, temp, order = self._execute_match(order, from_add)
            while temp:
                heapq.heappush(self.buy_list, temp.pop())
        return order

    def print_order_book(self):
        '''
        Displays the current list of buy and sell orders.
        '''
        print('BUY ORDERS:')
        for buy_order in sorted(self.buy_list):
            if buy_order[2] > 0:
                if buy_order[4] is None:
                    print(f'Price: {buy_order[0]}, Quantity: {buy_order[2]}')
                else:
                    print(f'Product: {buy_order[3]}, Expiration: {str(buy_order[4])}, '
                          f'Price: {buy_order[0]}, Quantity: {buy_order[2]}')

        print('\nSELL ORDERS:')
        for sell_order in sorted(self.sell_list):
            if sell_order[2] > 0:
                if sell_order[4] is None:
                    print(f'Price: {sell_order[0]}, Quantity: {sell_order[2]}')
                else:
                    print(f'Product: {sell_order[3]}, Expiration: {str(sell_order[4])}, '
                          f'Price: {sell_order[0]}, Quantity: {sell_order[2]}')


if __name__ == '__main__':
    print('Task 1')
    book1 = OrderBook()

    book1.add_order(Order({"type": "BUY", "price": 102, "quantity": 5}))
    book1.add_order(Order({"type": "SELL", "price": 104, "quantity": 2}))
    book1.add_order(Order({"type": "BUY", "price": 101, "quantity": 3}))
    book1.add_order(Order({"type": "SELL", "price": 103, "quantity": 4}))
    book1.print_order_book()

    print('\nTask 2\n')
    book2 = OrderBook()

    book2.add_order(Order({"type": "BUY", "price": 102, "quantity": 5}))
    book2.add_order(Order({"type": "SELL", "price": 104, "quantity": 2}))
    book2.add_order(Order({"type": "BUY", "price": 101, "quantity": 3}))
    book2.add_order(Order({"type": "SELL", "price": 103, "quantity": 4}))
    book2.add_order(Order({"type": "SELL", "price": 102, "quantity": 1}), True)
    book2.print_order_book()

    print('\nTask 3\n')
    book3 = OrderBook()
    book3.add_order(Order({"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCQ4 Comdty"}), True)
    book3.add_order(Order({"type": "SELL", "price": 1500, "quantity": 2, "contract": "GCQ4 Comdty"}), True)
    book3.add_order(Order({"type": "BUY", "price": 1550, "quantity": 3, "contract": "GCZ4 Comdty"}), True)
    book3.add_order(Order({"type": "SELL", "price": 1550, "quantity": 1, "contract": "GCZ4 Comdty"}), True)
    book3.print_order_book()
