import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt


class Visualizer:
    
    def __init__(self):
        self.details = None
        self.summary = None

    
    def visualize(self, activity):
        self.summary = activity['summary']
        self.details = activity['details']

        distance = self.details['distance']['data']
        distance = [d/1000 for d in distance]

        # Create 3 vertical subplots with a shared x-axis
        fig, (ax1, ax2) = plt.subplots(
            nrows=2,
            sharex=True,
            figsize=(12, 8),
            gridspec_kw={'hspace': 0.1}
        )

        # First subplot: Heart Rate and Power with twin axes
        ax1.plot(distance, self.details['heartrate']['data'], color='tab:red', label='Heart Rate (bpm)')
        ax1.set_ylabel('HR (bpm)', color='tab:red')
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.legend(loc='upper left')
        ax1.set_title(f"{self.summary['name']} ({self.summary['id']})")

        ax1b = ax1.twinx()
        ax1b.plot(distance, self.details['watts']['data'], color='tab:blue', alpha=0.5, label='Power (watts)')
        ax1b.set_ylabel('Power (W)', color='tab:blue')
        ax1b.tick_params(axis='y', labelcolor='tab:blue')
        ax1b.legend(loc='upper right')

        pace = self.calculate_pace()
        ax2.plot(distance[1:], pace, color='tab:green', label='Pace (min/km)')
        # ax2.set_ylim([0, 25])
        ax2.invert_yaxis()
        ax2.set_ylabel('Pace (min/km)', color='tab:green')
        ax2.legend(loc='upper right')

        # Third subplot: Gradient
        ax3 = ax2.twinx()
        ax3.plot(distance, self.details['grade_smooth']['data'], color='tab:purple', alpha=0.5, label='Gradient (%)')
        ax3.set_ylabel('Gradient (%)', color='tab:purple')
        ax3.legend(loc='upper left')

        # Final adjustments
        ax2.set_xlabel('Distance (km)')
        
        # Add ticks
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
        ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))
        ax1.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.8)
        ax1.grid(which='major', linewidth=0.5, alpha=0.8)

        ax2.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
        ax2.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))
        ax2.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.8)
        ax2.grid(which='major', linewidth=0.5, alpha=0.8)

        filename = f"activity_{self.summary['id']}.png"
        plt.savefig(f"output/{filename}", dpi=150, bbox_inches="tight")
        print(f"Plot saved to {filename}")


    def calculate_pace(self):
        time_s = np.array(self.details['time']['data'])       # seconds
        dist_m = np.array(self.details['distance']['data'])   # meters

        # differences
        dt = np.diff(time_s)
        dd = np.diff(dist_m)

        # stricter filter for movement
        mask = (dt > 0) & (dd > 1.0)   # must move at least 1 m

        # instantaneous pace (min/km)
        pace = np.full_like(dt, np.nan, dtype=float)
        pace[mask] = (1000 * dt[mask]) / (60 * dd[mask])  # min/km
        pace = np.clip(pace, 2.5, 20.0)

        # smooth while keeping NaNs
        window = 10
        kernel = np.ones(window) / window

        # use nan-safe convolution
        valid = np.where(np.isnan(pace), 0, pace)
        weights = np.where(np.isnan(pace), 0, 1)

        pace_smooth = np.divide(
            np.convolve(valid, kernel, mode="same"),
            np.convolve(weights, kernel, mode="same"),
            out=np.full_like(valid, np.nan, dtype=float),
            where=np.convolve(weights, kernel, mode="same") != 0
        )

        return pace_smooth