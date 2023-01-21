from pathlib import Path

from src.comparison.algorithm_comparison import algorithm_comparison
from src.comparison.best_models import calculate_best_models
from src.comparison.dataset_comparison import dataset_comparison
from src.dataset.utils import get_dataset_names

RESULTS_BASE_DIR = Path("results")
FRIEDMAN_BASE_DIR = Path("friedman")
FRIEDMAN_TABLES = FRIEDMAN_BASE_DIR / "tables"
COMPARISON_TABLES = FRIEDMAN_BASE_DIR / "comparison_tables"
DATASET_TABLES = FRIEDMAN_BASE_DIR / "dataset_tables"
COMPARISON_TABLES.mkdir(parents=True, exist_ok=True)
DATASET_TABLES.mkdir(parents=True, exist_ok=True)

datasets = get_dataset_names()

if __name__ == "__main__":
    # calculate the best model for each dataset
    calculate_best_models(datasets, RESULTS_BASE_DIR, FRIEDMAN_BASE_DIR)

    # calculate comparison tables per algorithm combination
    algorithm_comparison(datasets, FRIEDMAN_TABLES, COMPARISON_TABLES)

    # iterate over friedman tables and create different tables per dataset
    dataset_comparison(datasets, COMPARISON_TABLES, DATASET_TABLES)
