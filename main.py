from src.activity_handler.fetcher import ActivityFetcher
from src.common.utils import load_json

def main():
    client = load_json(".local/strava-client.json")

    fetcher = ActivityFetcher(client['id'], client['secret'])
    activities = fetcher.fetch_activities(per_page=10, max_pages=2)
    print(f"Fetched {len(activities)} activities:")
    for act in activities:
        print(f"- {act['name']} on {act['start_date']} ({act['distance']/1000:.2f} km)")
        if act['type'] == 'Run':
            details = fetcher.fetch_activity_details(act['id'])
            for i, split in enumerate(details["splits_metric"], 1):
                print(f"  Split {i}: {split['distance']} m in {split['moving_time']} sec; pace: {(split['moving_time']/60)/(split['distance']/1000):.2f} min/km")

# === MAIN ===
if __name__ == "__main__":
    main()