def bart_parse():
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc
    driver = uc.Chrome()

    u_name = 'grisasafronov219@gmail.com'
    pass_ = 'Gs20042912'

    driver.get("https://bard.google.com")

    # login
    driver.find_element(By.XPATH, '/html/body/chat-app/side-navigation/mat-sidenav-container/mat-sidenav-content/main/welcome-window/div/div/div/div[2]/button').click()
    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))).send_keys(u_name)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]').click()
    time.sleep(5)
    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))).send_keys(pass_)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]').click()

    # bart queries
    cnt = 0

    with open('rofls/test.txt', mode='r', encoding='utf-8') as f:
        data = f.readlines()

    while cnt <= len(data):
        query = str(f'''вот ссылка на товар: https://betaren.ru/catalog/sredstva-zashchity-rasteniy/gerbitsidy/acetal_pro/
Мне нужны 30 пар вопрос-ответ такого формата: "Вопрос: Каков химический класс "Азорро, КС"?
Ответ: "Азорро, КС" относится к химическим классам бензимидазолов и стробилуринов."
важно что информация для составления вопросов должна браться только с этой ссылки и больше ни с какого источника''')
        WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-0"]'))).send_keys(query)
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 100000).until(EC.element_to_be_clickable((By.XPATH, '/html/body/chat-app/side-navigation/mat-sidenav-container/mat-sidenav-content/main/chat-window/div[1]/div[2]/input-area/div/div/button'))))
        resp = WebDriverWait(driver, 1000000).until(EC.presence_of_element_located((By.XPATH, f'/html/body/chat-app/side-navigation/mat-sidenav-container/mat-sidenav-content/main/chat-window/div[1]/div[1]/infinite-scroller/div[{cnt+1}]/model-response/div/response-container/div'))).get_attribute('innerHTML')

        with open(f'rofls/test/{str(cnt)}.txt', mode='w+', encoding='utf-8') as f:
            f.write(resp + '\n' + data[cnt])

        cnt += 1

if True:
    bart_parse()