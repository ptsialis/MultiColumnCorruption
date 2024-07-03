import os
from pathlib import Path
import json


# scripts to run multiple experiments 


# Binary Experiments

# binary_task_id_mappings = json.loads(Path("./data/raw/binary.txt").read_text())
# BINARY_TASK_IDS = [int(x) for x in binary_task_id_mappings.keys()]

# methods = ["mode", "knn", "forest", "dl", "gain", "vae"]
print(os.getcwd()) 

# for i in BINARY_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment.py {i} {j} corrupted_binary_experiment --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

# Multi Experiments


multi_task_id_mappings = json.loads(Path("./data/raw/multi.txt").read_text())
MULTI_TASK_IDS = [int(x) for x in multi_task_id_mappings.keys()]

methods = ["mode"] #, "knn", "forest", "dl" "gain", "vae"]


for i in MULTI_TASK_IDS:
    for j in methods:
        os.system(f"python ./scripts/run-experiment.py {i} {j} corrupted_multi_experiment_MLP --missing-fractions 0.5 --missing-types MCAR --strategies single_all --num-repetitions 3 --base-path ../results")

        
# # Regression Experiments

# regression_task_id_mappings = json.loads(Path("./data/raw/regression.txt").read_text())
# REGRESSION_TASK_IDS = [int(x) for x in regression_task_id_mappings.keys()]

# methods = ["mode", "knn", "forest", "dl", "gain", "vae"]



# for i in REGRESSION_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment-subset.py {i} {j} corrupted_regression_experiment --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")







# # Binary Subset Experiments

# binary_task_id_mappings = json.loads(Path("./data/raw/binary.txt").read_text())
# BINARY_TASK_IDS = [int(x) for x in binary_task_id_mappings.keys()]

# methods = ["mode", "knn", "forest", "dl", "gain", "vae"]


# for i in BINARY_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment-subset.py {i} {j} corrupted_binary_experiment_subset --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

# # Multi Subset Experiments


# multi_task_id_mappings = json.loads(Path("./data/raw/multi.txt").read_text())
# MULTI_TASK_IDS = [int(x) for x in multi_task_id_mappings.keys()]

# methods = ["mode", "knn", "forest", "dl" "gain", "vae"]


# for i in MULTI_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment-subset.py {i} {j} corrupted_multi_experiment_subset --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

        
# # Regression Subset Experiments

# regression_task_id_mappings = json.loads(Path("./data/raw/regression.txt").read_text())
# REGRESSION_TASK_IDS = [int(x) for x in regression_task_id_mappings.keys()]

# methods = ["mode", "knn", "forest", "dl", "gain", "vae"]



# for i in REGRESSION_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment.py {i} {j} corrupted_regression_experiment_subset --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

 


# # Binary Baseline Experiments

# binary_task_id_mappings = json.loads(Path("./data/raw/binary.txt").read_text())
# BINARY_TASK_IDS = [int(x) for x in binary_task_id_mappings.keys()]

# methods = ["mode"]#, "knn", "forest", "dl", "gain", "vae"]


# for i in BINARY_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment.py {i} {j} baseline_binary_experiment --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

# # Multi Baseline Experiments


# multi_task_id_mappings = json.loads(Path("./data/raw/multi.txt").read_text())
# MULTI_TASK_IDS = [int(x) for x in multi_task_id_mappings.keys()]

# methods = ["mode"]#, "knn", "forest", "dl" "gain", "vae"]


# for i in MULTI_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment.py {i} {j} baseline_multi_experiment --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")

        
# # Regression Baseline Experiments

# regression_task_id_mappings = json.loads(Path("./data/raw/regression.txt").read_text())
# REGRESSION_TASK_IDS = [int(x) for x in regression_task_id_mappings.keys()]

# methods = ["mode"]#, "knn", "forest", "dl", "gain", "vae"]



# for i in REGRESSION_TASK_IDS:
#     for j in methods:
#         os.system(f"python ./scripts/run-experiment.py {i} {j} baseline_regression_experiment --missing-fractions 0.01,0.1,0.3,0.5 --missing-types MCAR,MAR,MNAR --strategies single_single --num-repetitions 3 --base-path ../results")



