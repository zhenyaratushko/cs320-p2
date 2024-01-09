import json
import zipfile
import csv
from io import TextIOWrapper

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup.keys():
                self.race.add(race_lookup[r])
            
    def __repr__(self):
        return f"Applicant({repr(self.age)}, {list(self.race)})"
    
    def lower_age(self):
        age_in_range = self.age.replace("<", "")
        age_in_range = age_in_range.replace(">", "")
        age_in_range = age_in_range.split("-")
        lower_age = int(age_in_range[0])
        return lower_age
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

class Loan:
    def __init__(self, values):
        if values["loan_amount"] == "NA" or values["loan_amount"] == "Exempt":
            self.loan_amount = -1
        else:
            self.loan_amount = float(values["loan_amount"])
            
        if values["property_value"] == "NA" or values["property_value"] == "Exempt":
            self.property_value = -1
        else:
            self.property_value = float(values["property_value"])
            
        if values["interest_rate"] == "NA" or values["interest_rate"] == "Exempt":
            self.interest_rate = -1
        else:
            self.interest_rate = float(values["interest_rate"])
        
        applicant_list = []
        applicant_age = values["applicant_age"]
        applicant_races = []
        
        for i in range(1, 6):
            if values[f"applicant_race-{i}"] != "":
                applicant_races.append(values[f"applicant_race-{i}"])
                    
        applicant_list.append(Applicant(applicant_age, (applicant_races)))
        self.applicants = applicant_list
        
        if values["co-applicant_age"] != "9999":
            co_applicant_age = values["co-applicant_age"]
            co_applicant_races = []
            for i in range(1, 6):
                if values[f"co-applicant_race-{i}"] != "":
                    co_applicant_races.append(values[f"co-applicant_race-{i}"])

            applicant_list.append(Applicant(co_applicant_age, (co_applicant_races)))
        self.applicants = applicant_list
        
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert self.loan_amount > 0 and self.interest_rate > 0
        amt = self.loan_amount

        while amt > 0:
            yield amt
            amt += self.interest_rate/100 * amt
            amt = amt - yearly_payment
       
    
f = open("banks.json")
banks_data = json.load(f)
f.close()
    
class Bank:
    def __init__(self, name):
        self.name = name
        for val in banks_data:
            if val["name"] == self.name:
                self.lei = val["lei"]
                
        zf = zipfile.ZipFile("wi.zip")
        f = zf.open("wi.csv")
        
        reader = csv.DictReader(TextIOWrapper(f))
        
        loan_objects_list = []
        for row in reader:
            if row["lei"] != self.lei:
                continue
            else:
                loan_objects_list.append(Loan(row))
                
        self.loan_info = loan_objects_list
        
        f.close()
        zf.close()
           
    def __len__(self):
        return len(self.loan_info)
    
    def __getitem__(self, lookup):
        loan_idx = int(lookup)
        loan = self.loan_info[loan_idx]
        if type(lookup) == int:
            return loan


    
                
            
        
