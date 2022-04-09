# History

# 0.9.1 (Dev)
- Fix issue #23 where tuple would cause an error. Also clarified error message.
- Fix issue #25 where append is deprecated in pandas.
- Adding stb.pretty() formatting

# 0.9.0 (2021-8-18)
- Fix issue #19 so that users can release memory for big dataframes. Thanks Laurent Esingle.
- Add new flatten() function to clean up multiindex column names
- Fix bug where threshold would not work for categorical columns

# 0.8.0 (2020-11-29)
- Fix styling for missing
- Counts would break on completely null columns. Filter those out.
- Add a warning if thresh is < 1

# 0.7.0 (2020-8-21)
- Add counts function to show the number of total and unique values in a column
- Some doc cleanups and clarifications

# 0.6.0 (2020-7-4)
- Frequency results were not proper percentages. Updated so percentages used correctly.
  This is a backwards-incompatible change
- Also changed the column labels to be lower_case
- Changed Grand Total to be grand_total

# 0.5.0 (2020-06-22)
- Subtotal sorting was not working consistently. Fixed
- Dropping cumulative count and percent was broken. Fixed

# 0.4.0 (2020-06-21)
- Adding a subtotal function
- Allow sorting by column values in freq table
- Add flag to drop cumulative count and frequency if they are not needed

# 0.3.0 (2020-05-31)
- First public release

# 0.2.0 (2020-05-27)
- Changing accessor to .stb in order to avoid any confusion with streamlit

# 0.1.0 (2020-05-26)
- Initial release
- First release on PyPI.
