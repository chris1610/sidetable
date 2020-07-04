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
    table = titanic.stb.freq(['sex'])
    assert table.shape == (2, 5)
    assert table['count'].sum() == 891


def test_double_group(titanic):
    """Aggregate multiple columns
    """
    table = titanic.stb.freq(['sex', 'class'])
    assert table.shape == (6, 6)
    assert table['count'].sum() == 891


def test_values(titanic):
    """ Sum the values of the fares
    """
    table = titanic.stb.freq(['embark_town', 'class'], value='fare')
    assert table.count()['class'] == 9

def test_sorting(titanic):
    """ Sum the values of the fares and sort based on columns

    """
    table = titanic.stb.freq(['embark_town', 'class'], value='fare', sort_cols=True)
    assert table.shape == (9, 6)
    assert table.iloc[-1,0] == 'Southampton'

    table = titanic.stb.freq(['embark_town', 'class'], value='fare', cum_cols=False, sort_cols=True)
    assert table.shape == (9,4)

def test_clipping(titanic):
    """Make sure we can show all the values
    """
    table = titanic.stb.freq(['class', 'deck'])
    assert table.shape == (11, 6)

    table = titanic.stb.freq(['class', 'deck'], clip_0=False)
    assert table.shape == (21, 6)

    table = titanic.stb.freq(['class', 'deck'], value='fare')
    assert table.shape == (11, 6)


def test_cutoff(titanic):
    """ Does the cutoff limit the extra rows
    """
    table = titanic.stb.freq(['class', 'deck'], value='fare')
    assert table.shape == (11, 6)

    table = titanic.stb.freq(['class', 'deck'], value='fare', thresh=94)
    assert table.shape == (5, 6)


def test_missing(titanic):
    """Validate the missing table works
    """
    table = titanic.stb.missing()
    assert table.shape == (15, 3)


def test_grand_total(titanic):
    """Validate grand total works without groups
    """
    table = titanic.stb.subtotal()
    assert table.shape == (892, 15)
    assert table.loc['grand_total', 'fare'] == 28693.9493


def test_grand_total_label(titanic):
    """Validate grand total label works
    """
    table = titanic.stb.subtotal(grand_label='Total')
    assert table.shape == (892, 15)
    assert table.loc['Total', 'fare'] == 28693.9493


def test_subtotal(titanic):
    """ Test subtotal scenarios
    """
    table = titanic.groupby(['sex', 'deck', 'class']).agg({'fare': ['sum']})
    assert table.stb.subtotal().shape == (59, 1)
    assert table.stb.subtotal(sub_level=2).shape == (57, 1)
    assert table.stb.subtotal(sub_level=2,
                              sub_label='Group Total').shape == (57, 1)
    assert table.stb.subtotal(sub_level=2, show_sep=False).shape == (57, 1)
    assert table.stb.subtotal(sub_level=[1, 2]).shape == (59, 1)
