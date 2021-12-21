import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
        'new york city': 'new york city.csv',
        'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    goodInput = False
    good_city_inputs = ['chicago', 'new york city', 'washington']
    while not goodInput:  # not False -> True
        city = input("Enter the city you wish to analyze (chicago, new york city, or washington)\n").lower() # hello, chiqago
        if city in good_city_inputs:
            goodInput = True
        else:
            print("You messed up your input - please input one of the cities listed")
    # get user input for month (all, january, february, ... , june)
    goodInput = False
    good_month_inputs = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                         'october', 'november', 'december', 'all']
    while not goodInput:  # not False -> True
        month = input("Enter the month you wish to analyze (january...december or 'all')\n").lower()
        if month in good_month_inputs:
            goodInput = True
        else:
            print("You messed up your input - please input one of the months or 'all'")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    goodInput = False
    good_day_inputs = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while not goodInput:  # not False -> True
        day = input("Enter the day you wish to analyze (monday...friday or all)\n").lower()
        if day in good_day_inputs:
            goodInput = True
        else:
            print("You messed up your input - please input one of the days or 'all'")

    print('-' * 40)
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
    # chicago, all, all
    # file = city + '_sample.csv'
    file = 'C:/Users/Hp/Documents/Udacity/Bikeshare Project/Bikeshare Data/' + city + '.csv'
    df = pd.read_csv(file)

    # print(df)
    # # Creating the 4 columns by splitting the start time and end time columns -> Start TS, Start Date, End TS, End Date
    new = df['Start Time'].str.split(' ', n=1, expand=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Date'] = pd.to_datetime(new[0])
    df['Start Timestamp'] = new[1]
    df['Start Hour'] = df['Start Timestamp'].str.split(':', n=1, expand=True)[0]

    # print(df)
    #
    new = df['End Time'].str.split(' ', n=1, expand=True)
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['End Date'] = pd.to_datetime(new[0])
    df['End Timestamp'] = new[1]

    df['Time Travelled'] = (df['End Time'] - df['Start Time']) / pd.Timedelta(minutes=1) #.astype('timedelta64[m]')

    # print(df)

    # print(df)
    #
    # # add new column -> day_of_week from the start date
    df['Weekday'] = df['Start Date'].dt.day_name().str.lower()

    # print(df)
    # # add new column -> month from the start date
    df['Month'] = df['Start Date'].dt.month_name().str.lower()
    #
    # print(df)
    # # look for all rows that have month=month and day=day
    if day != 'all':
        df = df[df['Weekday'] == day]
    if month != 'all':
        df = df[df['Month'] == month]
    #
    # print(df)
    # print(df.head(5))
    return df


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(df['Month'].mode())
    # display the most common day of week
    print(df['Weekday'].mode())
    # # display the most common start hour
    print(df['Start Hour'].mode())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(df['Start Station'].mode())
    # display most commonly used end station
    print(df['End Station'].mode())
    # display most frequent combination of start station and end station trip
    print(df.groupby(['Start Station', 'End Station']).size().idxmax())
    # print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(df['Time Travelled'].sum())
    # display mean travel time
    print(df['Time Travelled'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    # Display counts of gender

    # if (condition - form of a question):
    #   do some code
    # else:
    #   do other code
    # print(hello)
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    # Display earliest, most recent, and most common year of birth

    # Earliest
    if 'Birth Year' in df.columns:
        print(df['Birth Year'].min())

    # Latest
        print(df['Birth Year'].max())

    #most common
        print(df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def raw_data(df):
    ask_user = input('Would you like to view raw data for the city selected? Print yes or no:\n')

    # letters = [a,b,c,d,e,f,g,h,i,j,k,l] (12)
    # x[1] == b
    # x[start=0:stop=len(x)-1:step_size=1]
    # x[3:6]
    idx = 0
    if ask_user == 'yes':
        print(df.iloc[idx:idx+5]) # -> df.iloc[0:5]

        while True:
            ask_user = input('Would you like to view more raw data for the city selected? Print yes or no:\n')
            if ask_user == 'yes':
                idx = idx + 5
                print(df.iloc[idx:idx+5])
            else:
                break



    # city, month, day = get_filters()
    # print('city = ' + city)
    # print('month = ' + month)
    # print('day = ' + day)
    # df = load_data('chicago', 'all', 'all')
    # user_stats(df)
    # time_stats(df)
    # station_stats(df)
    # user_stats(df)
    # time_stats(df)
    # station_stats(df)
    # user_stats(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
