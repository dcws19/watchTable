import datetime


def get_week_number():
    # Define the start date of Week 1 (e.g., Saturday, August 31, 2024)
    start_date = datetime.date(2024, 8, 31)

    # Calculate the current date
    today = datetime.date.today()

    # Calculate the difference in days between today and the start date
    day_diff = (today - start_date).days

    # Calculate the week number
    # Each week is 7 days, so divide the day difference by 7 and add 1 for the current week
    if day_diff >= 0:
        week_number = (day_diff // 7) + 1
    else:
        # If today's date is before the start date, return Week 1
        week_number = 1

    return week_number
