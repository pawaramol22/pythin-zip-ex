import chardet
import zipfile
import io

def is_system_file(file_info):
    # Check if the dos_attributes bit for a system file is set
    return file_info.external_attr & 0x10 != 0 or file_info.external_attr & 0x02 != 0

def detect_file_encoding(raw_data):
    try:
        result = chardet.detect(raw_data)
        return result['encoding']
    except Exception as e:
        print(f"Error detecting file encoding: {e}, returning default encoding")
        return 'utf-8'


def read_all_files_from_zip(zip_file_path):
    count = 0
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:

            infolist = zip_file.infolist()
            for file_info in infolist:
                # Skip directories
                if file_info.is_dir():
                    continue
                if is_system_file(file_info):
                    continue

                with zip_file.open(file_info, force_zip64=True) as file:
                    try:
                        content = file.read()
                        encoding_ = detect_file_encoding(content)
                        #print(f"Content of {encoding_} '{file_info.filename}':\n{content.decode(encoding_, errors='replace')}")
                        print(f"Processing file {file_info}")
                        count += 1
                        print(f"Files read {count}/{len(infolist)}")
                    except Exception as ie:
                        print(f"Error reading file {encoding_} {file} - {ie}")

    except Exception as e:
        print(f"Error reading files from zip: {e}")

# Usage
zip_file_path = '/Users/yashwita/Documents/Documentation/Archive.zip'
read_all_files_from_zip(zip_file_path)
