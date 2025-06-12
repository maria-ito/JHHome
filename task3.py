'''
### Stage 3: Extending for Gold Futures Contracts
In this stage, you will extend the order book to handle futures contracts.
A futures contract is a legal agreement to buy or sell a particular commodity or financial instrument at a predetermined
 price at a specified time in the future. Unlike stocks, futures contracts have expiration dates. As the expiration date
 approaches, the futures contract reaches its settlement period, where the final trade of the contract is executed, and
 the contract is either delivered (physical delivery of the commodity) or settled in cash (for financial futures).

Your task is to modify or extend your order book to handle additional information related to futures contracts,
specifically Gold Futures (GC1). Orders will include a contract ticker, such as GCQ4 Comdty. Here, "GC" stands for Gold,
"Q4" represents the expiration month and year, and "Comdty" indicates the commodity market. You are expected to use this
information to determine the expiration of the contract.

__Contract Ticker Breakdown__:
- GC: The product code for Gold.
- Q4: The expiration code. The letter represents the month, and the number represents the last digit of the year.
- Comdty: Stands for "commodity" and indicates the type of market.

__Expiration Code Table__:

To derive the expiration month and year from the contract ticker, use the following table:

| Code | Month      |
|------|------------|
| F    | January    |
| G    | February   |
| H    | March      |
| J    | April      |
| K    | May        |
| M    | June       |
| N    | July       |
| Q    | August     |
| U    | September  |
| V    | October    |
| X    | November   |
| Z    | December   |

For example, a ticker "GCQ4 Comdty" would represent a Gold Futures Contract expiring in August 2024.

__Implementation Requirements__:
- Update your order book to parse and store expiration information from the contract ticker.
- Ensure that orders can only match if they share the same contract ticker, including the expiration.
- Modify your order book display or query functionality to allow filtering or viewing orders by their expiration.
- Implement logic to handle the settlement or expiry of contracts appropriately based on their expiration date.

__Input__:
You receive the following new orders:

```
{"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCQ4 Comdty"}
{"type": "SELL", "price": 1500, "quantity": 2, "contract": "GCQ4 Comdty"}
{"type": "BUY", "price": 1550, "quantity": 3, "contract": "GCZ4 Comdty"}
{"type": "SELL", "price": 1550, "quantity": 1, "contract": "GCZ4 Comdty"}
```

The contract ticker indicates:

- GCQ4 Comdty represents Gold Futures Contracts expiring in August 2024.
- GCZ4 Comdty represents Gold Futures Contracts expiring in December 2024.

__Expected Output__:
After processing the new orders, considering both price and expiration date, the state of the order book should
reflect the following:

```
Match: BUY 2@1500 with SELL 2@1500 on GCQ4 Comdty

GCQ4 Comdty:
No open orders.

Match: BUY 3@1550 with SELL 1@1550 on GCZ4 Comdty

GCZ4 Comdty:
BUY ORDERS:
Price: 1550, Quantity: 2
```

- The first BUY and SELL orders for GCQ4 Comdty match perfectly by price and contract, leading to a trade.
Since the quantities are equal, both orders are fully satisfied and removed from the order book.
- The second set of BUY and SELL orders for GCZ4 Comdty also match by price and contract. However, since
the BUY order's quantity exceeds that of the SELL order, the SELL order is fully satisfied and removed, while the BUY
order remains in the order book with its quantity reduced by the matched amount.
'''

import heapq
import uuid

from collections import OrderedDict
from datetime import date
from settings import *

class Order:
    def __init__(self, order_dict):
        self.price = order_dict['price']
        self.quantity = order_dict['quantity']
        self.type = order_dict['type'].lower()
        self.instrument = order_dict.get('instrument', None)
        self.order_id = str(uuid.uuid4())

        contract = order_dict['contract'].split()
        self.product = product_mapping[contract[0][:-2].upper()]
        self.exp_date = date(int(f'202{contract[0][-1]}'), month_mapping[contract[0][-2].upper()], 1)
        self.market = contract[1]


class OrderBook:
    def __init__(self):
        self.buy_list = []
        self.sell_list = []
        self.order_map = OrderedDict()

    def add_order(self, order, match_bool):
        if match_bool:
            order = self.match_order(order, True)
        if order.quantity == 0:
            return

        if order.price < 0:
            raise ValueError('Price must be positive.')
        if order.type == 'buy':
            heapq.heappush(
                self.buy_list,
                [order.price, order.order_id, order.quantity, order.product, order.exp_date]
            )
            print(f'Buy list: {self.buy_list}')
        elif order.type == 'sell':
            heapq.heappush(
                self.sell_list,
                [-order.price, order.order_id, order.quantity, order.product, order.exp_date]
            )
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
            self._delete_from_list(order, order_id)
            print(f'Order {order_id} cancelled.')
            print(f'Order_map: {self.order_map}')

        else:
            raise KeyError('Order ID unavailable.')

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
            multiplier = -1 if order.type == 'buy' else 1
            if ((multiplier * best_order[0] <= order.price) and \
                    (best_order[3] == order.product) and \
                    (best_order[4] == order.exp_date)):

                if best_order[2] >= order.quantity:
                    best_order[2] -= order.quantity
                    order.quantity = 0
                    if best_order[2] > 0:
                        temp.append(best_order)
                    else:
                        self.order_map.pop(best_order[1])
                elif best_order[2] < order.quantity:
                    order.quantity -= best_order[2]
                    best_order[2] = 0
            else:
                temp.append(best_order)
        if not add_bool and order.quantity > 0:
            heapq.heappush(temp_list, [-order.price, order.order_id, order.quantity])
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


class InstrumentOrderBook(OrderBook):
    def __init__(self):
        super().__init__()
        self.instrument_order_map = {}

    def add_order_instrument(self, order):
        if not order.instrument:
            raise KeyError('Missing instrument type in order.')
        super().add_order(order, False)
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

    book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}), False)
    book.add_order(Order({"type": "SELL", "price": 104, "quantity": 3}), False)

    book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}), False)
    book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}), False)

    book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}), True)
    book.match_order(Order({"type": "BUY", "price": 102, "quantity": 2}), False)

    book.cancel_order(list(book.order_map.keys())[0])
    book.cancel_order(list(book.order_map.keys())[-1])
    book.print_order_book()




