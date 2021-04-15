import random
import numpy as np
import pandas as pd


def create_fake_dataframe():
    user_count = 20000
    for i in range(11):
        data_userid = np.random.randint(1, user_count, size=user_count)
        df_user = pd.DataFrame(data_userid, columns=['user_id'])
        data_postid = np.random.randint(1, user_count, size=user_count)
        df_post = pd.DataFrame(data_postid, columns=['post_id'])
        data_rating = np.random.randint(1, 5, size=user_count)
        df_rating = pd.DataFrame(data_rating, columns=['rating'])
    df_merge = pd.concat([df_user, df_post], axis=1)
    df_merge = df_merge.reset_index(drop=True)
    df = pd.concat([df_merge, df_rating], axis=1)
    df.drop_duplicates()
    print(df)
    return df


if __name__ == '__main__':
    df_rating_reduced = create_fake_dataframe()
