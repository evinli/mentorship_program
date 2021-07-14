import csv
from os import name

# global lists to keep track of mentees and mentors
mentee = []
mentor = []

# student class
class student:
    def __init__(self, name, specialization, meetingType, responses):
        # data structure for responses will be a set of enumerations, at least for now
        # sets have O(1) lookup time so we don't need to iterate through the list every time
        self.name = name
        self.specialization = specialization
        self.meetingType = meetingType

        self.responses = set()
        for s in responses:
            self.responses.add(s)

    # getter functions
    def get_name(self):
        return self.name

    def get_specialization(self):
        return self.specialization

    def get_meetingType(self):
        return self.meetingType

    def get_responses(self):
        return self.responses


# open and read files for mentee and mentor lists
def read(filename, isMentee):
    # isMentee is a bool, parameter is passed in as true if mentee file is being read, false if otherwise

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)  # turns the spreadsheet into a reader object
        next(reader)  # skip header line

        # reads and stores each row of data as student object
        if isMentee:
            for row in reader:
                s = student(
                    row[0], row[1], row[2], {row[3], row[4], row[5], row[6], row[7]}
                )
                mentee.append(s)  # each mentee is appended to the global mentee list
        else:
            for row in reader:
                s = student(
                    row[0], row[1], row[2], {row[3], row[4], row[5], row[6], row[7]}
                )
                mentor.append(s)  # each mentor is appended to the global mentor list


def compare(mentee, mentor):
    """
    Computes the compatibility between mentees and mentors based on a weighted comparison of 
    their (top choice of) specialization, meeting preferences, and interests/hobbies. 
    Mentee-mentor compatibility is then returned as a numerical score. 

    """
    score = 0

    if mentee.get_specialization() == mentor.get_specialization():
        score += 80

    if mentee.get_meetingType() == mentor.get_meetingType():
        score += 50

    shared = [element for element in mentor.get_responses()]
    for a in mentee.get_responses():
        if a in mentor.get_responses():
            shared.remove(a)
    score += 10 * (len(mentor.get_responses()) - len(shared))

    return score


def get_matches(threshold):
    """
    Prints all mentee-mentor matches above a certain score threshold as a sorted list. Matches are shown
    in terms of mentees in the first list and mentors in the second list. The motivation behind having separate
    lists is to help confirm whether top matches are mutual for both the mentee and mentor.
    """

    # for outputting sorted results in terms of mentees
    print("MATCHES IN TERMS OF MENTEES:\n")
    for currentMentee in mentee:
        possibleMatches = (
            []
        )  # list of mentors for this mentee, gets reset every iteration
        sortedMatches = []
        matches = []

        print(currentMentee.get_name() + ": ")

        for currentMentor in mentor:
            score = compare(currentMentee, currentMentor)
            if threshold <= score:
                possibleMatches.append([currentMentor.get_name(), score])
        sortedMatches = sorted(
            possibleMatches, key=lambda match: match[1], reverse=True
        )

        for match in sortedMatches:
            matches.append(match[0] + str(match[1]))
        print(matches)

    # for outputting sorted results in terms of mentors
    print(
        "\n-----------------------------------------------------------\n\n\n\nMATCHES IN TERMS OF MENTORS:\n"
    )
    for currentMentor in mentor:
        possibleMatches = (
            []
        )  # list of mentees for this mentor, gets reset every iteration
        sortedMatches = []
        matches = []

        print(currentMentor.get_name() + ": ")

        for currentMentee in mentee:
            score = compare(currentMentee, currentMentor)
            if threshold <= score:
                possibleMatches.append([currentMentee.get_name(), score])
        sortedMatches = sorted(
            possibleMatches, key=lambda match: match[1], reverse=True
        )

        for match in sortedMatches:
            matches.append(match[0] + str(match[1]))
        print(matches)


# main function
def main(menteeList, mentorList, threshold):
    read(menteeList, True)
    read(mentorList, False)
    get_matches(threshold)


# calls main function to run matching algorithm
main("mentee.csv", "mentor.csv", 30)


# areas of improvement: optimize algorithm to find all maximal matching so that you don't have
#                       150-score pairings and then 30-scores elsewhere
# ideas: maximize overall score, do research on google

