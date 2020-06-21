from importlib import reload
from selenium import webdriver
import os

import time

import libvis_mods
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
        print("Installed modules:", libvis_mods.installed())

        # 1.
        vis = libvis.Vis(ws_port=7700, vis_port=7000, debug=True)
        m = modules.WebPage(addr='https://example.com')
        modname = m.name

        vis.vars.test = m

        # 2.
        browser.get('http://localhost:7000')

        widget = add_widget(browser, 'test')
        # Wait for libvis to answer. 
        # This is probably not the best way, since loading time may vary 
        # for complex visualisations or big data. 
        # May cause false negatives
        time.sleep(0.1)
        test_root = widget.find_element_by_xpath(
            f".//*[@class=\"{modname}-presenter\"]")
        assert test_root

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
