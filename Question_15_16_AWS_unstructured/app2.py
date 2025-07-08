from src.s3_processor import process_resumes_from_s3

def main():
    print("\n PRCESSING RESUMES FROM S3")
    process_resumes_from_s3()

if __name__ == "__main__":
    main()
