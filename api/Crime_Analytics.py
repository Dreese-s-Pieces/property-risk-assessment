import pandas as pd
import requests

url1 = 'https://api.usa.gov/crime/fbi/sapi/api/nibrs/'
url2 = '/offender/regions/'
url3 = '/age?'
regions = ['Northeast', 'South', 'West', 'Midwest']
offenses = ['aggravated-assault', 'burglary', 'larceny', 'motor-vehicle-theft', 'homicide', 'rape', 'robbery', 'arson',
            'violent-crime', 'property-crime']


class Crime_Stats():

    def __init__(self):
        pass

    def get_region_offense_number(self, region, offense):
        response = requests.get(url1 + region + url2 + offense + url3 +
                                'API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv')
        df = pd.DataFrame.from_dict(response.json()["data"])
        total = df['value'].sum()
        return total

    def get_national_offense_number(self, offense):
        total = 0
        for region in regions:
            total += self.get_region_offense_number(self, region, offense)
        return total

    def get_region_offense_proportion(self, region, offense):
        return self.get_region_offense_numbers(self, region, offense) / self.get_region_offense_array(self,
                                                                                                      region).sum()

    def get_region_offense_array(self, region):
        offenseNums = []
        for i in range(0, len(offenses)):
            offenseNums[i] = self.get_region_offense_numbers(region, offenses[i])

    def get_region_top_three_offense_proportions(self, region):
        offenseNums = self.get_region_offense_numbers()
        firstIndex, secondIndex, thirdIndex = 0, 0, 0
        for i in range(0, len(offenseNums)):
            if offenseNums[i] > offenseNums[firstIndex]:
                firstIndex = i
            elif offenseNums[i] > offenseNums[secondIndex]:
                secondIndex = i
            elif offenseNums[i] > offenseNums[thirdIndex]:
                thirdIndex = i

        topOffenseProps, firstProp, secondProp, thirdProp = [], [], [], []
        firstProp[0] = offenses[firstIndex]
        firstProp[1] = self.get_region_offense_proportion(self, region, offenses[firstIndex])
        firstProp[2] = self.get_region_offense_number(self, region, offenses[firstIndex]) / \
                       self.get_national_offense_number(self, offenses[firstIndex])
        secondProp[0] = offenses[secondIndex]
        secondProp[1] = self.get_region_offense_proportion(self, region, offenses[secondIndex])
        secondProp[2] = self.get_region_offense_number(self, region, offenses[secondIndex]) / \
                        self.get_national_offense_number(self, offenses[secondIndex])
        thirdProp[0] = offenses[thirdIndex]
        thirdProp[1] = self.get_region_offense_proportion(self, region, offenses[thirdIndex])
        thirdProp[2] = self.get_region_offense_number(self, region, offenses[thirdIndex]) / \
                       self.get_national_offense_number(self, offenses[thirdIndex])
        topOffenseProps[0] = firstProp
        topOffenseProps[1] = secondProp
        topOffenseProps[2] = thirdProp
        return topOffenseProps
