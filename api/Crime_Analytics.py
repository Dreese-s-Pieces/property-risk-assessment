import pandas as pd
import requests

url1 = 'https://api.usa.gov/crime/fbi/sapi/api/nibrs/'
url2 = '/offender/regions/'
url3 = '/age?'
regions = ['Northeast', 'South', 'West', 'Midwest']
offenses = ['aggravated-assault', 'burglary', 'larceny', 'motor-vehicle-theft', 'homicide', 'rape', 'robbery', 'arson',
            'violent-crime', 'property-crime']
display_offenses = {'aggravated-assault': 'Aggravated Assault',
                    'burglary': 'Burglary', 
                    'larceny': 'Larceny', 
                    'motor-vehicle-theft': 'Motor Vehicle Theft', 
                    'homicide': 'Homicide', 
                    'rape': 'Rape', 
                    'robbery': 'Robbery', 
                    'arson': 'Arson',
                    'violent-crime': 'Violent Crime', 
                    'property-crime': 'Property Crime'
                    }


class Crime_Stats():

    def __init__(self):
        pass

    def get_region_offense_number(self, region, offense):
        response = requests.get(url1 + offense + url2 + region + url3 +
                                'API_KEY=ZqUc5hUFA4vvHzkj1H0x5Ln10sNnDG2nPIIeAhYO').json()
        df = pd.DataFrame.from_dict(response["data"])
        total = df['value'].sum()
        return total

    def get_national_offense_number(self, offense):
        total = 0
        for region in regions:
            total += self.get_region_offense_number(region, offense)
        return total

    def get_region_offense_proportion(self, region, offense):
        return self.get_region_offense_number(region, offense) / sum(self.get_region_offense_array(region))

    def get_region_offense_array(self, region):
        offenseNums = [0] * len(offenses)
        for i in range(0, len(offenses)):
            offenseNums[i] = self.get_region_offense_number(region, offenses[i])

        return offenseNums

    def get_region_top_three_offense_proportions(self, region):
        offenseNums = self.get_region_offense_array(region)
        firstIndex, secondIndex, thirdIndex = 0, 0, 0
        for i in range(0, len(offenseNums)):
            if offenseNums[i] > offenseNums[firstIndex]:
                firstIndex = i
            elif offenseNums[i] > offenseNums[secondIndex]:
                secondIndex = i
            elif offenseNums[i] > offenseNums[thirdIndex]:
                thirdIndex = i

        topOffenseProps, firstProp, secondProp, thirdProp = [0] * 3, [0] * 3, [0] * 3, [0] * 3
        
        firstProp[0] = display_offenses[offenses[firstIndex]]
        firstProp[1] = (self.get_region_offense_proportion(region, offenses[firstIndex])) * 100
        firstProp[2] = (self.get_region_offense_number(region, offenses[firstIndex]) / self.get_national_offense_number(offenses[firstIndex])) * 100
       
        secondProp[0] = display_offenses[offenses[secondIndex]]
        secondProp[1] = (self.get_region_offense_proportion(region, offenses[secondIndex])) * 100
        secondProp[2] = (self.get_region_offense_number(region, offenses[secondIndex]) / self.get_national_offense_number(offenses[secondIndex])) * 100
       
        thirdProp[0] = display_offenses[offenses[thirdIndex]]
        thirdProp[1] = (self.get_region_offense_proportion(region, offenses[thirdIndex])) * 100
        thirdProp[2] = (self.get_region_offense_number(region, offenses[thirdIndex]) / self.get_national_offense_number(offenses[thirdIndex])) * 100
        
        topOffenseProps[0] = firstProp
        topOffenseProps[1] = secondProp
        topOffenseProps[2] = thirdProp

        return topOffenseProps
