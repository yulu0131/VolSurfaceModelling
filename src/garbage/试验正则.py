import pandas as pd
import re

string1 = "50ETF购9月2500"
string2 = "50ETF购12月2500"
pattern = r'\D\d\D\d+'
result1 = re.split(pattern, string1)
result2 = re.split(pattern, string2)
print(result1)
print(result2)
