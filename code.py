import os

import requests
import bs4

from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('URL')
URL_LOGIN = os.getenv('URL_LOGIN')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

class Cookies:
    def saveCookie(self,requestsCookieJar):
        self.cookies=requestsCookieJar

    def login(self, user, pwd):
        s= requests.Session()
        s.headers.update({"Referer":URL})
        defaultPage=s.get(URL)
        htmlObject = bs4.BeautifulSoup(defaultPage.content,'html.parser')
        rvt = htmlObject.find(id="loginform").input['value']
        data = {
            "_UserName": user,
            "_Password": pwd,
            "__RequestVerificationToken": rvt
        }
        logged = s.post(URL_LOGIN, data=data)
        self.saveCookie(s.cookies)

r = requests.Session()
r.headers.update({"Referer": URL})
c = Cookies()

def login(usr,pwd):
    c.login(usr,pwd)
    r.cookies = c.cookies

def my_profile():
    a = r.get("https://student.amizone.net/Electives/NewCourseCoding?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    row1=[x.text for x in b.find_all("div",attrs={"class":"col-md-3"})]
    row2 = [x.text for x in b.find_all("div", attrs={"class": "col-md-2"})]
    name=row1[0]
    Enrollment=row1[1]
    programme=row2[0]
    sem=row2[1]
    passyear=row2[2]
    img="https://amizone.net/amizone/Images/Signatures/"+username+"_P.png"
    print(name)
    print(Enrollment)
    print(programme)
    print(sem)
    print(passyear)
    print("Image URL: "+img)

def my_courses():
    a = r.get("https://student.amizone.net/Academics/MyCourses?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseName = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Name"})]
    attendance = [c.text.strip() for c in b.find_all(attrs={'data-title': "Attendance"})]
    syllabus   = [c.decode_contents() for c in b.find_all(attrs={'data-title': "Course Syllabus"})]
    # this returned a list(string) of anchor tags so the below code is to extract href from it
    syllabus   = [i[i.find('"')+1:i.find('"',i.find('"')+1)] for i in syllabus]

    print("Course code     Course name"+" "*50+"Attendance      Syllabus Download Url")
    for i in range(len(courseCode)):
        print("{:15s} {:60s} {:15s} {}".format(courseCode[i], courseName[i], attendance[i], syllabus[i]))

def results():
    a=r.get("https://student.amizone.net/Examination/Examination?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
    GradeObtained = [c.text.strip() for c in b.find_all(attrs={'data-title': "Go"})]
    GradePoint=[c.text.strip() for c in b.find_all(attrs={'data-title': "GP"})]

    sgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "SGPA"})]
    cgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]

    print("Result of sem "+str(len(sgpa))+":")
    print("S.no.  Course code     Course Title" + " " * 49 + "Go   GP")
    for i in range(len(courseCode)):
        print("{}      {:15s} {:60s} {:4s} {:2s}".format(i + 1, courseCode[i], courseTitle[i], GradeObtained[i],GradePoint[i]))
    print()

    print("Combined result:")
    print("Semester SGPA CGPA")
    for i in range(len(sgpa)):
        print("{}        {:4} {:4}".format(i+1,sgpa[i],cgpa[i]))

def my_faculty():
    a=r.get("https://student.amizone.net/FacultyFeeback/FacultyFeedback?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    faculties=[x.text.strip() for x in b.find_all(attrs={"class":"faculty-name"})]
    subjects=[x.text.strip() for x in b.find_all(attrs={"class":"subject"})]
    images=[x["src"] for x in b.find_all(attrs={"class":"img-responsive"})]
    print("Subjects"+" "*68+"Faculties"+" "*22+"Image Url")
    for i in range(len(subjects)):
         print("{:75s} {:30s} {}".format(subjects[i],faculties[i],images[i]))
           
def exam_schedule():
    a=r.get('https://student.amizone.net/Examination/ExamSchedule?X-Requested-With=XMLHttpRequest')
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
    ExamDate = [c.text.strip() for c in b.find_all(attrs={'data-title': "Exam Date"})]
    Time = [c.text.strip() for c in b.find_all(attrs={'data-title': "Time"})]
    print("CourseCode  "+"Course Title"+" "*49+"Exam Date  "+"Time")
    for i in range(len(courseCode)):
         print("{:11s} {:60s} {:10} {}".format(courseCode[i],courseTitle[i],ExamDate[i],Time[i]))
            
def timetable():
    a=r.get("https://student.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [x.text.strip() for x in b.find_all(attrs={"class":"course-code"})]
    courseTeacher = [c.text.strip() for c in b.find_all(attrs={'class': "course-teacher"})]
    classLocation = [x.text.strip() for x in b.find_all(attrs={"class":"class-loc"})]
    Time = [x.text.strip() for x in b.find_all(attrs={"class": "class-time"})]
    print("CourseCode "+" CourseTeacher"+" "*40+"ClassLocation "+"   Time")
    for i in range(len(courseCode)):
         print("{:12s}{:55s}{:10s}{}".format(courseCode[i],courseTeacher[i],classLocation[i],Time[i]))


if __name__ == "__main__":
    login(username,password)
    my_profile()
    print()
    my_courses()
    print()
    my_faculty()
    print()
    results()
    print()
    exam_schedule()
    print()
    timetable()
