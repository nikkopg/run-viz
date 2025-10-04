from src.activity_handler.fetcher import ActivityFetcher
from src.visualizer.visualizer import Visualizer
from src.common.utils import load_json
from src.common.logger import Logger

def main():
    client = load_json(".local/strava-client.json")

    logger = Logger()
    fetcher = ActivityFetcher(client['id'], client['secret'], logger)
    activity_data = fetcher.get_n_activities(10, save=True)
    
    vis = Visualizer(logger)
    for activity in activity_data:
        vis.visualize(activity)


if __name__ == "__main__":
    main()