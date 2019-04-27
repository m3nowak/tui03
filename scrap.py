import re
import sys
from contextlib import closing

from bs4 import BeautifulSoup

from common import load_json, save_json

DOW_TEXT_NUM_DICT = {
    'pn': 1,
    'wt': 2,
    'śr': 3,
    'cz': 4,
    'pt': 5,
}


def chunks(source, chunk_size):
    for i in range(0, len(source), chunk_size):
        yield source[i:i + chunk_size]


def main():
    with closing(open(sys.argv[1], 'r')) as raw_html:
        soup = BeautifulSoup(raw_html, 'lxml')

    uwagi_hide_list = soup.find_all('tr', class_='uwagi_hide')
    for uwagi_hide in uwagi_hide_list:
        uwagi_hide.extract()

    group_tag = soup.find_all('b', string=re.compile("Grupy zajęciowe"))[0]
    group_tag_parent = group_tag.parent
    info_table = group_tag_parent.find_all('table', recursive=False)[-2]
    info_tr_list = info_table.find_all('tr', recursive=False)[3:-1]

    group_repo = load_json(sys.argv[2])

    for line_1, line_2, line_3 in chunks(info_tr_list, 3):
        line_1_td_list = line_1.find_all('td', recursive=False)

        #print("Kod grupy: {}".format(line_1_td_list[0].text.strip()))
        group_code = line_1_td_list[0].text.strip()
        #print("Kod kursu: {}".format(line_1_td_list[1].text.strip()))
        course_code = line_1_td_list[1].text.strip()

        line_2_td_list = line_2.find_all('td', recursive=False)
        # print("Prowadzący: {}".format(
        #    re.sub(r'\s+', ' ', line_2_td_list[0].text.strip())))
        #profesor_name = re.sub(r'\s+', ' ', line_2_td_list[0].text.strip())

        line_3_table_td_list = line_3.find('table').find_all('td')
        time_list = [td.text for td in line_3_table_td_list]
        formatted_time_list = []

        for time_element in time_list:
            hours = re.findall(re.compile(r'\d\d:\d\d'), time_element)
            dow_text = time_element.strip()[:2]
            dow_num = DOW_TEXT_NUM_DICT[dow_text]
            ftw_dict = {
                'start': hours[0].replace(':', ''),
                'end': hours[1].replace(':', ''),
                'dow': dow_num
            }
            par_ind = time_element.strip()[3:5]
            if par_ind in ('TP', 'TN'):
                ftw_dict['par'] = 1 if par_ind == 'TN' else 2
            formatted_time_list.append(ftw_dict)

        if 'courses' not in group_repo:
            group_repo['courses'] = {}

        if course_code not in group_repo['courses']:
            course_dict = {}
            group_repo['courses'][course_code] = course_dict
        else:
            course_dict = group_repo['courses'][course_code]

        course_dict[group_code] = formatted_time_list

    save_json(sys.argv[2], group_repo)


if __name__ == "__main__":
    main()
