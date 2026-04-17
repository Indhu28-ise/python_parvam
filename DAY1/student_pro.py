import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


EXCEL_FILE = os.path.join(os.path.dirname(__file__), "student_performance.xls")
SUBJECTS = ["Math", "Science", "English"]
SS_NS = "urn:schemas-microsoft-com:office:spreadsheet"
ET.register_namespace("", SS_NS)


def calculate_grade(average):
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 50:
        return "C"
    return "D"


def get_student_data():
    print("Student Performance Input System")
    print("-" * 35)

    while True:
        name = input("Enter student name: ").strip().title()
        if name:
            break
        print("Name cannot be empty.")

    marks = {}
    for subject in SUBJECTS:
        while True:
            try:
                score = float(input(f"Enter marks for {subject} (0-100): ").strip())
                if 0 <= score <= 100:
                    marks[subject] = score
                    break
                print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter numeric marks.")

    return {
        "Name": name,
        "Math": marks["Math"],
        "Science": marks["Science"],
        "English": marks["English"],
    }


def get_cell_text(cell):
    data = cell.find(f"{{{SS_NS}}}Data")
    if data is None or data.text is None:
        return ""
    return data.text


def load_existing_data():
    if not os.path.exists(EXCEL_FILE):
        return []

    try:
        tree = ET.parse(EXCEL_FILE)
    except ET.ParseError:
        return []

    rows = tree.getroot().findall(f".//{{{SS_NS}}}Row")
    records = []

    for row in rows[1:]:
        cells = row.findall(f"{{{SS_NS}}}Cell")
        if len(cells) < 4:
            continue

        name = get_cell_text(cells[0]).strip()
        if not name:
            continue

        try:
            records.append(
                {
                    "Name": name,
                    "Math": float(get_cell_text(cells[1])),
                    "Science": float(get_cell_text(cells[2])),
                    "English": float(get_cell_text(cells[3])),
                }
            )
        except ValueError:
            continue

    return records


def save_workbook(records):
    lines = [
        '<?xml version="1.0"?>',
        '<?mso-application progid="Excel.Sheet"?>',
        '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"',
        ' xmlns:o="urn:schemas-microsoft-com:office:office"',
        ' xmlns:x="urn:schemas-microsoft-com:office:excel"',
        ' xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">',
        ' <Worksheet ss:Name="Student Performance">',
        '  <Table>',
        '   <Row>',
        '    <Cell><Data ss:Type="String">Name</Data></Cell>',
        '    <Cell><Data ss:Type="String">Math</Data></Cell>',
        '    <Cell><Data ss:Type="String">Science</Data></Cell>',
        '    <Cell><Data ss:Type="String">English</Data></Cell>',
        '    <Cell><Data ss:Type="String">Average</Data></Cell>',
        '    <Cell><Data ss:Type="String">Grade</Data></Cell>',
        '   </Row>',
    ]

    for record in records:
        average = round(
            (record["Math"] + record["Science"] + record["English"]) / len(SUBJECTS), 2
        )
        grade = calculate_grade(average)

        lines.append("   <Row>")
        lines.append(f'    <Cell><Data ss:Type="String">{escape(record["Name"])}</Data></Cell>')
        lines.append(f'    <Cell><Data ss:Type="Number">{record["Math"]}</Data></Cell>')
        lines.append(f'    <Cell><Data ss:Type="Number">{record["Science"]}</Data></Cell>')
        lines.append(f'    <Cell><Data ss:Type="Number">{record["English"]}</Data></Cell>')
        lines.append(
            '    <Cell ss:Formula="=AVERAGE(RC[-3]:RC[-1])">'
            f'<Data ss:Type="Number">{average}</Data></Cell>'
        )
        lines.append(
            '    <Cell ss:Formula="=IF(RC[-1]>=85,&quot;A&quot;,IF(RC[-1]>=70,&quot;B&quot;,IF(RC[-1]>=50,&quot;C&quot;,&quot;D&quot;)))">'
            f'<Data ss:Type="String">{grade}</Data></Cell>'
        )
        lines.append("   </Row>")

    lines.extend([
        "  </Table>",
        " </Worksheet>",
        "</Workbook>",
    ])

    with open(EXCEL_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def save_student_data(student_record):
    records = load_existing_data()
    average = round(
        (student_record["Math"] + student_record["Science"] + student_record["English"]) / 3, 2
    )
    grade = calculate_grade(average)

    student_record["Average"] = average
    student_record["Grade"] = grade

    existing_record = next(
        (record for record in records if record["Name"].lower() == student_record["Name"].lower()),
        None,
    )

    if existing_record is not None:
        existing_record["Name"] = student_record["Name"]
        existing_record["Math"] = student_record["Math"]
        existing_record["Science"] = student_record["Science"]
        existing_record["English"] = student_record["English"]
        message = f"Updated existing record for {student_record['Name']}."
    else:
        records.append(
            {
                "Name": student_record["Name"],
                "Math": student_record["Math"],
                "Science": student_record["Science"],
                "English": student_record["English"],
            }
        )
        message = f"Added new record for {student_record['Name']}."

    save_workbook(records)
    return message


def main():
    student_record = get_student_data()
    message = save_student_data(student_record)
    print(message)
    print(f"Average: {student_record['Average']}")
    print(f"Grade: {student_record['Grade']}")
    print(f"Excel file saved at: {EXCEL_FILE}")

    try:
        os.startfile(EXCEL_FILE)
        print("Excel file opened automatically.")
    except OSError:
        print("Could not open the Excel file automatically.")


if __name__ == "__main__":
    main()
