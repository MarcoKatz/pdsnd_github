import time
import pandas as pd
#import numpy as np     # I have eliminated this statement because numpy is not used thru the code
from datetime import timedelta



CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington DC': 'washington.csv' }

def seek_choice(message,option_list,no_choice=False,all_choice=False,fold=True):
  
    """
    Collects 1 choice from a user, from within a list of options
    Uses a numerical identifier for each option
    The user can quit the selection if he/she wants to break the process

    Args:
    -   message (str): the question that is asked to the user
    -   option_list (list): the list (of strings) from which a selection must be made
    -   no_choice (boolean, default False): if True, activates 'None' as a valid choice
    -   all_choice (boolean default False): if True, activates 'All' as a valid choice
    -   fold (boolean, default True): if True, options are presented on different lines,
            If false, options are presented on the same line, separated by comma's
    Returns:
    -   choice (str): the chosen option, 'Quit', or 'None' and/or 'All' if applicable   
        
       
    
    """   

    print("\n" + message)
    
    # Initiate set up of the main message, the queue for the user's reply, and the list of valid choices
    fold_char = ("\n" if fold else ", ")
    option_message = ""
    choice_message = "("
    valid_choices = []
    
    # Build the messages and the list of valid choices 
    for i, option in enumerate(option_list):
        option_message += option + ": " + str(i+1) + fold_char
        choice_message += str(i+1) + ","
        valid_choices.append(str(i+1))
    
    # If None is an option, add this to messages and list of choices
    if no_choice:
        option_message += "None: N" + fold_char
        choice_message += "N,"
        valid_choices.append("N")
    
    # If All is an option, add this to messages and list of choices
    if all_choice:
        option_message += "All: A" + fold_char
        choice_message += "A,"
        valid_choices.append("A")
    
    # Quit is always an option
    option_message += "Quit: Q"
    choice_message += "Q"
    valid_choices.append("Q")
    
    # Print messages and collect input
    print(option_message)
    choice_message = "Your choice"+choice_message +"): "
    while True:
        try:
            choice_index = input(choice_message).title() # Expect a string in return
            if choice_index in valid_choices:
                if choice_index == "Q":
                    choice = 'Quit'
                elif choice_index == "A":
                    choice = 'All'
                elif choice_index == "N":
                    choice = 'None'
                else:
                    choice = option_list[int(choice_index)-1] # Pick up option corresponding to the input
                break
            print("Invalid choice: please re-try")
        except ValueError:
            print("Invalid input: please re-try")
        except KeyboardInterrupt:
            choice = 'Quit'
            break
    return choice





def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
    -   (str) city - name of the city to analyze
    -   (str) month - name of the month to filter by, or 'All' to apply no month filter
    -   (str) day - name of the day of week to filter by, or 'All' to apply no day filter
    """

    # Initialize the logic
    city   = 'Quit'
    filter = 'Quit'
    month  = 'Quit'
    day    = 'Quit'
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while city == 'Quit':  # This loop will only run once
        
        # Get user input for the city (chicago, new york city, washington). None is not allowed.
        # All is not allowed. Present the cities/options on different lines
        city_list = ['Chicago','New York City','Washington DC']
        city_question = "Please select the city you want to see results for:"
        city = seek_choice(city_question,city_list,no_choice=False,all_choice=False,fold=True)
        
        if city == 'Quit':
            break
        else:
            print('-'*40)
    

        
        
        while filter == 'Quit': # This loop will only run once
            # Offer the user a choice for what we should filter by (month, week-day)
            # Allow the option of not filtering at all or filtering by both month and week-daay
            # Present options on 1 line
            filter_list = ['Month','Week-Day']
            filter_question = "Do you want to filter by ... "
            filter = seek_choice(filter_question,filter_list,no_choice=True,all_choice=True,fold=False)          
            if filter == 'Quit':
                break
            else:
                
                if filter == 'None':    # We want to see all months and all week-days / no filtering
                    month ='All'
                    day   ='All'
                                        # We want to filter by Month or by both dimensions   
                elif ((filter == 'All') or (filter == 'Month')):
                                     
                    while month == 'Quit':  # This loop will only run once
                        
                        # Get user input for month (all, january, february, ... , june)
                        # Force 1 choice, None or All is not allowed. Present options on 1 line
                        month_list = ['January','February','March','April','May','June']
                        month_question = "Please select the month you wish to filter by:"
                        month = seek_choice(month_question,month_list,no_choice=False,all_choice=False,fold=False)
                        if month == 'Quit':  
                            break
                        else:
                            print('-'*40)
                else:
                    month = 'All'         # If we have chosen to filter by week-day, then we want all months 
                
                                          # We want to filter by week-day or by both dimensions
                if (((filter == 'All') or (filter == 'Week-Day')) and (month != 'Quit')):
                    while day == 'Quit': # This loop will only run once
                        
                        # Get user input for month (all, january, february, ... , june)
                        # Force 1 choice, None or All is not allowed. Present options on 1 line                        
                        day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                        day_question = "Please select the week-day you wish to filter by:"
                        day=seek_choice(day_question,day_list,no_choice=False,all_choice=False,fold=False)
                        if day == 'Quit':  
                            break
                        else:
                            print('-'*40)
                else:
                    day = 'All'          # If we have chosen to filter by month, then we want all week-days


    return city, month, day



def print_in_tab(title,headers,values):

    """Prints n number of headers and values in tabular format"""
    
    """
    Args:
    -   title(str) : if empty then no title is printed
    -   headers(list of str)
    -   values(list of str)
    """
    
    # If there is a title, then print it
    if len(title) !=0:
        print(' '*5,title)
    
    # Initiate list of table column lengths, and contstruction of the print positioning string
    l_items = []
    pos_var = []
    pos_string = "{:<5}|"

    # If the lists of headers and values contain an unequal number of elements... just do regular print
    num_headers = len(headers)
    num_values  = len(values)    
    if num_headers != num_values:
        print(' '*5,headers)
        print(' '*5,values)
    else:
        # Count 1 vertical bar before each entry, increase length of box by as much
        len_box = num_headers 
     
        for i in range(0,num_headers):
            # Construct a list with the width of each column (give each column 2 extra spaces)
            l_items.append(max(len(headers[i]),len(values[i]))+2)
            # Construct formatting string and grid elements
            pos_var.append("{:<"+str(l_items[i])+"}")
            pos_string += pos_var[i]+"|"
            # Increment total length of box
            len_box += l_items[i]

        # If box is too long to fit on a screen, just do a regular print
        if len_box > 85:
            print(' '*5,headers)
            print(' '*5,values)
        else:
                                                    # Assume an indent of 5
            print(' '*5,'-'*len_box)                # Print the top of the box
            print(pos_string.format(" ",*headers))  # Print the line with the headers 
            print(' '*5,'-'*len_box)                # Print the middle of the box
            print(pos_string.format(" ",*values))   # Print the line with the values 
            print(' '*5,'-'*len_box)                # Print the bottom of the box



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
    -   (str) city - name of the city to analyze
    -   (str) month - name of the month to filter by, or "all" to apply no month filter
    -   (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
    -   df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Read the file
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month from Start Time to create a new column
    df['month'] = df['Start Time'].dt.month_name()
    # Extract day of week from Start Time to create a new column 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    
    if month != 'All':  #Unless you want all months, filter by month                  
        # Filter by month to create the new dataframe
        df = df.loc[(df['month'] == month)]
    if day != 'All':    #Unless you want all days, filter by day of week        
        # Filter by day of week to create the new dataframe
        df = df.loc[(df['day_of_week'] == day)]

    return df


def time_stats(df,city,month,day,time_track=False):
    """Displays statistics on the most frequent times of travel."""

    if time_track:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

    # Initialize for table-print
    print_headers = []
    print_values  = []

    # Search and display the most common month - unless it is pre-selected
    # Add items to the table-print list
    if month == 'All':
        popular_month = df['month'].mode()[0]
        print_headers.append('Most popular month')
        print_values.append(popular_month)
    else:
        print_headers.append('Selected month')
        print_values.append(month)        
 
    # Search and display the most common day of week - unless it is pre-selected   
    # Add items to the table-print list    
    if day == 'All':
        popular_week_day = df['day_of_week'].mode()[0]
        print_headers.append('Most popular day of week')
        print_values.append(popular_week_day)        
    else:
        print_headers.append('Selected day of week')
        print_values.append(day)    


    # Search and display the most common start hour
    # Add items to the table-print list   
    df['Start Time conv']=pd.to_datetime(df['Start Time'])
    df['Start hour']=df['Start Time conv'].dt.hour
    popular_hour = df['Start hour'].mode()[0]
    print_headers.append('Most popular hour')
    print_values.append(str(popular_hour))

    # Now print the table, no title needed as it is self-explanatory
    print_in_tab("",print_headers,print_values)

    if time_track:
        print("\nThis took %s seconds." % (time.time() - start_time))



def station_stats(df,time_track=False):
    """Displays statistics on the most popular stations and trip."""

    if time_track:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        
    # Initialize for table-print
    print_headers = []
    print_values  = []
    
    # Search and display the most commonly used start station
    # Add items to the table-print list
    popular_start_station = df['Start Station'].mode()[0]
    print_headers.append("Most popular start station")
    print_values.append(popular_start_station)
    
    # Search and display the most commonly used end station
    # Add items to the table-print list
    popular_end_station = df['End Station'].mode()[0]
    print_headers.append("Most popular end station")
    print_values.append(popular_end_station)

    # Now print the table, no title needed as it is self-explanatory
    print_in_tab("",print_headers,print_values)

    # Calculte, search and display most frequent combination of start station and end station trip
    df['Trip']=df['Start Station'] + " towards " + df['End Station']   
    popular_trip = df['Trip'].mode()[0]
    
    # Now print the table, no title needed as it is self-explanatory    
    # Note - print_in_tab may print in normal way if the value provided is too long
    print_in_tab("",["Most popular Trip"],[popular_trip])

    if time_track:
        print("\nThis took %s seconds." % (time.time() - start_time))



def trip_duration_stats(df,time_track=False):
    """Displays statistics on the total and average trip duration."""

    if time_track:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()
        
    # Initialize for table-print
    print_headers = []
    print_values  = []

    # Search and display the total number of trips 
    # Add items to the table-print list
    trip_count = df['Trip Duration'].count()
    print_headers.append("Number of trips")
    print_values.append(str(trip_count))

    # Search and display total travel time
    # Add items to the table-print list
    total_travel_time = df['Trip Duration'].sum()
    print_headers.append("Total travel time")
    # Convert total travel time to an day hh mm ss format
    print_values.append(str(timedelta(seconds=int(total_travel_time))))
    
    # Search and display average travel time
    # Add items to the table-print list    
    average_travel_time = df['Trip Duration'].mean()
    print_headers.append("Average travel time")
    # Cconvert average travel time to an day hh mm ss format
    print_values.append(str(timedelta(seconds=int(average_travel_time))))

    # Now print the table, no title needed as it is self-explanatory 
    print_in_tab("",print_headers,print_values)

    if time_track:    
        print("\nThis took %s seconds." % (time.time() - start_time))



def user_stats(df,time_track=False):
    """Displays statistics on bikeshare users."""

    if time_track:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

    # Initialize for table-print
    print_headers=[]
    print_values=[]

    # Search and display counts of user types
    # Add items to the table-print list 
    user_types = df['User Type'].value_counts()
    # Find out how many different types there are (.shape returns it in a tuple)
    num_types=user_types.shape[0]
    if num_types > 4:
        # If more than 4 user types then don't bother displaying this in tab format (may be too long)
        print(user_types)
    else:
        # Extract the index names of user types from the data series
        user_types_indexes = user_types.index
        # Find total number of records... it is a good reference point when looking at user types
        print_headers.append("Total")
        # Beware, as the value_counts of above do not include the NaN's
        user_types_total = user_types.sum()
        # Search for number of NaN in the data, add them to previous total count, to obtain "true" total
        user_types_nan = df['User Type'].isnull().sum()
        print_values.append(str(user_types_total+user_types_nan))

        # Build the table-print columns
        for i in range(0,num_types):
            print_headers.append(user_types_indexes[i])
            print_values.append(str(user_types[i]))
        if user_types_nan > 0:
            print_headers.append("No t-data")
            print_values.append(str(user_types_nan))


    # Test for presence of gender in the data (rather than "assume" it)
    if 'Gender' in df.columns:

        # Search and display counts of gender, beware as value_counts does not include NaN
        # Add items to the table-print list 
        user_gender = df['Gender'].value_counts()
        # Find out how many different genders there are (.shape returns it in a tuple)(should be 2 :))
        num_gender = user_gender.shape[0]
        # Extract the index names of user types from the series
        user_gender_indexes=user_gender.index
        # Search for number of NaN in the data
        gender_nan = df['Gender'].isnull().sum()
        # Build the table-print columns
        for i in range(0,num_gender):
            print_headers.append(user_gender_indexes[i])
            print_values.append(str(user_gender[i]))
        if gender_nan > 0:
            print_headers.append("No g-data")
            print_values.append(str(gender_nan))
            
    # Now print the table, a title is needed to explain what it is             
    print_in_tab("User type and gender (as available) counts",print_headers,print_values)

    #Test for presence of year-of-birth data
    if 'Birth Year' in df.columns:

        # Re-initialize for table-print     
        print_headers = []
        print_values  = []

        
        # Search and display earliest, most recent, and most common year of birth
        # Add items to the table-print list 
        birth_years=df['Birth Year']
        # Eliminate decimal point in the year, it is ugly (convert to int)
        earliest_year=int(birth_years.nsmallest(1).values[0])
        latest_year=int(birth_years.nlargest(1).values[0])
        most_common_year=int(birth_years.mode()[0])
        print_headers.append("Earliest")
        print_headers.append("Latest")
        print_headers.append("Most common")
        print_values.append(str(earliest_year))
        print_values.append(str(latest_year))
        print_values.append(str(most_common_year))
        
        # Now print the table, a title is needed to explain what it is   
        print_in_tab("Years of birth data",print_headers,print_values)

    if time_track:
        print("\nThis took %s seconds." % (time.time() - start_time))


def print_raw_data(df):
    
    """ Displays raw data records in groups of 5 """

  
    seq = 0         # Initiate the 5-record counter  

    # Make sure we can limit the number of blocks to print to the maximum num of records
    trip_count = df['Trip Duration'].count()
    
    while True:
        # Tweak the message so you can differentiate 1st from next passes
        more = "more " * min([seq,1])    
        more_details = input("\nWould you like to see "+more+"raw data ? Enter y(es) or no: ")
        if (more_details.lower() != 'yes' and more_details.lower() != 'y') :
            break
        # Print in batches of 2 or 3 columns
        print(df[['Start Time','End Time','Trip Duration']][seq*5:(seq*5)+4],"\n")
        print(df[['Start Station','End Station']][seq*5:(seq*5)+4],"\n")
        last_print_selection=['User Type']
        # Test for presenced of Gender and Birth Year data before trying to include
        if 'Gender' in df.columns:
            last_print_selection.append('Gender')
        if 'Birth Year' in df.columns:
            last_print_selection.append('Birth Year')
        print(df[last_print_selection][seq*5:(seq*5)+4])

        seq += 1    # Prepare for next block of 5 records
        # Do not continue if you are going over the total number of records
        if ((seq*5)+4) > trip_count:
            break


def main():
    while True:
        # Get the user to tell us what he / she want to see
        city, month, day = get_filters()

        # Validate the selection by printing it
        print_in_tab("Your data",['City','Month','Day of week'],[city,month,day])

        # User can quit at any time
        if (city == 'Quit' or month == 'Quit' or day == 'Quit'):
            break
        
        # Start time counter
        start_time = time.time()

        # Grab the data from the file
        df = load_data(city, month, day)

        # Get and display the 4 types of requested statistics
        time_stats(df,city, month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Print elapsed time
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)        

        # On request of the user, print sets of raw data
        print_raw_data(df)

        # Want another run ?
        restart = input("\nWould you like to restart? Enter y(es) or no: ")
        if (restart.lower() != 'yes' and restart.lower() != 'y') :
            break

        


if __name__ == "__main__":
	main()
