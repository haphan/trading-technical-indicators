"""
Trading-Technical-Indicators (tti) python library

File name: plot.py
    Plotting methods defined under the tti.utils package.
"""

import matplotlib.pyplot as plt


def linesGraph(data, y_label, title, lines_color, alpha_values, areas,
               x_label='Date'):
    """
    Returns a lines graph of type matplotlib.pyplot. The graph can be either
    a figure with a single plot, or a figure containing two vertical subplots.
    
    Parameters:
        data (pandas.DataFrame or a list of maximum two pandas.DataFrame
            objects): The data to include in the graph. If data is a single
            pandas.DataFrame then a single plot is prepared. If data is a list
            of two pandas.DataFrame, then a plot with two subplots vertically
            stacked is prepared. Each pandas.DataFrame in the list is used for
            a separate subplot. The index of the dataframe represents the data
            on the x-axis and it should be of type pandas.DatetimeIndex. Each
            column of the dataframe represents a line in the graph.
            
        y_label (string): The label of the y-axis of the graph.

        title (string): The title on the top of the graph.

        lines_color (list of matplotlib.colors): The colors to be used for
            each line of the graph, in the defined order. In case where the 
            lines are more than the colors, then the list is scanned again from 
            the zero index.
        
        alpha_values (list of floats): Alpha value of each line, to be used in 
            the call of the matplotlib.pyplot.plot method. In case where the 
            lines are more than the members of the list, then the list is 
            scanned again from the zero index.
            
        areas (list of dictionaries): Includes the areas to be plotted by using
            the fill_between matplotlib method. Each member of the list should
            be a dictionary with the below keys:
            {'x':, 'y1':, 'y2':, 'color':}, see fill_between matplotlib method
            for more details.

        x_label (string): The label of the x-axis of the graph. Default value
            is `Date`.
        
    Raises:
        -

    Returns:
        matplotlib.pyplot: The prepared graph object.
    """

    # For handling a list as input always
    if type(data) != list:
        data = [data]

    plt.figure(figsize=(7, 5))
    
    # Add the subplots
    j = 0  # Used for plot attributes use in rotation

    # Maximum of two DataFrames are considered from the data parameter
    for i in range(2):
        plt.subplot(min(2, len(data)), 1, i + 1)

        for line_name in data[i].columns.values:
            plt.plot(data[i].index, data[i][line_name], label=line_name,
                     color=lines_color[j % len(lines_color)],
                     alpha=alpha_values[j % len(alpha_values)])

            j += 1

        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)

        # Set attributes for each subplot depending its position      
        if i == 0:
            plt.title(title, fontsize=11, fontweight='bold')
            if len(data) > 1:
                plt.gca().axes.get_xaxis().set_visible(False)
    
    # Last subplot x-axis
    plt.xlabel(x_label, fontsize=11, fontweight='bold')
    plt.gcf().autofmt_xdate()    
    
    # Common y-axis label
    plt.gcf().text(0.04, 0.5, y_label, fontsize=11, fontweight='bold',
                   va='center', rotation='vertical')
    
    # Plot areas
    if areas is not None:
        for a in areas:
            plt.gca().fill_between(x=a['x'], y1=a['y1'], y2=a['y2'],
                                   color=a['color'])

    return plt