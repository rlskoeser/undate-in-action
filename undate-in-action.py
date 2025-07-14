import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium", app_title="Undate in Action")


@app.cell
def _():
    import marimo as mo

    # path to public directory relative to this notebook
    NOTEBOOK_PUBLIC_DIR = mo.notebook_location() / "public"
    return NOTEBOOK_PUBLIC_DIR, mo


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

    import altair as alt
    import polars as pl

    from undate import Undate

    year, month, day = 2000, 11, 7

    # these are equivalent and we initialize them the same way
    dt_november7 = datetime.date(year, month, day)
    november7 = Undate(year, month, day)
    return Undate, alt, datetime, day, dt_november7, month, november7, pl, year


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""We can print both of them in ISO8601 format (YYYY-MM-DD) and we can compare them."""
    )
    return


@app.cell
def _(dt_november7, mo, november7):
    mo.md(
        f"""
    - `datetime.date`: {dt_november7}
    - `Undate`: {november7}

    Are these dates considered equal? **{bool(november7 == dt_november7)}**
    """
    )
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
    mo.md(
        f"""
    - `november` in `year2k` ? {november in year2k}
    - `november7` in `november` ? {november7 in november}
    - `easter1916` in `year2k` ? {easter1916 in year2k}
    - `november7_some_year` in `year2k` ? {november7_some_year in year2k}
    """
    )
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
    mo.md(
        f"""
    ### {someyear_1900s.label} : {someyear_1900s}
    - duration: `{someyear_1900s.duration()}`
    - duration in days: `{someyear_1900s.duration().days}`

    ### {late2022.label} : {late2022}
    - duration: `{late2022.duration()}`
    - duration in days: `{late2022.duration().days}`
    """
    )
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


@app.cell
def _(mo):
    mo.md(r"""## Example use cases from specific projects""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Princeton Geniza Project

    The [Princeton Geniza Project](https://geniza.princeton.edu/) is based on materials from a synagogue in Cairo; primarily medieval, primarily Hebrew script. Documents that have dates use a variety of calendars - Hebrew Anno Mundi and Seleucid calendars, as well as the Islamic Hijri calendar.
    """
    )
    return


@app.cell
def _(NOTEBOOK_PUBLIC_DIR, Undate, pl):
    import re

    from lark.exceptions import UnexpectedEOF
    from lark.visitors import VisitError


    # limit to documents with dates; using standard date and not inferred dates for this
    pgp_documents_df = pl.read_csv(
        str(NOTEBOOK_PUBLIC_DIR / "pgp_documents.csv")
    ).filter(pl.col("doc_date_standard").is_not_null())


    # set this to True to see details about parsing
    VERBOSE_PARSE_OUTPUT = False


    def remove_ordinals(val):
        return re.sub(r"(\d+)(st|nd|rd|th)", "\\1", val)


    def parse_original_date(doc_date_original, doc_date_calendar):
        # print(f"PGPID {row.pgpid} {row.doc_date_original} ({row.doc_date_calendar})")
        undate_calendar = None
        if doc_date_calendar == "Anno Mundi":
            undate_calendar = "Hebrew"
        elif doc_date_calendar == "Hijrī":
            undate_calendar = "Islamic"
        elif doc_date_calendar == "Seleucid":
            # handle seleucid as hebrew with offset (adapted from PGP code)
            undate_calendar = "Seleucid"

        if undate_calendar:
            value = doc_date_original

            # some dates have unknown digits, e.g. 1[.] Kislev 48[..] or 152[.]
            # ... the calendar parser don't support this, even though Undate does support unknown digits
            # in future, perhaps we can add missing digit logic with this syntax to share across appropriate parsers
            if "[." in value:
                if VERBOSE_PARSE_OUTPUT:
                    print(f"ignoring missing digits for now {value}")
                value = (
                    value.replace("[.]", "0")
                    .replace("[..]", "00")
                    .replace("[...]", "000")
                )

            # some dates have inferred numbers, e.g. Friday, [25] Nisan [4810] or 8 Elul (4)811'
            # for now, just strip out brackets before parsing;
            # in future, could potentially infer uncertainty based on these
            value = (
                value.replace("[", "")
                .replace("]", "")
                .replace("(", "")
                .replace(")", "")
            )

            # for now, remove modifiers that are not supported by undate parser:
            #   Late Tevet 4903, Last decade of Kislev 5004, first third of ...
            #   some dates include of, e.g. day of month
            modifiers = [
                "Late ",
                "(first|middle|last)( third|half|decade|tenth)? (of )?",
                "(Beginning|end) of ",
                "last day",
                "First 10 days",
                " of",
                "spring",
                "decade ",
                "night, ",
            ]
            for mod in modifiers:
                value = re.sub(mod, "", value, flags=re.I)

            # there are a handful of misspelled wednesdays...
            value = value.replace("Wedensday", "Wednesday")
            # and a Thrusday
            value = value.replace("Thrusday", "Thursday")

            # three Hebrew calendar dates include text "AM" at end; at least one AH date
            if value.endswith(" AM") or value.endswith(" AH"):
                value = value[:-3]
            if value.endswith("."):  # strip off trailing period
                value = value[:-1]

            # about 62 have ordinals; strip them out
            value = remove_ordinals(value)

            try:
                return Undate.parse(value, undate_calendar)
            except (VisitError, ValueError, UnexpectedEOF) as err:
                if VERBOSE_PARSE_OUTPUT:
                    print(f"Parse error : {value} ({undate_calendar}): {err}")
                return None


    pgp_documents_df = pgp_documents_df.with_columns(
        undate_orig=pl.struct(
            "doc_date_original", "doc_date_calendar"
        ).map_elements(
            lambda row: parse_original_date(
                row["doc_date_original"], row["doc_date_calendar"]
            ),
            return_dtype=pl.datatypes.Object,
        )
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # filter to records that were successfully parsed; determine weekday for use with day-level precision dates

    pgp_documents_df = (
        pgp_documents_df.filter(pl.col("undate_orig").is_not_null())
        .with_columns(
            pl.col("type").fill_null("Unknown"),  # set null type to unknown
            orig_date_precision=pl.col("undate_orig").map_elements(
                lambda x: str(x.precision).lower(),
                return_dtype=pl.datatypes.String,
            ),
            undate_weekday=pl.col("undate_orig").map_elements(
                lambda x: x.earliest.weekday, return_dtype=pl.datatypes.Int32
            ),
        )
        .with_columns(
            undate_weekday_name=pl.col("undate_weekday").map_elements(
                lambda x: days[x], return_dtype=pl.datatypes.String
            )
        )
    )


    pgp_documents_df.select(
        "pgpid",
        "type",
        "doc_date_original",
        "doc_date_calendar",
        "doc_date_standard",
        "undate_orig",
        "orig_date_precision",
        "undate_weekday_name",
    ).head(10)
    return days, pgp_documents_df


@app.cell
def _(mo):
    mo.md(
        r"""
    Calendar dates preserve original values for year, month, and day but underneath we calculate the earliest and latest dates in Gregorian calendar so dates can be used together across calendars.

    When working across calendars, dates with the same precision (year, month), have different durations in days!
    """
    )
    return


@app.cell
def _(pgp_documents_df, pl):
    pgp_documents_df.filter(
        pl.col("orig_date_precision").is_in(["year", "month"])
    ).limit(20).with_columns(
        earliest=pl.col("undate_orig").map_elements(
            lambda x: x.earliest, return_dtype=pl.datatypes.Object
        ),
        latest=pl.col("undate_orig").map_elements(
            lambda x: x.latest, return_dtype=pl.datatypes.Object
        ),
        duration=pl.col("undate_orig").map_elements(
            lambda x: x.duration().days, return_dtype=pl.datatypes.Object
        ),
    ).select(
        "doc_date_original",
        "doc_date_calendar",
        "undate_orig",
        "earliest",
        "latest",
        "duration",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Undate objects store date precision, so we can easily see what the variation is in the precision of the dates we're able to parse.

    Note that this is somewhat skewed by the dates we're able to parse and the  modifiers we don't yet handle that were ignored during parsing.
    """
    )
    return


@app.cell
def _(pgp_documents_df):
    # this is skewed because of the kinds of dates we're not able to parse or modifiers we're omitting entirely
    pgp_documents_df["orig_date_precision"].value_counts()
    return


@app.cell
def _(alt, days, pgp_documents_df, pl):
    alt.Chart(
        pgp_documents_df.filter(pl.col("orig_date_precision").eq("day")).select(
            "type", "undate_weekday", "undate_weekday_name", "pgpid"
        )
    ).mark_rect().encode(
        alt.X("undate_weekday_name", sort=days, title="weekday"),
        alt.Color("count(pgpid)", title="# of documents"),
    ).facet(
        row=alt.Facet(
            "type",
            title="",
            header=alt.Header(
                labelAngle=0, labelAnchor="start", labelBaseline="bottom"
            ),
        )
    ).resolve_scale(color="independent").properties(
        title="Document frequency by weekday"
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Shakespeare and Company Project

    [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/) is based on the materials from Sylvia Beach's famous English-language lending library which operated in Paris in the 1920s and 1930s.


    This project includes borrowing events with unknown years; with `undate` we can calculate how long a book was borrowed even when we don't know the exact year.

    First we define a couple of methods that we'll use with the data; one to parse the date and calculate duration in days, and another for an indicator whether the year was known or not.
    """
    )
    return


@app.cell
def _():
    from undate import UndateInterval
    from undate.date import ONE_DAY, UnInt
    from undate.converters.iso8601 import ISO8601DateFormat


    def undate_duration(start_date, end_date):
        isoformat = ISO8601DateFormat()

        unstart = isoformat.parse(start_date)
        unend = isoformat.parse(end_date)
        interval = UndateInterval(earliest=unstart, latest=unend)

        # borrow durations in Shakespeare and Company Project were defined as not including both ends (or half both ends)
        # to reconcile differences between duration logic with undate, which includes both endpoints, we subtract one day
        return (interval.duration() - ONE_DAY).days


    def known_year(date):
        return "known" if ISO8601DateFormat().parse(date).known_year else "unknown"
    return known_year, undate_duration


@app.cell
def _(mo):
    mo.md(
        r"""Then we load the Project events data, filter to Gertrude Stein's borrow events, and limit to the set of fields relevant to this analysis."""
    )
    return


@app.cell
def _(NOTEBOOK_PUBLIC_DIR, known_year, pl, undate_duration):
    stein_borrow_events_df = (
        pl.read_csv(
            str(NOTEBOOK_PUBLIC_DIR / "SCoData_events_v2.0_2025.csv"),
            infer_schema_length=10000,
        )
        .filter(
            pl.col("member_ids").eq("stein-gertrude"),
            pl.col("event_type").eq("Borrow"),
            # slight cheat: we're going to limit to events that Project
            pl.col("borrow_duration_days").is_not_null(),
        )
        .select(
            "event_type",
            "start_date",
            "end_date",
            "borrow_duration_days",
            "item_title",
            "item_authors",
            "item_year",
        )
    )

    # calculate durations; returns a dataframe with one column
    duration_df = stein_borrow_events_df.select("start_date", "end_date").map_rows(
        lambda x: undate_duration(x[0], x[1]), return_dtype=pl.datatypes.Int32
    )

    # add fields to the main dataframe for duration and whether year is known
    stein_borrow_events_df = stein_borrow_events_df.with_columns(
        undate_duration=duration_df["map"],
        known_year=stein_borrow_events_df["start_date"].map_elements(
            known_year, return_dtype=pl.datatypes.String
        ),
    )

    stein_borrow_events_df.head()
    return (stein_borrow_events_df,)


@app.cell
def _(mo):
    mo.md(
        r"""
    Next we define a method to plot the durations as a raincloud plot. which will let us look at the distribution in two different ways.

    I'm borrowing the raincloud plot code from my own previous work here, if you want to see the original and associated article, check it out at https://github.com/rlskoeser/shxco-missingdata-specreading
    """
    )
    return


@app.cell
def _(alt):
    def raincloud_plot(dataset, fieldname, field_label, color_opts=None):
        """Create a raincloud plot for the density of the specified field
        in the given dataset. Takes an optional tooltip for the strip plot.
        Returns an altair chart."""

        # create a density area plot of specified fieldname

        duration_density = (
            alt.Chart(dataset)
            .transform_density(
                fieldname,
                as_=[fieldname, "density"],
            )
            .mark_area(orient="vertical")
            .encode(
                x=alt.X(
                    fieldname, title=None, axis=alt.X(labels=False, ticks=False)
                ),
                y=alt.Y(
                    "density:Q",
                    # suppress labels and ticks because we're going to combine this
                    title=None,
                    axis=alt.Axis(
                        labels=False, values=[0], grid=False, ticks=False
                    ),
                ),
            )
            .properties(height=100, width=800)
        )

        # Now create jitter plot of the same field
        # jittering / stripplot adapted from https://stackoverflow.com/a/71902446/9706217

        chart_color_opts = {}
        if color_opts is not None:
            chart_color_opts = {"color": color_opts}

        stripplot = (
            alt.Chart(dataset)
            .mark_circle(size=50)
            .encode(
                x=alt.X(
                    fieldname,
                    title=field_label,
                    axis=alt.Axis(labels=True),
                ),
                y=alt.Y("jitter:Q", title=None, axis=None),
                **chart_color_opts,
                # color=alt.Color(color_by),  # .scale(**color_scale),
            )
            .transform_calculate(jitter="(random() / 200) - 0.0052")
            .properties(
                height=120,
                width=800,
            )
        )

        # use vertical concat to combine the two plots together
        raincloud_plot = alt.vconcat(duration_density, stripplot).configure_concat(
            spacing=0
        )
        return raincloud_plot
    return (raincloud_plot,)


@app.cell
def _(alt, raincloud_plot, stein_borrow_events_df):
    stein_borrows = raincloud_plot(
        stein_borrow_events_df,
        "undate_duration",
        "Borrow duration in days",
        alt.Color("known_year", title="Year"),
    )

    # uncomment to save as PDF; requires vl-convert
    # stein_borrows.save("shxco_stein_borrows.pdf")
    stein_borrows
    return


if __name__ == "__main__":
    app.run()
