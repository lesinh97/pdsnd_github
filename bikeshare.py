import time
import pandas as pd
import click

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS = ('sunday', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday')


def get_choice(prompt, choices=('y', 'n')):
    """Get a valid user input based on provided choices."""
    while True:
        user_input = input(prompt).lower().strip()
        if user_input == 'end':
            raise SystemExit
        elif ',' not in user_input:
            if user_input in choices:
                return user_input
        else:
            selected_choices = [i.strip().lower()
                                for i in user_input.split(',')]
            if all(choice in choices for choice in selected_choices):
                return selected_choices
        prompt = "\nInvalid input. Please enter a valid option:\n>"


def get_filters():
    """Ask user to specify city(ies), month(s), and weekday(s)."""
    print("\nLet's explore some US bikeshare data!")
    print("Type 'end' anytime to exit.\n")

    city = get_choice(
        "\nWhich city(ies)? (e.g., New York City, Chicago, Washington)\n>", CITY_DATA.keys())
    month = get_choice("\nWhich month(s)? (From January to June)\n>", MONTHS)
    day = get_choice("\nWhich weekday(s)?\n>", WEEKDAYS)

    confirmation = get_choice(
        f"\nConfirm filters:\n City(ies): {city}\n Month(s): {month}\n Weekday(s): {day}\n [y] Yes\n [n] No\n>",
        ('y', 'n')
    )
    return (city, month, day) if confirmation == 'y' else get_filters()


def load_data(city, month, day):
    """Load data based on the specified filters."""
    print("\nLoading data for your selected filters...")
    start_time = time.time()

    df = pd.concat([pd.read_csv(CITY_DATA[c]) for c in city], sort=True) if isinstance(
        city, list) else pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = df[df['Month'].isin([MONTHS.index(m) + 1 for m in month])]
    else:
        df = df[df['Month'] == MONTHS.index(month) + 1]

    if isinstance(day, list):
        df = df[df['Weekday'].isin([d.title() for d in day])]
    else:
        df = df[df['Weekday'] == day.title()]

    print(f"\nData loaded in {time.time() - start_time:.2f} seconds.")
    return df


def display_time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nMost Frequent Times of Travel:\n')

    most_common_month = MONTHS[df['Month'].mode()[0] - 1].title()
    most_common_day = df['Weekday'].mode()[0]
    most_common_hour = df['Start Hour'].mode()[0]

    print(f'Month: {most_common_month}')
    print(f'Day: {most_common_day}')
    print(f'Hour: {most_common_hour}')


def display_station_stats(df):
    """Display statistics on the most popular stations and trips."""
    print('\nMost Popular Stations and Trip:\n')

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_trip = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()

    print(f'Start Station: {most_common_start_station}')
    print(f'End Station: {most_common_end_station}')
    print(f'Trip: {most_common_trip[0]} to {most_common_trip[1]}')


def display_trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nTrip Duration:\n')

    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()

    print(
        f'Total Duration: {total_duration // 86400}d {total_duration % 86400 // 3600}h {total_duration % 3600 // 60}m {total_duration % 60}s')
    print(
        f'Average Duration: {average_duration // 60}m {average_duration % 60}s')


def display_user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nUser Stats:\n')

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types.to_string())

    if 'Gender' in df.columns:
        gender_distribution = df['Gender'].value_counts()
        print('\nGender Distribution:\n', gender_distribution.to_string())
    else:
        print(f'\nNo gender data available for {city.title()}.')

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print(f'\nEarliest Birth Year: {earliest_birth_year}')
        print(f'Most Recent Birth Year: {most_recent_birth_year}')
        print(f'Most Common Birth Year: {most_common_birth_year}')
    else:
        print(f'\nNo birth year data available for {city.title()}.')


def display_raw_data(df):
    """Display raw data, 5 rows at a time."""
    print("\nDisplaying raw data:\n")

    start_index = 0
    while True:
        print(df.iloc[start_index:start_index + 5])
        start_index += 5

        if get_choice("\nShow more data? [y] Yes, [n] No\n>", ('y', 'n')) != 'y':
            break


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            choice = get_choice(
                "\nSelect option:\n [ts] Time Stats\n [ss] Station Stats\n [td] Trip Duration\n [us] User Stats\n [rd] Raw Data\n [r] Restart\n>",
                ('ts', 'ss', 'td', 'us', 'rd', 'r')
            )
            click.clear()

            if choice == 'ts':
                display_time_stats(df)
            elif choice == 'ss':
                display_station_stats(df)
            elif choice == 'td':
                display_trip_duration_stats(df)
            elif choice == 'us':
                display_user_stats(df, city)
            elif choice == 'rd':
                display_raw_data(df)
            elif choice == 'r':
                break

        if get_choice("\nRestart? [y] Yes, [n] No\n>", ('y', 'n')) != 'y':
            break


if __name__ == "__main__":
    main()
