'''
Created on 26 Aug. 2020

@author: tim
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter




# for i in range(2):
#     plt.figure()
#     plt.show()
#     
#  
# plt.show()

def main():
    print("testing")
#     plt.style.use('ggplot')
    
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
#     plt.show()
    
    data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('entry a')
    plt.ylabel('entry b')
#     plt.show()
    
   
    
    
#     
#     print(plt.style.available)
#     
#     df = pd.read_excel("https://github.com/chris1610/pbpython/blob/master/data/sample-salesv3.xlsx?raw=true")
#     print(df.head())
#     
#     top_10 = (df.groupby('name')['ext price', 'quantity'].agg({'ext price': 'sum', 'quantity': 'count'})
#               .sort_values(by='ext price', ascending=False))[:10].reset_index()
#     top_10.rename(columns={'name': 'Name', 'ext price': 'Sales', 'quantity': 'Purchases'}, inplace=True)
#     
#     print(top_10)
#     
#     top_10.plot(kind='barh', y="Sales", x="Name")
#     
#     
#     
    fig, (ax1, ax2) = plt.subplots(1,2)  # Create a figure containing a single axes.
    ax1.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
    ax2.plot([10, 20, 3, 4], [1, 40, 2, 3])
    
    plt.show()

    print("Finished")
    
if __name__ == '__main__':
    main()
