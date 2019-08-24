from DataParser import DataParser
from DeepLearning import DeepLearning
import pandas as pd
from urllib.request import Request, urlopen


def main():
    # ======= COLLECT DATA =======
    # set to true if need to collect data
    if False:
        dp = DataParser()
        dp.readData()

    # ======= READ IN DATA =======
    df = pd.DataFrame()
    for i in range(0, 5):
        df = df.append(pd.read_csv("data/vancouver_data_{0}.csv".format(i), sep="\t", index_col=False))
    
    # ======= PROCESS DATA =======
    dl = DeepLearning(df.values)
    dl.process()
    

if __name__ == "__main__":
    main()