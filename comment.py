import sys, os, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException


def login(driver, str_id, str_pw):
    driver.get("https://everytime.kr/login")
    driver.find_element_by_name("userid").send_keys(str_id)
    driver.find_element_by_name("password").send_keys(str_pw)
    driver.find_element_by_class_name("submit").click()
    print("login success")

def find_element_click(driver, by, expression):
    search_window = driver
    while True:
        try:
            web_element = search_window.find_element(by=by, value=expression)
            web_element.click()
            return True
        except Exception:
            pass
    return False

def make_article(title, text):
    driver.get("https://everytime.kr/370438")
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"container\"]/div[2]/a"))
        )
    except TimeoutException:
        pass

    driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/a").click()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"container\"]/div[2]/form/p[1]/input"))
        )
    except TimeoutException:
        pass
    driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/p[1]/input").send_keys(title)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"container\"]/div[2]/form/p[2]/textarea"))
        )
    except TimeoutException:
        pass
    driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/p[2]/textarea").send_keys(text)
    
    TF = find_element_click(driver=driver, by=By.CLASS_NAME, expression="submit")
    if TF is True:
        print("Wrote new article.")
    else:
        print("Failed to write new article.")

def comment(link_in=None):
    link = "https://everytime.kr/370438/v/133919434"
    if link_in is not None:
        link = link_in
    else:
        raise ValueError("Link input is needed.")
    
    driver.get(link)
    time.sleep(2)

    i = 0
    vote_save = ""

    while True:
        try:
            vote = driver.find_element_by_class_name("vote")  # 현재 vote 수 찾기
            vote = vote.text
            # vote_save = vote
            
            '''  Making error so that remarked.
            close = driver.find_element_by_class_name("close")  # "앱으로 이용해보세요" 팝업이 아래에 떠있는 경우 있는데 없애기
            if close is not None:
                close.click()
            '''
            
            if int(vote_save) != int(vote):
                try:
                    string = vote + "개"  # 댓글을 어떤 식으로 달지

                    driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/article/div/form/input").send_keys(string)  # 댓글 입력창 찾아서 string 쓰기
                    TF = find_element_click(driver=driver, by=By.CLASS_NAME, expression="submit")  # 댓글 입력 버튼 누르기
                    vote_save = vote  # 현재 vote 값으로 vote_save 저장하기

                    print("Likes, iterations, T/F : ", vote, i, TF)
                    i += 1
                    if TF is False:
                        driver.refresh()
                except UnexpectedAlertPresentException as e:  # 댓글을 너무 많이 달아서 팝업이 뜨면 확인 버튼 누르기
                    print(str(e))
                    obj = driver.switch_to_alert()
                    obj.accept()
        except UnexpectedAlertPresentException as e:  # 댓글을 너무 많이 달아서 팝업이 뜨면 확인 버튼 누르기
            print(str(e))
            obj = driver.switch_to_alert()
            obj.accept()
        except NoSuchElementException as e:  # 팝업으로 인해서 "vote"
            print(str(e))

        driver.refresh()
        time.sleep(2)
        # sleep을 통해서 얼마나 빠르게 돌건지 선택 가능한데, sleep(5)로 하면 약간 느린 것 같음.
        # sleep을 없애면 페이지가 로드되기 이전에 위에서 vote를 찾을 수 있기 때문에 implicit wait을 하거나
        # 그냥 time.sleep()을 사용하기는 해야함.


if __name__ == '__main__':
    # 웹드라이버 키기
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    try:
        driver = webdriver.Chrome('./chromedriver.exe', options=options)
        driver.maximize_window()
    except:
        pass
    try:
        if getattr(sys, 'frozen', False):
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            driver = webdriver.Chrome(chromedriver_path, options=options)
    except:
        pass


    # ID PW 입력하기
    str_id = "EVERYTIME_ID"
    str_pw = "EVERYTIME_PW"

    # Login to evertytime.
    login(driver, str_id, str_pw)

    # Make new article
    make_article(title="이 글의 좋아요 개수가 댓글로 작성됩니다.", text="좋아요를 눌러보세요.")

    # Comment the current number of Likes.
    comment()

    driver.quit()
