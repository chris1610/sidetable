# -*- coding: utf-8 -*-

import pandas as pd
from pandas.api.types import is_numeric_dtype
from functools import reduce
import warnings
import weakref
import math
from operator import itemgetter


@pd.api.extensions.register_dataframe_accessor("stb")
class SideTableAccessor:
    """Pandas dataframe accessor that computes simple summary tables for your data.
    Computes a frequency table on one or more columns with df.stb.freq(['col_name'])
    Compute a table of missing values with df.stb.missing()
    """
    SORT_FLAG = '~~~~zz'

    def __init__(self, pandas_obj):
        self._finalizer = weakref.finalize(self, self._cleanup)
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _cleanup(self):
        del self._obj

    def remove(self):
        self._finalizer()

    @staticmethod
    def _validate(obj):
        # verify this is a DataFrame
        if not isinstance(obj, pd.DataFrame):
            raise AttributeError("Must be a pandas DataFrame")

    def freq(self,
             cols,
             thresh=100,
             other_label='others',
             clip_0=True,
             value=None,
             style=False,
             sort_cols=False,
             cum_cols=True):
        """ Create a table that counts the frequency of occurrence or summation of values
        for one or more columns of data. Table is sorted and includes cumulative
        values which can be useful for identifying a cutoff.

        Example of Titanic df.stb.freq(['class']):
                 class	  count	    percent	    cumulative_count	cumulative_percent
                0	Third	491	    55.1066	    491	                55.1066
                1	First	216	    24.2424	    707	                79.3490
                2	Second	184	    20.6510	    891	                100.0

        Args:
            cols (list):       dataframe column names that will be grouped together
            thresh (float):    all values after this percentage will be combined into a
                               single category. Default is to not cut any values off
            other_label (str): if cutoff is used, this text will be used in the dataframe results
            clip_0 (bool):     In cases where 0 counts are generated, remove them from the list
            value (str):       Column that will be summed. If provided, summation is done
                               instead of counting each entry
            style (bool):      Apply a pandas style to format percentages
            sort_cols (bool):  By default False, will sort on numeric results.
                               If True, will sort based on column values.
            cum_cols (bool):   Default is True and will include Cumulative Count and Cumulative
                               Percent. Set to False and these columns will not be returned

        Returns:
            Dataframe that summarizes the number of occurrences of each value in the provided
            columns or the sum of the data provided in the value parameter
        """
        if not isinstance(cols, list):
            raise AttributeError('Must pass a list of columns')

        if isinstance(value, list):
            raise AttributeError('value must be a string not a list')

        if value and value not in self._obj.columns:
            raise AttributeError('value must be a column name')

        if value and not is_numeric_dtype(self._obj[value]):
            raise AttributeError(f'{value} must be a numeric column')

        if thresh > 100:
            raise AttributeError('Thresh must be <= 100')

        if thresh <= 1:
            warnings.warn(
                f'thresh should be expressed as a percentage. Did you mean {int(thresh*100)}?'
            )

        # Determine aggregation (counts or summation) for each item in column

        # TODO: NaNs need to be handled better. Wait for pandas 1.1
        # https://pandas.pydata.org/pandas-docs/dev/whatsnew/v1.1.0.html#allow-na-in-groupby-key
        if value:
            col_name = value
            agg_func = {value: 'sum'}
            group_data = self._obj.groupby(cols).agg(agg_func).reset_index()
        else:
            col_name = 'count'
            group_data = self._obj.groupby(cols).size().reset_index(
                name=col_name)

        # Sort the results either by the grouped column(s) or numeric values
        # cleanup the index
        if sort_cols:
            results = group_data.sort_values(
                cols, ascending=True).reset_index(drop=True)
        else:
            results = group_data.sort_values(
                [col_name] + cols, ascending=False).reset_index(drop=True)

        # In data with null values, can include 0 counts filter them out by default
        if clip_0:
            results = results[results[col_name] > 0]

        # Include percents
        total = results[col_name].sum()
        results['percent'] = (results[col_name] / total) * 100

        # Keep track of cumulative counts or totals as well as their relative percent
        results[f'cumulative_{col_name}'] = results[col_name].cumsum()
        results['cumulative_percent'] = (results[f'cumulative_{col_name}'] /
                                         total) * 100

        # cutoff is a percentage below which all values are grouped together in an
        # others category
        if thresh < 100:
            # Flag the All Other rows
            results[other_label] = False
            results.loc[results['cumulative_percent'] > thresh,
                        other_label] = True

            # Calculate the total amount and percentage of the others
            other_total = results.loc[results[other_label], col_name].sum()
            other_pct = (other_total / total) * 100

            # Create the footer row to append to the results
            all_others = pd.DataFrame({
                col_name: [other_total],
                'percent': [other_pct],
                f'cumulative_{col_name}': [total],
                'cumulative_percent': [100.0]
            })
            # Categorical columns can break the merge. Convert to strings
            cat_cols = results.select_dtypes(['category']).columns
            results[cat_cols] = results[cat_cols].apply(lambda x: x.astype(str))
            # Add the footer row, remove the Others column and rename the placeholder
            results = pd.concat(
                [results[results[other_label] == False], all_others],
                ignore_index=True).drop(columns=[other_label]).fillna(
                    dict.fromkeys(cols, other_label))
        if not cum_cols:
            results = results.drop(
                columns=['cumulative_percent', f'cumulative_{col_name}'])
        if style:
            format_dict = {
                'percent': '{:.2f}%',
                'cumulative_percent': '{:.2f}%',
                'count': '{0:,.0f}',
                f'{col_name}': '{0:,.0f}',
                f'cumulative_{col_name}': '{0:,.0f}'
            }
            return results.style.format(format_dict)
        else:
            return results

    def missing(self, clip_0=False, style=False):
        """ Build table of missing data in each column.

            clip_0 (bool):     In cases where 0 counts are generated, remove them from the list
            style (bool):     Apply a pandas style to format percentages

        Returns:
            DataFrame with each Column including total Missing Values, Percent Missing
            and Total rows
        """
        missing = pd.concat(
            [self._obj.isna().sum(),
             self._obj.isna().mean().mul(100)],
            axis='columns').rename(columns={
                0: 'missing',
                1: 'percent'
            })
        missing['total'] = len(self._obj)
        if clip_0:
            missing = missing[missing['missing'] > 0]

        results = missing[['missing', 'total',
                           'percent']].sort_values(by=['missing'],
                                                   ascending=False)
        if style:
            format_dict = {
                'percent': '{:.2f}%',
                'total': '{0:,.0f}',
                'missing': '{0:,.0f}'
            }
            return results.style.format(format_dict)
        else:
            return results

    def counts(self,
               include=None,
               exclude=None,
               sort_ascending=True,
               sort_col='unique'):
        """ Build a table of total and unique values in a column.
        Also include most and least frequent counts and items.

        |             |   count |   unique | most_freq   |   most_freq_count | least_freq   |   least_freq_count |
        |:------------|--------:|---------:|:------------|------------------:|:-------------|-------------------:|
        | survived    |     891 |        2 | 0           |               549 | 1            |                342 |
        | sex         |     891 |        2 | male        |               577 | female       |                314 |
        | adult_male  |     891 |        2 | True        |               537 | False        |                354 |

        Args:
            include ([type], optional): List of types to include. Defaults to None.
                                        number object, category, datetime are valid options
                                        as well as valid options for select_dtypes
            exclude ([type], optional): List of types to exclude. Defaults to None.
                                        number, object, category, datetime are valid options
                                        as well as valid options for select_dtypes
            sort_ascending (bool, optional): Sort order. Defaults to True.
            sort_col (str, optional): Column (or index) to use for sorting. Defaults to 'unique'.

        Raises:
            ValueError: If invalid sort_col requested
            ValueError: If exclude options not correct

        Returns:
            DataFrame: Table with counts as well as unique values and most and least freq counts
        """
        # Descriptions for the resulting columns
        col_labels = [
            'count', 'unique', 'most_freq', 'most_freq_count', 'least_freq',
            'least_freq_count'
        ]

        # Can only sort on columns that are numeric
        valid_sort_cols = [
            'index', 'count', 'unique', 'most_freq_count', 'least_freq_count'
        ]

        # By default we support sorting by column names but can handle an index sort
        sort_by_col = True
        if sort_col not in valid_sort_cols:
            msg = f"sort_col must be one of {valid_sort_cols}"
            raise ValueError(msg)
        if sort_col == 'index':
            sort_by_col = False

        # if all is passed to include, make sure no exclusions made too
        # then assign all columns
        if include == 'all':
            if exclude is not None:
                msg = "exclude must be None when include is 'all'"
                raise ValueError(msg)
            # Filter out columns that are completely null
            cols_to_use = self._obj.columns[~self._obj.isna().all()]

        # Default is to include all columns
        elif (include is None) and (exclude is None):
            # Filter out completely null columns
            cols_to_use = self._obj.columns[~self._obj.isna().all()]

        # Pass the include and exclude values to select_dtypes
        else:
            cols_to_use = self._obj.select_dtypes(include=include,
                                                  exclude=exclude).columns

        # Calculate the results for all selected columns and build a DataFrame
        results = [(self._obj[col].count(), self._obj[col].nunique(),
                    self._obj[col].value_counts().idxmax(),
                    self._obj[col].value_counts().max(),
                    self._obj[col].value_counts().idxmin(),
                    self._obj[col].value_counts().min())
                   for col in cols_to_use]
        result_df = pd.DataFrame.from_records(results,
                                              index=cols_to_use,
                                              columns=col_labels)

        # Return the DataFrame sorted by a specific column or the index
        if sort_by_col:
            return result_df.sort_values(by=[sort_col],
                                         ascending=sort_ascending)
        else:
            return result_df.sort_index(ascending=sort_ascending)

    def _get_group_levels(self, level=1):
        """Internal helper function to flatten out the group list from a multiindex

        Args:
            level (int, optional): [description]. Defaults to 1.

        Returns:
            [type]: [description]
        """
        list_items = [col[0:level] for col in self._obj.index]
        results = []
        for x in list_items:
            if x not in results:
                results += [x]
        return results

    def _clean_labels(self, multi_index):
        """ Remove flags on the subtotal labels that are used to enforce sorting. This
        is an internal function

        Args:
            multi_index (pandas multi-index): Multi Index that includes the subtotal ordering
                                              text
        """
        master_list = []
        names = list(multi_index.names)
        for index_item in multi_index:
            sub_list = []
            for level in index_item:
                if level.startswith(self.SORT_FLAG):
                    level_val = level[len(self.SORT_FLAG):]
                else:
                    level_val = level
                sub_list.append(level_val)
            master_list.append(tuple(sub_list))
        return pd.MultiIndex.from_tuples(tuple(master_list), names=names)

    def subtotal(self,
                 sub_level=None,
                 grand_label='grand_total',
                 sub_label='subtotal',
                 show_sep=True,
                 sep=' | '):
        """ Add a numeric subtotals to a DataFrame. If the DataFrame has a multi-index, will
        add a subtotal at all levels defined in sub_level as well as a Grand Total

            sub_level (int or list): Grouping level to calculate subtotal. Default is max
                                     available. Can pass a single integer or a list of valid
                                     levels.
            grand_label (str):       Label override for the total of the entire DataFrame
            sub_label (str):         Label override for the sub total of the group
            show_sep  (bool):        Default is True to show subtotal levels separated by one
                                     or more characters
            sep (str):               Seperator for levels, defaults to |

        Returns:
            DataFrame with Grand Total and Sub Total levels as specified in sub_level
        """
        all_levels = self._obj.index.nlevels

        # Validate seperator is a string
        if not isinstance(sep, str):
            raise AttributeError('sep must be a string')
        # No value is specified, use the maximum
        if sub_level is None:
            sub_calc_list = list(range(1, all_levels))
        # Sort the list or tuple
        elif isinstance(sub_level, (list, tuple)):
            sub_calc_list = list(sub_level)
            sub_calc_list.sort()
        # Convert an integer to a list
        elif isinstance(sub_level, int):
            sub_calc_list = [sub_level]

        grand_total_label = tuple([f'{grand_label}'] +
                                  [' ' for _ in range(1, all_levels)])

        # If this is not a multiindex, add the grand total to the DataFrame
        if all_levels == 1:
            # No subtotals since no groups
            # Make sure the index is an object so we can append the subtotal without
            # Getting into Categorical issues
            self._obj.index = self._obj.index.astype('object')

            # Get list of all boolean columns
            # Recent version of pandas have deprecated automatic boolean
            # to numeric conversion. This preserves the previous behavior
            # where boolean values are treated as integers
            bool_col_convert = {
                x: 'int64'
                for x in self._obj.select_dtypes(include='bool').columns
            }

            # If not multi-level, rename should not be a tuple
            # Add the Grand Total label at the end

            return pd.concat([
                self._obj.astype(bool_col_convert),
                self._obj.sum(numeric_only=True).rename(
                    grand_total_label[0]).to_frame().T
            ],
                             axis='index')

        # Check that list is in the appropriate range
        if sub_calc_list[0] <= 0 or sub_calc_list[-1] > all_levels - 1:
            if (all_levels-1) == 1:
                error_msg = 'DataFrame only has 1 level. sub_level must be 1.'
            else:
                error_msg = f'sub_level must be between 1 and {all_levels-1}.'
            raise AttributeError(error_msg)

        # Remove any categorical indices
        self._obj.index = pd.MultiIndex.from_tuples(
            [n for i, n in enumerate(self._obj.index)],
            names=list(self._obj.index.names))

        subtotal_levels = []
        # Calculate the subtotal at each level given
        for i in sub_calc_list:
            level_result = self._calc_subtotal(sub_level=i,
                                               sub_label=sub_label,
                                               show_sep=show_sep,
                                               sep=sep)
            subtotal_levels.append(level_result)

        # Use combine first to join all the individual levels together into a single
        # DataFrame
        results = reduce(lambda l, r: l.combine_first(r), subtotal_levels)

        # Remove the subtotal sorting values
        results.index = self._clean_labels(results.index)
        # Final step is to add Grand total
        return pd.concat([
            results,
            self._obj.sum(numeric_only=True).rename(
                grand_total_label).to_frame().T
        ],
                         axis='index')

    def _calc_subtotal(self,
                       sub_level=None,
                       sub_label='subtotal',
                       show_sep=True,
                       sep=' | '):
        """ Internal helper function to calculate one level of subtotals. Do not call directly.

            sub_level (int):       Grouping level to calculate subtotal. Default is max available.
            sub_label (str):       Label override for the sub total of the group
            show_sep  (bool):      Default is True to show subtotal levels separated by one
                                   or more characters
            sep (str):             Seperator for levels, defaults to |

        Returns:
            DataFrame Sub Total
        """

        all_levels = self._obj.index.nlevels
        output = []
        # Get the total for each cross section of the multi-index
        for cross_section in self._get_group_levels(sub_level):
            # Need to have blank spaces in label names so that all results will
            # line up correctly
            num_spaces = all_levels - len(cross_section)
            if show_sep:
                total_label = self.SORT_FLAG + sep.join(
                    cross_section) + f' - {sub_label}'
            else:
                total_label = self.SORT_FLAG + f'{sub_label}'
            sub_total_label = list(cross_section[0:sub_level]) + [
                total_label
            ] + [' '] * num_spaces
            # Pull out the actual section and total it
            section = self._obj.xs(cross_section, drop_level=False)
            subtotal = section.sum(numeric_only=True).rename(
                tuple(sub_total_label)).to_frame().T
            output.append(pd.concat([section, subtotal]))
        return pd.concat(output)

    def flatten(self, reset=True, levels=None, sep='_'):
        """ Flatten multi-index column names into a single level of columns on a DataFrame

            reset (bool):       Should reset_index() be used before returning results
            levels (int, list): Indicate how many levels should be included in the column names
                                Can also pass a list of column levels (0-indexed) [0,1,2]
            sep (str):          Seperator for levels, defaults to _

            Returns:
                DataFrame with flattened column levels
        """
        tmp = self._obj.copy()
        valid_nlevels = tmp.columns.nlevels
        if valid_nlevels == 0:
            # Do nothing since there is no multiindex
            return tmp
        if levels is None:
            # Default to the max depth
            levels = valid_nlevels
        # Process when an integer is passed
        if type(levels) in [int]:
            if levels not in range(1, valid_nlevels + 1):
                raise AttributeError(
                    f"Levels must be between 1 and {valid_nlevels}")
            else:
                index = valid_nlevels - levels
                col_vals = [col[index:valid_nlevels] for col in tmp.columns.values]
        # Process a list or tuple of values
        if type(levels) in [list, tuple]:
            val_check = all([val in range(0, valid_nlevels) for val in levels])
            if not val_check:
                raise AttributeError(f"Value out of {range(0, valid_nlevels-1)}")
            else:
                if len(levels) > 1:
                    col_vals = [itemgetter(*levels)(col) for col in tmp.columns.values]
                else:
                    # Only one value so get a single level only
                    # Format this as a tuple so that the join doesn't break up the string
                    col_vals = [(col[levels[0]],) for col in tmp.columns.values]
        # Generate the column names and assign to the df
        columns = [
            sep.join(tuple(map(str, col))).rstrip(sep) for col in col_vals
        ]
        tmp.columns = columns
        if reset:
            return tmp.reset_index()
        else:
            return tmp

    def _pretty_col(self, col, precision, percent, pct_thresh):
        # Code from https://github.com/azaitsev/millify
        millnames = ['', 'k', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
        max_val = col.astype('float').max(axis=0)
        magnitude = int(
            math.floor(0 if max_val == 0 else math.log10(abs(max_val)) / 3))
        millindex = max(0, min(len(millnames) - 1, magnitude))
        values = col.div(10**(3 * millindex))
        format_letter = millnames[millindex]
        precision = f'.{precision}'
        if percent and max_val <= pct_thresh:
            format_string = "{:" + precision + "%}"
        else:
            format_string = '{:' + precision + 'f}' + f'{format_letter}'
        return values, format_string

    def pretty(self,
               precision=2,
               percent=True,
               nan='--',
               hide_index=False,
               pct_thresh=1,
               rows=20,
               exclude=None,
               caption=None):
        """ Pretty print a dataframe

        precision (int):    How many digits to show
        percent (bool):     Format numbers less than 1 as percentages
        nan (string):       Display instead of NaN values
        hide_index (bool):  Suppress the style of the index
        pct_thresh (int):   Value below which will be shown
        rows(int):          Number of rows to display in the output
        exclude(list):      List of column names to exclude
        caption (str):      Caption to display at the top of the dataframe

        Returns:
        """
        numeric_cols = self._obj.select_dtypes(include='number').columns
        # Allow the user to filter out numeric columns that should not be formatted
        exclude_list = exclude or []
        other_cols = self._obj.select_dtypes(exclude='number')
        format_dict = {}
        results = []
        for col in numeric_cols:
            if col not in exclude_list:
                new_col, format_data = self._pretty_col(
                    self._obj[col], precision, percent, pct_thresh)
                format_dict[col] = format_data
            else:
                format_dict[col] = None
                new_col = self._obj[col].values
            results.append(pd.Series(new_col, name=col))
        formatted_df = pd.concat(results, axis=1)
        full_df = pd.concat([other_cols, formatted_df], axis=1)
        # Truncate the number of rows
        # Max sure the column order is preserved
        # Add a filler to indicate truncation
        if isinstance(full_df.index, pd.MultiIndex):
            filler = pd.DataFrame(columns=full_df.index.names,
                                  index=[('--', ) * full_df.index.nlevels])
        else:
            filler = pd.DataFrame(columns=full_df.columns, index=['--'])
            filler.loc['--'] = pd.NA
        orig_col_order = self._obj.columns
        if len(full_df.index) > rows:
            short_table = pd.concat(
                [full_df.head(int(rows / 2)), filler,
                 full_df.tail(int(rows / 2))])
            return_data = short_table[orig_col_order].style.format(format_dict,
                                                                   na_rep=nan)
        else:
            return_data = full_df[orig_col_order].style.format(format_dict,
                                                               na_rep=nan)
        if hide_index:
            return_data.hide(axis="index")
        if caption:
            return_data.set_caption(caption)
        return return_data
        