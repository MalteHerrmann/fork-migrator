import numpy as np
from check_fork import compare_repositories


def test_compare_same_repositories():
    repo1_path = 'testdata/evmos'

    overlap_percentages = compare_repositories(repo1_path, repo1_path)
    assert overlap_percentages != []
    assert np.mean([x[2] for x in overlap_percentages]) == 100


def test_compare_replaced_repo():
    repo1_path = 'testdata/aether'
    repo2_path = 'testdata/evmos'

    overlap_percentages = compare_repositories(repo1_path, repo2_path)
    assert overlap_percentages != []
    assert np.mean([x[2] for x in overlap_percentages]) < 100
