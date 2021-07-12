import pandas as pd


def create_df():
    """
    Create the rating dataframe from the rating.csv and adjust to fit our case
    :return: df
    """

    df = pd.read_csv("../datasets/ml-datasets/ratings-ml100k.csv")
    df.columns = ['user_id', 'post_id', 'rating_value', 'timestamp']

    # 4->3, 3->4, 5->2, 2->5
    df["rating_value"].replace({3.0: 7.0}, inplace=True)
    df["rating_value"].replace({4.0: 3.0}, inplace=True)
    df["rating_value"].replace({7.0: 4.0}, inplace=True)
    df["rating_value"].replace({5.0: 8.0}, inplace=True)
    df["rating_value"].replace({2.0: 5.0}, inplace=True)
    df["rating_value"].replace({8.0: 2.0}, inplace=True)

    df.drop('timestamp', inplace=True, axis=1)
    df.drop_duplicates()
    df = df.reset_index(drop=True)

    print(df)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    """
    # specify size of generated dataset
    df_size = 1000
    df = df.head(df_size)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)
    """

    # generate dataset -> .csv file
    df.to_csv("../datasets/ml-100k.csv")

    return df, number_of_rows


if __name__ == '__main__':
    dataset, dataset_size = create_df()




