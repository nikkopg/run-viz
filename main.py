from src.activity_handler.fetcher import ActivityFetcher


def main():
    fetcher = ActivityFetcher()
    activities = fetcher.fetch_activities(per_page=30, max_pages=2)
    print(f"Fetched {len(activities)} activities:")
    for act in activities:
        print(f"- {act['name']} on {act['start_date']} ({act['distance']/1000:.2f} km)")


# === MAIN ===
if __name__ == "__main__":
    main()