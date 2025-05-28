import csv
import numpy as np
import matplotlib.pyplot as plt

class InvestmentAnalyzer:
    """
    A class for analyzing investment data and finding optimal parameters.
    
    This class loads data from a CSV file and provides methods to calculate
    expected values and find optimal investment parameters.
    """
    
    def __init__(self, file_path, stop_loss=0.3, with_scam=False):
        """
        Initialize the InvestmentAnalyzer with data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file containing investment data
            stop_loss (float, optional): Default stop loss value. Defaults to 0.3.
        """
        self.file_path = file_path
        self.stop_loss = stop_loss
        self.data = self.load_csv_data(file_path)
        self.with_scam = with_scam
    
    def load_csv_data(self, file_path):
        """
        Load data from a CSV file, extracting the third element from each row.
        
        Args:
            file_path (str): Path to the CSV file to load
            
        Returns:
            list: List of integer values extracted from the third column
        """
        data = []
        with open(file_path, 'r', encoding='latin-1') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                # Get the third element (index 2) from each row
                try:
                    value = int(row[2])  # Convert the third element to integer
                    scam = str(row[17]) == "True"  # Convert the fourth element to boolean
                    data.append((value, scam))
                except (ValueError, IndexError):
                    # Skip headers or invalid rows
                    continue
        return data
    
    def expected_value(self, stop_loss=0.0, multiplier=1.0, rate=0.5):
        """
        Calculate the expected value based on stop loss, multiplier and success rate.
        
        Args:
            stop_loss (float, optional): Loss value in case of failure. Defaults to 0.0.
            multiplier (float, optional): Gain multiplier in case of success. Defaults to 1.0.
            rate (float, optional): Success rate. Defaults to 0.5.
            
        Returns:
            float: The calculated expected value
        """
        return rate * multiplier + (1 - rate) * stop_loss
    
    def find_rate(self, x, y):
        """
        Calculate the ratio of values above y to values above x in the dataset.
        
        Args:
            x (int): Lower threshold value
            y (int): Upper threshold value
            
        Returns:
            float: Ratio of values above y to values above x
            int: Count of values above x
            int: Count of values above y
        """
        x_count = 0
        y_count = 0
        if self.with_scam:
            for row, scam in self.data:
                if row > x:  # Only consider non-scam entries
                    x_count += 1
                if row > y:  # Only consider non-scam entries
                    y_count += 1
        else:
            for row, scam in self.data:
                if row > x and not scam:  # Only consider non-scam entries
                    x_count += 1
                if row > y and not scam:  # Only consider non-scam entries
                    y_count += 1
        return y_count / x_count if x_count > 0 else 0, x_count, y_count
    
    def find_value(self, x, y):
        """
        Calculate the expected value for given thresholds x and y.
        
        Args:
            x (int): Lower threshold value
            y (int): Upper threshold value
            
        Returns:
            float: Expected value for the given parameters
            int: Count of values above x
            int: Count of values above y
        """
        rate, x_count, y_count = self.find_rate(x, y)
        return self.expected_value(stop_loss=self.stop_loss, multiplier=y/x, rate=rate), x_count, y_count
    
    def find_optimal_parameters(self, x_range=(20000, 1000000), y_range=(20000, 1000000), step=10000, visualize=False):
        """
        Find optimal x and y parameters that maximize the expected value.
        
        Args:
            x_range (tuple, optional): Range for x values as (min, max). Defaults to (20000, 1000000).
            y_range (tuple, optional): Range for y values as (min, max). Defaults to (20000, 1000000).
            step (int, optional): Step size for iterations. Defaults to 10000.
            visualize (bool, optional): Whether to generate visualization. Defaults to False.
            
        Returns:
            tuple: Optimal parameters as (x, y, value)
        """
        max_value = [0, 0, 0]  # [x, y, value]
        
        # Store all values for visualization
        all_values = []
        
        for x in range(x_range[0], x_range[1] + 1, step):
            for y in range(x + step, y_range[1] + 1, step):
                value, x_count, y_count = self.find_value(x, y)
                all_values.append((x, y, value))
                if value > max_value[2]:
                    max_value = [x, y, value, x_count, y_count]
        
        # Generate visualization if requested
        if visualize:
            self.visualize_results(all_values)
            
        return tuple(max_value)
    
    def visualize_results(self, values):
        """
        Generate visualizations for the expected values across different parameter pairs.
        
        Args:
            values (list): List of tuples (x, y, value) containing parameter pairs and their expected values
        """
        x_vals = [v[0] for v in values]
        y_vals = [v[1] for v in values]
        z_vals = [v[2] for v in values]
        
        # 1. 3D Surface plot
        fig = plt.figure(figsize=(15, 10))
        
        # 3D scatter plot
        ax1 = fig.add_subplot(121, projection='3d')
        scatter = ax1.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='viridis')
        ax1.set_xlabel('X parameter')
        ax1.set_ylabel('Y parameter')
        ax1.set_zlabel('Expected value')
        ax1.set_title('3D view of expected values')
        fig.colorbar(scatter, ax=ax1, label='Expected value')
        
        # 2D heatmap for clearer visualization
        # We need to convert our irregular points to a grid
        # Create a grid of x and y values
        x_unique = sorted(list(set(x_vals)))
        y_unique = sorted(list(set(y_vals)))
        
        # Create a 2D array to hold the expected values
        z_grid = np.zeros((len(y_unique), len(x_unique)))
        
        # Fill the array with our values
        for x, y, z in values:
            i = x_unique.index(x)
            j = y_unique.index(y)
            z_grid[j, i] = z
        
        # Create a heatmap
        ax2 = fig.add_subplot(122)
        heatmap = ax2.imshow(z_grid, cmap='viridis', origin='lower', 
                            extent=[min(x_unique), max(x_unique), min(y_unique), max(y_unique)])
        
        ax2.set_xlabel('X parameter')
        ax2.set_ylabel('Y parameter')
        ax2.set_title('Heatmap of expected values')
        fig.colorbar(heatmap, ax=ax2, label='Expected value')
        
        plt.tight_layout()
        plt.savefig('investment_analysis.png')
        plt.show()


# Example usage
if __name__ == "__main__":
    # Create an instance of InvestmentAnalyzer
    analyzer = InvestmentAnalyzer('test.csv', with_scam=False, stop_loss=0.3)

    # Find optimal parameters with visualization
    optimal_x, optimal_y, optimal_value, x_count, y_count = analyzer.find_optimal_parameters(
        x_range=(20000, 1000000), 
        y_range=(20000, 1000000), 
        step=10000,
        visualize=True
    )
    
    # Print results
    print(f"Max value found: x={optimal_x}, y={optimal_y}, value={optimal_value}, x_count={x_count}, y_count={y_count}")