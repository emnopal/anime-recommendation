import time
import os
import json

from utils.encoder import NpEncoder
from utils.profiling import timeit

@timeit
def convert_to_html(df, df2=None, path=f"{os.getcwd()}/output"):
    if not os.path.exists(path):
        os.makedirs(path)
    now = time.strftime("%Y%m%d-%H%M%S")
    name = f"{path}/temp-{now}.html"
    if df2 is None:
        df.to_html(name, index=False)
        print(f"Open Here: {name}")
    else:
        df0_html = '<table border="1" class="dataframe"><thead><tr style="text-align: right;"><th>MAL_ID</th><th>Name</th><th>Score</th><th>Genres</th><th>Synopsis</th><th>Type</th><th>Episodes</th><th>Premiered</th><th>Studios</th><th>Source</th><th>Rating</th><th>Ranked</th><th>Popularity</th><th>Favorites</th></tr></thead><tbody>'  # noqa
        for idx in df.index:
            df0_html += '<tr>'
            for cols in df.columns:
                df0_html += f'<td>{df[cols][idx]}</td>'
            df0_html += '</tr>'
        df0_html += '</tbody></table>'
        df1_html = '<table border="1" class="dataframe"><thead><tr style="text-align: right;"><th>MAL_ID</th><th>Name</th><th>Score</th><th>Genres</th><th>Synopsis</th><th>Type</th><th>Episodes</th><th>Premiered</th><th>Studios</th><th>Source</th><th>Rating</th><th>Ranked</th><th>Popularity</th><th>Favorites</th></tr></thead><tbody>'  # noqa
        for idx in df2.index:
            df1_html += '<tr>'
            for cols in df2.columns:
                df1_html += f'<td>{df2[cols][idx]}</td>'
            df1_html += '</tr>'
        df1_html += '</tbody></table>'
        df_html = f"<h1>Anime: </h1><br>{df0_html} <br> <h1>Similar anime: </h1><br>{df1_html}"  # noqa

        with open(name, 'w', encoding='utf-8') as f:
            f.writelines(df_html)
        print(f"Open Here: {name}")

@timeit
def convert_to_json(df, df2=None, path=f"{os.getcwd()}/output"):
    if not os.path.exists(path):
        os.makedirs(path)
    now = time.strftime("%Y%m%d-%H%M%S")
    name = f"{path}/temp-{now}.json"
    if df2 is None:
        df_json = {}
        df_json['anime'] = df.to_dict(orient='list')
        with open(name, 'w', encoding='utf-8') as outfile:
            json.dump(df_json, outfile, cls=NpEncoder)
        print(f"Open Here: {name}")
        return
    else:
        df_json = {
            "anime": {},
            "similar_anime": {}
        }
        df_json['anime'] = df.to_dict(orient='list')
        df_json['similar_anime'] = df2.to_dict(orient='list')
        with open(name, 'w', encoding='utf-8') as outfile:
            json.dump(df_json, outfile, cls=NpEncoder)
        print(f"Open Here: {name}")
        return

@timeit
def convert_to_json_api(df, df2=None):
    if df2 is None:
        df_json = {}
        df_json['anime'] = df.to_dict(orient='list')
        return df_json
    else:
        df_json = {
            "anime": {},
            "similar_anime": {}
        }
        df_json['anime'] = df.to_dict(orient='list')
        df_json['similar_anime'] = df2.to_dict(orient='list')
        return df_json
