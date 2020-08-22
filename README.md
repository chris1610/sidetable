# sidetable


[![Pypi link](https://img.shields.io/pypi/v/sidetable.svg)](https://pypi.python.org/pypi/sidetable)
![PyPI - Downloads](https://img.shields.io/pypi/dw/sidetable)

sidetable is a supercharged combination of pandas `value_counts` plus `crosstab` 
that builds simple but useful summary tables of your pandas DataFrame. sidetable can also
add subtotals to your DataFrame.


Usage is straightforward. Install and `import sidetable`. Then access it through the 
new `.stb` accessor on your DataFrame. 

For the Titanic data: `df.stb.freq(['class'])` will build a frequency table like this:

|    | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |   55.1066 |                491 |              55.1066 |
|  1 | First   |     216 |   24.2424 |                707 |              79.349  |
|  2 | Second  |     184 |   20.651  |                891 |             100      |

You can also summarize missing values with `df.stb.missing()`:

|             |   missing |   total |   percent |
|:------------|----------:|--------:|----------:|
| deck        |       688 |     891 | 77.2166   |
| age         |       177 |     891 | 19.8653   |
| embarked    |         2 |     891 |  0.224467 |
| embark_town |         2 |     891 |  0.224467 |
| survived    |         0 |     891 |  0        |
| pclass      |         0 |     891 |  0        |
| sex         |         0 |     891 |  0        |
| sibsp       |         0 |     891 |  0        |
| parch       |         0 |     891 |  0        |
| fare        |         0 |     891 |  0        |
| class       |         0 |     891 |  0        |
| who         |         0 |     891 |  0        |
| adult_male  |         0 |     891 |  0        |
| alive       |         0 |     891 |  0        |
| alone       |         0 |     891 |  0        |

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
      <th>grand_total</th>
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
* Count the number of unique values for each column.
* Add grand totals on any DataFrame and subtotals to any grouped DataFrame

## Table of Contents:

- [Quick Start](#quickstart)
- [Rationale](#rationale)
- [Installation](#installation)
- [Usage](#usage)
  - [freq](#freq)
  - [counts](#counts)
  - [missing](#missing)
  - [subtotal](#subtotal)
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

$  python -m pip install -U sidetable
```

This is the preferred method to install sidetable, as it will always
install the most recent stable release. sidetable requires pandas 1.0 or higher and no
additional dependencies. It should run anywhere that pandas runs.

If you prefer to use conda, sidetable is available on conda-forge:

```batch
$ conda install -c conda-forge sidetable
```

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

### freq
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
        df['class'].value_counts(normalize=True).mul(100).rename('percentage')], axis=1)
```
|        |   count |   percentage |
|:-------|--------:|-------------:|
| Third  |     491 |      55.1066 |
| First  |     216 |      24.2424 |
| Second |     184 |      20.651  |

Using sidetable is much simpler and you get cumulative totals, percents and more flexibility:

```python
df.stb.freq(['class'])
```
|    | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |   55.1066 |                491 |              55.1066 |
|  1 | First   |     216 |   24.2424 |                707 |              79.349  |
|  2 | Second  |     184 |   20.651  |                891 |             100      |

If you want to style the results so percentages and large numbers are easier to read, 
use `style=True`:

```python
df.stb.freq(['class'], style=True)
```
|    | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  55.11%   |                491 |               55.11% |
|  1 | First   |     216 |  24.24%   |                707 |               79.35% |
|  2 | Second  |     184 |  20.65%   |                891 |              100.00% |



In addition, you can group columns together. If we want to see the breakdown among
class and sex:

```python
df.stb.freq(['sex', 'class'])
```
|    | sex    | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | male   | Third   |     347 |  38.945   |                347 |              38.945  |
|  1 | female | Third   |     144 |  16.1616  |                491 |              55.1066 |
|  2 | male   | First   |     122 |  13.6925  |                613 |              68.7991 |
|  3 | male   | Second  |     108 |  12.1212  |                721 |              80.9203 |
|  4 | female | First   |      94 |  10.5499  |                815 |              91.4703 |
|  5 | female | Second  |      76 |   8.52974 |                891 |             100      |

You can use as many groupings as you would like.

By default, sidetable counts the data. However, you can specify a `value` argument to 
indicate that the data should be summed based on the data in another column. 
For this data set, we can see how the fares are distributed by class:

```python
df.stb.freq(['class'], value='fare')
```
|    | class   |     fare |   percent |   cumulative_fare |   cumulative_percent |
|---:|:--------|---------:|----------:|------------------:|---------------------:|
|  0 | First   | 18177.4  |   63.3493 |           18177.4 |              63.3493 |
|  1 | Third   |  6714.7  |   23.4011 |           24892.1 |              86.7504 |
|  2 | Second  |  3801.84 |   13.2496 |           28693.9 |             100      |

Another feature of sidetable is that you can specify a threshold. For many data analysis,
you may want to break down into large groupings to focus on and ignore others. You can use
the `thresh` argument to define a threshold and group all entries above that threshold 
into an "other" grouping:

```python
df.stb.freq(['class', 'who'], value='fare', thresh=80)
```
|    | class   | who    |    fare |   percent |   cumulative_fare |   cumulative_percent |
|---:|:--------|:-------|--------:|----------:|------------------:|---------------------:|
|  0 | First   | woman  | 9492.94 |  33.0834  |           9492.94 |              33.0834 |
|  1 | First   | man    | 7848.18 |  27.3513  |          17341.1  |              60.4348 |
|  2 | Third   | man    | 3617.53 |  12.6073  |          20958.6  |              73.042  |
|  3 | Second  | man    | 1886.36 |   6.57406 |          22845    |              79.6161 |
|  4 | others  | others | 5848.95 |  20.3839  |          28693.9  |             100      |

You can further customize by specifying the label to use for all the others:
```python
df.stb.freq(['class', 'who'], value='fare', thresh=80, other_label='All others')
```
|    | class      | who        |    fare |   percent |   cumulative_fare |   cumulative_percent |
|---:|:-----------|:-----------|--------:|----------:|------------------:|---------------------:|
|  0 | First      | woman      | 9492.94 |  33.0834  |           9492.94 |              33.0834 |
|  1 | First      | man        | 7848.18 |  27.3513  |          17341.1  |              60.4348 |
|  2 | Third      | man        | 3617.53 |  12.6073  |          20958.6  |              73.042  |
|  3 | Second     | man        | 1886.36 |   6.57406 |          22845    |              79.6161 |
|  4 | All others | All others | 5848.95 |  20.3839  |          28693.9  |             100      |

### counts
The `counts()` function shows how many unique values are in each column as well as 
the most and least frequent values & their total counts. This summary view can help you determine if you need
to convert data to a categorical value. It can also help you understand the high 
level structure of your data.

```python
df.stb.counts()
```
|             |   count |   unique | most_freq   |   most_freq_count | least_freq   |   least_freq_count |
|:------------|--------:|---------:|:------------|------------------:|:-------------|-------------------:|
| survived    |     891 |        2 | 0           |               549 | 1            |                342 |
| sex         |     891 |        2 | male        |               577 | female       |                314 |
| adult_male  |     891 |        2 | True        |               537 | False        |                354 |
| alive       |     891 |        2 | no          |               549 | yes          |                342 |
| alone       |     891 |        2 | True        |               537 | False        |                354 |
| pclass      |     891 |        3 | 3           |               491 | 2            |                184 |
| embarked    |     889 |        3 | S           |               644 | Q            |                 77 |
| class       |     891 |        3 | Third       |               491 | Second       |                184 |
| who         |     891 |        3 | man         |               537 | child        |                 83 |
| embark_town |     889 |        3 | Southampton |               644 | Queenstown   |                 77 |
| sibsp       |     891 |        7 | 0           |               608 | 5            |                  5 |
| parch       |     891 |        7 | 0           |               678 | 6            |                  1 |
| deck        |     203 |        7 | C           |                59 | G            |                  4 |
| age         |     714 |       88 | 24.0        |                30 | 20.5         |                  1 |
| fare        |     891 |      248 | 8.05        |                43 | 63.3583      |                  1 |

By default, all data types are included but you may use the `exclude` and `include` parameters
to select specific types of columns. The syntax is the same as pandas 
[select_dtypes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html)

For example,
```python
df.stb.counts(exclude='number')
```

|             |   count |   unique | most_freq   |   most_freq_count | least_freq   |   least_freq_count |
|:------------|--------:|---------:|:------------|------------------:|:-------------|-------------------:|
| sex         |     891 |        2 | male        |               577 | female       |                314 |
| adult_male  |     891 |        2 | True        |               537 | False        |                354 |
| alive       |     891 |        2 | no          |               549 | yes          |                342 |
| alone       |     891 |        2 | True        |               537 | False        |                354 |
| embarked    |     889 |        3 | S           |               644 | Q            |                 77 |
| class       |     891 |        3 | Third       |               491 | Second       |                184 |
| who         |     891 |        3 | man         |               537 | child        |                 83 |
| embark_town |     889 |        3 | Southampton |               644 | Queenstown   |                 77 |
| deck        |     203 |        7 | C           |                59 | G            |                  4 |

### missing
sidetable also includes a summary table that shows the missing values in
your data by count and percentage of total missing values in a column.

```python
df.stb.missing()
```
|             |   missing |   total |   percent |
|:------------|----------:|--------:|----------:|
| deck        |       688 |     891 | 77.2166   |
| age         |       177 |     891 | 19.8653   |
| embarked    |         2 |     891 |  0.224467 |
| embark_town |         2 |     891 |  0.224467 |
| survived    |         0 |     891 |  0        |
| pclass      |         0 |     891 |  0        |
| sex         |         0 |     891 |  0        |
| sibsp       |         0 |     891 |  0        |
| parch       |         0 |     891 |  0        |
| fare        |         0 |     891 |  0        |
| class       |         0 |     891 |  0        |
| who         |         0 |     891 |  0        |
| adult_male  |         0 |     891 |  0        |
| alive       |         0 |     891 |  0        |
| alone       |         0 |     891 |  0        |

If you wish to see the results with styles applied to the Percent and Total column,
use:

```python
df.stb.missing(style=True)
```

|             |   missing |   total |    percent |
|:------------|----------:|--------:|-----------:|
| deck        |       688 |     891 | 77.22%     |
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

Finally, you can exclude the columns that have 0 missing values using
the `clip_0=True` parameter:

```python
df.stb.missing(clip_0=True, style=True)
```
|             |   missing |   total |   percent |
|:------------|----------:|--------:|----------:|
| deck        |       688 |     891 | 77.22%    |
| age         |       177 |     891 | 19.87%    |
| embarked    |         2 |     891 |  0.22%    |
| embark_town |         2 |     891 |  0.22%    |


### subtotal
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
| grand_total |        342 |     2057 | nan    | 21205.2 |     466 |     340 | 28693.9  | nan        | nan     | nan   |          537 | nan    | nan           | nan     |     537 |

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
|    | fare_bin   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:-----------|--------:|----------:|-------------------:|---------------------:|
|  0 | medium     |     224 |   25.1403 |                224 |              25.1403 |
|  1 | low        |     223 |   25.0281 |                447 |              50.1684 |
|  2 | x-high     |     222 |   24.9158 |                669 |              75.0842 |
|  3 | high       |     222 |   24.9158 |                891 |             100      |

The other caveat is that null or missing values can cause data to drop out while aggregating.
For instance, if we look at the `deck` variable, there are a lot of missing values.

```python
df.stb.freq(['deck'])
```
|    | deck   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:-------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      |      59 |  29.064   |                 59 |              29.064  |
|  1 | B      |      47 |  23.1527  |                106 |              52.2167 |
|  2 | D      |      33 |  16.2562  |                139 |              68.4729 |
|  3 | E      |      32 |  15.7635  |                171 |              84.2365 |
|  4 | A      |      15 |   7.38916 |                186 |              91.6256 |
|  5 | F      |      13 |   6.40394 |                199 |              98.0296 |
|  6 | G      |       4 |   1.97044 |                203 |             100      |


The total cumulative count only goes up to 203 not the 891 we have seen in other examples.
Future versions of sidetable may handle this differently. For now, it is up to you to 
decide how best to handle unknowns. For example, this version of the Titanic data set
has a categorical value for `deck` so using `fillna` requires an extra step:

```python
df['deck_fillna'] = df['deck'].cat.add_categories('UNK').fillna('UNK')
df.stb.freq(['deck_fillna'])
```
|    | deck_fillna   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:--------------|--------:|----------:|-------------------:|---------------------:|
|  0 | UNK           |     688 | 77.2166   |                688 |              77.2166 |
|  1 | C             |      59 |  6.62177  |                747 |              83.8384 |
|  2 | B             |      47 |  5.27497  |                794 |              89.1134 |
|  3 | D             |      33 |  3.7037   |                827 |              92.8171 |
|  4 | E             |      32 |  3.59147  |                859 |              96.4085 |
|  5 | A             |      15 |  1.6835   |                874 |              98.092  |
|  6 | F             |      13 |  1.45903  |                887 |              99.5511 |
|  7 | G             |       4 |  0.448934 |                891 |             100      |

Another variant is that there might be certain groupings where there are no valid counts.

For instance, if we look at the `deck` and `class`:

```python
df.stb.freq(['deck', 'class'])
```
|    | deck   | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      | First   |      59 |  29.064   |                 59 |              29.064  |
|  1 | B      | First   |      47 |  23.1527  |                106 |              52.2167 |
|  2 | D      | First   |      29 |  14.2857  |                135 |              66.5025 |
|  3 | E      | First   |      25 |  12.3153  |                160 |              78.8177 |
|  4 | A      | First   |      15 |   7.38916 |                175 |              86.2069 |
|  5 | F      | Second  |       8 |   3.94089 |                183 |              90.1478 |
|  6 | F      | Third   |       5 |   2.46305 |                188 |              92.6108 |
|  7 | G      | Third   |       4 |   1.97044 |                192 |              94.5813 |
|  8 | E      | Second  |       4 |   1.97044 |                196 |              96.5517 |
|  9 | D      | Second  |       4 |   1.97044 |                200 |              98.5222 |
| 10 | E      | Third   |       3 |   1.47783 |                203 |             100      |


There are only 11 combinations. If we want to see all - even if there are not any passengers
fitting that criteria, use `clip_0=False` 

```python
df.stb.freq(['deck', 'class'], clip_0=False)
```
|    | deck   | class   |   count |   percent |   cumulative_count |   cumulative_percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | C      | First   |      59 |  29.064   |                 59 |              29.064  |
|  1 | B      | First   |      47 |  23.1527  |                106 |              52.2167 |
|  2 | D      | First   |      29 |  14.2857  |                135 |              66.5025 |
|  3 | E      | First   |      25 |  12.3153  |                160 |              78.8177 |
|  4 | A      | First   |      15 |   7.38916 |                175 |              86.2069 |
|  5 | F      | Second  |       8 |   3.94089 |                183 |              90.1478 |
|  6 | F      | Third   |       5 |   2.46305 |                188 |              92.6108 |
|  7 | G      | Third   |       4 |   1.97044 |                192 |              94.5813 |
|  8 | E      | Second  |       4 |   1.97044 |                196 |              96.5517 |
|  9 | D      | Second  |       4 |   1.97044 |                200 |              98.5222 |
| 10 | E      | Third   |       3 |   1.47783 |                203 |             100      |
| 11 | G      | Second  |       0 |   0       |                203 |             100      |
| 12 | G      | First   |       0 |   0       |                203 |             100      |
| 13 | F      | First   |       0 |   0       |                203 |             100      |
| 14 | D      | Third   |       0 |   0       |                203 |             100      |
| 15 | C      | Third   |       0 |   0       |                203 |             100      |
| 16 | C      | Second  |       0 |   0       |                203 |             100      |
| 17 | B      | Third   |       0 |   0       |                203 |             100      |
| 18 | B      | Second  |       0 |   0       |                203 |             100      |
| 19 | A      | Third   |       0 |   0       |                203 |             100      |
| 20 | A      | Second  |       0 |   0       |                203 |             100      |

In many cases this might be too much data, but sometimes the fact that a combination is 
missing could be insightful.

The final caveat relates to `subtotal`. When working with the `subtotal` function, sidetable 
convert a Categorical MultiIndex to a plain index in order to easily add the subtotal labels.

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