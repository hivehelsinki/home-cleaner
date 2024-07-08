import intra
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yaml
import requests

with open('config.yml', 'r') as f:
    data = yaml.full_load(f)
ic = intra.IntraAPIClient(data['intra']['client'], data['intra']['secret'], progress_bar=True)

def get_students():
    campus_id = data.get('campus_id')
    res = ic.pages_threaded(f'campus/{campus_id}/users')
    students = []
    for student in res:
        if not '3b' in student['login'] and not student['login'] in data['god_mode_accoutns']:
            students.append(student['login'])

    return students

def get_incative_students(homes):
    print ("Getting students...")
    students = get_students()
    print (f"Found {len(students)} students")
    inactive_duration_in_months = data['inactive_duration_in_months']
    today = datetime.now()
    end_at = today.strftime('%Y-%m-%d')
    begin_at = (today - relativedelta(months=inactive_duration_in_months)).strftime('%Y-%m-%d')
    inactive_students = []
    payload = {
        "begin_at": begin_at,
        "end_at": end_at
    }
    students_with_home = []

    print ("Getting students with homes...")
    for student in students:
        if student in homes:
            students_with_home.append(student)
    print (f"Found {len(students_with_home)} students with homes")

    print ("Getting locations stats...")
    inactive_students = []
    for i, student in enumerate(students_with_home):
        location_stats = ic.pages_threaded(f'users/{student}/locations_stats', params=payload)
        if location_stats == {}:
            inactive_students.append(student)
        
        # Print the current progress
        print(f'Processing student {i + 1}/{len(students_with_home)}: {student}', end='\r', flush=True)
    print('\nProcessing complete.')

    print (f"Found {len(inactive_students)} inactive students with homes")
    return inactive_students

def get_homes():
    print ("Getting homes...")
    url = f'{data['homemaker']['base-url']}/homes'
    headers = {
    'Authorization': f'Bearer {data['homemaker']['admin-token']}'
    }
    res = requests.get(url, headers=headers)
    homes = res.json()
    homes_identifiers = []
    for home in homes:
        homes_identifiers.append(home['identifier'])
    return homes_identifiers

def delete_homes(inactive_students):
    print ("Deleting homes...")
    for student in inactive_students:
        print(student)
    unable_to_delete = []
    for i, student in enumerate(inactive_students):
        url = f'{data['homemaker']['base-url']}/homes/{student}'
        headers = {
        'Authorization': f'Bearer {data['homemaker']['admin-token']}'
        }
        res = requests.delete(url, headers=headers)
        if res.status_code != 204:
            unable_to_delete.append({"student": student, "code": res.status_code})
        print(f'Deleting home {i + 1}/{len(inactive_students)}: {student}', end='\r', flush=True)
    print('\nDeleting complete.')
    print (f"Unable to delete {len(unable_to_delete)} homes")
    for home in unable_to_delete:
        print (f"Student: {home['student']} Code: {home['code']}")


def home_cleaner():
    homes = get_homes()
    inactive_students = get_incative_students(homes)
    print ("Cleaning homes...")
    delete_homes(inactive_students)


if __name__ == "__main__":
    home_cleaner()