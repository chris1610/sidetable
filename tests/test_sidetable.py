# -*- coding: utf-8 -*-

"""Tests for `sidetable` package."""

import pytest
from sidetable import sidetable
import pandas as pd


@pytest.fixture
def titanic():
    """Use seaborn's titanic data for testing
    Includes multiple different types of data.
    Good for testing.
    """
    import seaborn as sns
    df = sns.load_dataset('titanic')
    return df

def test_single_group(titanic):
    """Basic test that we aggregate correctly for one column
    """
    table = titanic.st.freq(['sex'])
    assert table.shape == (2,5)
    assert table['Count'].sum() == 891

def test_double_group(titanic):
    """Aggregate multiple columns
    """
    table = titanic.st.freq(['sex', 'class'])
    assert table.shape == (6, 6)
    assert table['Count'].sum() == 891

def test_values(titanic):
    """ Summ the values of the fares
    """
    table = titanic.st.freq(['embark_town', 'class'], value='fare')
    assert table.count()['class'] == 9

def test_clipping(titanic):
    """Make sure we can show all the values
    """
    table = titanic.st.freq(['class', 'deck'])
    assert table.shape == (11, 6)

    table = titanic.st.freq(['class', 'deck'], clip_0=False)
    assert table.shape == (21, 6)

    table = titanic.st.freq(['class', 'deck'], value='fare')
    assert table.shape ==  (11,6)

def test_cutoff(titanic):
    """ Does the cutoff limit the extra rows
    """
    table = titanic.st.freq(['class', 'deck'], value='fare')
    assert table.shape == (11, 6)

    table = titanic.st.freq(['class', 'deck'], value='fare', thresh=.94)
    assert table.shape == (5, 6)