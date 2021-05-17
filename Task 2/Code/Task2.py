import pandas as pd
import sys

# Command line argument(filename)
file_name = sys.argv[1]
df = pd.read_csv(file_name)

# Creating a dictionary to store the respective toppers
Topper={}

# Using HeapSort to find the topperin each subject
Topper['Maths'] = df.sort_values(by=['Maths'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']
Topper['Biology'] = df.sort_values(by=['Biology'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']
Topper['English'] = df.sort_values(by=['English'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']
Topper['Physics'] = df.sort_values(by=['Physics'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']
Topper['Chemistry'] = df.sort_values(by=['Chemistry'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']
Topper['Hindi'] = df.sort_values(by=['Hindi'],ascending=False, kind='Heapsort',na_position='last').iloc[0]['Name']

# Finding Total Marks
df['Total']=df.sum(axis=1)

# Finding the top 3 students and storing them as a list within the dictionary
Topper['Total'] = df.sort_values(by=['Total'],ascending=False, kind='Heapsort',na_position='last').iloc[0:3]['Name'].tolist()

# Printing the Details
print("Topper in Maths is: " +Topper['Maths'])
print("Topper in Biology is: " +Topper['Biology'])
print("Topper in English is: " +Topper['English'])
print("Topper in Physics is: " +Topper['Physics'])
print("Topper in Chemistry is: " +Topper['Chemistry'])
print("Topper in Hindi is: " +Topper['Hindi'])
print("Best students in the class are ",Topper['Total'][0],",", Topper['Total'][1],",", Topper['Total'][2] )

# The Time Complexity is O(nlogn)
# I choose heapsort as the time complexity remains the same for best case, average case and worst case scenarios(other searching algorithms like merge and quick sort can also be used)
