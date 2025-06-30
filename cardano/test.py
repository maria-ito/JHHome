import unittest

from assignment import *
from settings import *


class TestLiabilities(unittest.TestCase):

    def test_present_value(self):
        '''
        Tests for equality to present value, using input Excel spreadsheet
        Test values have been calculated using excel
        '''
        in_df = pd.read_excel(input_file, sheet_name=liabilities_sheet, header=4)
        test_output = 7215075.85

        cash_flow = Liabilities(in_df, 0.015)
        cash_flow.calculate_present_value()
        self.assertEqual(round(cash_flow.present_value, 2), test_output)

    def test_dv(self):
        '''
        Tests for equality to DV01, using input Excel spreadsheet
        Test values have been calculated using excel
        '''
        in_df = pd.read_excel(input_file, sheet_name=liabilities_sheet, header=4)
        test_output = 11875.50

        cash_flow1 = Liabilities(in_df, 0.015)
        cash_flow1.calculate_present_value()

        cash_flow2 = Liabilities(in_df, 0.0151)
        cash_flow2.calculate_present_value()

        dv_calc = DV(cash_flow1.present_value, cash_flow2.present_value)
        dv_calc.calculate_dv()
        self.assertEqual(round(dv_calc.dv, 2), test_output)

    def test_modified_duration(self):
        '''
        Tests for equality to the modified duration, using input Excel spreadsheet
        Test values have been calculated using excel
        '''
        in_df = pd.read_excel(input_file, sheet_name=liabilities_sheet, header=4)
        test_output = 16.48

        cash_flow = Liabilities(in_df, 0.015)
        cash_flow.calculate_present_value()
        cash_flow.calculate_modified_duration()
        self.assertEqual(round(cash_flow.modified_duration, 2), test_output)

class TestBonds(unittest.TestCase):
    def test_present_value_a(self):
        '''

        '''
        test_output = 152186

        bond_cf = Bonds(156517, 0.015, 0.012, 10)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_present_value()
        self.assertEqual(int(test_result), test_output)


    def test_present_value_b(self):
        '''

        '''
        test_output = 156517

        bond_cf = Bonds(156517, 0.015, 0.015, 20)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_present_value()
        self.assertEqual(int(test_result), test_output)


    def test_present_value_c(self):
        '''

        '''
        test_output = 175311

        bond_cf = Bonds(156517, 0.015, 0.02, 30)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_present_value()

        self.assertEqual(int(test_result), test_output)

    def test_dv_a(self):
        '''

        '''
        test_output = 141.97

        bond_cf = Bonds(156517, 0.015, 0.012, 10)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_dv()

        self.assertEqual(round(test_result, 2), test_output)

    def test_dv_b(self):
        '''

        '''
        test_output = 268.45

        bond_cf = Bonds(156517, 0.015, 0.015, 20)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_dv()

        self.assertEqual(round(test_result, 2), test_output)

    def test_dv_c(self):
        '''

        '''
        test_output = 401.97

        bond_cf = Bonds(156517, 0.015, 0.02, 30)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_dv()

        self.assertEqual(round(test_result, 2), test_output)

    def test_mod_dur_a(self):
        '''

        '''
        test_output = 9.46

        bond_cf = Bonds(156517, 0.015, 0.012, 10)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_modified_duration()
        self.assertEqual(round(test_result, 2), test_output)

    def test_mod_dur_b(self):
        '''

        '''
        test_output = 17.41

        bond_cf = Bonds(156517, 0.015, 0.015, 20)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_modified_duration()
        self.assertEqual(round(test_result, 2), test_output)

    def test_mod_dur_c(self):
        '''

        '''
        test_output = 23.29

        bond_cf = Bonds(156517, 0.015, 0.02, 30)
        bond_cf.calc_cash_flow()
        test_result = bond_cf.calc_bond_modified_duration()
        self.assertEqual(round(test_result, 2), test_output)


class TestHedge(unittest.TestCase):


    def test_choose_bond(self):
        '''

        '''
        hedge_bond = Hedge(mapping)
        test_result1, test_result2 = hedge_bond.choose_bond(0.015)
        self.assertEqual(test_result1, 'b')
        self.assertEqual(round(test_result2, 2), 0.93)


    def test_hedge(self):
        '''

        '''
        test_output = 22.12

        hedge_bond = Hedge(mapping)
        best_bond, _ = hedge_bond.choose_bond(0.015)
        test_result = hedge_bond.hedge_risk(0.5, best_bond)

        self.assertEqual(round(test_result, 2), test_output)

if __name__ == '__main__':
    unittest.main()