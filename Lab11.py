import matplotlib.pyplot as plt
import os

def main():
    with open("data/students.txt") as students:
        student_info = []
        for student in students:
            student_info.append(student.strip())
        studentdir = {}
        for i in range(len(student_info)):
            studentdir[student_info[i][0:3]] = {"name":student_info[i][3:], "grades":{}}
    with open("data/assignments.txt") as assignments:
        assignment_data = []
        for item in assignments:
            assignment_data.append(item.strip())
        assignment_lib = {}
        for i in range(0, len(assignment_data), 3):
            assignment_lib[assignment_data[i+1]] = [assignment_data[i], assignment_data[i+2]]

    submissions = os.path.join("data/submissions")
    submits = []
    for data, submissions, files in os.walk(submissions):
        for file in files:
            submits.append((open(os.path.join(data, file))).read())
        for i in range (len(submits)):
            if submits[i][8] == '|':
                studentdir[submits[i][0:3]]["grades"][assignment_lib[submits[i][4:8]][0]] = int(submits[i][9:]) * (int(assignment_lib[submits[i][4:8]][1]) / 100)
            else:
                studentdir[submits[i][0:3]]["grades"][assignment_lib[submits[i][4:9]][0]] = int(submits[i][10:])*(int(assignment_lib[submits[i][4:9]][1])/100)

    while True:
        print("1. Students grade\n2. Assignment statistics\n3. Assignment graph\n")
        select = int(input("Enter your selection: "))
        if select == 1:
            name = input("What is the student's name: ")
            nonexist=True
            for id in studentdir:
                if name == studentdir[id]["name"]:
                    grade = 0
                    for assignment in studentdir[id]["grades"]:
                        grade += studentdir[id]["grades"][assignment]
                    print(f"{round((grade/1000)*100)}%")
                    print("")
                    nonexist=False
            if nonexist:
                print('Student not found\n')
        if select == 2:
            name = input("What is the assignment name: ")
            total = 0
            lowest = 100
            highest = 0
            nonexist=True
            for ids in assignment_lib:
                if name in assignment_lib[ids]:
                    for student in studentdir:
                        score = studentdir[student]['grades'][name]*100/int(assignment_lib[ids][1])
                        total += score
                        if lowest > score:
                            lowest = score
                        if highest < score:
                            highest = score
                    print(f"Min: {round(lowest)}%\nAvg: {round(total/(len(studentdir)))}%\nMax: {round(highest)}%")
                    nonexist = False
            if nonexist:
                print("Assignment name not found\n")

        if select == 3:
            name = input("What is the assignment name: ")
            nonexist= True
            for ids in assignment_lib:
                if name in assignment_lib[ids]:
                    scores = []
                    for student in studentdir:
                        scores.append(studentdir[student]['grades'][name]*100/int(assignment_lib[ids][1]))
                    plt.hist(scores,bins=[50,55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
                    plt.show()
                    print("")
                    nonexist=False

            if nonexist:
                print("Assignment name not found\n")


if __name__ == "__main__":
    main()