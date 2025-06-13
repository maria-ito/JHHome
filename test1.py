import unittest

from task2 import *


class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 102, "quantity": 7}))
        book.add_order(Order({"type": "SELL", "price": 109, "quantity": 6}))

        self._run_test_list(book)
        self._run_test_map(book)

    def test_cancel_buy_order(self):
        """
        Test that it can cancel buy orders
        """
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 104, "quantity": 5}))
        book.add_order(Order({"type": "BUY", "price": 102, "quantity": 7}))
        book.add_order(Order({"type": "SELL", "price": 109, "quantity": 6}))

        book.cancel_order(list(book.order_map.keys())[0])

        self._run_test_list(book)
        self._run_test_map(book)

    def _run_test_list(self, bookobj):
        """
        Test that it can add buy and sell orders
        """

        self.assertEqual(bookobj.buy_list[0][0], 102)
        self.assertEqual(bookobj.buy_list[0][2], 7)

        self.assertEqual(bookobj.sell_list[0][0], -109)
        self.assertEqual(bookobj.sell_list[0][2], 6)

    def _run_test_map(self, bookobj):
        self.assertEqual(len(bookobj.order_map), 2)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, bookobj.buy_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, bookobj.buy_list[0][2])

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, bookobj.sell_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, bookobj.sell_list[0][2])

# class TestInstrumentOrderBook(unittest.TestCase):
#     def test_add_order(self):
#         book = InstrumentOrderBook()
#         book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 1}))
#         book.add_order_instrument(Order({"type": "SELL", "instrument": "EQ", "price": 103, "quantity": 2}))
#
#         book.add_order_instrument(Order({"type": "BUY", "instrument": "FI", "price": 105, "quantity": 4}))
#         book.add_order_instrument(Order({"type": "SELL", "instrument": "FI", "price": 107, "quantity": 5}))
#         self._run_test_list(book)
#         self._run_test_map(book)
#
#     def test_cancel_buy_order(self):
#         book = InstrumentOrderBook()
#         book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 103, "quantity": 7}))
#         book.add_order_instrument(Order({"type": "BUY", "instrument": "EQ", "price": 102, "quantity": 1}))
#         book.add_order_instrument(Order({"type": "SELL", "instrument": "EQ", "price": 103, "quantity": 2}))
#
#         book.add_order_instrument(Order({"type": "BUY", "instrument": "FI", "price": 105, "quantity": 4}))
#         book.add_order_instrument(Order({"type": "SELL", "instrument": "FI", "price": 107, "quantity": 5}))
#         book.cancel_order_instrument(list(book.instrument_order_map['EQ'].keys())[0])
#         self._run_test_list(book)
#         self._run_test_map(book)
#
#     def _run_test_list(self, bookobj):
#         self.assertEqual(bookobj.buy_list[0][0], 102)
#         self.assertEqual(bookobj.buy_list[0][2], 1)

    #     self.assertEqual(bookobj.buy_list[1][0], 105)
    #     self.assertEqual(bookobj.buy_list[1][2], 4)
    #
    # def _run_test_map(self, bookobj):
    #     self.assertEqual(len(bookobj.order_map), 4)
    #     self.assertEqual(bookobj.instrument_order_map['EQ'][list(bookobj.instrument_order_map['EQ'].keys())[0]].\
    #                      price, bookobj.buy_list[0][0])
    #     self.assertEqual(bookobj.instrument_order_map['EQ'][list(bookobj.instrument_order_map['EQ'].keys())[0]].\
    #                      quantity, bookobj.buy_list[0][2])
    #
    #     self.assertEqual(bookobj.instrument_order_map['FI'][list(bookobj.instrument_order_map['FI'].keys())[0]].\
    #                      price, bookobj.buy_list[1][0])
    #     self.assertEqual(bookobj.instrument_order_map['FI'][list(bookobj.instrument_order_map['FI'].keys())[0]].\
    #                      quantity, bookobj.buy_list[1][2])


if __name__ == '__main__':
    unittest.main()
