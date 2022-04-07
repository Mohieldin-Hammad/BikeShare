import time
import pandas as pd
import numpy as np



CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters(restart=None):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # makeing sure that greating will be printed in the first time only  
    if restart == None:
        print('Hello! Let\'s explore some US bikeshare data!')
    # that help when selcting the data from user using while loop to not ask the question more than one time
    c, m, d = False, False, False
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # ans will be returned as None or month or day or both
    ans = None
    while True:

        # get user input for city (chicago, new york city, washington).
        if c == False:
            city = input("Would you like to see data for Chicago, New York, or Washington?\n").strip().title()
            if city not in ["Chicago", "New York", "Washington"]:
                print("\nSeems you typed it incorrectly! So...")
                continue
            
            # maing the program more interactive with user
            print(f"\nDid you mean {city}! If this is not true, please restart the program now!")
            c = True
        # ask user to filter the data or not
        filter = input("\nWould you like to filter the data? Please answer by 'yes' or 'no'...\n").strip().lower()
        
        # if the user didn't answer correctly, the message will be printed again
        if filter not in ["yes", "no"]: continue
        
        if filter == "yes":
            f = False
            
            while True:
                # the user has the choice to filter the data by month, day, or both of them
                if f != True:
                    ans = input("Would you like it by month, day, or both?\n").strip().lower()
                    if ans not in ["month", "day", "both"]:
                        print("\nSeems you typed it incorrectly! So...")
                        continue
                    f = True
                if ans == "both":
                    if m != True:
                        # get user input for month (all, january, february, ... , june)
                        month = input("Which month? Choose from ('January', 'February', 'March', 'April', 'May', 'June')\n").strip().title()
                        if month not in months:
                            print("\nSeems you typed it incorrectly! So...")
                            continue    
                        m = True
                    if d != True:     
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        day = input("Which day? please type the weekday name (e.g. sunday)\n").strip().title()
                        if day not in weekdays:
                            print("\nSeems you typed it incorrectly! So...")
                            continue
                        d = True
                elif ans == "month":
                    if m != True:
                        # get user input for month (all, january, february, ... , june)
                        month = input("Which month? Choose from ('January', 'February', 'March', 'April', 'May', 'June')\n").strip().title()
                        if month not in months:
                            print("\nSeems you typed it incorrectly! So...")
                            continue    
                        m, d, day = True, True, "all"
                elif ans == "day":
                    if d != True:     
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        day = input("Which day? please type the weekday name (e.g. sunday)\n").strip().title()
                        if day not in weekdays:
                            print("\nSeems you typed it incorrectly! So...")
                            continue
                        d, m, month = True, True, "all"
                if f == m == d == True:
                    break
            break
        # if the user didn't want to filter the data, it wil be returned as it is(not filtered).
        elif filter == "no":
            month, day = "all", "all"
            break
        else: break        
    print("\nloading the data...")
    print('-'*40)
    return city, month, day, ans


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df, cond):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if cond != "both":
        # display the most common month
        if (cond == None) or (cond == "month"):
            com_month = df["month"].mode()[0]
            print("Most common month:", com_month)
        
        # display the most common day of week
        if (cond == None) or (cond == "day"):
            com_day = df["day_of_week"].mode()[0]
            print("Most common day of week:", com_day)
        
    # display the most common start hour
    com_hour = df["Start Time"].dt.hour.mode()[0]
    print("Most common start hour:", com_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df["Start Station"].mode()[0]
    print("Most commonly used start station:", start)

    # display most commonly used end station
    last = df["End Station"].mode()[0]
    print("Most commonly used end station:", last)

    # display most frequent combination of start station and end station trip
    comb = df.groupby(["Start Station", "End Station"]).size().max()
    print("MFC for both the start and the end:", comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    t_time = df["Trip Duration"].sum()
    print("Total travel time:", t_time)

    # display mean travel time
    avg_time = df["Trip Duration"].mean()
    print("The average duration:", avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    u_types = df["User Type"].value_counts().index.tolist()

    for x in u_types:
        value = df["User Type"].value_counts()[u_types.index(x)]
        print(x + ":", value)
    

    if city in ["Chicago", "New York"]:
        print('*'*20)
        # Display counts of gender
        g_types = df["Gender"].value_counts().index.tolist()

        for x in g_types:
            value = df["Gender"].value_counts()[g_types.index(x)]
            print(x + ":", value)
        print('*'*20)

        # Display earliest, most recent, and most common year of birth
        print("The most earliest year of birth:", int(df["Birth Year"].min()))
        print("The most recent year of birth:", int(df["Birth Year"].max()))
        print("The most common year of birth", int(df["Birth Year"].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    restart = None
    while True:
        city, month, day, cond = get_filters(restart)
        df = load_data(city, month, day)
        
        time_stats(df, cond)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        start = 0
   
        while True:
            if start == 0:
                show = input("Would you like to see 5 lines of raw data? Enter yes or no\n").strip().lower()
            else:
                show = input("Would you like to see another 5 lines of raw data? Enter yes or no\n").strip().lower()
            if show == "yes":
                end = start + 5 
                print(df[start:end])
                start = end
            elif show == "no":
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
