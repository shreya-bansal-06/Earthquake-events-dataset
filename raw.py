import requests

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
                # Extract field names from the first feature
                fields = list(features[0]["attributes"].keys())

                # Create and write the CSV file
                output_file = f"{station_name.lower().replace(' ', '_')}.csv"
                with open(output_file, "w", newline="") as csvfile:
                    csvfile.write(",".join(fields) + "\n")
                    for feature in features:
                        attributes = feature["attributes"]
                        row_data = [str(attributes[field]) for field in fields]
                        csvfile.write(",".join(row_data) + "\n")

                print(f"CSV file downloaded and saved as {output_file}")
            else:
                print(f"No data found for station '{station_name}'.")
        else:
            print("Unexpected response format from the API.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    station_name = "Keshod (A)"  # Replace "Ahmedabad" with the desired station_name
    # Download earthquake data as a CSV file using the API
    download_earthquake_data_csv_using_api(station_name)
