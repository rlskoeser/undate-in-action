import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


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


if __name__ == "__main__":
    app.run()
