## US Bikeshare Data Project

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Added lists
city_list = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
raw_data_line = 0

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city would you like to see data for? Chicago, New York or Washington? \n').lower()
        if city in city_list:
            break
        else:
            print('\nPlease enter a valid city name \n')
            
    # Filter by month, day, both or none     
    filter_type = input('\nWould you like to filter the data by Month, Day or neither? If neither, please type "all" for no time filter \n').lower()
    while True:
        if filter_type == 'month':
            
        # Get user input for month (all, january, february, ... , june)
            month = input('\nAnd which of the selected months? January, February, March, April, May or June? Or view all months by entering "All".\n').lower()
            day = 'all'
            if month in months:
                break
            else:
                print('\nPlease enter a valid month \n')
        
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        elif filter_type == 'day':
            day = input('\nAnd which of the selected day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? Or view all days by entering "All".\n').lower()
            month = 'all'
            if day in days:
                break
            else:
                print('\nPlease enter a valid day \n')
        
        # No filter type
        elif filter_type == 'all':    
            month = 'all'
            day = 'all'
            break
        
        # invalid entry
        else:
            print('\nPlease enter a valid filter type\n')
            filter_type = input('\nWould you like to filter the data by Month, Day or neither? If neither, please type "all" for no time filter \n').lower()
            continue

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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert Start Time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extracting month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day
    
    # filtering by month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    # filtering by day
    if day !=  'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Display the most common month
    popular_month = df['month'].mode()[0]
    
    print('\nMost common month: \n--> {}'.format(months[popular_month -1]).capitalize())

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost common day of the week: \n--> {}'.format(popular_day).capitalize())

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    
    print('\nMost common start hour in 24 Hour format: \n--> {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost common Start Station used: \n--> {}'.format(popular_start_station))
    
    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost common End Station used: \n--> {}'.format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    start_and_end = 'Start Station: ' + df['Start Station'] + '; End Station: ' + df['End Station']
    frequent_start_end = start_and_end.mode()[0]
    print('\nMost common Start and End Station trip combination: \n--> {}'.format(frequent_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Display total travel time
    df['Trip Time'] = df['End Time'] - df['Start Time']
    total_duration = df['Trip Time'].sum()
    print('\nTotal Travel time: \n--> {}'.format(total_duration))

    # Display mean travel time
    average_duration = df['Trip Time'].mean()
    print('\nAverage Travel time: \n--> {}'.format(average_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts for each User Type: \n{}'.format(user_types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nCounts for each Gender: \n{}'.format(gender))
    
    except:
        print('\nThere is no gender data available\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print('\nThe earliest year of birth: \n--> {}'.format(earliest_birth))
        print('\nThe most recent year of birth: \n--> {}'.format(recent_birth))
        print('\nThe most common year of birth: \n--> {}'.format(common_birth))
    
    except:
        print('\nThere is no birth data available\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Display additional bikeshare data"""
    
    global raw_data_line
    count = 0
    raw_data = input ('\nWould you like to view individual trip data? Please enter "Yes" or "No".\n').lower()
    
    while True:
        if raw_data == 'yes':
            print(df.head(raw_data_line + 5))
            raw_data_line = raw_data_line + 5
            count = count + 1
            raw_data = input('\nWould you like to view more individual trip data? Please enter "Yes" or "No"\n').lower()
            if raw_data == 'yes':
                continue
            if raw_data == 'no':
                print('\nThanks! In total you have viewed data for {} users\n'.format(count * 5))
                break
            else:
                raw_data = input ('\nPlease enter "Yes" or "No".\n').lower()
                continue
         
        if raw_data == 'no':
            print('\nThanks! In total you have viewed data for {} users\n'.format(count * 5))
            break
            
        if raw_data != 'yes' or 'no':
            raw_data = input ('\nPlease enter "Yes" or "No".\n').lower()
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        # enter yes to continue or anything else to exit 
        restart = input('\nWould you like to restart? Enter "Yes" to restart. Enter any input to quit.\n')
        if restart == 'yes':
            continue
        else:
            print('\nThanks for using US Bike Share Data\n')
            break
            


if __name__ == "__main__":
	main()
