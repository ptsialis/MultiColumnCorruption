from typing import Optional

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

from ..basis import (
    BinaryClassificationTask,
    MultiClassClassificationTask,
    RegressionTask,
    Task
)


class OpenMLTask(Task):

    def __init__(self, openml_id: int, train_size: float = 0.8, seed: Optional[int] = None):
        """
        Base class for task that get data from [OpenML](https://www.openml.org).

        Args:
            openml_id (int): ID of the to-be-fetched data from [OpenML](https://www.openml.org)
            train_size (float, optional): Defines the data split. Defaults to 0.8.
            seed (Optional[int], optional): Seed for determinism. Defaults to None.
        """

        
        seed=32 #PD

        print("______________________________")#PD
#        print(seed, "seed for training-test-split")#PD
#        print(openml_id, "Datensatz Nummer")#PD
        print("SUBSET OPENML ________________________________-")
        print("______________________________")#PD


        X, y = fetch_openml(data_id=openml_id, as_frame=True, return_X_y=True, cache=False)


        # NEW FOR SUBSET TESTS!!!
        #X.to_csv("1_X_after_pull.csv")   
        #y.to_csv("2_y_after_pull.csv")      
        print(type(X))
        print(type(y))
        before_subset = pd.concat([X, y], axis=1)
        #before_subset.to_csv("3_before_subset_concat.csv")  

        np.random.seed(32)
        len_dataset = len(before_subset)
        print(len_dataset,'Length of dataset')
#        remove_n = (len_dataset*0.9)
#        print(remove_n,'amount of values to remove')
#        drop_indices = np.random.choice(before_subset.index, remove_n, replace=False)
        df_subset = before_subset.sample(frac=0.10)
#        df_subset = before_subset.drop(drop_indices)
        #df_subset.to_csv("4_subset.csv")
        y_df = df_subset.iloc[:,-1:]
        y = y_df.iloc[:,0]
        #y.to_csv("5_y_new.csv")
        print(type(y))
        X = df_subset[df_subset.columns[:-1]]
        #X.to_csv("6_X_new.csv")
        print(type(X))
        # NEW FOR SUBSET TESTS!!!UNTIL HERE!!!!!  


        seed=32 #PD
        train_data, test_data, train_labels, test_labels = train_test_split(X, y, train_size=train_size)
        #test_data.to_csv("corrupted_original_test_data_after_pull.csv")#PD
        categorical_columns = [
            column for column in X.columns
            if pd.api.types.is_categorical_dtype(X[column])
        ]
        numerical_columns = [
            column for column in X.columns
            if pd.api.types.is_numeric_dtype(X[column]) and column not in categorical_columns
        ]

        super().__init__(
            train_data=train_data,
            train_labels=train_labels,
            test_data=test_data,
            test_labels=test_labels,
            categorical_columns=categorical_columns,
            numerical_columns=numerical_columns,
            is_image_data=False,
            seed=seed
        )


class OpenMLRegressionTask(OpenMLTask, RegressionTask):
    """
    Class that represents a regression task and gets data from [OpenML](https://www.openml.org).
    """

    pass


class OpenMLMultiClassClassificationTask(OpenMLTask, MultiClassClassificationTask):
    """
    Class that represents a multi-class classification task and gets data from [OpenML](https://www.openml.org).
    """

    pass


class OpenMLBinaryClassificationTask(OpenMLTask, BinaryClassificationTask):
    """
    Class that represents a binary classification task and gets data from [OpenML](https://www.openml.org).
    """

    pass
