import requests
import csv

def download_earthquake_data_csv_using_api(station_name):
    api_url = "https://arc.indiawris.gov.in/server/rest/services/NWIC/Extreme_Temp_RF/MapServer/1/query"
    params = {
        "f": "json",
        "outFields": "*",
        "spatialRel": "esriSpatialRelIntersects",
        "where": f"station_name = '{station_name}'"
    }

    try:
        # Send a GET request to the API
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        # Get the JSON data
        data = response.json()

        # Check if the response contains features
        if "features" in data:
            features = data["features"]
            if len(features) > 0:
                # Create and save the CSV file
                output_file = f"{station_name.lower().replace(' ', '_')}.csv"
                with open(output_file, "w", newline="") as csvfile:
                    # Manually write the column headers to the CSV file
                    fieldnames = features[0]["attributes"].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    # Write the data rows to the CSV file
                    for feature in features:
                        writer.writerow(feature["attributes"])

                print(f"CSV file downloaded and saved as {output_file}")
            else:
                print(f"No data found for station '{station_name}'.")
        else:
            print("Unexpected response format from the API.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    station_name = "Ahmedabad"  # Replace "Ahmedabad" with the desired station_name
    # Download earthquake data as a CSV file using the API
    download_earthquake_data_csv_using_api(station_name)
