import xml.etree.ElementTree as ET
import pandas as pd

def convert_aqi_xml_to_csv(xml_input, csv_output):
    # Parse the XML file
    tree = ET.parse(xml_input)
    root = tree.getroot()
    
    station_list = []
    
    # Iterate through the hierarchy: State -> City -> Station
    for state in root.findall('.//State'):
        state_id = state.get('id')
        for city in state.findall('City'):
            city_id = city.get('id')
            for station in city.findall('Station'):
                # Extract base station information
                row = {
                    'State': state_id,
                    'City': city_id,
                    'Station_Name': station.get('id'),
                    'Last_Update': station.get('lastupdate'),
                    'Latitude': station.get('latitude'),
                    'Longitude': station.get('longitude')
                }
                
                # Extract Pollutant metrics
                for pollutant in station.findall('Pollutant_Index'):
                    p_id = pollutant.get('id')
                    row[f'{p_id}_Min'] = pollutant.get('Min')
                    row[f'{p_id}_Max'] = pollutant.get('Max')
                    row[f'{p_id}_Avg'] = pollutant.get('Avg')
                
                # Extract overall Air Quality Index (AQI)
                aqi = station.find('Air_Quality_Index')
                if aqi is not None:
                    row['AQI_Value'] = aqi.get('Value')
                    row['Predominant_Parameter'] = aqi.get('Predominant_Parameter')
                else:
                    row['AQI_Value'] = 'NA'
                    row['Predominant_Parameter'] = 'NA'
                    
                station_list.append(row)
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(station_list)
    df.to_csv(csv_output, index=False)
    print(f"Conversion complete! Data saved to {csv_output}")

# Execute the conversion
convert_aqi_xml_to_csv('data_aqi_cpcb.xml', 'aqi_data.csv')
print(pd.read_csv('aqi_data.csv'))