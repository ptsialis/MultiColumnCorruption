import json
import math
import random
import time
import logging
from pathlib import Path
from statistics import mean, stdev
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd
from jenga.corruptions.generic import MissingValues
from jenga.tasks.openml import OpenMLTask
from jenga.utils import BINARY_CLASSIFICATION, MULTI_CLASS_CLASSIFICATION, REGRESSION
from numpy import nan
from sklearn.metrics import f1_score, mean_absolute_error, mean_squared_error

from .imputation._base import BaseImputer
from .imputation.utils import set_seed


class EvaluationError(Exception):
    """Exception raised for errors in Evaluation classes"""
    pass


class EvaluationResult(object):

    def __init__(self, task: OpenMLTask, target_column: str):

        self._task = task
        self._target_column = target_column
        self._finalized = False
        self.results: List[pd.DataFrame] = []
        self.downstream_performances: List[pd.DataFrame] = []
        self.elapsed_train_times: List[float] = []
        self.best_hyperparameters: List[Dict[str, List[dict]]] = []
        self.repetitions = 0

        if self._task._task_type == BINARY_CLASSIFICATION or self._task._task_type == MULTI_CLASS_CLASSIFICATION:
            self._baseline_metric = ("F1_micro", "F1_macro", "F1_weighted")

        elif self._task._task_type == REGRESSION:
            self._baseline_metric = ("MAE", "MSE", "RMSE")

        self._baseline_performance = self._task.get_baseline_performance()
        self._set_imputation_task_type()

    def append(
        self,
#        target_column: str,
    ):

        if self._finalized:
            raise EvaluationError("Evaluation already finalized")



        self.downstream_performances.append(
            pd.DataFrame(
                {
                    "baseline": {
                        self._baseline_metric[0]: self._baseline_performance[0],
                        self._baseline_metric[1]: self._baseline_performance[1],
                        self._baseline_metric[2]: self._baseline_performance[2]
                    },
                }
            )
        )


        self.repetitions += 1

    def finalize(self):

        if self._finalized:
            raise EvaluationError("Evaluation already finalized")


        results_mean_list = self.downstream_performances
        results_mean_list = results_mean_list[0]
        results_mean_df = pd.DataFrame(results_mean_list, columns=['baseline'])

        self.downstream_performance = results_mean_df

        self._finalized = True

        return self

    

    def _set_imputation_task_type(self):
        if pd.api.types.is_numeric_dtype(self._task.train_data[self._target_column]):
            self._imputation_task_type = "regression"

        elif pd.api.types.is_categorical_dtype(self._task.train_data[self._target_column]):
            num_classes = len(self._task.train_data[self._target_column].dtype.categories)

            if num_classes == 2:
                self._imputation_task_type = "binary_classification"

            elif num_classes > 2:
                self._imputation_task_type = "multiclass_classification"

            else:
                raise EvaluationError(f"Found categorical imputation with {num_classes} categories")

        else:
            raise EvaluationError(f"datatype of column '{self._target_column}' not recognized")

    # TODO: reduce code...
    def _update_results(
        self,
        train: pd.Series,
        train_imputed: pd.Series,
        test: pd.Series,
        test_imputed: pd.Series,
        imputation_type: str
    ):

        if self._imputation_task_type == "regression":
            self.results.append(
                pd.DataFrame(
                    {
                        "train": {
                            "MAE": mean_absolute_error(train, train_imputed) if ~train_imputed.isna().any() else nan,
                            "MSE": mean_squared_error(train, train_imputed) if ~train_imputed.isna().any() else nan,
                            "RMSE": math.sqrt(mean_squared_error(train, train_imputed)) if ~train_imputed.isna().any() else nan
                        },
                        "test": {
                            "MAE": mean_absolute_error(test, test_imputed) if ~test_imputed.isna().any() else nan,
                            "MSE": mean_squared_error(test, test_imputed) if ~test_imputed.isna().any() else nan,
                            "RMSE": math.sqrt(mean_squared_error(test, test_imputed)) if ~test_imputed.isna().any() else nan
                        }
                    }
                )
            )

        elif "classification" in self._imputation_task_type:
            self.results.append(
                pd.DataFrame(
                    {
                        "train": {
                            "F1_micro": f1_score(train, train_imputed, average="micro") if ~train_imputed.isna().any() else nan,
                            "F1_macro": f1_score(train, train_imputed, average="macro") if ~train_imputed.isna().any() else nan,
                            "F1_weighted": f1_score(train, train_imputed, average="weighted") if ~train_imputed.isna().any() else nan,
                        },
                        "test": {
                            "F1_micro": f1_score(test, test_imputed, average="micro") if ~test_imputed.isna().any() else nan,
                            "F1_macro": f1_score(test, test_imputed, average="macro") if ~test_imputed.isna().any() else nan,
                            "F1_weighted": f1_score(test, test_imputed, average="weighted") if ~test_imputed.isna().any() else nan,
                        }
                    }
                )
            )


class Evaluator(object):

    def __init__(
        self,
        task: OpenMLTask,
        missing_fraction: float,
        missing_type: str,
        target_columns: List[str],
        imputer_class: Callable[..., BaseImputer],
        imputer_args: dict,
        discard_in_columns: Optional[List[str]] = None,
        path: Optional[Path] = None,
        seed: Optional[int] = 42
    ):

        self._task = task
        self._missing_fraction = missing_fraction
        self._missing_type = missing_type
        self._target_columns = target_columns
        self._imputer_class = imputer_class
        self._imputer_arguments = imputer_args
        self._discard_in_columns = discard_in_columns if discard_in_columns is not None else self._target_columns
        self._path = path
        self._result: Optional[Dict[str, EvaluationResult]] = None
        self._seed = seed

        for target_column in self._target_columns:
            if target_column not in self._discard_in_columns:
                raise EvaluationError("All target_columns must be in discard_in_columns")

        # fit task's baseline model and get performance
        self._task.fit_baseline_model()

        # Because we set determinism here, supres downstream determinism mechanisms
        if self._seed:
            set_seed(self._seed)
            self._imputer_arguments.pop("seed", None)

    @staticmethod
    def report_results(result_dictionary: Dict[str, EvaluationResult]) -> None:
        target_columns = list(result_dictionary.keys())

        print(f"Evaluation result contains {len(target_columns)} target columns: {', '.join(target_columns)}")
        print("All are in a round-robin fashion imputed and performances are as follows:\n")

        for key, value in result_dictionary.items():
            print(f"Target Column: {key} - Necessary train time in seconds: {round(value.elapsed_train_time, 4)}")
            print(value.result)
            print()
            print(value.downstream_performance)
            print("\n")

    def evaluate(self, num_repetitions: int):

        result = {}

        for target_column in self._target_columns:

            result_temp = EvaluationResult(self._task, target_column)
        
            # NOTE: masks are DataFrames => append expects Series
            result_temp.append(
                #target_column=target_column,
            )

            result[target_column] = result_temp.finalize()

        self._result = result
        self._save_results()

        return self

    def report(self) -> None:
        if self._result is None:
            raise EvaluationError("Not evaluated yet. Call 'evaluate' first!")

        else:
            self.report_results(self._result)

    def _discard_values(
        self,
        task: OpenMLTask,
        to_discard_columns: List[str],
        missing_fraction: float,
        missing_type: str,
 #       seed: int,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:

        columns = to_discard_columns
        fraction = missing_fraction / len(columns)
        missing_values = []
        for column in columns:
            missing_values.append(MissingValues(column=column, fraction=fraction, missingness=missing_type))

        # Apply all
        train_data = task.train_data.copy()
        test_data = task.test_data.copy()

        for missing_value in missing_values:
            #train_data = missing_value.transform(train_data)
            #test_data = missing_value.transform(test_data)
            train_data = missing_value.transform(train_data)
            test_data = missing_value.transform(test_data)

        return (train_data, test_data)

    def _save_results(self):
        if self._path is not None:
            self._path.mkdir(parents=True, exist_ok=True)

            for column in self._result.keys():

                # '/' in column screw up the file paths
                column_string = column.replace("/", ":")

                # Mean results
                
                self._result[column].downstream_performance.to_csv(self._path / f"downstream_performance_mean_{column_string}.csv")

                results_path = self._path / column_string
                results_path.mkdir(parents=True, exist_ok=True)

                for index, (impute_data_frame, performance_data_frame, best_hyperparameters, elapsed_train_time) in enumerate(
                    zip(
                        self._result[column].results,
                        self._result[column].downstream_performances,
                        self._result[column].best_hyperparameters,
                        self._result[column].elapsed_train_times
                    )
                ):

                    impute_data_frame.to_csv(results_path / f"impute_performance_rep_{index}.csv")
                    performance_data_frame.to_csv(results_path / f"downstream_performance_rep_{index}.csv")
                    Path(results_path / f"elapsed_train_time_rep_{index}.json").write_text(json.dumps(elapsed_train_time))
                    Path(results_path / f"best_hyperparameters_rep_{index}.json").write_text(json.dumps(best_hyperparameters))


class SingleColumnEvaluator(Evaluator):
    """
    Evaluate Missing Value effects on single column.
    """

    def __init__(
        self,
        task: OpenMLTask,
        missing_fraction: float,
        missing_type: str,
        target_column: str,
        imputer_class: Callable[..., BaseImputer],
        imputer_args: dict,
        path: Optional[Path] = None,
        seed: Optional[int] = 42
    ):
        #logger.info(f"seed in experiment script")
        super().__init__(
            task=task,
            missing_fraction=missing_fraction,
            missing_type=missing_type,
            target_columns=[target_column],
            imputer_class=imputer_class,
            imputer_args=imputer_args,
            discard_in_columns=[target_column],
            path=path,
            seed=seed
        )


class MultipleColumnsEvaluator(Evaluator):
    """
    Evaluate Missing Value effects on multiple columns.
    """

    def __init__(
        self,
        task: OpenMLTask,
        missing_fraction: float,
        missing_type: str,
        target_column: List[str],
        imputer_class: Callable[..., BaseImputer],
        imputer_args: dict,
        path: Optional[Path] = None,
        seed: Optional[int] = 42
    ):

        super().__init__(
            task=task,
            missing_fraction=missing_fraction,
            missing_type=missing_type,
            target_columns=target_column,
            imputer_class=imputer_class,
            imputer_args=imputer_args,
            discard_in_columns=target_column,
            path=path,
            seed=seed
        )


class SingleColumnAllMissingEvaluator(Evaluator):
    """
    Evaluate Missing Value effects on single column when all columns contain missing values.
    """

    def __init__(
        self,
        task: OpenMLTask,
        missing_fraction: float,
        missing_type: str,
        target_column: str,
        imputer_class: Callable[..., BaseImputer],
        imputer_args: dict,
        path: Optional[Path] = None,
        seed: Optional[int] = 42
    ):

        super().__init__(
            task=task,
            missing_fraction=missing_fraction,
            missing_type=missing_type,
            target_columns=[target_column],
            imputer_class=imputer_class,
            imputer_args=imputer_args,
            discard_in_columns=task.train_data.columns.tolist(),
            path=path,
            seed=seed
        )


class MultipleColumnsAllMissingEvaluator(Evaluator):
    """
    Evaluate Missing Value effects on multiple columns when all columns contain missing values.
    """

    def __init__(
        self,
        task: OpenMLTask,
        missing_fraction: float,
        missing_type: str,
        target_column: List[str],
        imputer_class: Callable[..., BaseImputer],
        imputer_args: dict,
        path: Optional[Path] = None,
        seed: Optional[int] = 42
    ):

        super().__init__(
            task=task,
            missing_fraction=missing_fraction,
            missing_type=missing_type,
            target_columns=target_column,
            imputer_class=imputer_class,
            imputer_args=imputer_args,
            discard_in_columns=task.train_data.columns.tolist(),
            path=path,
            seed=seed
        )