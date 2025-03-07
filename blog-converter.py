import re
import csv
import datetime
from urllib.parse import unquote

def parse_blog_data(text_content):
    """
    Parse the blog data from the text content and extract the relevant information.
    
    Args:
        text_content (str): The raw text content from the file.
        
    Returns:
        list: List of dictionaries containing the parsed blog data.
    """
    blog_entries = []
    current_date = None
    
    # Split the content by lines
    lines = text_content.split('<br>\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if line is a date
        if re.match(r'\d{4}-\d{2}-\d{2}', line):
            current_date = line
            i += 2  # Skip the separator line (dashes)
        
        # Check if line contains a blog entry
        elif '<a href=' in line:
            # Extract URL, title, and source using regex
            match = re.search(r'<a href="([^"]+)">(.+?)</a>:(.+)', line)
            if match:
                url = match.group(1)
                title = match.group(2)
                source = match.group(3).strip()
                
                # Create entry
                entry = {
                    'date': current_date,
                    'url': url,
                    'title': title,
                    'source': source
                }
                blog_entries.append(entry)
            
            i += 2  # Skip the separator line (dots)
        else:
            i += 1
    
    return blog_entries

def save_to_csv(blog_entries, output_file='blog_data.csv'):
    """
    Save the parsed blog entries to a CSV file.
    
    Args:
        blog_entries (list): List of dictionaries containing the parsed blog data.
        output_file (str): Name of the output CSV file.
    """
    if not blog_entries:
        print("No blog entries found.")
        return
    
    fieldnames = ['date', 'url', 'title', 'source']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(blog_entries[:100])
    
    print(f"Successfully wrote {len(blog_entries)} blog entries to {output_file}")

def main(input_file='index.html', output_file='blog_data.csv'):
    """
    Main function to read the input file, parse the blog data, and save it to a CSV file.
    
    Args:
        input_file (str): Name of the input text file.
        output_file (str): Name of the output CSV file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        blog_entries = parse_blog_data(text_content)
        save_to_csv(blog_entries, output_file)
        
        # Preview the CSV content
        print("\nCSV Preview (first 5 entries):")
        for entry in blog_entries[:5]:
            print(f"{entry['date']}, {entry['title']}, {entry['source']}")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

main()
