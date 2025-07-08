def join_or_first(items, keywords=None, limit=2):
    if not items:
        return ''
    if keywords:
        for item in items:
            if any(k.lower() in item.lower() for k in keywords ):
                return item
    return ";".join(items[:limit])


def transform_parsed_data(data:dict)-> dict:
    transformed_data={
        "name":data.get("name"),
        "email":data.get("email"),
        "phone":data.get("phone"),
        "education_summary":join_or_first(data["education"],keywords=["B.Tech","Bachelor","M.Tech","Masters","MCA",]),
        "experience_summary":join_or_first(data["experience"],keywords=["Intern","Traineee","Developer","Analyst","Engineer",""]),
        "projects":data.get('projects')
    }
    return transformed_data