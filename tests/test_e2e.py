from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://127.0.0.1:5000"

def test_login_verify_redirect():
    browser = webdriver.Chrome()
    browser.get(URL + "/login")

    browser.find_element(By.NAME, "username").send_keys("hugoo")
    browser.find_element(By.NAME, "password").send_keys("Hugo@1234")
    browser.find_element(By.XPATH, "//button[text()='Login']").click()

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Your Tasks")
    )
    assert True
    browser.quit()

def test_create_task():
    browser = webdriver.Chrome()
    browser.get(URL + "/login")

    browser.find_element(By.NAME, "username").send_keys("hugoo")
    browser.find_element(By.NAME, "password").send_keys("Hugo@1234")
    browser.find_element(By.XPATH, "//button[text()='Login']").click()
    browser.get(URL + "/tasks/new")

    title = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "title")))
    title.send_keys("send tp")
    browser.find_element(By.XPATH, "//button[text()='Save']").click()

    tasks = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "task-item")))

    last_task = tasks[-1]
    header_div = last_task.find_element(By.CSS_SELECTOR, ".task-header > div:first-child")
    full_text = header_div.text.strip()
    for badge in ["Open", "Done", "Overdue"]:
        if full_text.endswith(badge):
            full_text = full_text[: -len(badge)].strip()

    title_text = full_text
    assert title_text == "send tp"

    browser.quit()

def test_toggle_task():
    browser = webdriver.Chrome()
    browser.get(URL + "/login")

    browser.find_element(By.NAME, "username").send_keys("hugoo")
    browser.find_element(By.NAME, "password").send_keys("Hugo@1234")
    browser.find_element(By.XPATH, "//button[text()='Login']").click()

    toggle_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//ul[@class='task-list']/li[1]//form/button")))
    toggle_button.click()

    task_list = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.task-list")))
    badge = task_list.find_element(By.XPATH, "./li[1]//span[contains(@class,'badge')]")

    assert badge.text in ["Done", "Open"]
    browser.quit()