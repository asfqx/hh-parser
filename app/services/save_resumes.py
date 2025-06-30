from openpyxl import Workbook
import json


def safe_json_parse(value):
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value.replace("'", '"'))
    except Exception:
        return value


def format_education(edu) -> str:
    edu = safe_json_parse(edu)
    if not isinstance(edu, dict):
        return str(edu)
    level = edu.get("level", {}).get("name", "")
    primary = edu.get("primary", [])
    if primary and isinstance(primary, list):
        name = primary[0].get("name", "")
        year = primary[0].get("year", "")
        return f"{level} {name} {year}".strip()
    return level


def format_experience(exp) -> str:
    exp = safe_json_parse(exp)
    if isinstance(exp, list) and exp:
        latest = exp[0]
        position = latest.get("position", "")
        company = latest.get("company", "")
        start = latest.get("start", "")
        return f"{position} в {company} (с {start})"
    return str(exp)


def format_gender(gender) -> str:
    gender = safe_json_parse(gender)
    if isinstance(gender, dict):
        return gender.get("name", "")
    return str(gender)


def format_salary(salary) -> str:
    salary = safe_json_parse(salary)
    if isinstance(salary, dict):
        amount = salary.get("amount")
        currency = salary.get("currency", "")
        return f"{amount} {currency}" if amount else ""
    return str(salary)


def format_total_experience(exp) -> str:
    exp = safe_json_parse(exp)
    if isinstance(exp, dict):
        months = exp.get("months", 0)
        years = months // 12
        rest = months % 12
        return f"{years} лет {rest} мес." if months else ""
    return str(exp)


def save_resumes_to_excel(resumes: list[dict], chat_id):
    filename: str = f"resumes_for_{chat_id}.xlsx"
    if not resumes:
        print("Пустой список резюме. Excel не будет создан.")
        return False

    selected_fields = [
        "alternate_url",
        "certificate",
        "created_at",
        "education",
        "experience",
        "gender",
        "salary",
        "total_experience",
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumes"
    ws.append(selected_fields)

    for resume in resumes:
        row = []
        for field in selected_fields:
            value = resume.get(field, "")
            if field == "education":
                row.append(format_education(value))
            elif field == "experience":
                row.append(format_experience(value))
            elif field == "gender":
                row.append(format_gender(value))
            elif field == "salary":
                row.append(format_salary(value))
            elif field == "total_experience":
                row.append(format_total_experience(value))
            else:
                row.append(str(value))
        ws.append(row)

    wb.save(filename)
    print(f"Excel-файл '{filename}' успешно создан с {len(resumes)} строками.")
    return True
