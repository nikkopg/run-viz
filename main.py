from src.activity_handler.fetcher import ActivityFetcher
from src.visualizer.visualizer import Visualizer
from src.common.utils import load_json, save_json
from src.common.logger import Logger

def main():
    client = load_json(".local/strava-client.json")

    logger = Logger()
    fetcher = ActivityFetcher(client['id'], client['secret'], logger)
    activities = fetcher.fetch_activities(per_page=10, max_pages=2)
    logger.logger.info(f"Fetched {len(activities)} activities:")

    activity_data = []
    for act in activities:
        logger.logger.info(f"- {act['name']} on {act['start_date']} ({act['distance']/1000:.2f} km)")
        if act['type'] == 'Run':
            details = fetcher.fetch_activity_details(act['id'], streams=True)

            # merge summary + details
            activity_data.append({
                "summary": act,
                "details": details
            })

    save_json(activity_data, "output/activities.json")

    # activity_data = load_json("output/activities.json")

    vis = Visualizer(logger)
    for activity in activity_data:
        vis.visualize(activity)


if __name__ == "__main__":
    main()