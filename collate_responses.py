import csv
import sys
import json

import os
from os import listdir
from os.path import isfile, join

csvfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]

FIELDS = ["pptID",
	      "fileName",
          "age",
          "gender",
          "nationality",
          "firstLang",
          "condition",
          "trial",
          "clipName",
          "freetext"] +\
          ["q%02d" % (i + 1) for i in range(30)] +\
          ["response_time"]

MAPPING = {"q01":"The children were competing with one another.",
           "q02":"The children were cooperating with one another.",
           "q03":"The children were playing separately.",
           "q04":"The children were playing together.",
           "q05":"The child on the left was sad.",
           "q06":"The child on the right was sad.",
           "q07":"The child on the left was happy.",
           "q08":"The child on the right was happy.",
           "q09":"The child on the left was angry.",
           "q10":"The child on the right was angry.",
           "q11":"The child on the left was excited.",
           "q12":"The child on the right was excited.",
           "q13":"The child on the left was calm.",
           "q14":"The child on the right was calm.",
           "q15":"The child on the left was friendly.",
           "q16":"The child on the right was friendly.",
           "q17":"The child on the left was aggressive.",
           "q18":"The child on the right was aggressive.",
           "q19":"The child on the left was engaged with what they were doing on the table.",
           "q20":"The child on the right was engaged with what they were doing on the table.",
           "q21":"The child on the left was distracted from the table.",
           "q22":"The child on the right was distracted from the table.",
           "q23":"The child on the left was bored.",
           "q24":"The child on the right was bored.",
           "q25":"The child on the left was frustrated.",
           "q26":"The child on the right was frustrated.",
           "q27":"The child on the left was dominant.",
           "q28":"The child on the right was dominant.",
           "q29":"The child on the left was submissive.",
           "q30":"The child on the right was submissive."}

outputfile = open("fulldata.csv", "w")
outputcsv = csv.DictWriter(outputfile, fieldnames=FIELDS)
outputcsv.writeheader()

def get(responses, line):
    return json.loads(responses[line]["responses"])

for f in csvfiles:
    with open(join(sys.argv[1], f),'r') as csvfile:
        print("Processing %s:" % f)

        participant_row = {}
        try:
            csvdict = csv.DictReader(csvfile)

            responses = {int(row["trial_index"]): row for row in csvdict }

            participant_row["pptID"] = responses[0]["subject"]
            participant_row["fileName"] = f
            participant_row["condition"] = responses[0]["condition"]
            participant_row["age"] = get(responses, 5)["Q0"]
            participant_row["gender"] = get(responses, 4)["Q2"]
            participant_row["nationality"] = get(responses, 4)["Q0"]
            participant_row["firstLang"] = get(responses, 4)["Q1"]
            participant_row["response_time"] = 0

            #...condition,...

            def collect_questions(idx):
                participant_row["freetext"] =  get(responses, idx)["Q0"]
                questions = get(responses, idx + 1)
                questions.update(get(responses, idx + 2))
                questions.update(get(responses, idx + 3))
                questions.update(get(responses, idx + 4))
                participant_row["q01"] =  questions[MAPPING["q01"]]
                participant_row["q02"] =  questions[MAPPING["q02"]]
                participant_row["q03"] =  questions[MAPPING["q03"]]
                participant_row["q04"] =  questions[MAPPING["q04"]]
                participant_row["q05"] =  questions[MAPPING["q05"]]
                participant_row["q06"] =  questions[MAPPING["q06"]]
                participant_row["q07"] =  questions[MAPPING["q07"]]
                participant_row["q08"] =  questions[MAPPING["q08"]]
                participant_row["q09"] =  questions[MAPPING["q09"]]
                participant_row["q10"] =  questions[MAPPING["q10"]]
                participant_row["q11"] =  questions[MAPPING["q11"]]
                participant_row["q12"] =  questions[MAPPING["q12"]]
                participant_row["q13"] =  questions[MAPPING["q13"]]
                participant_row["q14"] =  questions[MAPPING["q14"]]
                participant_row["q15"] =  questions[MAPPING["q15"]]
                participant_row["q16"] =  questions[MAPPING["q16"]]
                participant_row["q17"] =  questions[MAPPING["q17"]]
                participant_row["q18"] =  questions[MAPPING["q18"]]
                participant_row["q19"] =  questions[MAPPING["q19"]]
                participant_row["q20"] =  questions[MAPPING["q20"]]
                participant_row["q21"] =  questions[MAPPING["q21"]]
                participant_row["q22"] =  questions[MAPPING["q22"]]
                participant_row["q23"] =  questions[MAPPING["q23"]]
                participant_row["q24"] =  questions[MAPPING["q24"]]
                participant_row["q25"] =  questions[MAPPING["q25"]]
                participant_row["q26"] =  questions[MAPPING["q26"]]
                participant_row["q27"] =  questions[MAPPING["q27"]]
                participant_row["q28"] =  questions[MAPPING["q28"]]
                participant_row["q29"] =  questions[MAPPING["q29"]]
                participant_row["q30"] =  questions[MAPPING["q30"]]


            # TRIAL 1
            participant_row["trial"] = 1
            participant_row["clipName"] = responses[9]["stimulus"]
            collect_questions(idx=10)
            outputcsv.writerow(participant_row)

            # TRIAL 2
            participant_row["trial"] = 2
            participant_row["clipName"] = responses[16]["stimulus"]
            collect_questions(idx=17)
            outputcsv.writerow(participant_row)

            # TRIAL 3
            participant_row["trial"] = 3
            participant_row["clipName"] = responses[23]["stimulus"]
            collect_questions(idx=24)
            outputcsv.writerow(participant_row)

            # TRIAL 4
            participant_row["trial"] = 4
            participant_row["clipName"] = responses[30]["stimulus"]
            collect_questions(idx=31)
            outputcsv.writerow(participant_row)

        except UnicodeDecodeError:
            print("Skipping %s due to unicode errors" % f )


outputfile.close()
print("Done!")
