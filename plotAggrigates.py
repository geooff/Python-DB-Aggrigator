import sys
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def correlation(df):

	# Filter out irrelivant columns
	df_corr = df[['Time On Page (minutes) for Page Planning', 'Time On Page (minutes) for Page Store Overview', 'Time On Page (minutes) for Page Tags', 'Time On Page (minutes) for Page Retailers', 'Time On Page (minutes) for Page Report Page', 'Time On Page (minutes) for Page Calendars', 'Time On Page (minutes) for Page Data Export', 'Time On Page (minutes) for Page Territories', 'Time On Page (minutes) for Page Reports', 'Time On Page (minutes) for Page Edit Report Page', 'Time On Page (minutes) for Page Dashboard', 'Time On Page (minutes) for Page Product Settings', 'Time On Page (minutes) for Page Trends', 'Time On Page (minutes) for Page Store Details', 'Yoy']]

	# Convert total time on page to percernt total
	for col in df_corr:
		if "Time On Page" in col:
			df_corr[col] = df_corr[col] / df["Time on Site (minutes)"]
			nameToKeep = col.split("Time On Page (minutes) for ")
			df_corr.rename(columns={col: "Percent useage for page "+nameToKeep[1]}, inplace=True)

	# Compute the correlation matrix
	corr = df_corr.corr()

	# Generate a mask for the upper triangle
	mask = np.zeros_like(corr, dtype=np.bool)
	mask[np.triu_indices_from(mask)] = True

	# Set up the matplotlib figure
	f, ax = plt.subplots(figsize=(11, 9))

	# Generate a custom diverging colormap
	cmap = sns.diverging_palette(220, 10, as_cmap=True)

	# Draw the heatmap with the mask and correct aspect ratio
	sns.heatmap(corr, mask=mask, cmap=cmap, square=True, linewidths=.5)

	plt.show()

def regression(df):

	x = "Events"
	y = "Yoy"

	sns.set(color_codes=True)
	plot = sns.regplot(x=x, y=y, data=df)

	# Add annotations one by one with a loop
	for line in range(0,df.shape[0]):
		plot.text(df.x[line]+0.2, df.y[line], df.group['name'][line], horizontalalignment='left', size='medium', color='black', weight='semibold')

	# Show Plot
	plt.show()


def plot(csv_filename):

	# Import Data from saved csv
	df = pd.read_csv(csv_filename, index_col=0)

	# Remove bad rows from csv
	df = df[df['Yoy'] != 1.0]
	df = df[df['Yoy'] != 0.0]

	regression(df)

if __name__ == "__main__":
  
	#Take client and set parameters
	csv_filename = sys.argv[1]
	plot(csv_filename)