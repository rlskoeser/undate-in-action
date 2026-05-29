# Undate in Action


This notebook provides an introduction to the [`undate` python library](https://github.com/dh-tech/undate-python/) with an emphasis on demonstrating supported functionality with some example use cases from specific projects. `undate` is designed for working with uncertain and partially known dates, and also includes support for dates in multiple calendars and with mixed precision. This paper provides an overview of the basic functionality with comparison to the Python built-in `datetime.date`, demonstrating support for missing and partially known values. Use cases and data from [Princeton Geniza Project](https://geniza.princeton.edu/) and [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/) are used to further demonstrate the value and practical application of `undat`e` for parsing and comparing mixed precision dates in multiple calendars, and for calculating and plotting duration for events with known days but unknown years.

View as an interactive notebook online:  https://rlskoeser.github.io/undate-in-action/

Read the paper:

> Rebecca Sutton Koeser. 2025. “[Undate in Action](https://doi.org/10.63744/SFtXXpIE4ERh).” In Digital Humanities Tech Symposium 2025—Anthology of Computers and the Humanities, edited by Julia Damerow and Rebecca Sutton Koeser, vol. 2.


## Developer notes

To edit the notebook locally:

```
marimo edit undate-in-action.py
```

To compile notebook to static html + web assembly:

```
marimo export html-wasm undate-in-action.py -o docs --mode edit
```