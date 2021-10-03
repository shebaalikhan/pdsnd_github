import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday', 'sunday']

def get_input(input_type, input_str):
    """
    Gets the input from user of the passed type.

    Returns:
        (str) input value
    """
        
    while True:
        invalid = False
        val = input(input_str).lower()
        # ignore case when comparing
        if input_type == "city":
            if val in CITY_DATA.keys():
                return val
            else:
                invalid = True
        elif input_type == "month":
            if val in MONTHS:
                return val
            else:
                invalid = True
        elif input_type == "day":
            if val in DAYS:
                return val
            else:
                invalid = True

        if invalid is True:
            print("\nInvalid %s, please try again!"%(input_type))
        

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input
    city = get_input("city", "Enter the name of the city: ")
    month = get_input("month", "Enter the month to filter by, or ""all"" if no filter: ")
    day = get_input("day", "Enter the name of the day of week to filter by, or ""all"" if no filter: ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    cur_city = CITY_DATA[city]
    df = pd.read_csv(cur_city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTHS.index(month)
        df = df[ df['month'] == month ]

    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    cur_month = df['month'].value_counts().idxmax()
    print("Most common month: ", cur_month)

    # display the most common day of week
    cur_day = df['day_of_week'].value_counts().idxmax()
    print("Most common day of week: ", cur_day)

    # display the most common start hour
    cur_hour = df['hour'].value_counts().idxmax()
    print("Most common start hour: ", cur_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()    

    # display most commonly used start station
    cur_station_start = df['Start Station'].value_counts().idxmax()
    print("Most commonly used start station: ", cur_station_start)

    # display most commonly used end station
    cur_station_end = df['End Station'].value_counts().idxmax()
    print("Most commonly used end station: ", cur_station_end)

    # display most frequent combination of start station and end station trip
    station_arr = df[['Start Station', 'End Station']].mode()
    
    cur_station_start_common = station_arr[0]
    cur_station_end_common = station_arr[1]
    
    print("Most commonly used start station and end station: {}, {}"\
            .format(cur_station_start_common, cur_station_end_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
        
    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time :", total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time :", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        for index,gender_count  in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))

    print()
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        # most common birth year
        most_common_year = birth_year.value_counts().idxmax()
        print("Most common birth year:", most_common_year)
        # most recent birth year
        most_recent = birth_year.max()
        print("Most recent birth year:", most_recent)
        # most earliest birth year
        earliest_year = birth_year.min()
        print("Most earliest birth year:", earliest_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    i = 0
    raw = input("\nWould you like to see first 5 rows of raw data; type 'yes' or 'no'?\n").lower()
    pd.set_option('display.max_columns',200)
    while True:
        if raw == 'no':
            break
    print(df[i:i+5])
    raw = input('\nWould you like to see next rows of raw data?\n').lower()
    i += 5
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    
