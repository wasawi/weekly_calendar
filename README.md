# Lifetime Calendar

Generate a "life in weeks" wall calendar as a PDF: one row per year, one box per
ISO week, with the week of your birthday highlighted in every row. Inspired by
the classic idea that visualizing your life week-by-week makes its length
viscerally clear.

Each generated PDF is an A4-sized grid where:
- every row represents one year of life
- every box represents one ISO calendar week
- the box containing your birthday is drawn with a bolder border
- optionally, weeks already lived can be colored differently from weeks still
  to come

## Requirements

- Python 3
- [pycairo](https://pycairo.readthedocs.io/)

```bash
pip install pycairo
```

## Usage

Birthdays are read from a plain text file, one person per line:

```
Name, YYYY, M, D
```

For example, a file named `birthdays.txt`:

```
Jane Doe, 1990, 7, 14
John Smith, 1985, 12, 1
```

Then generate the calendars:

```python
from weekly_calendar import generate_calendars_from_file

# One PDF per person, 100 rows (years) each
generate_calendars_from_file('birthdays.txt', 100)

# Same, but also color in the weeks already lived (filename gets a "_" suffix)
generate_calendars_from_file('birthdays.txt', 100, True)
```

Running the script directly (see the bottom of `weekly_calendar.py`) will do
the same thing. PDFs are written to an `output/` directory, created
automatically if it doesn't exist, named after each person (e.g.
`Jane Doe.pdf`, `Jane Doe_.pdf` for the "drawn to date" version).

You can also generate a single calendar directly for one birthday:

```python
from datetime import date
from weekly_calendar import create_weekly_calendar

create_weekly_calendar(date(1990, 7, 14), 100, filename='jane.pdf')
```

## How the birthday week is chosen

Birthdays are matched to ISO calendar weeks, which don't always align neatly
with the Gregorian year: the first few days of January can technically belong
to the last ISO week of the *previous* year, and the last few days of
December can belong to the first ISO week of the *next* year. The calendar
accounts for this by bolding whichever row's box the birthday's true ISO week
actually falls into, rather than forcing an approximate match into the wrong
row.

February 29 birthdays are celebrated on March 1 in non-leap years.

## Configuration

A few constants near the top of `weekly_calendar.py` control the layout:

| Constant | Description |
|---|---|
| `BOX_SIZE` | Size of each week box, in points |
| `MARGIN` | Horizontal/vertical gap between boxes |
| `EXTRA_MARGIN` | Extra vertical gap added every 10 years, to break up the grid into decades |
| `BOX_LINE_WIDTH` | Border width of a normal week box |
| `BIRTHDAY_LINE_WIDTH` | Border width of the birthday week box |
| `DOC_WIDTH` / `DOC_HEIGHT` | Page size in points (defaults to A4) |

## License

MIT

output:

![alt text](https://github.com/wasawi/weekly_calendar/blob/main/readme_imgs/j.png?raw=true)

![alt text](https://github.com/wasawi/weekly_calendar/blob/main/readme_imgs/j_.png?raw=true)
