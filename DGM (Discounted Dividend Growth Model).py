def gordon_growth_model(dividend, discount_rate, growth_rate):
    intrinsic_value = dividend / (discount_rate - growth_rate)
    return intrinsic_value

def discounted_cash_flow(cash_flows, discount_rate, terminal_multiple):
    terminal_value = cash_flows[-1] * terminal_multiple
    present_value = sum([cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows[:-1])])
    intrinsic_value = present_value + terminal_value / (1 + discount_rate) ** len(cash_flows)
    return intrinsic_value

# Assumptions for Set 1
dividend_set1 = 2.5
discount_rate_set1 = 0.1
growth_rate_set1 = 0.03
cash_flows_set1 = [5, 7, 9, 11, 13]
terminal_multiple_set1 = 15

# Assumptions for Set 2
dividend_set2 = 3.0
discount_rate_set2 = 0.12
growth_rate_set2 = 0.02
cash_flows_set2 = [6, 8, 10, 12, 14]
terminal_multiple_set2 = 12

# Assumptions for Set 3
dividend_set3 = 2.0
discount_rate_set3 = 0.08
growth_rate_set3 = 0.04
cash_flows_set3 = [4, 6, 8, 10, 12]
terminal_multiple_set3 = 18

# Calculate intrinsic value using Gordon Growth Model for each set of assumptions
ggm_value_set1 = gordon_growth_model(dividend_set1, discount_rate_set1, growth_rate_set1)
ggm_value_set2 = gordon_growth_model(dividend_set2, discount_rate_set2, growth_rate_set2)
ggm_value_set3 = gordon_growth_model(dividend_set3, discount_rate_set3, growth_rate_set3)

# Calculate intrinsic value using Discounted Cash Flow with Terminal Multiple for each set of assumptions
dcf_value_set1 = discounted_cash_flow(cash_flows_set1, discount_rate_set1, terminal_multiple_set1)
dcf_value_set2 = discounted_cash_flow(cash_flows_set2, discount_rate_set2, terminal_multiple_set2)
dcf_value_set3 = discounted_cash_flow(cash_flows_set3, discount_rate_set3, terminal_multiple_set3)

# Print results
print(f'Set 1 - Intrinsic Value (Gordon Growth Model): {ggm_value_set1:.2f}')
print(f'Set 1 - Intrinsic Value (DCF with Terminal Multiple): {dcf_value_set1:.2f}')
print()
print(f'Set 2 - Intrinsic Value (Gordon Growth Model): {ggm_value_set2:.2f}')
print(f'Set 2 - Intrinsic Value (DCF with Terminal Multiple): {dcf_value_set2:.2f}')
print()
print(f'Set 3 - Intrinsic Value (Gordon Growth Model): {ggm_value_set3:.2f}')
print(f'Set 3 - Intrinsic Value (DCF with Terminal Multiple): {dcf_value_set3:.2f}')