from tools import (
    get_student_info,
    get_student_marks,
    calculator,
    get_passing_rules
)

print(get_student_info.invoke("22CS045"))

print(get_student_marks.invoke("22CS045"))

print(calculator.invoke("85 + 72 + 90 + 78"))

print(calculator.invoke("(85 + 72 + 90 + 78) / 4"))

print(get_passing_rules.invoke(""))