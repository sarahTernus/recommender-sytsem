import pandas as pd


def create_df():
    """
    Create the rating dataframe from the rating.csv and adjust to fit our case
    :return: df
    """

    df = pd.read_csv("../datasets/ml-datasets/ratings-ml20m.csv")
    df.columns = ['userId', 'postId', 'rating', 'timestamp']

    """df_movie = df_movie[(df_movie.rating != 0.5) & (df_movie.rating != 1.5) &
                        (df_movie.rating != 2.5) & (df_movie.rating != 4.5)]"""

    df["rating"].replace({0.5: 1}, inplace=True)
    df["rating"].replace({1.5: 2}, inplace=True)
    df["rating"].replace({2.5: 2}, inplace=True)
    df["rating"].replace({3.5: 3}, inplace=True)
    df["rating"].replace({4.5: 3}, inplace=True)

    df.drop('timestamp', inplace=True, axis=1)
    df.drop_duplicates()
    df = df.reset_index(drop=True)

    print(df)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    df_size = 1000000
    df = df.head(df_size)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    df.to_csv("../datasets/dataset4.csv")

    return df, number_of_rows


if __name__ == '__main__':
    dataset, dataset_size = create_df()
