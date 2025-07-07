import os
import time
import requests

# הגדרת מפתח API
api_key = 'YOUR_VIRUSTOTAL_API_KEY'
# הגדרת נתיב לתיקיה לבדיקה
folder_path = 'C:\\Users\\User\\Desktop\\קורס'

# פונקציה לסריקת קובץ ב-VirusTotal
def scan_file(file_path):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {'x-apikey': api_key}
    
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        response = requests.post(url, headers=headers, files=files)
        
    if response.status_code == 200:
        result = response.json()
        scan_id = result['data']['id']
        return scan_id
    else:
        print(f'Failed to scan: {file_path}')
        return None

# פונקציה לבדיקת תוצאות הסריקה
def check_scan_result(scan_id):
    url = f'https://www.virustotal.com/api/v3/analyses/{scan_id}'
    headers = {'x-apikey': api_key}

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            status = result['data']['attributes']['status']
            if status == 'completed':
                stats = result['data']['attributes']['stats']
                if stats['malicious'] == 0:
                    return "הקובץ בטוח"
                else:
                    return "הקובץ מסוכן"
            else:
                print("ממתין לסיום הסריקה...")
                time.sleep(10)
        else:
            print(f'Error fetching scan result: {response.status_code}\nResponse: {response.json()}')
            return "Error"

# פונקציה למעבר על כל הקבצים בתיקיה
def scan_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            scan_id = scan_file(file_path)
            if scan_id:
                result = check_scan_result(scan_id)
                print(f'File: {file_path} - {result}')

# קריאה לפונקציה שמתחילה את הסריקה
scan_folder(folder_path)
