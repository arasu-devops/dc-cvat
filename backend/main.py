import os
import csv
import json

def parse_json_to_csv(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Simplified CSV logic: extract image names and annotation counts
    items = data.get('items', [])
    csv_path = json_path.replace('.json', '.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image Name', 'Annotation Count'])
        for item in items:
            writer.writerow([item.get('name'), len(item.get('annotations', []))])

    # Simplified analysis
    analysis_data = {
        'total_images': len(items),
        'total_annotations': sum(len(item.get('annotations', [])) for item in items)
    }

    return csv_path, analysis_data
