from tim import InvestmentAnalyzer

analyser = InvestmentAnalyzer('test.csv', with_scam=True, stop_loss=0.3)
print(analyser.find_value(540000, 990000))