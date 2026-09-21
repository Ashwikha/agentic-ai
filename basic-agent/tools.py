from database import (
    get_student,
    get_drive,
    get_eligibility_rule
)


def student_tool(roll_no):
    student = get_student(roll_no)

    if student is None:
        return {
            "error": "Student not found"
        }

    return {
        "roll_no": student[0],
        "name": student[1],
        "branch": student[2],
        "cgpa": student[3],
        "backlogs": student[4],
        "grad_year": student[5]
    }


def drive_tool(company_name):
    drive = get_drive(company_name)

    if drive is None:
        return {
            "error": "Company drive not found"
        }

    return {
        "drive_id": drive[0],
        "company": drive[1],
        "role": drive[2],
        "ctc_lpa": drive[3],
        "deadline": drive[4],
        "status": drive[5]
    }


def eligibility_tool(drive_id):
    rule = get_eligibility_rule(drive_id)

    if rule is None:
        return {
            "error": "Eligibility rule not found"
        }

    return {
        "min_cgpa": rule[0],
        "max_backlogs": rule[1],
        "allowed_branch": rule[2],
        "grad_year": rule[3]
    }