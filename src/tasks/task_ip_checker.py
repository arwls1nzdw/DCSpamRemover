import time
from logging import getLogger
from urllib.parse import urlparse, urlunparse

from selenium.webdriver.common.by import By

import dc
import webdriver
from common import *
from config import get_config

logger = getLogger()


def task():
    driver = webdriver.create()

    gall_id = get_config().get('gallery', 'id')
    gall_url = urlparse(f"https://gall.dcinside.com/mgallery/board/lists?id={gall_id}")

    last_pid = 0
    while True:
        driver.get(urlunparse(gall_url))

        time.sleep(5)

        posts = driver.find_elements(By.CSS_SELECTOR, 'tr.us-post[data-no]')
        posts = map(lambda p: dc.DCPostTR(p), posts)
        posts = filter(lambda p: p.postId > last_pid, posts)
        posts = filter(lambda p: p.writer_uid is None, posts)
        posts = filter(lambda p: p.post_type != "icon_notice", posts)
        posts = list(posts)

        for p in posts:
            log_post("IP Check", p)

        if len(posts) > 0:
            last_pid = max(map(lambda p: p.postId, posts))

        time.sleep(30)
