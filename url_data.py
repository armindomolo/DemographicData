urls = {
    "world_bank": {
        "spending_gov": "https://api.worldbank.org/v2/country/all/indicator/GC.XPN.TOTL.GD.ZS?format=json&per_page=500",
        "gdp": "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=500",
        "population": "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=500",
        "gdp_per_capita": "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&per_page=500",
        "gdp_per_capita_growth": "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD.ZG?format=json&per_page=500",
        "education_expenditure": "https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TOTL.GD.ZS?format=json&per_page=500",
        "child_mortality": "https://api.worldbank.org/v2/country/all/indicator/SH.DYN.MORT?format=json&per_page=500",
        "infant_mortality": "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.IMRT.IN?format=json&per_page=500",
        "life_expectancy": "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=500",
        "quality_of_education": "https://api.worldbank.org/v2/country/all/indicator/SE.PRM.CMPT.ZS?format=json&per_page=500",
        "military_expenditure": "https://api.worldbank.org/v2/country/all/indicator/MS.MIL.XPND.GD.ZS?format=json&per_page=500",
        "government_expenditure": "https://api.worldbank.org/v2/country/all/indicator/GC.XPN.TOTL.GD.ZS?format=json&per_page=500",
        "nutrition": "https://api.worldbank.org/v2/country/all/indicator/SH.STA.MALN.ZS?format=json&per_page=500"
    },
    "imf": {
        "gdp": "https://www.imf.org/external/datamapper/api/v1/NGDPD",
        "gdp_per_capita": "https://www.imf.org/external/datamapper/api/v1/NGDPDPC",
        "gdp_per_capita_growth": "https://www.imf.org/external/datamapper/api/v1/NGDPDPCDG",
        "spending_gov": "https://www.imf.org/external/datamapper/api/v1/GCXPNTOTLGDZS",
        "education_expenditure": "https://www.imf.org/external/datamapper/api/v1/SEXPDTOTLGDZS",
        "military_expenditure": "https://www.imf.org/external/datamapper/api/v1/MSMILXPNDGDZS",
        "government_expenditure": "https://www.imf.org/external/datamapper/api/v1/GCXPNTOTLGDZS"
    },
    "unicef": {
        "education_expenditure": "https://data.unicef.org/wp-content/uploads/2023/11/education_expenditure.json",
        "child_mortality": "https://data.unicef.org/wp-content/uploads/2023/11/child_mortality.json",
        "infant_mortality": "https://data.unicef.org/wp-content/uploads/2023/11/infant_mortality.json",
        "life_expectancy": "https://data.unicef.org/wp-content/uploads/2023/11/life_expectancy.json",
        "quality_of_education": "https://data.unicef.org/wp-content/uploads/2023/11/quality_of_education.json",
        "nutrition": "https://data.unicef.org/wp-content/uploads/2023/11/nutricion.json",
        "military_expenditure": "https://data.unicef.org/wp-content/uploads/2023/11/military_expenditure.json",
        "government_expenditure": "https://data.unicef.org/wp-content/uploads/2023/11/government_expenditure.json"
    }
}
# Function to get the URL for a specific indicator and source
def get_url(indicator, source):
    if source in urls and indicator in urls[source]:
        return urls[source][indicator]
    else:
        print(f"URL not found for indicator '{indicator}' and source '{source}'.")
        return None
if __name__ == "__main__":
    def get_url(indicator, source):
        if source in urls and indicator in urls[source]:
            return urls[source][indicator]
        else:
            print(f"URL not found for indicator '{indicator}' and source '{source}'.")
            return None    