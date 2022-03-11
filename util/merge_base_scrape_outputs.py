import pandas as pd
import os
import sys

scrape_results = ['Blog_Scrape_for_Android_Malware.xlsx', 'Blog_Scrape_for_Google_Malware.xlsx', 'Blog_Scrape_for_Play_Store_Malware.xlsx', 'Blog_Scrape_for_Playstore_Malware.xlsx']
sheets_to_merge = ['Malware Details (2016+2017)', 'Malware Details (2016+2017) - E', 'Malware Details (2019)']
blogs_already_done = ['Google_Or_Android_Malware.xlsx']

columns = ['title', 'date', 'blog_url', 'matches', 'company']
def main():
    main_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

    blogs_read = pd.read_excel(os.path.join(main_dir, 'temp', 'BlogsAlreadyDone.xlsx'), sheet_name = 'Tag matching')
    blogs_checked = pd.read_excel(os.path.join(main_dir, 'temp', 'blog_scrape_output', 'BlogsLeftToRead.xlsx'))

    urls_read = set()
    urls_checked = set()

    for url in blogs_checked['blog_url'].values:
        urls_checked.add(url.strip())

    for url in blogs_read['url'].values:
        urls_read.add(url.strip())

    urls_for_company = {}

    for root, dirs, files in os.walk(os.path.join(main_dir, 'temp', 'base_urls_for_keywords')):
        for file_name in files:
            if file_name.endswith('.txt'):
                with open(os.path.join(root, file_name)) as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]

                    if file_name not in urls_for_company:
                        urls_for_company[file_name] = set()

                    for line in content:
                        if line not in urls_read and line not in urls_checked:
                            urls_for_company[file_name].add(line)

    download_directory = os.path.join(main_dir, 'temp', 'base_scrape_output')
    for key in urls_for_company:
        print(key)

        file = open(os.path.join(download_directory, key), 'w+')
        file.truncate(0)

        for url in urls_for_company[key]:
            file.write(url + '\n')

if __name__== "__main__":
    main()
