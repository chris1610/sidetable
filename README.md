# sidetable


[![Pypi link](https://img.shields.io/pypi/v/sidetable.svg)](https://pypi.python.org/pypi/sidetable)

sidetable is a supercharged combination of pandas `value_counts` plus `crosstab` 
that builds simple but useful summary tables of your pandas DataFrame. sidetable can also
add subtotals to your DataFrame.


Usage is straightforward. Install and `import sidetable`. Then access it through the 
new `.stb` accessor on your DataFrame. 

For the Titanic data: `df.stb.freq(['class'])` will build a frequency table like this:

|    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  0.551066 |                491 |             0.551066 |
|  1 | First   |     216 |  0.242424 |                707 |             0.79349  |
|  2 | Second  |     184 |  0.20651  |                891 |             1        |

You can also summarize missing values with `df.stb.missing()`:

|             |   Missing |   Total |    Percent |
|:------------|----------:|--------:|-----------:|
| deck        |       688 |     891 | 0.772166   |
| age         |       177 |     891 | 0.198653   |
| embarked    |         2 |     891 | 0.00224467 |
| embark_town |         2 |     891 | 0.00224467 |
| survived    |         0 |     891 | 0          |
| pclass      |         0 |     891 | 0          |
| sex         |         0 |     891 | 0          |
| sibsp       |         0 |     891 | 0          |
| parch       |         0 |     891 | 0          |
| fare        |         0 |     891 | 0          |
| class       |         0 |     891 | 0          |
| who         |         0 |     891 | 0          |
| adult_male  |         0 |     891 | 0          |
| alive       |         0 |     891 | 0          |
| alone       |         0 |     891 | 0          |

You can group the data and add subtotals and grand totals with `stb.subtotal()`:

```python
df.groupby(['sex', 'class']).agg({'fare': ['sum']}).stb.subtotal()
```

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th>fare</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>sum</th>
    </tr>
    <tr>
      <th>sex</th>
      <th>class</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">female</th>
      <th>First</th>
      <td>9975.8250</td>
    </tr>
    <tr>
      <th>Second</th>
      <td>1669.7292</td>
    </tr>
    <tr>
      <th>Third</th>
      <td>2321.1086</td>
    </tr>
    <tr>
      <th>female - subtotal</th>
      <td>13966.6628</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">male</th>
      <th>First</th>
      <td>8201.5875</td>
    </tr>
    <tr>
      <th>Second</th>
      <td>2132.1125</td>
    </tr>
    <tr>
      <th>Third</th>
      <td>4393.5865</td>
    </tr>
    <tr>
      <th>male - subtotal</th>
      <td>14727.2865</td>
    </tr>
    <tr>
      <th>Grand Total</th>
      <th></th>
      <td>28693.9493</td>
    </tr>
  </tbody>
</table>


sidetable has several useful features:

* See total counts and their relative percentages in one table. This is roughly equivalent to combining the
  output of `value_counts()` and `value_counts(normalize=True)` into one table.
* Include cumulative totals and percentages to better understand your thresholds. 
  The [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) applies to many different scenarios
  and this function makes it easy to see how your data is cumulatively distributed.
* Aggregate multiple columns together to see frequency counts for grouped data.
* Provide a threshold point above which all data is grouped into a single bucket. This is useful for
  quickly identifying the areas to focus your analysis.
* Get a count of the missing values in your data.
* Add grand totals on any DataFrame and subtotals to any grouped DataFrame

## Table of Contents:

- [Quick Start](#quickstart)
- [Rationale](#rationale)
- [Installation](#installation)
- [Usage](#usage)
- [Caveats](#caveats)
- [TODO](#todo)
- [Contributing](#contributing)
- [Credits](#credits)

## Quickstart
For the impatient:

```batch
$ python -m pip install sidetable
```

```python
import sidetable
import pandas as pd

# Create your DataFrame
df = pd.read_csv(myfile.csv)

# Build a frequency table for one or more columns
df.stb.freq(['column1', 'column2'])

# See what data is missing
df.stb.missing()

# Group data and add a subtotal
df.groupby(['column1', 'column2'])['col3'].sum().stb.subtotal()
```
That's it. 

Read on for more details and more examples of what you can do sidetable.

## Rationale
The idea behind sidetable is that there are a handful of useful data analysis tasks that
you might run on any data set early in the data analysis process. While each of these
tasks can be done in a handful of lines of pandas code, it is a lot of typing and 
difficult to remember.

In addition to providing useful functionality, this project is also a test to see how to
build custom accessors using some of pandas relatively new API. I am hopeful this can
serve as a model for other projects whether open source or just for your own usage.
Please check out the [release announcement](https://pbpython.com/sidetable.html) for more
information about the usage and how to use this as a model for your own projects.

The solutions in sidetable are heavily based on three sources:

- This [tweet thread](https://twitter.com/pmbaumgartner/status/1235925419012087809) by Peter Baumgartner
- An [excellent article](https://opendatascience.com/frequencies-and-chaining-in-python-pandas/)
  by Steve Miller that lays out many of the code concepts incorporated into sidetable.
- Ted Petrou's [post](https://medium.com/dunder-data/finding-the-percentage-of-missing-values-in-a-pandas-dataframe-a04fa00f84ab) 
  on finding the percentage of missing values in a DataFrame.

I very much appreciate the work that all three authors did to point me in this direction.

## Installation

```batch

$ python -m pip install sidetable
```

This is the preferred method to install sidetable, as it will always
install the most recent stable release. sidetable requires pandas 1.0 or higher and no
additional dependencies. It should run anywhere that pandas runs.

## Usage
```python
import pandas as pd
import sidetable
import seaborn as sns

df = sns.load_dataset('titanic')
```

sidetable uses the pandas DataFrame [accessor api](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) 
to add a `.stb` accessor to all of your DataFrames. Once you `import sidetable` you are ready to 
go. In these examples, I will be using seaborn's Titanic dataset as an example but
seaborn is not a direct dependency.

If you have used `value_counts()` before, you have probably wished it were easier to
combine the values with percentage distribution.

```python
df['class'].value_counts()

Third     491
First     216
Second    184
Name: class, dtype: int64

df['class'].value_counts(normalize=True)

Third     0.551066
First     0.242424
Second    0.206510
Name: class, dtype: float64
```

Which can be done, but is messy and a lot of typing and remembering:

```python
pd.concat([df['class'].value_counts().rename('count'), 
        df['class'].value_counts(normalize=True).rename('percentage')], axis=1)
```
|        |   count |   percentage |
|:-------|--------:|-------------:|
| Third  |     491 |     0.551066 |
| First  |     216 |     0.242424 |
| Second |     184 |     0.20651  |

Using sidetable is much simpler and you get cumulative totals, percents and more flexibility:

```python
df.stb.freq(['class'])
```

|    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  0.551066 |                491 |             0.551066 |
|  1 | First   |     216 |  0.242424 |                707 |             0.79349  |
|  2 | Second  |     184 |  0.20651  |                891 |             1        |

If you want to style the results so percentages and large numbers are easier to read, 
use `style=True`:

```python
df.stb.freq(['class'], style=True)
```
|    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  55.11%   |                491 |               55.11% |
|  1 | First   |     216 |  24.24%   |                707 |               79.35% |
|  2 | Second  |     184 |  20.65%   |                891 |              100.00% |



In addition, you can group columns together. If we want to see the breakdown among
class and sex:

```python
df.stb.freq(['sex', 'class'])
```
|    | sex    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | male   | Third   |     347 | 0.38945   |                347 |             0.38945  |
|  1 | female | Third   |     144 | 0.161616  |                491 |             0.551066 |
|  2 | male   | First   |     122 | 0.136925  |                613 |             0.687991 |
|  3 | male   | Second  |     108 | 0.121212  |                721 |             0.809203 |
|  4 | female | First   |      94 | 0.105499  |                815 |             0.914703 |
|  5 | female | Second  |      76 | 0.0852974 |                891 |             1        |

You can use as many groupings as you would like.

By default, sidetable counts the data. However, you can specify a `value` argument to 
indicate that the data should be summed based on the data in another column. 
For this data set, we can see how the fares are distributed by class:

```python
df.stb.freq(['class'], value='fare')
```
|    | class   |     fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:--------|---------:|----------:|------------------:|---------------------:|
|  0 | First   | 18177.4  |  0.633493 |           18177.4 |             0.633493 |
|  1 | Third   |  6714.7  |  0.234011 |           24892.1 |             0.867504 |
|  2 | Second  |  3801.84 |  0.132496 |           28693.9 |             1        |

Another feature of sidetable is that you can specify a threshold. For many data analysis,
you may want to break down into large groupings to focus on and ignore others. You can use
the `thresh` argument to define a threshold and group all entries above that threshold 
into an "Other" grouping:

```python
df.stb.freq(['class', 'who'], value='fare', thresh=.80)
```
|    | class   | who    |    fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:--------|:-------|--------:|----------:|------------------:|---------------------:|
|  0 | First   | woman  | 9492.94 | 0.330834  |           9492.94 |             0.330834 |
|  1 | First   | man    | 7848.18 | 0.273513  |          17341.1  |             0.604348 |
|  2 | Third   | man    | 3617.53 | 0.126073  |          20958.6  |             0.73042  |
|  3 | Second  | man    | 1886.36 | 0.0657406 |          22845    |             0.796161 |
|  4 | Others  | Others | 5848.95 | 0.203839  |          28693.9  |             1        |

You can further customize by specifying the label to use for all the others:
```python
df.stb.freq(['class', 'who'], value='fare', thresh=.80, other_label='All others')
```
|    | class      | who        |    fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:-----------|:-----------|--------:|----------:|------------------:|---------------------:|
|  0 | First      | woman      | 9492.94 | 0.330834  |           9492.94 |             0.330834 |
|  1 | First      | man        | 7848.18 | 0.273513  |          17341.1  |             0.604348 |
|  2 | Third      | man        | 3617.53 | 0.126073  |          20958.6  |             0.73042  |
|  3 | Second     | man        | 1886.36 | 0.0657406 |          22845    |             0.796161 |
|  4 | All others | All others | 5848.95 | 0.203839  |          28693.9  |             1        |

Finally, sidetable includes a summary table that shows the missing values in
your data by count and percentage of total missing values in a column.

```python
df.stb.missing()
```
|             |   Missing |   Total |    Percent |
|:------------|----------:|--------:|-----------:|
| deck        |       688 |     891 | 0.772166   |
| age         |       177 |     891 | 0.198653   |
| embarked    |         2 |     891 | 0.00224467 |
| embark_town |         2 |     891 | 0.00224467 |
| survived    |         0 |     891 | 0          |
| pclass      |         0 |     891 | 0          |
| sex         |         0 |     891 | 0          |
| sibsp       |         0 |     891 | 0          |
| parch       |         0 |     891 | 0          |
| fare        |         0 |     891 | 0          |
| class       |         0 |     891 | 0          |
| who         |         0 |     891 | 0          |
| adult_male  |         0 |     891 | 0          |
| alive       |         0 |     891 | 0          |
| alone       |         0 |     891 | 0          |

If you wish to see the results with styles applied to the Percent and Total column,
use:

```python
df.stb.missing(style=True)
```

|             |   Missing |   Total |    Percent |
|:------------|----------:|--------:|-----------:|
| deck        |       688 |     891 | 77.25%     |
| age         |       177 |     891 | 19.87%     |
| embarked    |         2 |     891 | 0.22%      |
| embark_town |         2 |     891 | 0.22%      |
| survived    |         0 |     891 | 0          |
| pclass      |         0 |     891 | 0          |
| sex         |         0 |     891 | 0          |
| sibsp       |         0 |     891 | 0          |
| parch       |         0 |     891 | 0          |
| fare        |         0 |     891 | 0          |
| class       |         0 |     891 | 0          |
| who         |         0 |     891 | 0          |
| adult_male  |         0 |     891 | 0          |
| alive       |         0 |     891 | 0          |
| alone       |         0 |     891 | 0          |

Another useful function is the subtotal function. Trying to add a subtotal 
to grouped pandas data is not easy. sidetable adds a `subtotal()` function that
makes adds a subtotal at one or more levels of a DataFrame.

The subtotal function can be applied to a simple DataFrame in order to add a Grand Total
label:

```python
df.stb.subtotal()
```

|             |   survived |   pclass | sex    |     age |   sibsp |   parch |     fare | embarked   | class   | who   |   adult_male | deck   | embark_town   | alive   |   alone |
|:------------|-----------:|---------:|:-------|--------:|--------:|--------:|---------:|:-----------|:--------|:------|-------------:|:-------|:--------------|:--------|--------:|
| 887         |          1 |        1 | female |    19   |       0 |       0 |    30    | S          | First   | woman |            0 | B      | Southampton   | yes     |       1 |
| 888         |          0 |        3 | female |   nan   |       1 |       2 |    23.45 | S          | Third   | woman |            0 | nan    | Southampton   | no      |       0 |
| 889         |          1 |        1 | male   |    26   |       0 |       0 |    30    | C          | First   | man   |            1 | C      | Cherbourg     | yes     |       1 |
| 890         |          0 |        3 | male   |    32   |       0 |       0 |     7.75 | Q          | Third   | man   |            1 | nan    | Queenstown    | no      |       1 |
| Grand Total |        342 |     2057 | nan    | 21205.2 |     466 |     340 | 28693.9  | nan        | nan     | nan   |          537 | nan    | nan           | nan     |     537 |

The real power of subtotal is being able to add it to one or more levels of your 
grouped data. For example, you can group the data and add a subtotal at each level:

```python
df.groupby(['sex', 'class', 'embark_town']).agg({'fare': ['sum']}).stb.subtotal()
```

Which yields this view (truncated for simplicity):

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th>fare</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th>sum</th>
    </tr>
    <tr>
      <th>sex</th>
      <th>class</th>
      <th>embark_town</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="13" valign="top">female</th>
      <th rowspan="4" valign="top">First</th>
      <th>Cherbourg</th>
      <td>4972.5333</td>
    </tr>
    <tr>
      <th>Queenstown</th>
      <td>90.0000</td>
    </tr>
    <tr>
      <th>Southampton</th>
      <td>4753.2917</td>
    </tr>
    <tr>
      <th>female | First - subtotal</th>
      <td>9815.8250</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Second</th>
      <th>Cherbourg</th>
      <td>176.8792</td>
    </tr>
    <tr>
      <th>Queenstown</th>
      <td>24.7000</td>
    </tr>
    <tr>
      <th>Southampton</th>
      <td>1468.1500</td>
    </tr>
    <tr>
      <th>female | Second - subtotal</th>
      <td>1669.7292</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Third</th>
      <th>Cherbourg</th>
      <td>337.9833</td>
    </tr>
    <tr>
      <th>Queenstown</th>
      <td>340.1585</td>
    </tr>
    <tr>
      <th>Southampton</th>
      <td>1642.9668</td>
    </tr>
    <tr>
      <th>female | Third - subtotal</th>
      <td>2321.1086</td>
    </tr>
    <tr>
      <th>female - subtotal</th>
      <th></th>
      <td>13806.6628</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">male</th>
      <th rowspan="2" valign="top">First</th>
      <th>Cherbourg</th>
      <td>3928.5417</td>
    </tr>
    <tr>
      <th>Queenstown</th>
      <td>90.0000</td>
    </tr>
  </tbody>
</table>

By default, every level in the DataFrame will be subtotaled but you can control this behavior
by using the `sub_level` argument. For instance, you can subtotal on `sex` and `class` by 
passing the argument `sub_level=[1,2]`

```python
summary_table = df.groupby(['sex', 'class', 'embark_town']).agg({'fare': ['sum']})
summary_table.stb.subtotal(sub_level=[1, 2])
```

The `subtotal` function also allows the user to configure the labels and separators used in 
the subtotal and Grand Total by using the `grand_label`, `sub_label`, `show_sep` and `sep`
arguments. 

## Caveats
sidetable supports grouping on any data type in a pandas DataFrame. This means that
you could try something like:

```python
df.stb.freq(['fare'])
```
In some cases where there are a fairly small discrete number of this may be useful. However,
if you have a lot of unique values, you should [bin the data](https://pbpython.com/pandas-qcut-cut.html)
first. In the example, above the data would include 248 rows and not be terribly useful.

One alternative could be:

```python
df['fare_bin'] = pd.qcut(df['fare'], q=4, labels=['low', 'medium', 'high', 'x-high'])
df.stb.freq(['fare_bin'])
```
|    | fare_bin   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-----------|--------:|----------:|-------------------:|---------------------:|
|  0 | medium     |     224 |  0.251403 |                224 |             0.251403 |
|  1 | low        |     223 |  0.250281 |                447 |             0.501684 |
|  2 | x-high     |     222 |  0.249158 |                669 |             0.750842 |
|  3 | high       |     222 |  0.249158 |                891 |             1        |


The other caveat is that null or missing values can cause data to drop out while aggregating.
For instance, if we look at the `deck` variable, there are a lot of missing values.

```python
df.stb.freq(['deck'])
```
|    | deck   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      |      59 | 0.29064   |                 59 |             0.29064  |
|  1 | B      |      47 | 0.231527  |                106 |             0.522167 |
|  2 | D      |      33 | 0.162562  |                139 |             0.684729 |
|  3 | E      |      32 | 0.157635  |                171 |             0.842365 |
|  4 | A      |      15 | 0.0738916 |                186 |             0.916256 |
|  5 | F      |      13 | 0.0640394 |                199 |             0.980296 |
|  6 | G      |       4 | 0.0197044 |                203 |             1        |


The total cumulative count only goes up to 203 not the 891 we have seen in other examples.
Future versions of sidetable may handle this differently. For now, it is up to you to 
decide how best to handle unknowns. For example, this version of the Titanic data set
has a categorical value for `deck` so using `fillna` requires and extra step:

```python
df['deck_fillna'] = df['deck'].cat.add_categories('UNK').fillna('UNK')
df.stb.freq(['deck_fillna'])
```
|    | deck_fillna   |   Count |    Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------------|--------:|-----------:|-------------------:|---------------------:|
|  0 | UNK           |     688 | 0.772166   |                688 |             0.772166 |
|  1 | C             |      59 | 0.0662177  |                747 |             0.838384 |
|  2 | B             |      47 | 0.0527497  |                794 |             0.891134 |
|  3 | D             |      33 | 0.037037   |                827 |             0.928171 |
|  4 | E             |      32 | 0.0359147  |                859 |             0.964085 |
|  5 | A             |      15 | 0.016835   |                874 |             0.98092  |
|  6 | F             |      13 | 0.0145903  |                887 |             0.995511 |
|  7 | G             |       4 | 0.00448934 |                891 |             1        |

Another variant of this is that there might be certain groupings where there are no
valid counts.

For instance, if we look at the `deck` and `class`:

```python
df.stb.freq(['deck', 'class'])
```
|    | deck   | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      | First   |      59 | 0.29064   |                 59 |             0.29064  |
|  1 | B      | First   |      47 | 0.231527  |                106 |             0.522167 |
|  2 | D      | First   |      29 | 0.142857  |                135 |             0.665025 |
|  3 | E      | First   |      25 | 0.123153  |                160 |             0.788177 |
|  4 | A      | First   |      15 | 0.0738916 |                175 |             0.862069 |
|  5 | F      | Second  |       8 | 0.0394089 |                183 |             0.901478 |
|  6 | F      | Third   |       5 | 0.0246305 |                188 |             0.926108 |
|  7 | G      | Third   |       4 | 0.0197044 |                192 |             0.945813 |
|  8 | E      | Second  |       4 | 0.0197044 |                196 |             0.965517 |
|  9 | D      | Second  |       4 | 0.0197044 |                200 |             0.985222 |
| 10 | E      | Third   |       3 | 0.0147783 |                203 |             1        |

There are only 11 combinations. If we want to see all - even if there are not any passengers
fitting that criteria, use `clip_0=False` 

```python
df.stb.freq(['deck', 'class'], clip_0=False)
```
|    | deck   | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      | First   |      59 | 0.29064   |                 59 |             0.29064  |
|  1 | B      | First   |      47 | 0.231527  |                106 |             0.522167 |
|  2 | D      | First   |      29 | 0.142857  |                135 |             0.665025 |
|  3 | E      | First   |      25 | 0.123153  |                160 |             0.788177 |
|  4 | A      | First   |      15 | 0.0738916 |                175 |             0.862069 |
|  5 | F      | Second  |       8 | 0.0394089 |                183 |             0.901478 |
|  6 | F      | Third   |       5 | 0.0246305 |                188 |             0.926108 |
|  7 | G      | Third   |       4 | 0.0197044 |                192 |             0.945813 |
|  8 | E      | Second  |       4 | 0.0197044 |                196 |             0.965517 |
|  9 | D      | Second  |       4 | 0.0197044 |                200 |             0.985222 |
| 10 | E      | Third   |       3 | 0.0147783 |                203 |             1        |
| 11 | G      | Second  |       0 | 0         |                203 |             1        |
| 12 | G      | First   |       0 | 0         |                203 |             1        |
| 13 | F      | First   |       0 | 0         |                203 |             1        |
| 14 | D      | Third   |       0 | 0         |                203 |             1        |
| 15 | C      | Third   |       0 | 0         |                203 |             1        |
| 16 | C      | Second  |       0 | 0         |                203 |             1        |
| 17 | B      | Third   |       0 | 0         |                203 |             1        |
| 18 | B      | Second  |       0 | 0         |                203 |             1        |
| 19 | A      | Third   |       0 | 0         |                203 |             1        |
| 20 | A      | Second  |       0 | 0         |                203 |             1        |

In many cases this might be too much data, but sometimes the fact that a combination is 
missing could be insightful.

With the subtotal function, sidetable convert a Categorical MultiIndex to a plain index
in order to easily add the subtotal labels.

## TODO

- [ ] Handle NaN values more effectively
- [ ] Offer binning options for continuous variables
- [ ] Offer more options, maybe plotting?


## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. If you have a new idea for a simple table
that we should add, please submit a ticket.

For more info please click [here](./CONTRIBUTING.md)

## Credits

This package was created with Cookiecutter and the `oldani/cookiecutter-simple-pypackage` project template.
The code used in this package is heavily based on the posts from Peter Baumgartner, Steve Miller
and Ted Petrou. Thank you!

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [oldani/cookiecutter-simple-pypackage](https://github.com/oldani/cookiecutter-simple-pypackage)
- Peter Baumgartner - [tweet thread](https://twitter.com/pmbaumgartner/status/1235925419012087809)
- Steve Miller - [article](https://opendatascience.com/frequencies-and-chaining-in-python-pandas/)
- Ted Petrou - [post](https://medium.com/dunder-data/finding-the-percentage-of-missing-values-in-a-pandas-dataframe-a04fa00f84ab)