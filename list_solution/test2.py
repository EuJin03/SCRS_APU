table_data = [
    ['a', 'b', 'c'],
    ['aaaaaaaaaa', 'b', 'c'], 
    ['a', 'bbbbbbbbbb', 'c']
]
for row in table_data:
    print("{: >10} {: >20} {: >20}".format(*row))