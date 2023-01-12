import sys
import pandas as pd
import numpy as np

"""
Merge 2 files into 1

Usage:
python3 ./analysis.py x_list.txt y_list.txt
"""

def main():
    x = pd.read_csv(sys.argv[1], sep="\t")
    y = pd.read_csv(sys.argv[2], sep="\t")
    print(x)

    res = pd.DataFrame.from_records(
        [
            np.concatenate((x_row, y_row), axis=None)
            for x_index, x_row in x.iterrows()
            for y_index, y_row in y.iterrows()
        ],
        columns=["ID_x", "value_x","ID_y","value_y"],
    )

    print(res[res["ID_x"] == res["ID_y"]].drop(columns="ID_y"))


if __name__ == "__main__":
    main()
