import sys
import os
import pandas as pd
import numpy as np

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

    perform_diff_check()


def perform_diff_check():
    main_dir = os.path.dirname(os.path.realpath(__file__))

    google_results = read_excel_data(file = main_dir+'/temp/data/GoogleMalwareResults.xlsx',sheet_name = 'Results(2016-2018)')
    android_results = read_excel_data(file = main_dir+'/temp/data/AndroidMalwareResults.xlsx',sheet_name = 'Results(2016-2018)')

    columns = ['title', 'date', 'url', 'matches', 'company', 'from_android_malware_results']
    combined_results = []
    urls = []

    for row in android_results:
        title = row[0]
        date = row[1]
        url = row[2]
        matches = row[3]
        company = row[4]
        if(not contains(url, urls)):
            urls.append(url)
            combined_results.append([title, date, url, matches, company, 'yes'])

    for row in google_results:
        title = row[0]
        date = row[1]
        url = row[2]
        matches = row[3]
        company = row[4]
        if(not contains(url, urls)):
            urls.append(url)
            combined_results.append([title, date, url, matches, company, 'no'])

    result_dataframe = pd.DataFrame(combined_results, columns = columns)

    print(result_dataframe)
    print('saving to ' + main_dir+'/temp/compare_results/output.xlsx')
    result_dataframe.to_excel(main_dir+'/temp/compare_results/output.xlsx')

def contains(url, urls):
    for item in urls:
        if (url == item):
            return True

    return False

def read_excel_data(file, sheet_name):
    columns = ['title', 'date', 'blog_url', 'matches', 'company']

    df = pd.read_excel(file, sheet_name)

    df['title'] = df['title'].apply(lambda l: l.rstrip())
    df['title'] = df['title'].apply(lambda l: l.lstrip())
    df['title'] = df['title'].apply(lambda l: l.strip())

    results = []

    for row in df.iterrows():
        title = row[1]['title']
        date = row[1]['date']
        blog_url = row[1]['blog_url']
        matches = row[1]['matches']
        company = row[1]['company']

        data = [title, date, blog_url, matches, company]
        results.append(data)

    return results


def diffResults():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    file_one_urls = []
    file_one = main_dir + '/temp/data/2016_to_2018_android_malware.txt'
    print(file_one)
    with open(file_one, 'r') as blogFile:
        row = blogFile.readlines()
        for url in row:
            if url:
                file_one_urls.append(url.strip())

    file_two_urls = []
    file_two = main_dir + '/temp/data/2016_to_2018_google_malware.txt'
    with open(file_two, 'r') as blogFile:
        row = blogFile.readlines()
        for url in row:
            if url:
                file_two_urls.append(url.strip())

    urls_in_both_sets = []
    unique_to_file_one = []
    unique_to_file_two = []

    for url in file_two_urls:
        if findMatch(url, file_one_urls):
            urls_in_both_sets.append(url)
        else:
            unique_to_file_two.append(url)

    for url in file_one_urls:
        if not findMatch(url, file_two_urls):
            unique_to_file_one.append(url)

    print('COMMON TO BOTH')
    print(urls_in_both_sets)
    print(len(urls_in_both_sets))
    print('------------')
    print('UNIQUE TO FILE ONE')
    print(unique_to_file_one)
    print(len(unique_to_file_one))
    print('------------')
    print('UNIQUE TO FILE TWO')
    print(unique_to_file_two)
    print(len(unique_to_file_two))

    results_file = open(main_dir + '/temp/compare_results/2016_to_2018_comparisons.txt', 'w+')

    results_file.truncate(0)
    results_file.write('UNIQUE TO ANDROID MALWARE:\n\n')

    for row in unique_to_file_one:
        results_file.write(row + '\n')

    results_file.write('UNIQUE TO GOOGLE MALWARE:\n\n')

    for row in unique_to_file_two:
        results_file.write(row + '\n')

    results_file.write('COMMON TO BOTH:\n\n')

    for row in urls_in_both_sets:
        results_file.write(row + '\n')


def findMatch(match_url, comparison_urls):
    for url in comparison_urls:
        if match_url == url:
            return True

    return False

if __name__== "__main__":
    main()
