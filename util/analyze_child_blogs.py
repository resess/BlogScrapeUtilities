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

    blog_file_path = os.path.join(main_dir, 'temp', 'BlogSheet.xlsx')

    url_list = set()

    df = pd.DataFrame()
    for sheet in sheets_to_merge:
        sheet_df = pd.read_excel(blog_file_path, sheet_name=sheet)
        df = df.append(sheet_df, ignore_index = True)

    for url in df['child blog url'].values:
        url_list.add(url)

    urls_from_crawler = set()

    for root, dirs, files in os.walk(os.path.join(main_dir, 'temp', 'base_urls_for_keywords')):
        for file_name in files:
            if file_name.endswith('.txt'):
                with open(os.path.join(root, file_name)) as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]

                    for line in content:
                        urls_from_crawler.add(line)

    for url in url_list:
        if url not in urls_from_crawler:
            print(url)

if __name__== "__main__":
    main()
