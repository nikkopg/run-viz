from src.activity_handler.fetcher import ActivityFetcher
from src.visualizer.visualizer import Visualizer
from src.common.utils import load_json, save_json

def main():
    client = load_json(".local/strava-client.json")

    fetcher = ActivityFetcher(client['id'], client['secret'])
    activities = fetcher.fetch_activities(per_page=10, max_pages=2)
    print(f"Fetched {len(activities)} activities:")

    activity_data = []
    for act in activities:
        print(f"- {act['name']} on {act['start_date']} ({act['distance']/1000:.2f} km)")
        if act['type'] == 'Run':
            details = fetcher.fetch_activity_details(act['id'], streams=True)

            # merge summary + details
            activity_data.append({
                "summary": act,
                "details": details
            })

    save_json(activity_data, "output/activities.json")

    vis = Visualizer()
    for activity in activity_data:
        vis.visualize(activity)


if __name__ == "__main__":
    main()