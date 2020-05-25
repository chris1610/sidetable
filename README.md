# sidetable


[![Pypi link](https://img.shields.io/pypi/v/sidetable.svg)](https://pypi.python.org/pypi/sidetable)

sidetable is a combination of a supercharged pandas `value_counts` plus `crosstab` that 
builds simple but useful summary tables of your pandas DataFrame.

Usage is simple. Install and import sidetable. Then access it through the new `.st` accessor 
on your DataFrame. 

For the Titanic data: `df.st.freq(['class'])` will build a frequency table like this:

|    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  0.551066 |                491 |             0.551066 |
|  1 | First   |     216 |  0.242424 |                707 |             0.79349  |
|  2 | Second  |     184 |  0.20651  |                891 |             1        |

You can also summarize missing values with `df.st.missing()`:

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

sidetable has several useful features:

* See total counts and their relative percentages in one table. This is roughly equivalent to combining the
  output of `value_counts()` and `value_counts(normalize=True)` into one table.
* Include cumulative totals and percentages to better understand your thresholds.
* Aggregate columns together to see frequency counts for grouped data
* Provide a threshold point above which all data is grouped into a single bucket. This is useful for
  quickly identifying the areas to focus your analysis.
* Get a count of the missing values in your data.

## Table of Contents:

- [Intallation](#installation)
- [Usage](#usage)
- [TODO](#todo)
- [Contributing](#contributing)
- [Credits](#credits)

## Installation


```batch

    $ pip install sidetable
```

This is the preferred method to install sidetable, as it will always
install the most recent stable release. sidetable requires pandas 1.0 or higher and no
additional dependencies.

## Usage
```python

    import pandas as pd
    import sidetable
    import seaborn as sns

    df = sns.load_dataset('titanic')
```

sidetable uses the pandas DataFrame accessory api to add a `.st` accessor to all of your
DataFrames. Once you `import sidetable` you are ready to go. In these examples, I will be
using seaborn's Titanic dataset as an example but seaborn is not a direct dependency.

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
df.st.freq(['class'])
```

|    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | Third   |     491 |  0.551066 |                491 |             0.551066 |
|  1 | First   |     216 |  0.242424 |                707 |             0.79349  |
|  2 | Second  |     184 |  0.20651  |                891 |             1        |

In addition, you can group columns together. If we want to see how they breakdown between
class and sex:

```python
df.st.freq(['sex', 'class'])
```
|    | sex    | class   |   Count |   Percent |   Cumulative Count |   Cumulative Percent |
|---:|:-------|:--------|--------:|----------:|-------------------:|---------------------:|
|  0 | male   | Third   |     347 | 0.38945   |                347 |             0.38945  |
|  1 | female | Third   |     144 | 0.161616  |                491 |             0.551066 |
|  2 | male   | First   |     122 | 0.136925  |                613 |             0.687991 |
|  3 | male   | Second  |     108 | 0.121212  |                721 |             0.809203 |
|  4 | female | First   |      94 | 0.105499  |                815 |             0.914703 |
|  5 | female | Second  |      76 | 0.0852974 |                891 |             1        |

You can use as many groupings as you would like and make sense for your data.

By default, sidetable counts the data. However, you can specify a `value` argument which is 
another column to perform a summation on. For this data set, we can see how the fares are
totaled by class:

```python
df.st.freq(['class'], value='fare')
```
|    | class   |     fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:--------|---------:|----------:|------------------:|---------------------:|
|  0 | First   | 18177.4  |  0.633493 |           18177.4 |             0.633493 |
|  1 | Third   |  6714.7  |  0.234011 |           24892.1 |             0.867504 |
|  2 | Second  |  3801.84 |  0.132496 |           28693.9 |             1        |

Another feature of sidetable is that you can specify a  threshold. Many data analysis
tasks can break down along the 80/20 rule. You can use the `thresh` to define a threshold
and group all entries above that threshold into an "Other" grouping:

```python
df.st.freq(['class', 'who'], value='fare', thresh=.80)
```
|    | class   | who    |    fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:--------|:-------|--------:|----------:|------------------:|---------------------:|
|  0 | First   | woman  | 9492.94 | 0.330834  |           9492.94 |             0.330834 |
|  1 | First   | man    | 7848.18 | 0.273513  |          17341.1  |             0.604348 |
|  2 | Third   | man    | 3617.53 | 0.126073  |          20958.6  |             0.73042  |
|  3 | Second  | man    | 1886.36 | 0.0657406 |          22845    |             0.796161 |
|  4 | Others  | Others | 5848.95 | 0.203839  |          28693.9  |             1        |

You can specify what label to use for all the others:
```python
df.st.freq(['class', 'who'], value='fare', thresh=.80, other_label='All others')
```
|    | class      | who        |    fare |   Percent |   Cumulative fare |   Cumulative Percent |
|---:|:-----------|:-----------|--------:|----------:|------------------:|---------------------:|
|  0 | First      | woman      | 9492.94 | 0.330834  |           9492.94 |             0.330834 |
|  1 | First      | man        | 7848.18 | 0.273513  |          17341.1  |             0.604348 |
|  2 | Third      | man        | 3617.53 | 0.126073  |          20958.6  |             0.73042  |
|  3 | Second     | man        | 1886.36 | 0.0657406 |          22845    |             0.796161 |
|  4 | All others | All others | 5848.95 | 0.203839  |          28693.9  |             1        |

Finally, sidetable includes a another summary table that shows the missing values in
your data by count and percentage of total missing values in a column.

```python
df.st.missing()
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


## TODO

- [ ] Handle NaN values more effectively


## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

For more info please click [here](./CONTRIBUTING.md)


## Credits

This package was created with Cookiecutter and the `oldani/cookiecutter-simple-pypackage` project template.

https://medium.com/dunder-data/finding-the-percentage-of-missing-values-in-a-pandas-dataframe-a04fa00f84ab

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [oldani/cookiecutter-simple-pypackage](https://github.com/oldani/cookiecutter-simple-pypackage)
