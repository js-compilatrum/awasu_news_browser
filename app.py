import arrow
import flask
from flask import render_template, redirect, url_for
from flask import request
from flask import send_from_directory
import json
import webbrowser

from config import LOCALHOST_URL
from config import NEWS_PER_PAGE
from config import OPEN_IN_BROWSER_EVERYTIME
from config import OUTPUT_DIR
from config import PUB_DIR
from manipulators import AwasuDataProcessor
from os import path

VER = "0.3.1A.1"


def _jinja2_filter_df_to_pxsize(df):
    """
    Get DataFrame size to calculate table height
    :param df: source Pandas DataFrame
    :return: size in pixels
    """
    height_row = 27  # px
    headline_row = 40  # px
    size_df = len(df)
    # size_df = NEWS_PER_PAGE
    count_channels = len(set(df['Channel Name']))
    px_size = (size_df * height_row) + (count_channels * headline_row)

    return px_size


def _jinja2_filter_repair_pl_chars(text):
    """
    Replace wrong character with correct PL
    :param text:
    :return:
    """
    char_map = {'Ä…': "ą",
                'ĹĽ': "ż",
                'Ĺ›': "ś",
                'Ä‡': "ć"}

    for wrong, correct in char_map.items():
        text = text.replace(wrong, correct)

    return text

def open_in_browser():
    if OPEN_IN_BROWSER_EVERYTIME:
        print(f'Opening in browser {LOCALHOST_URL}')
        webbrowser.open(LOCALHOST_URL)

app = flask.Flask(__name__)
app.jinja_env.filters['df_to_pxsize'] = _jinja2_filter_df_to_pxsize
app.jinja_env.filters['repair_pl_chars'] = _jinja2_filter_repair_pl_chars
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # CSS change load at the time of run
awasu = AwasuDataProcessor()

MENU_FOLDERS = awasu.main_folders()
print(f'MAIN FOLDERS:\n{MENU_FOLDERS}')


@app.route('/')
def index_menu():
    news_data = awasu.get_news()
    count_articles = len(news_data)
    count_channels = len(news_data.groupby('Channel Name').count())
    return render_template('nav/main.html',
                           menu_folders=MENU_FOLDERS,
                           count_articles=count_articles,
                           count_channels=count_channels,
                           ver=VER
                           )


@app.route('/add-article', methods=['POST'])
def add_article():
    if request.method == "POST":
        art_data = request.get_json()
        last_art = f"{art_data['channel']}<br>'<i>{art_data['title']}</i><br><sub>{art_data['published']}</sub>"
        new_to_art_list = art_data
        del new_to_art_list['view']

        awasu.add_to_selected(new_to_art_list)
        count = len(awasu.get_selected_arts())
        print(awasu.get_selected_arts())

    return json.dumps({'status': 'OK',
                       'info': last_art,
                       'count': count})


@app.route('/delete-art/<art_code>', methods=['POST'])
def del_article(art_code):
    awasu.remove_from_selected(art_code)
    return render_template('packs/selected_articles.html',
                           menu_folders=awasu.main_folders(),
                           selected_arts=awasu.get_selected_arts())


@app.route('/selected-arts')
def selected_arts():
    return render_template('packs/selected_articles.html',
                           menu_folders=awasu.main_folders(),
                           selected_arts=awasu.get_selected_arts())


@app.route('/export-selected-2txt')
def export_selected_2_txt():
    export_filename = f'kindle_urls_{arrow.now().format("YYYY.MM.DD_HH.mm")}.txt'
    export_dir = path.join(PUB_DIR, export_filename)
    print(export_dir)

    selected_urls = awasu.get_selected_arts()['url']  # DataFrame from class
    final_links = ""

    for link in selected_urls:
        final_links += link

    with open(export_dir, mode="w", encoding="utf8") as filedata:
        filedata.write(final_links)

    return send_from_directory(app.static_folder, export_filename)


@app.route('/awasu_update')
def awasu_update():
    awasu.update()
    return redirect('/')


@app.route('/save-selected')
def save_selected():
    output_path = OUTPUT_DIR
    date_and_time = str(arrow.now().format('YYYY-MM-DD HH_mm')).split(' ')

    export_filename = f"kindle_url_{date_and_time[0]}.hour_{date_and_time[1]}.txt"
    export_filename_csv = export_filename.replace('.txt', '.csv')
    export_path = path.join(output_path, export_filename)

    df_selected = awasu.get_selected_arts()
    links = df_selected['url']
    url_to_save = ""

    for url in links:
        url_to_save += url + '\n'

    with open(export_path, mode='w', encoding='utf8') as filedata:
        filedata.write(url_to_save)

    df_selected.to_csv(path.join(output_path, export_filename_csv))

    return redirect(url_for('index_menu'))


@app.route('/set-global-limit/<limit>')
def limit_news_count(limit):
    awasu.set_global_limit(limit)
    print(f"Set GLOBAL limit to [{limit}] per channel")
    return redirect(url_for('index_menu'))


@app.route('/remove-global-limit')
def remove_limit_news_view():
    awasu.remove_global_limit()
    print("GLOBAL limit removed!")
    return redirect(url_for('index_menu'))


@app.route('/paginator/<mode>/<option>/<page>')
def show_page(mode, option, page):
    page_size = NEWS_PER_PAGE
    page = int(page)
    show_paginator = False

    if page == 0:
        page = 1

    news_data = awasu.filter_articles(mode=mode, option=option)
    size = len(news_data.articles_data)
    indexes = news_data.indexes
    page = int(page)
    start_loc = (page - 1) * NEWS_PER_PAGE
    end_loc = page * page_size

    articles_to_read = size - end_loc
    count_pages = round(size / NEWS_PER_PAGE)

    if end_loc > size:
        end_loc = indexes[len(indexes) - 1]
    if size > NEWS_PER_PAGE:
        show_paginator = True

    prev_page = page
    next_page = page + 1

    if next_page > count_pages:
        next_page = page

    df_for_page = news_data.articles_data.iloc[start_loc:end_loc].dropna(axis=0, how='all')
    df_for_page = df_for_page.drop_duplicates(['Item URL'])
    df_for_page = df_for_page.sort_values(by=['Channel Name', 'Published'], ascending=[True, False])
    showed_articles = df_for_page.count()

    return render_template('skeleton.html',
                           exist_data=news_data.exist,
                           menu_folders=MENU_FOLDERS,
                           articles_data=df_for_page,
                           df_size= news_data.count,
                           paginator_mode=mode,
                           paginator_option=option,
                           page=prev_page,
                           paginator_page=next_page,
                           showed_articles=showed_articles,
                           show_paginator=show_paginator,
                           articles_to_read=articles_to_read,
                           count_pages=count_pages
                           )


if __name__ == '__main__':
    open_in_browser()
    app.run()
