import app.services.intra as intra
import app.services.homemaker as homemaker
from app.helpers.format_dates import make_date_payload, make_range
from app.helpers.make_homes_chunks import make_homes_chunks
from app.helpers.load_config import load_config

config = load_config("config.yml")

ic = intra.IntraAPIClient(
    config["intra"]["client"], config["intra"]["secret"], progress_bar=False
)
homeamker = homemaker.HomemakerAPIClient(
    config["homemaker"]["admin_token"], config["homemaker"]["base_url"]
)


def delete_homes(inactive_students):
    for student in inactive_students:
        homemaker.delete_home(student)


def get_inactive_students(students):
    payload = make_date_payload(config)
    inactive_students = []
    for student in students:
        try:
            location_stats = ic.pages_threaded(
                f"users/{student}/locations_stats", params=payload
            )
            if location_stats == {}:
                inactive_students.append(student)
        except Exception:
            print(
                f"\033[0;31mFailed to get location stats for student {student}\033[0m"
            )

    if len(inactive_students) == 0:
        print("No inactive students found. Exiting program.")
        exit()

    return inactive_students


def check_students_profile_creation_dates(homes):
    created_at = make_range(config)
    campus_id = config.get("campus_id")
    homes_chunks = make_homes_chunks(homes)
    new_homes = []
    for chunk in homes_chunks:
        slugs = ",".join(chunk)
        students_with_new_homes = ic.pages_threaded(
            f"campus/{campus_id}/users?filter[login]={slugs}&range[created_at]={created_at}"
        )
        if len(students_with_new_homes) > 0:
            for student in students_with_new_homes:
                new_homes.append(student["login"])
    old_homes = [home for home in homes if home not in new_homes]

    return old_homes


def get_homes():
    try:
        homes = homeamker.get_homes()
        assert homes is not None, "Failed to get homes"

        homes_identifiers = []
        for home in homes:
            if home["identifier"] not in config["god_mode_accounts"]:
                homes_identifiers.append(home["identifier"])
        if len(homes_identifiers) == 0:
            print("No homes found. Exiting program.")
            exit()

        return homes_identifiers
    except AssertionError:
        exit()


def check_that_homes_are_deleted(deleted_homes):
    homes = get_homes()
    undeleted_homes = [home for home in deleted_homes if home in homes]
    if len(undeleted_homes) == 0:
        print("All homes are deleted.")
    else:
        print(f"\033[0;31mFailed to delete {len(undeleted_homes)} homes:")
        print(", ".join(undeleted_homes))


def home_cleaner():
    homes = get_homes()
    students_profiles_older_than_n_months = check_students_profile_creation_dates(homes)
    inactive_students = get_inactive_students(students_profiles_older_than_n_months)
    # delete_homes(inactive_students)
    check_that_homes_are_deleted(inactive_students)


if __name__ == "__main__":
    home_cleaner()
