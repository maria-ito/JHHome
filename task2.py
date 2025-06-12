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

from collections import OrderedDict


class Order:
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type'].lower()
        self.instrument = order_dict.get('instrument', None)
        self.order_id = str(uuid.uuid4())


class OrderBook:
    def __init__(self):
        self.buy_list = []
        self.sell_list = []
        self.order_map = OrderedDict()
        self.trade_map = OrderedDict()

    def add_order(self, order, match_bool):
        if match_bool:
            order = self.match_order(order, True)
        # if order.quantity == 0:
        #     return

        if order.price < 0:
            raise ValueError('Price must be positive.')
        if order.type == 'buy':
            heapq.heappush(self.buy_list, [order.price, order.order_id, order.quantity])
            print(f'Buy list: {self.buy_list}')
        elif order.type == 'sell':
            heapq.heappush(self.sell_list, [-order.price, order.order_id, order.quantity])
            print(f'Sell list: {self.sell_list}')
        else:
            raise KeyError('Order type not available.')

        self._add_to_map(order)

    def _add_to_map(self, order):
        if order.type == 'sell':
            order.price *= -1
        self.order_map[order.order_id] = order

    def cancel_order(self, order_id):
        # TODO: expand this, to accommodate trades
        if order_id in self.order_map:
            print(f'Order_map: {self.order_map}')
            order = self.order_map.pop(order_id)
            self._delete_from_list(order, order_id)
            # self._cancel_update_trade(order)
            print(f'Order {order_id} cancelled.')
            print(f'Order_map: {self.order_map}')

        else:
            raise KeyError('Order ID unavailable.')

    # def _cancel_update_trade(self, order):
    #     for local_trade in self.trade_map:
    #         if order.order_id == local_trade['buy']:
    #             if local_trade['buy'] in self.order_map



    def _delete_from_list(self, order, order_id):
        if order.type == 'buy':
            self.buy_list = [x for x in self.buy_list if x[1] != order_id]
        else:
            self.sell_list = [x for x in self.sell_list if x[1] != order_id]

    def _execute_match(self, order, add_bool):
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
            if best_order[0] >= multiplier * order.price:
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
        if not add_bool and order.quantity > 0:
            heapq.heappush(temp_list, [-order.price, order.order_id, order.quantity])
            self._add_to_map(order)
        return temp_list, temp, order

    def match_order(self, order, from_add):
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
        print('BUY ORDERS:')
        for price, _, quantity in sorted(self.buy_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')
        print('SELL ORDERS:')
        for price, _, quantity in sorted(self.sell_list):
            if quantity > 0:
                print(f'Price: {price}, Quantity: {quantity}')


# class InstrumentOrderBook(OrderBook):
#     def __init__(self):
#         super().__init__()
#         self.instrument_order_map = {}
#
#     def add_order_instrument(self, order):
#         if not order.instrument:
#             raise KeyError('Missing instrument type in order.')
#         super().add_order(order, False)
#         if order.instrument not in self.instrument_order_map:
#             self.instrument_order_map[order.instrument] = {}
#         self.instrument_order_map[order.instrument][order.order_id] = self.order_map[order.order_id]
#
#     def cancel_order_instrument(self, order_id):
#         for instrument in (self.instrument_order_map.keys()):
#
#             if order_id in self.instrument_order_map[instrument]:
#                 print(f'Instrument_order_map: {self.order_map}')
#                 order = self.instrument_order_map[instrument].pop(order_id)
#                 self._delete_from_map(order, order_id)
#                 print(f'Order {order_id} cancelled.')
#                 print(f'Instrument_order_map: {self.order_map}')
#                 return
#         raise KeyError('Order ID unavailable.')


if __name__ == '__main__':
    print('Single Instrument')
    # Single instrument
    book = OrderBook()

    book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}), False)
    book.add_order(Order({"type": "SELL", "price": 104, "quantity": 3}), False)

    book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}), False)
    book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}), False)

    book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}), True)
    book.match_order(Order({"type": "BUY", "price": 102, "quantity": 2}), False)

    book.cancel_order(list(book.order_map.keys())[0])
    book.cancel_order(list(book.order_map.keys())[-1])
    book.print_order_book()



    # print('Multiple instruments')
    # # Multiple instruments
    # book = InstrumentOrderBook()
    # book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 1}))
    # book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 5}))
    # book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 6}))
    # book.add_order_instrument(Order({"type": "BUY", "instrument": "FX", "price": 101, "quantity": 3}))
    # book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 3}))
    # book.add_order_instrument(Order({"type": "SELL", "instrument": "EQ", "price": 104, "quantity": 2}))
    # book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 4}))
    # book.add_order_instrument(Order({"type": "SELL", "instrument": "FX", "price": 103, "quantity": 7}))
    # book.cancel_order_instrument(list(book.instrument_order_map['EQ'].keys())[0])
    # book.cancel_order_instrument(list(book.instrument_order_map['FX'].keys())[0])
    # book.print_order_book()

