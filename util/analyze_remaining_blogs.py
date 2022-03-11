import pandas as pd
import os
import sys

scrape_results = ['Blog_Scrape_for_Android_Malware.xlsx', 'Blog_Scrape_for_Google_Malware.xlsx', 'Blog_Scrape_for_Play_Store_Malware.xlsx', 'Blog_Scrape_for_Playstore_Malware.xlsx']
blogs_already_done = ['Google_Or_Android_Malware.xlsx']
years_to_include = ['2016', '2017', '2018']

columns = ['title', 'date', 'blog_url', 'matches', 'company']
def main():
    main_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

    blog_file_dir = os.path.join(main_dir, 'temp', 'blog_scrape_output')

    url_exclude_list = set()

    #create exclude url list
    for blog_file in blogs_already_done:
        blog_file_path = os.path.join(blog_file_dir, blog_file)
        df = pd.read_excel(blog_file_path, sheet_name='All Companies')

        for url in df['blog_url'].values:
            url_exclude_list.add(url)

    blogs_to_do_df = pd.DataFrame(columns=columns)

    for blog_file in scrape_results:
        blog_file_path = os.path.join(blog_file_dir, blog_file)
        df = pd.read_excel(blog_file_path, sheet_name='All Companies')

        for url in df['blog_url'].values:
            if url not in url_exclude_list:
                url_exclude_list.add(url)

                row = df[df['blog_url'] == url]

                year = str(row['date'].values[0])[0:4]

                if year in years_to_include:
                    blogs_to_do_df = blogs_to_do_df.append(row[columns], ignore_index = True)

    blogs_to_do_df.to_excel(os.path.join(main_dir, 'temp', 'blogs_to_do.xlsx'))

if __name__== "__main__":
    main()
