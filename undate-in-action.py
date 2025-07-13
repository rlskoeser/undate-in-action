import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium", app_title="Undate in Action")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Undate in Action""")
    return


@app.cell
async def _():
    import sys

    # when running under WASM, use micropip to install necessary dependencies
    if sys.platform == "emscripten":
        import micropip

        await micropip.install("polars")
        # PyMeeus is a dependency of convertdate; for some reason micropip can't install it automatically
        await micropip.install(
            "https://www.piwheels.org/simple/pymeeus/PyMeeus-0.5.12-py3-none-any.whl#sha256=3fb4b35e1efa77bcde9c858f5749f2eb0b315a53caba7825d25b89cf24c1b47f"
        )
        await micropip.install("undate")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## How is `Undate` like `datetime.date` ? 

    Both can be initialized by specifying numeric values for year, month, and day.

    Both can printed with using the default serialization (ISO8601, or YYYY-MM-DD), and we can compare them.

    """
    )
    return


@app.cell
def _():
    import datetime

    from undate import Undate

    year, month, day = 2000, 11, 7

    # these are equivalent and we initialize them the same way
    dt_november7 = datetime.date(year, month, day)
    november7 = Undate(year, month, day)
    return Undate, datetime, day, dt_november7, month, november7, year


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""We can print both of them in ISO8601 format (YYYY-MM-DD) and we can compare them."""
    )
    return


@app.cell
def _(dt_november7, mo, november7):
    mo.md(f"""
    - `datetime.date`: {dt_november7}
    - `Undate`: {november7}

    Are these dates considered equal? **{bool(november7 == dt_november7)}**
    """)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## How is `Undate` _not_ like `datetime.date` ? 

    An `Undate` can initialized with partial information.  

    `Undate` can also take an optional label, since sometimes it's useful to name a date.
    """
    )
    return


@app.cell
def _(Undate, day, month, november7, year):
    # November 2000
    november = Undate(year, month, label="November 2000")
    # Year 2000
    year2k = Undate(year, label="Y2K")
    # November 7 in an unknown year
    november7_some_year = Undate(month=month, day=day, label="Some November 7")
    # marimo won't let us duplicate a variable, but let's add a label to the date we initialized before
    november7.label = "November 7, 2000"

    # sometimes names are important
    easter1916 = Undate(1916, 4, 23, label="Easter 1916")
    return easter1916, november, november7_some_year, year2k


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """If you try to do that with `datetime.date`, you get a `TypeError` because all three fields are required."""
    )
    return


@app.cell
def _(datetime, month, year):
    try:
        datetime.date(year, month)
    except TypeError as err:
        print(err)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """Each of these `Undate` objects can be printed out in a standard format; the `Undate` class also tracks how precisely a date is specified, and can calculate the duration."""
    )
    return


@app.cell
def _(easter1916, mo, november, november7, november7_some_year, year2k):
    output = []

    for example_date in [
        november,
        year2k,
        november7_some_year,
        november7,
        easter1916,
    ]:
        output.append(f"""
    ### {example_date.label}: {example_date}
    - Date precision: {example_date.precision}
    - Duration in days: {example_date.duration().days}
    """)

    mo.md("---".join(output))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""We can also do some simple calculations, like checking whether one date falls within another date."""
    )
    return


@app.cell
def _(easter1916, mo, november, november7, november7_some_year, year2k):
    mo.md(f"""
    - `november` in `year2k` ? {november in year2k}
    - `november7` in `november` ? {november7 in november}
    - `easter1916` in `year2k` ? {easter1916 in year2k}
    - `november7_some_year` in `year2k` ? {november7_some_year in year2k}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## What else can `Undate` do?

    In the last set of examples, the values were all integers and parts of the date were either known or unknown.  But what if you know part of a date?

    You can initialize `Undate` with strings and use `X` to indcate unknown values.
    """
    )
    return


@app.cell
def _(Undate, mo):
    someyear_1900s = Undate("19XX", label="1900s")
    late2022 = Undate(2022, "1X", label="late 2022")

    output2 = []

    for example_date2 in [someyear_1900s, late2022]:
        output2.append(f"""
    ### {example_date2.label}: {example_date2}
    - Date precision: {example_date2.precision}
    - Duration in days: {max(example_date2.duration().days)}
    """)

    mo.md("---".join(output2))
    return late2022, someyear_1900s


@app.cell
def _(mo):
    mo.md(r"""If you try that with `datetime.date` you get another `TypeError`.""")
    return


@app.cell
def _(datetime):
    try:
        datetime.date("19XX", 1, 1)
    except TypeError as err:
        print(err)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Uncertain durations

    If you were paying close attention, you might have noticed I used the `max()` function the last time I output the duration.

    The most recent version of `undate` (v0.5) includes code for uncertain tim deltas.
    """
    )
    return


@app.cell
def _(late2022, mo, someyear_1900s):
    mo.md(f"""
    ### {someyear_1900s.label} : {someyear_1900s}
    - duration: `{someyear_1900s.duration()}`
    - duration in days: `{someyear_1900s.duration().days}`

    ### {late2022.label} : {late2022}
    - duration: `{late2022.duration()}`
    - duration in days: `{late2022.duration().days}`

    """)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Even without precise information, we can still do some useful comparisons. 

    February of an unknown year is still shorter than October, November, or December.
    """
    )
    return


@app.cell
def _(Undate, late2022, mo):
    some_february = Undate(month=2, label="February of some year")
    some_february.duration() < late2022.duration()

    mo.md(f"""### {some_february.label} : {some_february}
    - duration: `{some_february.duration()}`
    - duration in days: `{some_february.duration().days}`

    Is February of an unknown year shorter than an uncertain month 1X? (October, November, or December)

    `some_february.duration() < late2022.duration() = { some_february.duration() < late2022.duration() }`
    """)
    return


if __name__ == "__main__":
    app.run()
