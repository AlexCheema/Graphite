import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paginate query upto 5000 limit.
query = """
query ($skip: Int!) {
  claimTrackers(where: { amount: "400000000000000000000" }, first: 100, skip: $skip) {
    id
    timestamp
  }
}
"""

url = 'https://api.thegraph.com/subgraphs/name/tommyet/graphite-airdrop'

def fetch_claims():
    claims = []
    skip = 0
    max_skip = 5000  # Stop fetching before hitting the maximum skip limit
    while True:
        response = requests.post(url, json={'query': query, 'variables': {'skip': skip}})
        if response.status_code == 200:
            response_json = response.json()
            if 'errors' in response_json:
                print("Error in GraphQL query:", response_json['errors'])
                break
            new_claims = response_json.get('data', {}).get('claimTrackers', [])
            if not new_claims or skip >= max_skip:
                break
            claims.extend(new_claims)
            skip += len(new_claims)
        else:
            print("Failed to fetch data:", response.text)
            break
    return claims

def plot_claims(claims):
    # Convert timestamps to dates
    dates = [datetime.utcfromtimestamp(int(claim['timestamp'])).strftime('%Y-%m-%d') for claim in claims]
    
    # Find the earliest date
    earliest_date = min(dates)
    earliest_datetime = datetime.strptime(earliest_date, '%Y-%m-%d')

    # Filter out claims that are not within the first five days
    filtered_dates = [date for date in dates if datetime.strptime(date, '%Y-%m-%d') < earliest_datetime + timedelta(days=5)]
    
    # Sort dates
    filtered_dates.sort()

    # Count claims per date
    counts = {}
    for date in filtered_dates:
        counts[date] = counts.get(date, 0) + 1

    # Prepare plot data
    dates = list(counts.keys())
    values = list(counts.values())

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Daily number of claims')
    plt.title('Uniswap Airdrop Redemption - First 5 Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    claims = fetch_claims()
    plot_claims(claims)

if __name__ == "__main__":
    main()

