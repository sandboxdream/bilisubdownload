import requests
import json
import os
import re
import sys
import time
from datetime import timedelta

# Constants
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

def load_cookies():
    """Load cookies from cookies.txt if it exists"""
    cookies = {}
    if os.path.exists("cookies.txt"):
        try:
            with open("cookies.txt", "r", encoding="utf-8") as f:
                cookie_str = f.read().strip()
                if cookie_str:
                    # Parse cookies string into dictionary
                    for item in cookie_str.split(';'):
                        if '=' in item:
                            key, value = item.strip().split('=', 1)
                            cookies[key] = value
            print("Cookies loaded successfully.")
        except Exception as e:
            print(f"Error loading cookies: {e}")
    else:
        print("No cookies.txt file found. Proceeding without cookies.")
    return cookies

def get_video_info(bv_id, cookies=None):
    """Get video information including cid for each part"""
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://www.bilibili.com/video/{bv_id}"
    }

    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"

    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()

    data = response.json()
    if data["code"] != 0:
        raise Exception(f"Failed to get video info: {data['message']}")

    return data["data"]

def get_subtitle_url(bv_id, cid, cookies=None):
    """Get subtitle URL for a specific video part"""
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://www.bilibili.com/video/{bv_id}"
    }

    # Use the updated API endpoint as specified in the issue description
    url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bv_id}&cid={cid}"

    print(f"Requesting subtitle info from: {url}")
    # Add a delay of 5 seconds before making the API request to avoid rate limiting
    time.sleep(5)
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()

    data = response.json()
    if data["code"] != 0:
        raise Exception(f"Failed to get subtitle info: {data['message']}")

    print(f"Subtitle data: {json.dumps(data['data']['subtitle'], ensure_ascii=False, indent=2)}")

    subtitle_list = data["data"]["subtitle"]["subtitles"]
    if not subtitle_list:
        print("No subtitles found in the API response.")
        return None

    # Get the first subtitle (usually the main one)
    subtitle_url = subtitle_list[0]["subtitle_url"]
    if not subtitle_url.startswith("http"):
        subtitle_url = "https:" + subtitle_url

    return subtitle_url

def get_subtitle_content(subtitle_url, cookies=None):
    """Get subtitle content from the subtitle URL"""
    headers = {
        "User-Agent": USER_AGENT
    }

    # Add a delay of 5 seconds before making the API request to avoid rate limiting
    time.sleep(5)
    response = requests.get(subtitle_url, headers=headers, cookies=cookies)
    response.raise_for_status()

    return response.json()

def convert_to_srt(subtitle_json):
    """Convert subtitle JSON to SRT format"""
    srt_content = ""

    for i, item in enumerate(subtitle_json["body"], 1):
        start_time = timedelta(seconds=item["from"])
        end_time = timedelta(seconds=item["to"])

        # Format time as HH:MM:SS,mmm
        start_str = str(start_time).replace(".", ",")
        if "." not in str(start_time):
            start_str += ",000"

        end_str = str(end_time).replace(".", ",")
        if "." not in str(end_time):
            end_str += ",000"

        # Ensure proper formatting with leading zeros
        if len(start_str.split(":")[0]) == 1:
            start_str = "0" + start_str
        if len(end_str.split(":")[0]) == 1:
            end_str = "0" + end_str

        srt_content += f"{i}\n{start_str} --> {end_str}\n{item['content']}\n\n"

    return srt_content

def save_subtitle(subtitle_json, output_path_json, output_path_srt):
    """Save subtitle in both JSON and SRT formats"""
    # Save JSON
    with open(output_path_json, "w", encoding="utf-8") as f:
        json.dump(subtitle_json, f, ensure_ascii=False, indent=2)

    # Save SRT
    srt_content = convert_to_srt(subtitle_json)
    with open(output_path_srt, "w", encoding="utf-8") as f:
        f.write(srt_content)

def process_bv_id(bv_id, cookies):
    """Process a single BV ID to download its subtitles"""
    if not bv_id.startswith("BV"):
        print(f"Invalid BV ID format: {bv_id}. It should start with 'BV'. Skipping.")
        return False

    try:
        # Create output directory
        output_dir = f"output_{bv_id}"
        os.makedirs(output_dir, exist_ok=True)

        # Get video information
        print(f"Getting information for video {bv_id}...")
        video_info = get_video_info(bv_id, cookies)

        # Check if it's a multi-part video
        if len(video_info["pages"]) > 1:
            print(f"This is a multi-part video with {len(video_info['pages'])} parts.")
        else:
            print("This is a single-part video.")

        # Process each part
        for i, page in enumerate(video_info["pages"], 1):
            cid = page["cid"]
            part_title = page["part"]
            print(f"Processing part {i}: {part_title} (CID: {cid})...")

            # Get subtitle URL
            subtitle_url = get_subtitle_url(bv_id, cid, cookies)
            if not subtitle_url:
                print(f"No subtitle found for part {i}.")
                continue

            # Get subtitle content
            subtitle_json = get_subtitle_content(subtitle_url, cookies)

            # Save subtitle
            output_path_json = os.path.join(output_dir, f"part_{i}_{cid}.json")
            output_path_srt = os.path.join(output_dir, f"part_{i}_{cid}.srt")
            save_subtitle(subtitle_json, output_path_json, output_path_srt)

            print(f"Subtitle for part {i} saved to {output_path_json} and {output_path_srt}")

        print(f"All subtitles have been downloaded to the {output_dir} directory.")
        return True

    except Exception as e:
        print(f"An error occurred while processing {bv_id}: {e}")
        return False

def read_bv_ids_from_file(file_path):
    """Read BV IDs from a text file, one per line"""
    bv_ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace and skip empty lines
                bv_id = line.strip()
                if bv_id:
                    bv_ids.append(bv_id)
        return bv_ids
    except Exception as e:
        print(f"Error reading BV IDs from file {file_path}: {e}")
        return []

def print_usage():
    """Print usage instructions"""
    print("Bilibili Subtitle Downloader")
    print("Usage:")
    print("  1. Interactive mode: python main.py")
    print("  2. Command line mode: python main.py BV1Jm421p7RV [BV2xxx...]")
    print("  3. File mode: python main.py -f bv_ids.txt")
    print("")
    print("Examples:")
    print("  python main.py BV1Jm421p7RV")
    print("  python main.py -f my_videos.txt")

def main():
    # Load cookies
    cookies = load_cookies()

    # Check command line arguments
    if len(sys.argv) == 1:
        # Interactive mode
        print("=== Bilibili Subtitle Downloader (Interactive Mode) ===")
        bv_id = input("Please enter the BV ID (e.g., BV1Jm421p7RV): ")
        process_bv_id(bv_id, cookies)
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        # File mode
        file_path = sys.argv[2]
        print(f"=== Bilibili Subtitle Downloader (File Mode) ===")
        print(f"Reading BV IDs from file: {file_path}")

        bv_ids = read_bv_ids_from_file(file_path)
        if not bv_ids:
            print(f"No valid BV IDs found in {file_path}. Exiting.")
            return

        print(f"Found {len(bv_ids)} BV IDs to process.")

        success_count = 0
        for i, bv_id in enumerate(bv_ids, 1):
            print(f"\nProcessing BV ID {i}/{len(bv_ids)}: {bv_id}")
            if process_bv_id(bv_id, cookies):
                success_count += 1

        print(f"\nProcessing completed. Successfully processed {success_count}/{len(bv_ids)} BV IDs.")
    else:
        # Command line mode with direct BV IDs
        if sys.argv[1] in ["-h", "--help"]:
            print_usage()
            return

        print(f"=== Bilibili Subtitle Downloader (Command Line Mode) ===")
        bv_ids = sys.argv[1:]

        success_count = 0
        for i, bv_id in enumerate(bv_ids, 1):
            print(f"\nProcessing BV ID {i}/{len(bv_ids)}: {bv_id}")
            if process_bv_id(bv_id, cookies):
                success_count += 1

        print(f"\nProcessing completed. Successfully processed {success_count}/{len(bv_ids)} BV IDs.")

if __name__ == "__main__":
    main()
