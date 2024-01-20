class Student():
    def __init__(self, name, chinese, english):
        self.name = name
        self.chinese = chinese
        self.english = english

matthew = Student("matthew", 0, 0)
johnson = Student("Johnson", 100, 100)
students = [matthew, johnson]
for student in students:
    if student.name == "Johnson":
        print(f"Johnson's english score {johnson.english}")
print(matthew.english, johnson.english)