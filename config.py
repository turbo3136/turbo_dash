import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'static/')

LOGO_PATH = '/static/plotly_logo.png'  # can't use this for some reason: os.path.join(STATIC_DIR, 'plotly_logo.png')
HOMEPAGE_IMG_LINK = '/static/xkcd_homepage.png'
FOUROHFOUR_IMG_LINK = '/static/xkcd_fourohfour.png'
