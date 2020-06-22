from importlib import reload
from selenium import webdriver
import os

import time

import libvis
import libvis.modules.installed as modules


os.environ['MOZ_HEADLESS'] = '1'

def test_init_instal(tmp_path):
    """
    1. Start the Libvis
    2. Test front with selenium
    """
    print("Starting Selenium...")
    browser = webdriver.Firefox()

    try:

        # 1.
        vis = libvis.Vis(ws_port=7700, vis_port=7000, debug=True)

        my_url = "http://example.com"
        m = modules.WebPage(addr=my_url)
        modname = m.name

        vis.vars.test = m

        # 2.
        browser.get('http://localhost:7000')
        # Sleep a bit to load everything
        time.sleep(0.2)
        html = browser.find_element_by_css_selector('html')
        assert 'widget' in html.get_attribute('outerHTML')

        widget = add_widget(browser, 'test')
        # Wait for libvis to answer. 
        # This is probably not the best way, since loading time may vary 
        # for complex visualisations or big data. 
        # May cause false negatives
        time.sleep(1.1)

        widget_html = widget.get_attribute('outerHTML')
        assert 'iframe' in widget_html
        print("Widget html", widget_html)


        test_root = widget.find_element_by_css_selector(
            f".vistype-{modname}")
        assert test_root
        root_html = test_root.get_attribute('outerHTML')
        print("root html", root_html)
        assert 'iframe' in root_html

        iframe = test_root.find_element_by_css_selector('iframe')
        assert my_url in iframe.get_attribute('outerHTML')

    finally:
        vis.stop()
        browser.quit()


def add_widget(browser, name):
    add_button = browser.find_element_by_class_name('add-widget')
    add_button.click()
    widget = browser.find_element_by_xpath(
        '(//*[@id="root"]/div/div[2]/div/div)[last()]'
    )
    varname_input = widget.find_element_by_xpath('.//input')
    varname_input.clear()
    varname_input.send_keys(name)
    return widget
