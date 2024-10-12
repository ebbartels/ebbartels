import os
import json
import zipfile
import io
import csv
import loans
import statistics

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r]) 
    
    def __repr__(self):
        return f"Applicant('{self.age}', {sorted(self.race)})"
    
    def lower_age(self):
        return int(self.age.replace("<", "").replace(">", "").split('-')[0])
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()

class Loan:
    def __init__(self, values):
        if (values["loan_amount"] != "NA") and (values["loan_amount"] != "Exempt"):
            self.loan_amount = float(values["loan_amount"])
        else:
            self.loan_amount = -1
            
        if (values["property_value"] != "NA") and (values["property_value"] != "Exempt"):
            self.property_value = float(values["property_value"])
        else:
            self.property_value = -1
            
        if (values["interest_rate"] != "NA") and (values["interest_rate"] != "Exempt"):
            self.interest_rate = float(values["interest_rate"])
        else:
            self.interest_rate = -1
            
        age = values["applicant_age"]
        race_list = []
        for i in range(1,6):
            race_list.append(values["applicant_race-" + str(i)])
        self.applicants = []
        self.applicants.append(Applicant(age, race_list))
        if values["co-applicant_age"] != "9999":
            co_age = values["co-applicant_age"]
            co_race_list = []
            for i in range(1,6):
                co_race_list.append(values["co-applicant_race-" + str(i)])
            self.applicants.append(Applicant(co_age, co_race_list))
        
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate >= 0 
        assert self.loan_amount >= 0
        amt = self.loan_amount
        interest_rate = self.interest_rate

        while amt > 0:
            if amt < 0:
                break
            yield amt 
            amt = amt + amt * interest_rate/100 - yearly_payment

class Bank:
    def __init__(self, bank):
        self.loans = []
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "banks.json")
        with open(file_path) as file:
            data = json.load(file)
        self.name = None
        for i in data:
            if bank == i['name']:
                self.name = i['name']
                self.lei = i['lei']
        if self.name == None:
            raise ValueError(f'{bank} does not exist')
        
    def load_from_zip(self, path):
        cwd = os.getcwd()
        file_path = os.path.join(cwd, path)
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            with zip_file.open("wi.csv") as file_in_zip:
                csv_reader = csv.DictReader(io.TextIOWrapper(file_in_zip, encoding='utf-8'))
                for loan_dict in csv_reader:                        
                    if loan_dict["lei"] == self.lei:
                        loan_i = Loan(loan_dict)
                        self.loans.append(loan_i)
    def __len__(self):
        return len(self.loans)
    
    def __getitem__(self, index):
        return self.loans[index]

    def average_interest_rate(self):
        total = 0
        
        for loan in self.loans:
            total += loan.interest_rate
                
        return total/len(self.loans)
    
    def num_applicants(self):
        total_apps = 0
        for loan in self.loans:
            if len(loan.applicants) < 10:
                total_apps += len(loan.applicants)
        return total_apps/len(self.loans)
    
    def ages_dict(self):
        age_dict = {}
        for loan_dict in self.loans:
            for applicant in loan_dict.applicants:
                age = applicant.age
                lowerage = applicant.lower_age()
                if lowerage >200:
                    continue
                if age in age_dict.keys():
                    age_dict[age] +=1
                else:
                    age_dict[age] = 1
        return dict(sorted(age_dict.items()))
                
            