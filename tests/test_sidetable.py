# -*- coding: utf-8 -*-
"""Tests for `sidetable` package."""

import pytest
from sidetable import sidetable
import pandas as pd
import warnings


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
    table = titanic.stb.freq(['embark_town', 'class'],
                             value='fare',
                             sort_cols=True)
    assert table.shape == (9, 6)
    assert table.iloc[-1, 0] == 'Southampton'

    table = titanic.stb.freq(['embark_town', 'class'],
                             value='fare',
                             cum_cols=False,
                             sort_cols=True)
    assert table.shape == (9, 4)


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


def test_thresh_warning(titanic):
    """ Validate user warning runs if threshold < 1
    """
    with pytest.warns(UserWarning):
        table = titanic.stb.freq(['class', 'deck'], value='fare', thresh=.94)


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


def test_counts(titanic):
    """Test counts scenarios
    """
    assert titanic.stb.counts().shape == (15, 6)
    assert titanic.stb.counts(include='number').shape == (6, 6)
    assert titanic.stb.counts(exclude='number').shape == (9, 6)
    answer = pd.Series([891, 248, 8.05, 43, 5.0, 1],
                       index=[
                           'count', 'unique', 'most_freq', 'most_freq_count',
                           'least_freq', 'least_freq_count'
                       ],
                       name='fare',
                       dtype='object')
    pd.testing.assert_series_equal(
        titanic.stb.counts(sort_ascending=False).iloc[0], answer)


def test_flatten(titanic):
    """Test the flatten function
    """
    fares = titanic.groupby(['embark_town', 'class', 'sex']).agg({
        'fare': ['sum', 'mean']
    }).unstack()
    assert fares.shape == (9, 4)
    assert fares.stb.flatten().shape == (9, 6)
    assert fares.stb.flatten(reset=False).index.names == [
        'embark_town', 'class'
    ]
    assert list(fares.stb.flatten(sep='|').columns) == [
        'embark_town', 'class', 'fare|sum|female', 'fare|sum|male',
        'fare|mean|female', 'fare|mean|male'
    ]
    assert list(fares.stb.flatten(levels=2).columns) == [
        'embark_town', 'class', 'sum_female', 'sum_male', 'mean_female',
        'mean_male'
    ]
    assert list(fares.stb.flatten(levels=[2, 1]).columns) == [
        'embark_town', 'class', 'female_sum', 'male_sum', 'female_mean',
        'male_mean'
    ]
    assert list(fares.stb.flatten().columns) == [
        'embark_town', 'class', 'fare_sum_female', 'fare_sum_male',
        'fare_mean_female', 'fare_mean_male'
    ]
