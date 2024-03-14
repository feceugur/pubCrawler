import csv

class PlaceSorter:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def _read_csv(self):
        places = []
        with open(self.csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                place_name = row['place_name']
                vader_score = float(row['vader_score'])
                places.append((place_name, vader_score))
        return places

    def sort_places_by_vader_score(self):
        places = self._read_csv()
        sorted_places = sorted(places, key=lambda x: x[1], reverse=True)
        return sorted_places
    
    def group_sorted_places_by_name(self):
        places = self._read_csv()
        grouped_places = {}
        for place, vader_score in places:
            if place not in grouped_places:
                grouped_places[place] = []
            grouped_places[place].append((place, vader_score))
        return grouped_places
    
    def get_group_summary(self):
        grouped_places = self.group_sorted_places_by_name()
        group_summary = []
        for place, data in grouped_places.items():
            group_length = len(data)
            total_score = sum(score for _, score in data)
            group_summary.append((place, group_length, total_score))
        return group_summary