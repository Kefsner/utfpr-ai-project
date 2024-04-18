import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from os import path, makedirs

class Report:
    def __init__(self, df):
        self.df = df
        self.compute_statistics()  # Compute statistics immediately on initialization

    def compute_statistics(self):
        """Compute statistical measures for the experiments."""
        self.summary = self.df.groupby('algorithm').agg({
            'elapsed_time': ['mean', 'std', 'min', 'max'],
            'steps': ['mean', 'std', 'min', 'max'],
            'total_cost': ['mean', 'std', 'min', 'max']
        })
        self.summary.columns = ['_'.join(col).strip() for col in self.summary.columns.values]  # Flatten MultiIndex columns

    def plot_results(self):
        """Generate plots to visualize the results."""
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 6))
        
        # Plotting elapsed time
        self.df.boxplot(column='elapsed_time', by='algorithm', ax=axes[0])
        axes[0].set_title('Elapsed Time by Algorithm')
        axes[0].set_ylabel('Time (seconds)')
        
        # Plotting steps
        self.df.boxplot(column='steps', by='algorithm', ax=axes[1])
        axes[1].set_title('Steps by Algorithm')
        axes[1].set_ylabel('Steps')

        # Plotting total cost
        self.df.boxplot(column='total_cost', by='algorithm', ax=axes[2])
        axes[2].set_title('Total Cost by Algorithm')
        axes[2].set_ylabel('Cost')
        
        plt.suptitle('')  # Suppress the default title to tidy up the plots
        plt.tight_layout()
        plt.show()
    
    def save(self, directory='reports'):
        """Save the computed statistics and plots to files."""
        if not path.exists(directory):
            makedirs(directory)
        
        # Save the summary statistics to a CSV
        self.summary.to_csv(path.join(directory, 'report_summary.csv'))
        
        # Optionally, save plots as images or PDF
        self.plot_results()  # Ensure plots are generated
        plt.savefig(path.join(directory, 'report_plots.pdf'))  # Save the last plotted figure
        
        print(f"Report saved to {directory}")
