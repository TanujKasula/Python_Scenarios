from src.create_bucket import create_bucket_and_folders
from src.upload_resumes import upload_resume_to_s3
def main():
    print("CREATING S3 BUCKET AND FOLDER")
    create_bucket_and_folders()

    print("\n UPLOADING RESUME FILES TO S3 ")
    upload_resume_to_s3()

if __name__ == "__main__":
    main()
