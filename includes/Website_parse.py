import mysql.connector
import requests
from bs4 import BeautifulSoup

# Connect to MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Osamaebid123",
  database="uni_new"
)

# Create table
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE courses (course_code VARCHAR(255), "
                 "course_name VARCHAR(255), "
                 "program_area VARCHAR(255), "
                 "distribution_requirement VARCHAR(255), "
                 "prerequisites TEXT, exclusions TEXT)")

# Scrape data from website
url = "https://utm.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# Find all the course div elements
course_divs = soup.find_all("div", class_="no-break views-row")

# Loop through the course divs and extract the course information
for course_div in course_divs:
    # extract the course code and course name
    title_div = course_div.find("div", class_="views-field-title")
    title_span = title_div.find("span", class_="field-content")
    course_code, course_name = title_span.text.split(" • ")

    # extract the distribution requirement
    distribution_requirement = None
    for span in course_div.find_all("span"):
        if span.find("strong", class_="views-label-field-distribution-requirements"):
            distribution_requirement = span.find("span", class_="field-content").text.strip()

    # extract the exclusions
    exclusions = None
    for span in course_div.find_all("span"):
        if span.find("strong", class_="views-label-field-exclusion"):
            exclusions = span.find("span", class_="field-content").text.strip()

    # extract the prerequisites
    prerequisites = None
    for span in course_div.find_all("span"):
        if span.find("strong", class_="views-label-field-prerequisite"):
            prerequisites = span.find("span", class_="field-content").text.strip()

    # extract the program area, set to "N/A" if not found
    program_area = None
    for div in course_div.find_all("div", class_="views-field views-field-field-timetable-link"):
        for a in div.find_all("a"):
            if "/section/" in a.get("href"):
                program_area = a.text.strip()

    # Insert the course information into the MySQL database
    sql = "INSERT INTO courses (course_code, course_name, distribution_requirement," \
          " exclusions, prerequisites, program_area) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (course_code, course_name, distribution_requirement, exclusions, prerequisites, program_area)
    mycursor.execute(sql, val)
    # mydb.commit()

# Close the database connection
mydb.close()
