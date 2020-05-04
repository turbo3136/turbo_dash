from app import app
from turbo_dash import turbo_dash

from config import LOGO_PATH, HOMEPAGE_IMG_LINK


td = turbo_dash(
    app_to_callback=app,
    layout_template='homepage',
    turbo_header_logo_file_path=LOGO_PATH,
    turbo_header_links_list=[
        {'href': '/app1', 'text': 'app1'},
        {'href': '/app2', 'text': 'app2'},
    ],
    turbo_img_link=HOMEPAGE_IMG_LINK,
)

layout = td.layout
td.callbacks
