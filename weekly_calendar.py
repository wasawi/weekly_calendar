import os
import cairo
from datetime import date, datetime

# A4 standard international paper size
DOC_WIDTH = 1684  # 210mm / 8.27 inches
DOC_HEIGHT = 2384  # 297mm / 11.69 inches

BOX_LINE_WIDTH = 1
BIRTHDAY_LINE_WIDTH = 2
DRAW_TO_DATE = False
BOX_SIZE = 10  # Adjust the size of the boxes as needed
MARGIN = 6
EXTRA_MARGIN = 6

def get_iso_weeks(year):
    """Calculate the number of weeks in the ISO calendar for the given year."""
    last_day = date(year, 12, 31)
    total_weeks = last_day.isocalendar()[1]
    if total_weeks == 1:
        total_weeks = 52
    return total_weeks

def get_birthday_celebration(year, birthday):
    """Determine the celebration date based on the birthday."""
    if birthday.month == 2 and birthday.day == 29:
        # Check if the current year is a leap year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return birthday  # Use February 29 if it's a leap year
        else:
            return date(year, 3, 1)  # Use March 1 if it's not a leap year
    return birthday

def get_birthday_week(year, birthday):
    """Get the ISO week number that contains the user's birthday for a given year."""
    birthday = get_birthday_celebration(year, birthday)
    birthday_date = date(year, birthday.month, birthday.day)
    return birthday_date.isocalendar()[1]

def calculate_fade_color(year_index, fade_start_year, total_years):
    """Calculate the fade color based on the year index, where year 80 starts fading."""
    if year_index >= fade_start_year:
        fade_fraction = (year_index - fade_start_year) / (total_years - fade_start_year)
        return fade_fraction, fade_fraction, fade_fraction
    return 0, 0, 0

def draw_square(ctx, pos_x, pos_y, box_size, stroke_color, line_width):
    """Draw a single box (week) at the specified position."""
    ctx.set_line_width(line_width)
    ctx.set_source_rgb(*stroke_color)  # Set stroke color
    ctx.rectangle(pos_x, pos_y, box_size, box_size)
    ctx.stroke()  # Only stroke, don't preserve the path
    ctx.set_source_rgb(1, 1, 1)  # White fill
    ctx.fill()

def draw_year_row(ctx, year, pos_x, pos_y, birthday, start_week=None, end_week=None, fillcolour=(0, 0, 0)):
    """Draws a row of boxes for a given year, starting from a specific week and ending at a specific week."""
    current_date = datetime.now().date()
    current_year = current_date.year
    current_week = current_date.isocalendar()[1]

    weeks = get_iso_weeks(year)
    birthday_week = get_birthday_week(year, birthday)

    if start_week is None:
        start_week = 1
    if end_week is None:
        end_week = weeks

    for week in range(start_week - 1, end_week):
        box_pos_x = pos_x + week * (BOX_SIZE + MARGIN)  # Horizontal margin between weeks

        # Determine the color for past weeks
        if (year < current_year) or (year == current_year and week + 1 < current_week):
            if DRAW_TO_DATE:
                stroke_color = (0, 1, 1)  # Blue for past weeks
            else:
                stroke_color = fillcolour  # Use fading color for future weeks
        else:
            stroke_color = fillcolour  # Use fading color for future weeks

        if week + 1 == birthday_week:
            draw_square(ctx, box_pos_x, pos_y, BOX_SIZE, stroke_color, line_width=BIRTHDAY_LINE_WIDTH)
        else:
            draw_square(ctx, box_pos_x, pos_y, BOX_SIZE, stroke_color, line_width=BOX_LINE_WIDTH)

def create_weekly_calendar(birthday, num_years, filename='weekly_calendar.pdf'):
    if not os.path.exists("output"):
        os.makedirs("output")

    start_year = birthday.year
    surface = cairo.PDFSurface("output/" + filename, DOC_WIDTH, DOC_HEIGHT)
    ctx = cairo.Context(surface)

    vertical_margin = MARGIN
    extra_margin = EXTRA_MARGIN

    max_weeks = max(get_iso_weeks(year) for year in range(start_year, start_year + num_years))
    total_width = max_weeks * (BOX_SIZE + MARGIN) - MARGIN
    total_height = 0

    for i in range(num_years):
        total_height += BOX_SIZE + vertical_margin
        if (start_year + i) % 10 == 0:
            total_height += extra_margin

    total_height -= vertical_margin
    start_x = (DOC_WIDTH - total_width) / 2
    start_y = (DOC_HEIGHT - total_height) / 2

    current_position_y = start_y

    for i in range(num_years):
        current_year = start_year + i
        first_week = get_birthday_week(current_year, birthday) if i == 0 else None
        last_week = get_birthday_week(current_year, birthday) if i == num_years - 1 else None

        if current_year % 10 == 0:
            current_position_y += extra_margin

        #fill_colour = calculate_fade_color(i, int(num_years * 0.8), num_years)

        draw_year_row(ctx, current_year, start_x, current_position_y, birthday, start_week=first_week, end_week=last_week)
        current_position_y += BOX_SIZE + vertical_margin

    surface.finish()

def generate_calendars_from_file(file_path, num_years, draw_to_date = False):
    global DRAW_TO_DATE
    DRAW_TO_DATE = draw_to_date
    """Generates weekly calendar PDFs for each friend listed in the file."""
    with open(file_path, 'r') as file:
        for line in file:
            name, year, month, day = line.strip().split(',')
            birthday = date(int(year), int(month), int(day))
            if DRAW_TO_DATE:
                filename = f"{name}_.pdf"
            else:
                filename = f"{name}.pdf"
            create_weekly_calendar(birthday, num_years, filename)
            print(f"Generated {filename}")

# Example usage
#create_weekly_calendar(date(1982, 5, 19), 100)
generate_calendars_from_file('aniversaris amics.txt', 100)
generate_calendars_from_file('aniversaris amics.txt', 100, True)

#generate_calendars_from_file('aniversaris familia.txt', 100)
#generate_calendars_from_file('aniversaris familia.txt', 100, True)
