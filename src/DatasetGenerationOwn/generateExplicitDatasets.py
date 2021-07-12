import pandas as pd


def create_dataset_ex():
    """ create a explicit dataset from hybrid dataset
    :return: pandas dataframe
    """
    df = pd.read_csv("../datasets/location/dataset-location.csv", index_col=0)
    df = df[df.rating_value != 3]
    df = df.reset_index()
    df = df.drop(columns=['index'])

    df["rating_value"].replace({4.0: 3}, inplace=True)
    df["rating_value"].replace({5.0: 4}, inplace=True)

    df.to_csv("../datasets/explicit-test.csv")

    return df


if __name__ == '__main__':
    dataset = create_dataset_ex()
