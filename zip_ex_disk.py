import shutil
import zipfile
import os

def is_system_file(file_info):
    # Check if the dos_attributes bit for a system file is set
    return file_info.external_attr & 0x10 != 0 or file_info.external_attr & 0x02 != 0

def extract_and_process(zip_file_path, destination_path, max_size_bytes):
    total_extracted_size = 0
    file_count = 0
    try:

        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            for file_info in zip_file.infolist():

                # Skip directories
                if file_info.is_dir():
                    continue
                if is_system_file(file_info):
                    continue

                if file_info.file_size >= max_size_bytes:
                    # Process the file larger than available space as a single file
                    print(f"Process single file {file_info}")
                    file_count += 1
                if total_extracted_size >= max_size_bytes:
                    # Process the extracted files first if space already full
                    file_count_in_set = process_files(destination_path)
                    file_count += file_count_in_set
                    total_extracted_size = 0
                else:
                    #print(f"Extracting file {file_info}")
                    zip_file.extract(file_info, destination_path)
                    total_extracted_size += file_info.file_size

            # Process last set of extracted files (replace this with your processing logic)
            print(f"Process last set of files")
            file_count_in_set = process_files(destination_path)
            file_count += file_count_in_set
            print(f"Files processed {file_count}")

    except Exception as e:
        print(f"Error extracting and processing files: {e}")
    finally:
        # Clean up: Remove the extracted files
        shutil.rmtree(destination_path, ignore_errors=True)

def process_files(directory_path):
    file_count = 0
    # Replace this with your actual processing logic
    for root, dirs, files in os.walk(directory_path):
        try:
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                file_count += 1
        except Exception as e:
            print(f"Error extracting and processing files: {e}")
        finally:
            # Clean up: Remove the extracted files
            shutil.rmtree(directory_path, ignore_errors=True)
    return file_count

# Usage
zip_file_path = '/Users/yashwita/Documents/Documentation/Archive.zip'
max_size_bytes = 22 * 1024 # Example: 10 MB

# Temporary directory for extraction
temp_extraction_path = '/Users/yashwita/Documents/Documentation/Archive_temp'

# Ensure the temporary directory exists
os.makedirs(temp_extraction_path, exist_ok=True)

# Extract and process the files
extract_and_process(zip_file_path, temp_extraction_path, max_size_bytes)
