from src.utils import get_mysql_engine

def load_to_mysql(clients_df, projects_df, technologies_df, teams_df, milestones_df,if_exists):
    engine=get_mysql_engine()

    try:
        clients_df.to_sql('clients',con=engine,index=False,if_exists=if_exists)
        print("Clients table loaded")
        projects_df.to_sql('projects',con=engine,index=False,if_exists=if_exists)
        print("Projects table loaded")
        technologies_df.to_sql('technologies',con=engine,index=False,if_exists=if_exists)
        print("Technologies table loaded")
        teams_df.to_sql('teams',con=engine,index=False,if_exists=if_exists)
        print("Teams table loaded")
        milestones_df.to_sql('milestones',con=engine,index=False,if_exists=if_exists)
        print("Milestones table loaded")
    except Exception as e:
        print(f"Load failed:{e}")