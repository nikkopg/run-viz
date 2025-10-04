import argparse
from src.activity_handler.fetcher import ActivityFetcher
from src.visualizer.visualizer import Visualizer
from src.common.utils import load_json
from src.common.logger import Logger

def main():
    parser = argparse.ArgumentParser(description="Run activities visualizer.")
    parser.add_argument("-i", "--id", help="Strava API Client ID.", required=True)
    parser.add_argument("-s", "--secret", help="Strava API Client Secret", required=True)
    parser.add_argument("-n", "--n_activities", default=10, help="Total running activities to visualize. Default is 10.")

    args = parser.parse_args()

    if args.id and args.secret:
        logger = Logger()
        fetcher = ActivityFetcher(args.id, args.secret, logger)
        activity_data = fetcher.get_n_activities(args.n_activities, save=True)
        
        vis = Visualizer(logger)
        for activity in activity_data:
            vis.visualize(activity)


if __name__ == "__main__":
    main()