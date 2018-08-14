import time
import pandas as pd
import numpy as np
import datetime # classes for manipulating dates and times
import calendar # classes for accessing month and its attributes.

# location of csv files to be in appropriate direcotry of your local machine to have this program run successfully

CITY_DATA = { 'chicago': './chicago.csv',
              'new york city': './new_york_city.csv',
              'washington': './washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_list = ['Chicago','New York','Washington']
    month_list = ['January','Feburary','March','April','May','June','All']
    week_list= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
   
  # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\n Enter City of Interest (chicago, new york, washington) \n')
        if city.title() in city_list:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nEnter  month (January - June or All). \n')
        if month.title() in month_list:
            break

   # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\n Enter day of week (Sunday - Saturday or All)\n')
        if day.title() in week_list:
            break
# Below data file name assignment is just to deal with space in the city name "New york city".
# There may be other ways of handling this but doing it in the best interest of easy of workout.

    # Data file name assignment
    if city.lower() == "new york":
        city = CITY_DATA['new york city']
        print('-'*40)
        print('\nFile  used for data analysis is : ', city)
    else:
        city = CITY_DATA[city.lower()]
        print('-'*40)
        print('\nFile  used for data analysis is : ', city)

    print('-'*40)

    return city.lower(), month.lower(), day.lower()



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
    df = pd.read_csv(city)
    # print(df.groupby(['Gender'])['Gender'].count())
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 # since index start with Zero and january is 1st month, so adding 1 to match the calendar.
        # print('month :',month)


        df = df[df['month'] == month] # month data frame


    if day != 'all':

        df = df[df['day_of_week'] == day.title()] # day data frame


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #used this function to get the most common attribute in the dataframe: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mode.html
    # display the most common month
    df['Month'] = df['Start Time'].dt.month
    com_month = df['Month'].mode()[0]

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day
    com_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_hr = df['hour'].mode()[0]

    print('Most common month: ', calendar.month_name[com_month])
    print('Most common day: ', com_day)
    print('Most popular hour: ', com_hr)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['com_start'] = df['Start Station']
    # display most commonly used start station
    com_start = df['com_start'].mode()[0]
    print ('The most commonly used start station: ', com_start)

    # display most commonly used end station
    df['com_end'] = df['End Station']
    com_end = df['com_end'].mode()[0]
    print('The most commonly used end station: ', com_end)

    # display most frequent combination of start station and end station trip
    freq_comb = df['com_start'] + ' to ' + df['com_end']
    print('The most frequent combination of start station and end station trip: ', freq_comb.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # converting Trip start time and end time to datetime type.
    start = pd.to_datetime(df['Start Time'])
    end = pd.to_datetime(df['End Time'])

    # display total travel time
    df['total_travel_time'] = start - end
    total =  df['total_travel_time'].sum()
    print("The total travel time: " + str(total))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The mean travel time: " + str(mean_travel))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cnt_user = df['User Type'].value_counts()
    print('Count of user types: ', cnt_user)

    # Display counts of gender
    #verify if this file has column "Gender"
    gender_col =  "Gender" in list(df.columns.values)
    # print("yes Gender column exists in this file: ", y_col)
    # cnt_gender = df.groupby(['Gender'])['Gender'].count()
    # print('Count of gender : ', cnt_gender)
    if gender_col:
        cnt_gender = df.groupby(['Gender'])['Gender'].count()
        print('Count of gender : ', cnt_gender)
    else:
        print("Count of gender :  Ooops, sorry Washington.csv file doesn't have 'GENDER' column")

    # Display earliest, most recent, and most common year of birth
    birth_col =  "Birth Year" in list(df.columns.values)
    if birth_col:
         earliest_year = df.sort_values('Birth Year').iloc[0]
         common_year = df['Birth Year'].mode()[0]
         print('earliest year of birth: ', int(earliest_year['Birth Year']))
         print('Most common year of birth: ', int(common_year))

    else:
         print("earliest, most recent, and most common year of birth :  Ooops, sorry Washington.csv file doesn't have 'Birth Year' column") 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#As advised by Udacity Reviewer on 08/13/2018, below funciton is defined to display raw data in the event user want to see them:
def display_data(df):
    user_input = input("  \n\n Do you want to see next 5 lines of raw data? Enter yes or no.\n' ")
    if user_input.lower() != 'no':
        print(df.head(5))
        display_data(df)
            



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nThank you for Exploring US Bikeshare Data\....Have a good day\n")
            break

if __name__ == "__main__":
	main()
