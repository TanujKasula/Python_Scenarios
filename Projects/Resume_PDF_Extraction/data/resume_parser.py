import fitz
import os
import re
import pprint
def extract_text_from_pdf(file_path):
    doc=fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def parse_resume(file_path:str) -> dict:
    text=extract_text_from_pdf(file_path)
    lines=[line.strip() for line in text.splitlines() if line.strip()]

    data={
        "name":None,
        "email":None,
        "phone":None,
        "education":[],
        "experience":[],
        "projects":[]
    }

    email_pattern=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern=r"(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}"

    section=None

    for idx,line in enumerate(lines):
        if not data["email"]:
            email_match=re.search(email_pattern,line)
            if email_match:
                data["email"]=email_match.group()
                for back in range(1,5):
                    possible_name=lines[idx-back] if idx-back>=0 else ""
                    if possible_name and possible_name.istitle() and possible_name.replace(" ","").isalpha():
                        data["name"]=possible_name
                        break

        if not data["phone"]:
            phone_match=re.search(phone_pattern,line)
            if phone_match:
                data["phone"]=phone_match.group()

        lowered=line.lower()

        if "education" in lowered:
            section="education"
            continue
        elif "experience" in lowered:
            section="experience"
            continue
        elif "projects" in lowered:
            section="projects"
            continue
        elif any(x in lowered for x in ["skills","certifications","tools","technologies","publications","extracirricular"," activities"]):
            section=None

        if section:
            data[section].append(line)

    return data

if __name__=="__main__":
    file_path=r"C:\Users\Tanuj\Documents\UseCases\Projects\Resume_PDF_Extraction\data\Tanuj_Resume.pdf"
    result=parse_resume(file_path)
    pprint.pprint(result)
