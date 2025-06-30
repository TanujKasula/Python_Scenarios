from src.extraction import extract_from_mongo
from src.transformation import transform_data
from src.load import load_to_mysql

def main():
    df=extract_from_mongo()
    clients_df, projects_df, technologies_df, teams_df, milestones_df=transform_data(df)
    load_to_mysql(clients_df, projects_df, technologies_df, teams_df, milestones_df,if_exists='replace')

if __name__=="__main__":
    main()