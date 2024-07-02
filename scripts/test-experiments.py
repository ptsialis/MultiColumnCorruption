
import json
import subprocess
from pathlib import Path

# CHANGE ME!
# experiment_name = "fully_observed_corrupted"
# experiment_name = "corrupted"  # NOTE: 'corrupted' is the keyword to switch to the second experiment.


# Default Values
# num_repetitions = 3
# ase_path = "/results_mode_all_test"

MISSING_FRACTIONS = [0.01, 0.1, 0.3, 0.5]
MISSING_TYPES = ["MCAR","MNAR","MAR"]
IMPUTER = ["gain", "vae", "dl", "forest", "knn","mode"] 
STRATEGIES = ["single_all"]

binary_task_ids = json.loads(Path("../data/raw/binary.txt").read_text())
multi_task_ids = json.loads(Path("../data/raw/multi.txt").read_text())
regression_task_ids = json.loads(Path("../data/raw/regression.txt").read_text())

dataset_ids = [*binary_task_ids.keys(), *multi_task_ids.keys(), *regression_task_ids.keys()]
#

###############

types_as_argument_string = r'\,'.join(MISSING_TYPES)
strategies_as_argument_string = r'\,'.join(STRATEGIES)
fractions_as_argument_string = r'\,'.join([str(x) for x in MISSING_FRACTIONS])

imputation_methods = ["vae", "gain", "dl"]
experiment_name = "experiment_multi_column_corrupted"
missing_fractions = "0.01,0.1,0.3,0.5"
missing_types = "MAR,MCAR,MNAR"
strategies = "single_all"
num_repetitions = 3
base_path = "../results"

regression = [42545, 42675, 198, 23515, 189, 287, 42636, 42688, 42183, 1199, 197, 218, 42712, 1193, 216, 215, 23395, 42225, 1200, 1213, 42669]

binary1 = [737, 871, 40983, 728, 1489, 803, 923, 725, 42192, 1558, 310, 1046, 847, 40701, 41146, 1496, 1507, 823, 42493, 1471, 1120, 4315]

binary2_multi = [137, 251, 1220, 151, 901, 881, 40922, 42477, 23517, 1526, 183, 40498, 30, 40677, 1459, 40497, 4552, 26, 375, 32, 1481, 184, 41027, 6, 41671, 40685] 

for imputation_method in imputation_methods:
    for dataset_id in dataset_ids:
        # Aufbau des Befehls
        command = [
            "python",
            "run-experiment.py",
            str(dataset_id),
            "dl",
            experiment_name,
            "--missing-fractions", missing_fractions,
            "--missing-types", missing_types,
            "--strategies", strategies,
            "--num-repetitions", str(num_repetitions),
            "--base-path", base_path
        ]

    
        subprocess.run(command)
