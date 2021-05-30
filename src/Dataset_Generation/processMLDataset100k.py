import pandas as pd


def create_df():
    """
    Create the rating dataframe from the rating.csv and adjust to fit our case
    :return: df
    """

    df = pd.read_csv("../datasets/ml-datasets/ratings-ml100k.csv")
    df.columns = ['userId', 'postId', 'rating', 'timestamp']

    df.drop('timestamp', inplace=True, axis=1)
    df.drop_duplicates()
    df = df.reset_index(drop=True)

    print(df)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    """df_size = 10000
    df = df.head(df_size)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)"""

    df.to_csv("../datasets/dataset3b.csv")

    return df, number_of_rows


if __name__ == '__main__':
    dataset, dataset_size = create_df()




