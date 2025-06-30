import pandas as pd
import numpy as np

from settings import *

class Liabilities:
    def __init__(self, in_df, i_rate=0, t_maturity=1):
        self.input_df = in_df
        self.interest_rate = i_rate
        self.time_maturity = t_maturity
        self.present_value = None
        self.modified_duration = None

    def calculate_present_value(self, replace_interest=True):
        '''
        Calculates present value, based on either a fixed interest rate (replace_interest = True)
        or an existing interest rate column (replace_interest = False)
        '''

        self.input_df.drop([self.input_df.columns[0]], axis=1)
        if replace_interest:
            self.input_df['interest_rate'] = self.interest_rate
        self.input_df['discount'] = 1 / (1 + self.input_df['interest_rate']) ** self.input_df['Year']
        self.input_df['present_value'] = self.input_df['Cash flows'] * self.input_df['discount']
        self.present_value = round(sum(self.input_df.loc[:, 'present_value']), 2)

    def calculate_modified_duration(self):
        '''
        Calculates modified duration of liability
        '''
        if 'present_value' not in self.input_df.columns:
            raise KeyError('Please calculate the present value.')
        self.input_df['present_value_weighted'] = self.input_df['Year'] * self.input_df['present_value']
        macaulay = sum(self.input_df['present_value_weighted']) / self.present_value
        self.modified_duration = macaulay / (1 + self.interest_rate/self.time_maturity)

class DV:
    def __init__(self, i_ref, i_bp):
        self.int_ref = i_ref
        self.int_bp = i_bp
        self.dv = None

    def calculate_dv(self):
        '''
        Calculates DV01 for a given liability
        '''
        self.dv = self.int_ref - self.int_bp

class Bonds:
    def __init__(self, pr, i_rate, coup, mat):
        self.par = pr
        self.interest_rate = i_rate
        self.coupon = coup
        self.maturity =  mat
        self.bond_cash_flow_df = pd.DataFrame(index=np.arange(self.maturity),
                                         columns=['Year', 'Cash flows', 'discount', 'present_value'])

    def calc_cash_flow(self):
        '''
        Estimates bond cash flow dataframe based on a fixed interest rate, coupon and maturity
        '''
        self.bond_cash_flow_df['Year'] = np.arange(1, self.maturity+1)
        self.bond_cash_flow_df['Cash flows'] = self.par * self.coupon
        self.bond_cash_flow_df.loc[self.maturity-1, 'Cash flows'] += self.par

    def calc_bond_present_value(self):
        '''
        Calculates present value for a bond
        '''
        if self.bond_cash_flow_df.empty:
            raise ValueError('Input dataframe is empty.')

        bond_pv = Liabilities(self.bond_cash_flow_df, self.interest_rate)
        bond_pv.calculate_present_value()
        return bond_pv.present_value

    def calc_bond_dv(self):
        '''
        Calculates DV01 for a bond
        '''
        if self.bond_cash_flow_df.empty:
            raise ValueError('Input dataframe is empty.')
        bond_pv1 = Liabilities(self.bond_cash_flow_df, self.interest_rate)
        bond_pv1.calculate_present_value()

        bond_pv2 = Liabilities(self.bond_cash_flow_df, self.interest_rate + 0.0001)
        bond_pv2.calculate_present_value()

        bond_dv_calc = DV(bond_pv1.present_value, bond_pv2.present_value)
        bond_dv_calc.calculate_dv()
        return bond_dv_calc.dv

    def calc_bond_modified_duration(self):
        '''
        Calculates modified duration for a bond
        '''
        if self.bond_cash_flow_df.empty:
            raise ValueError('Input dataframe is empty.')
        bond_pv = Liabilities(self.bond_cash_flow_df, self.interest_rate, self.maturity)
        bond_pv.calculate_present_value()
        bond_pv.calculate_modified_duration()
        return bond_pv.modified_duration

class Hedge:
    def __init__(self, bond_map):
        self.target = None
        self.bond_mapping = bond_map
        self.in_df = pd.read_excel(input_file, sheet_name=liabilities_sheet, header=4)

    def choose_bond(self, i_rate):
        '''
        Chooses a bond do hedge, based on modified duration
        '''
        cash_flow = Liabilities(self.in_df, i_rate)
        cash_flow.calculate_present_value()
        cash_flow.calculate_modified_duration()

        best_modified = np.inf
        best_bond = ''
        for bond in self.bond_mapping.keys():
            bond_cf = Bonds(self.bond_mapping[bond]['par'],
                            self.bond_mapping[bond]['interest_rate'],
                            self.bond_mapping[bond]['coupon'],
                            self.bond_mapping[bond]['maturity'])
            bond_cf.calc_cash_flow()
            mod_duration = bond_cf.calc_bond_modified_duration()

            if abs(mod_duration - cash_flow.modified_duration) < best_modified:
                best_modified = abs(mod_duration - cash_flow.modified_duration)
                best_bond = bond
        return best_bond, best_modified

    def hedge_risk(self, target, best_bond):
        '''
        Calculates bond notional, based on the target hedge and the best bond
        '''
        cash_flow1 = Liabilities(self.in_df,0.015)
        cash_flow1.calculate_present_value()
        print('1.5% ', cash_flow1.present_value)

        cash_flow2 = Liabilities(self.in_df, 0.0151)
        cash_flow2.calculate_present_value()
        print('1.51% ', cash_flow2.present_value)

        dv_calc = DV(cash_flow1.present_value, cash_flow2.present_value)
        dv_calc.calculate_dv()

        best_bond_map = mapping[best_bond]
        best_bond_cf = Bonds(best_bond_map['par'], best_bond_map['interest_rate'],
                             best_bond_map['coupon'], best_bond_map['maturity'])
        best_bond_cf.calc_cash_flow()
        bond_dv = best_bond_cf.calc_bond_dv()

        total_hedge = dv_calc.dv * target
        notional = total_hedge / bond_dv
        return notional

class HedgeAnalysis:
    def __init__(self, in_df):
        self.input_df = in_df


    def calculate_hedge_ratio(self):
        self.input_df['Cash flows'] = mapping['b']['par'] * mapping['b']['coupon']
        liab1 = Liabilities(self.input_df)
        liab1.calculate_present_value(replace_interest=False)
        self.input_df['interest_rate'] += 0.0001
        liab2 = Liabilities(self.input_df)
        liab2.calculate_present_value(replace_interest=False)

        liab_dv = DV(liab1.present_value, liab2.present_value)
        liab_dv.calculate_dv()
        return 0


if __name__ == '__main__':
    # Task 1
    print('task 1')
    in_df = pd.read_excel(input_file, sheet_name=liabilities_sheet, header=4)
    cash_flow = Liabilities(in_df, 0.015)
    cash_flow.calculate_present_value()
    print('Present value ', cash_flow.present_value, '\n')

    # Task 2
    print('task 2')
    cash_flow1 = Liabilities(in_df,0.015)
    cash_flow1.calculate_present_value()
    print('1.5% ', cash_flow1.present_value)

    cash_flow2 = Liabilities(in_df, 0.0151)
    cash_flow2.calculate_present_value()
    print('1.51% ', cash_flow2.present_value)

    dv_calc = DV(cash_flow1.present_value, cash_flow2.present_value)
    dv_calc.calculate_dv()
    print('DV01 ', dv_calc.dv, '\n')

    # Task 3
    print('task 3')
    cash_flow = Liabilities(in_df, 0.015)
    cash_flow.calculate_present_value()
    cash_flow.calculate_modified_duration()
    print('Modified duration ', round(cash_flow.modified_duration, 2), '\n')

    # Task 4
    print('task 4')
    bond_cf = Bonds(1000, 0.015, 0.012, 10)
    bond_cf.calc_cash_flow()
    pv_a = bond_cf.calc_bond_present_value()
    print('Present value for bond a: ', round(pv_a, 2), '\n')

    # Task 5
    print('task 5')
    bond_cfa = Bonds(1000, 0.015, 0.012, 10)
    bond_cfa.calc_cash_flow()
    modified_duration_a = bond_cfa.calc_bond_modified_duration()
    print('Modified duration for bond a: ', round(modified_duration_a, 2))

    bond_cfb = Bonds(1000, 0.015, 0.015, 20)
    bond_cfb.calc_cash_flow()
    modified_duration_b = bond_cfb.calc_bond_modified_duration()
    print('Modified duration for bond b: ', round(modified_duration_b, 2))

    bond_cfc = Bonds(1000, 0.015, 0.02, 30)
    bond_cfc.calc_cash_flow()
    modified_duration_c = bond_cfc.calc_bond_modified_duration()
    print('Modified duration for bond b: ', round(modified_duration_c, 2), '\n')

    # Task 6
    print('task 6')
    print('Selection criteria based on modified duration.')
    mapping = {
        'a': {
            'par': 1000,
            'interest_rate': 0.015,
            'coupon': 0.012,
            'maturity': 10
        },
        'b': {
            'par': 1000,
            'interest_rate': 0.015,
            'coupon': 0.015,
            'maturity': 20
        },
        'c': {
            'par': 1000,
            'interest_rate': 0.015,
            'coupon': 0.02,
            'maturity': 30
        }
    }
    hedge_bond = Hedge(mapping)
    best_bond, _ = hedge_bond.choose_bond(0.015)
    print(f'Best matching bond based on modified duration: {best_bond} \n')

    # Task 7
    print('task 7')
    hedge_bond = Hedge(mapping)
    best_bond, _ = hedge_bond.choose_bond(0.015)
    notional = hedge_bond.hedge_risk(0.5, best_bond)
    print(f'Notional for bond b and 50% target: {notional}')

    # Task 8
    in_df = pd.read_excel(input_file, sheet_name=hedge_analysis, header=2)
    in_df = in_df.rename(columns={'Days from now': 'Year', 'Interest rate': 'interest_rate'})
    hedge_analysis = HedgeAnalysis(in_df)
    hedge_analysis.calculate_hedge_ratio()
    print()