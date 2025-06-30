import pandas as pd
import hashlib
from src.extraction import extract_from_mongo

def generate_client_id(name):
    return hashlib.md5(name.encode()).hexdigest()[:8]

def transform_data(df):
    clients=[]
    projects=[]
    technologies=[]
    teams=[]
    milestones=[]


    for row in df.itertuples(index=False):
        project_id=row.project_id
        project_name=row.project_name
        status=row.status
        client=row.client
        techs=row.technologies
        team_info=row.team
        milestones_list=row.milestones

        #Client
        client_id=generate_client_id(client['name'])
        clients.append({
            'client_id':client_id,
            'client_name':client['name'],
            'industry':client['industry'],
            'city':client['location']['city'],
            'country':client['location']['country']
        })

        projects.append({
            'project_id':project_id,
            'project_name':project_name,
            'status':status,
            'project_manager':team_info['project_manager'],
            'client_id':client_id
        })

        technologies.extend([
            {'project_id':project_id,'technology':tech} for tech in techs
        ])

        teams.extend([
            {
                'project_id':project_id,
                'member_name':member['name'],
                'role':member['role']
            }for member in team_info['members']
        ])

        milestones.extend([
            {
                'project_id':project_id,
                'milestone_name':ms['name'],
                'due_date':ms['due_date']
            }for ms in milestones_list
        ])

    clients_df=pd.DataFrame(clients).drop_duplicates()
    projects_df=pd.DataFrame(projects)
    technologies_df=pd.DataFrame(technologies)
    teams_df=pd.DataFrame(teams)
    milestones_df=pd.DataFrame(milestones)

    print("Transformation complete")

    return clients_df,projects_df,technologies_df,teams_df,milestones_df

if __name__=="__main__":
    df = extract_from_mongo()
    clients_df, projects_df, technologies_df, teams_df, milestones_df = transform_data(df)

    print(clients_df.head())
    print(projects_df.head())
    print(technologies_df.head())
    print(teams_df.head())
    print(milestones_df.head())
