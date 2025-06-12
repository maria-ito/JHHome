import unittest

from task2 import *


class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}), False)
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}), False)

        self._run_test_list(book)
        self._run_test_map(book)

    def test_add_order_match(self):
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}), False)
        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}), False)
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}), False)

        book.add_order(Order({"type": "SELL", "price": 108, "quantity": 2}), True)

        self._run_test_list(book)
        self._run_test_map(book)

    def test_cancel_buy_order(self):
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 106, "quantity": 3}), False)
        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}), False)
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}), False)
        book.cancel_order(list(book.order_map.keys())[0])

        self._run_test_list(book)
        self._run_test_map(book)

    def _run_test_list(self, bookobj):
        self.assertEqual(bookobj.buy_list[0][0], 109)
        self.assertEqual(bookobj.buy_list[0][2], 1)

        self.assertEqual(bookobj.sell_list[0][0], -102)
        self.assertEqual(bookobj.sell_list[0][2], 5)

    def _run_test_map(self, bookobj):
        self.assertEqual(len(bookobj.order_map), 2)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, bookobj.buy_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, bookobj.buy_list[0][2])

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, -bookobj.sell_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, bookobj.sell_list[0][2])