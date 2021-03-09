import os
import requests
import bs4

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL', 'https://s.amizone.net/')
URL_LOGIN = os.getenv('URL_LOGIN', 'https://s.amizone.net/')


class Cookies:

    def save_cookie(self, request_cookie_jar):
        self.cookies = request_cookie_jar

    def login(self, user, pwd):
        s = requests.Session()
        s.headers.update({"Referer": URL})
        default_page = s.get(URL)
        html_object = bs4.BeautifulSoup(default_page.content, 'html.parser')
        rvt = html_object.find(id="loginform").input['value']
        data = {
            "_UserName": user,
            "_Password": pwd,
            "__RequestVerificationToken": rvt
        }
        logged = s.post(URL_LOGIN, data=data)
        self.save_cookie(s.cookies)


class Amizone:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.r = requests.Session()
        self.r.headers.update({"Referer": URL})
        self.c = Cookies()

        self.login(username, password)

    def login(self, username, password):
        self.c.login(username, password)
        self.r.cookies = self.c.cookies

    def get_profile(self):
        a = self.r.get(URL + "Electives/NewCourseCoding?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        row1 = [x.text for x in b.find_all("div", attrs={"class": "col-md-3"})]
        row2 = [x.text for x in b.find_all("div", attrs={"class": "col-md-2"})]

        name = row1[0]
        enrollment = row1[1]
        programme = row2[0]
        sem = row2[1]
        pass_year = row2[2]
        img = "https://amizone.net/amizone/Images/Signatures/" + self.username + "_P.png"

        return {
            'name': name,
            'enrollment': enrollment,
            'programme': programme,
            'sem': sem,
            'pass_year': pass_year,
            'img_url': img,
        }

    def get_courses(self):
        result = []

        a = self.r.get(URL + "Academics/MyCourses?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        course_code = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        course_name = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Name"})]
        attendance = [c.text.strip() for c in b.find_all(attrs={'data-title': "Attendance"})]
        syllabus = [c.decode_contents() for c in b.find_all(attrs={'data-title': "Course Syllabus"})]

        # this returned a list(string) of anchor tags so the below code is to extract href from it
        syllabus = [i[i.find('"') + 1:i.find('"', i.find('"') + 1)] for i in syllabus]

        for i in range(len(course_code)):
            result.append({
                'course_code': course_code[i],
                'course_name': course_name[i],
                'attendance': attendance[i],
                'syllabus_download_url': syllabus[i],
            })

        return result

    def get_exam_results(self):
        results = {
            'subjects': [],
            'combined_results': []
        }

        a = self.r.get(URL + "Examination/Examination?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        course_code = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        course_title = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
        grade_obtained = [c.text.strip() for c in b.find_all(attrs={'data-title': "Go"})]
        grade_point = [c.text.strip() for c in b.find_all(attrs={'data-title': "GP"})]

        sgpa = [x.text.strip() for x in b.find_all(attrs={'data-title': "SGPA"})]
        cgpa = [x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]

        results['semester_number'] = str(len(sgpa))

        for i in range(len(course_code)):
            results['subjects'].append({
                'course_code': course_code[i],
                'course_title': course_title[i],
                'grade_obtained': grade_obtained[i],
                'grade_point': grade_point[i],
            })

        for i in range(len(sgpa)):
            results['combined_results'].append({
                'sgpa': sgpa[i],
                'cgpa': cgpa[i]
            })

        return results

    def get_faculties(self):
        result = []

        a = self.r.get(URL + "FacultyFeeback/FacultyFeedback?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        faculties = [x.text.strip() for x in b.find_all(attrs={"class": "faculty-name"})]
        subjects = [x.text.strip() for x in b.find_all(attrs={"class": "subject"})]
        images = [x["src"] for x in b.find_all(attrs={"class": "img-responsive"})]

        for i in range(len(subjects)):
            result.append({
                'subject': subjects[i],
                'faculty': faculties[i],
                'image_url': images[i],
            })

        return result

    def get_exam_schedule(self):
        result = []

        a = self.r.get(URL + "Examination/ExamSchedule?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        course_code = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
        course_title = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
        exam_date = [c.text.strip() for c in b.find_all(attrs={'data-title': "Exam Date"})]
        exam_time = [c.text.strip() for c in b.find_all(attrs={'data-title': "Time"})]

        for i in range(len(course_code)):
            result.append({
                'course_code': course_code[i],
                'course_title': course_title[i],
                'exam_date': exam_date[i],
                'exam_time': exam_time[i],
            })

        return result

    def get_timetable(self):
        result = []

        a = self.r.get(URL + "TimeTable/Home?X-Requested-With=XMLHttpRequest")
        b = bs4.BeautifulSoup(a.content, 'html.parser')

        course_code = [x.text.strip() for x in b.find_all(attrs={"class": "course-code"})]
        course_teacher = [c.text.strip() for c in b.find_all(attrs={'class': "course-teacher"})]
        class_location = [x.text.strip() for x in b.find_all(attrs={"class": "class-loc"})]
        exam_time = [x.text.strip() for x in b.find_all(attrs={"class": "class-time"})]

        for i in range(len(course_code)):
            result.append({
                'course_code': course_code[i],
                'course_teacher': course_teacher[i],
                'class_location': class_location[i],
                'exam_time': exam_time[i],
            })
        return result


if __name__ == "__main__":
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    instance = Amizone(username, password)

    instance.login(username, password)

    print(instance.get_profile())

    print(instance.get_courses())

    print(instance.get_faculties())
    print(instance.get_exam_results())
    print(instance.get_exam_schedule())
    print(instance.get_timetable())
