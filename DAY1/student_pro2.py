import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = os.path.dirname(__file__)
EXCEL_FILE = os.path.join(BASE_DIR, "Student_Performance.xlsx")
SUMMARY_FILE = os.path.join(BASE_DIR, "Student_Report.xlsx")
CHART_FILE = os.path.join(BASE_DIR, "student_average_chart.png")
PDF_FILE = os.path.join(BASE_DIR, "Student_Performance_Report.pdf")
GRAPH_DIR = os.path.join(BASE_DIR, "student_graphs")
SUBJECTS = ["Math", "Science", "English"]


def calculate_grade(average):
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 50:
        return "C"
    return "D"


def generate_student_graphs(df):
    os.makedirs(GRAPH_DIR, exist_ok=True)
    graph_files = {}

    for _, row in df.iterrows():
        safe_name = str(row["Name"]).replace(" ", "_")
        graph_path = os.path.join(GRAPH_DIR, f"{safe_name}_performance.png")

        plt.figure(figsize=(8, 4.5))
        plt.bar(SUBJECTS, [row[subject] for subject in SUBJECTS], color=["#4C78A8", "#59A14F", "#F28E2B"])
        plt.title(f"{row['Name']} - Subject Performance")
        plt.xlabel("Subjects")
        plt.ylabel("Marks")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

        graph_files[row["Name"]] = graph_path

    return graph_files


def create_pdf_report(df, subject_summary, report_notes, graph_files):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(PDF_FILE, pagesize=A4)
    elements = []

    elements.append(Paragraph("Student Performance Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Performance Table", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    performance_table_data = [
        ["Name", "Math", "Science", "English", "Average", "Grade", "Result"]
    ] + df[["Name", "Math", "Science", "English", "Average", "Grade", "Result"]].values.tolist()

    performance_table = Table(performance_table_data, repeatRows=1)
    performance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    elements.append(performance_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Class Overview", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Image(CHART_FILE, width=450, height=260))
    elements.append(Spacer(1, 16))

    overview_table_data = [["Metric", "Value"]] + report_notes.values.tolist()
    overview_table = Table(overview_table_data)
    overview_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E8B57")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(overview_table)
    elements.append(Spacer(1, 16))

    subject_summary_data = [["Subject", "Class Average", "Highest Score", "Lowest Score"]] + subject_summary.values.tolist()
    subject_summary_table = Table(subject_summary_data)
    subject_summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#8B4513")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(subject_summary_table)

    for _, row in df.iterrows():
        elements.append(PageBreak())
        elements.append(Paragraph(f"Student: {row['Name']}", styles["Heading1"]))
        elements.append(Spacer(1, 10))

        student_table_data = [
            ["Metric", "Value"],
            ["Math", row["Math"]],
            ["Science", row["Science"]],
            ["English", row["English"]],
            ["Total", row["Total"]],
            ["Average", row["Average"]],
            ["Grade", row["Grade"]],
            ["Result", row["Result"]],
        ]

        student_table = Table(student_table_data)
        student_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5B5EA6")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )

        elements.append(student_table)
        elements.append(Spacer(1, 14))
        elements.append(Image(graph_files[row["Name"]], width=430, height=240))

    pdf.build(elements)


def create_report():
    if not os.path.exists(EXCEL_FILE):
        print("No student data found. Run student_project.py first.")
        return

    df = pd.read_excel(EXCEL_FILE)

    if df.empty:
        print("The Excel sheet is empty. Add student records first.")
        return

    df["Total"] = df[SUBJECTS].sum(axis=1)
    df["Average"] = df[SUBJECTS].mean(axis=1).round(2)
    df["Highest Mark"] = df[SUBJECTS].max(axis=1)
    df["Lowest Mark"] = df[SUBJECTS].min(axis=1)
    if "Grade" not in df.columns:
        df["Grade"] = df["Average"].apply(calculate_grade)
    else:
        df["Grade"] = df["Grade"].fillna(df["Average"].apply(calculate_grade))
    df["Result"] = np.where(df["Average"] >= 50, "Pass", "Fail")

    subject_summary = pd.DataFrame(
        {
            "Subject": SUBJECTS,
            "Class Average": [round(df[subject].mean(), 2) for subject in SUBJECTS],
            "Highest Score": [df[subject].max() for subject in SUBJECTS],
            "Lowest Score": [df[subject].min() for subject in SUBJECTS],
        }
    )

    top_student = df.loc[df["Average"].idxmax(), "Name"]
    class_average = round(df["Average"].mean(), 2)

    report_notes = pd.DataFrame(
        {
            "Metric": [
                "Top Performer",
                "Class Average",
                "Number of Students",
                "Pass Count",
                "Fail Count",
            ],
            "Value": [
                top_student,
                class_average,
                len(df),
                int((df["Result"] == "Pass").sum()),
                int((df["Result"] == "Fail").sum()),
            ],
        }
    )

    plt.figure(figsize=(10, 6))
    plt.bar(df["Name"], df["Average"], color="teal")
    plt.axhline(class_average, color="red", linestyle="--", label=f"Class Average = {class_average}")
    plt.title("Student Average Performance")
    plt.xlabel("Student Name")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()

    graph_files = generate_student_graphs(df)

    with pd.ExcelWriter(SUMMARY_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Student Report", index=False)
        subject_summary.to_excel(writer, sheet_name="Subject Summary", index=False)
        report_notes.to_excel(writer, sheet_name="Overview", index=False)

    create_pdf_report(df, subject_summary, report_notes, graph_files)

    print("Student performance report created successfully.")
    print(f"Input data file: {EXCEL_FILE}")
    print(f"Report file: {SUMMARY_FILE}")
    print(f"Chart file: {CHART_FILE}")
    print(f"PDF file: {PDF_FILE}")
    print("\nDetailed Report:")
    print(df[["Name", "Total", "Average", "Grade", "Result"]].to_string(index=False))


if __name__ == "__main__":
    create_report()