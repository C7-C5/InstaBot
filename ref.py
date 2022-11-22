from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from direct_users_list import direct_users_list

class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(2, 4))

        username_input = browser.find_element('name', 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element('name', 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(8)

    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(2, 5))

        hrefs = browser.find_elements(By.TAG_NAME, 'a')
        posts_urls = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element(By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")
                like_button.click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def xpath_exists(self, url):

        browser = self.browser

        try:
            browser.find_element(By.XPATH, url)
            exists = True
        except NoSuchElementException:
            exists = False
        return exists


    def put_direct_like(self, userpost):

        browser = self.browser

        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "//h2[@class='_aacl _aacr _aacw _aacx _aad6 _aadb']"

        if self.xpath_exists(wrong_userpage):
            print('No such post found, check URL')
            self.close_browser()
        else:
            print('Post found.')
            time.sleep(3)

            like_button = "//button//span//*[name()='svg' and @aria-label='Нравится']"
            browser.find_element(By.XPATH, like_button).click()
            print(f'Post {userpost} liked!')
            time.sleep(3)

            self.close_browser()

    def get_users_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "//h2[@class='_aacl _aacr _aacw _aacx _aad6 _aadb']"

        if self.xpath_exists(wrong_userpage):
            print('No such userpage found, check URL')
            self.close_browser()
        else:
            print('User found')
            time.sleep(5)

            posts_count = int(browser.find_element(By.CLASS_NAME, "_ac2a").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                posts_urls = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
                for url in posts_urls:
                    urls.append(url)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f'Iteration #{i} of {loops_count}')

        file_name = userpage.split('/')[-2]

        with open(f'{file_name}.txt', 'a') as file:
            for post_url in urls:
                file.write(post_url + '\n')

        set_post_urls = set(urls)
        set_post_urls = list(set_post_urls)
        with open(f'{file_name}_set.txt', 'a') as file:
            for url in set_post_urls:
                file.write(url + '\n')

    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_users_urls(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(4)

        browser.get(userpage)
        time.sleep(4)


        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()
            for url in urls_list[0:6]:
                try:
                    browser.get(url)
                    time.sleep(random.randrange(3, 6))

                    like_button = browser.find_elements(By.XPATH, "//div[@class='_abm0 _abl_']")[0]
                    like_button.click()
                    print(f'I liked post {url}')

                    time.sleep(random.randrange(80, 100))

                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # def download_userpage_content(self, userpage):
    #
    #     browser = self.browser
    #     self.get_users_urls(userpage)
    #     file_name = userpage.split('/')[-2]
    #     time.sleep(4)
    #
    #     browser.get(userpage)
    #     time.sleep(4)
    #
    #     img_src_urls = []
    #
    #     with open(f'{file_name}_set.txt') as file:
    #         urls_list = file.readlines()
    #         for url in urls_list[0:6]:
    #             try:
    #                 browser.get(url)
    #                 time.sleep(random.randint(3, 6))
    #
    #                 img_src = browser.find_elements(By.XPATH, "//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3']")[-1]
    #                 post_id = url.split('/')[2]
    #
    #                 if self.xpath_exists(img_src):
    #                     img_src_url = browser.find_element(By.XPATH, img_src).get_attribute('src')
    #                     img_src_urls.append(img_src_url)
    #
    #                     get_img = requests.get(img_src_url)
    #                     with open(f'{post_id}_img.jpg', 'wb') as img_file:
    #                         img_file.write(get_img.content)
    #
    #
    #                 else:
    #                     print('Something goes wrong!')
    #                     print(f'{img_src_url}, no such URL.')
    #
    #                 print(f'Content from {url} saved as .jpg!')
    #             except Exception as ex:
    #                 print(ex)
    #                 self.close_browser()
    #
    #         self.close_browser()
    #
    #     with open('img_src_urls.txt', 'a') as file:
    #         for url in img_src_urls:
    #             file.write(url + '\n')
    def get_all_followers(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split('/')[-2]

        if os.path.exists(f'{file_name}'):
            print(f'Directory {file_name} already exists')
        else:
            print(f'{file_name} directory created')
            os.mkdir(file_name)

        wrong_userpage = "//h2[@class='_aacl _aacr _aacw _aacx _aad6 _aadb']"

        if self.xpath_exists(wrong_userpage):
            print('No such userpage found, check URL')
            self.close_browser()
        else:
            print(f'User {file_name} found')
            time.sleep(5)

            followers_button = browser.find_element(By.XPATH, f"//a[@href='/{file_name}/followers/']")
            if ',' not in followers_button.text:
                followers_count = int(followers_button.text.split(' ')[0])
            else:
                followers_count = int(followers_button.text.split(' ')[0].replace(',', ''))
            print(f'Number of followers: {followers_count}')
            time.sleep(3)

            loops_count = int(followers_count / 12)
            print(f'Number of iterations: {loops_count}')

            time.sleep(3)

            followers_button.click()
            time.sleep(3)

            followers_ul = browser.find_element(By.XPATH, "//div[@class='_aano']")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randint(2, 5))
                    print(f'Iteration # {i}')

                all_urls = followers_ul.find_elements(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")

                for url in all_urls:
                    url = url.get_attribute('href')
                    followers_urls.append(url)
                    print(url)


                with open(f'{file_name}/{file_name}.txt', 'a') as file:
                    for link in followers_urls:
                        file.write(link + '\n')

                with open(f'{file_name}/{file_name}.txt') as file:
                    users_urls = file.readlines()

                    for user in users_urls[0:2]:
                        # try:
                        #     # try:
                        #     #     with open(f'{file_name}/{file_name}_subscribe_list.txt', 'a') as subscribe_list_file:
                        #     #         lines = subscribe_list_file.readlines()
                        #     #         if user in lines:
                        #     #             print(f'We are already subscribed {user}, move to next user!')
                        #     #             continue
                        #     # except Exception as ex:
                        #     #     print(ex)
                        #     #     self.close_browser()
                        #
                        #
                        # except Exception as ex:
                        #     print('File was not created!')


                        browser = self.browser
                        browser.get(user)
                        page_owner = user.split('/')[-2]

                        if self.xpath_exists("//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _acan _acap _acat _acaw _a6hd']"):

                            print("It is my own profile, iteration pass")
                        elif self.xpath_exists("//div[@class='_ab8w  _ab94 _ab97 _ab9h _ab9k _ab9p _ab9x _abcm']"):
                            print(f"Already subscribed on {page_owner}, iteration pass")
                        else:
                            time.sleep(random.randrange(4, 8))

                            if self.xpath_exists("//h2[@class='_aa_u']"):
                                try:
                                    follow_button = browser.find(By.XPATH, "//div[@class='_aacl _aaco _aacw _aad6 _aade']").click()
                                    print(f'Closed profile. Sent request to{page_owner} for subscription.')
                                except Exception as ex:
                                    print(ex)
                            else:
                                try:
                                    if self.xpath_exists("//div[@class='_ab8w  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']"):
                                        follow_button = browser.find_element(By.XPATH, "//div[@class='_aacl _aaco _aacw _aad6 _aade']").click()
                                        print(f'Subscribed on {page_owner}. Opened profile.')

                                except Exception as ex:
                                    print(ex)

                            with open(f'{file_name}/{file_name}_subscribe_list.txt', 'a') as subscribe_list_file:
                                subscribe_list_file.write(user)

                            time.sleep(random.randrange(7, 15))

            except Exception as ex:
                print(ex)
                self.close_browser()

    def send_direct_message(self, usernames='', message=''):

        browser = self.browser
        time.sleep(random.randrange(2, 4))

        direct_button = browser.find_element(By.XPATH, "//a[@href='/direct/inbox/?next=%2F']")

        direct_button_xpath = "//a[@href='/direct/inbox/?next=%2F']"

        time.sleep(random.randrange(2, 4))

        if not self.xpath_exists(direct_button_xpath):
            print('Direct button not found')
            self.close_browser()

        else:
            print('Sending message...')
            direct_button.click()

        time.sleep(4)

        if self.xpath_exists("//button[@class='_a9-- _a9_1']"):
            browser.find_element(By.XPATH, "//button[@class='_a9-- _a9_1']").click()
        time.sleep(random.randrange(2, 4))

        send_message_button = browser.find_element(By.XPATH, "//button[@class='_acan _acap _acas']")
        time.sleep(2)
        send_message_button.click()

        for user in usernames:

            to_input = browser.find_element(By.XPATH, "//input[@name='queryBox']")
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            users_list = browser.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9o  _ab9v _abcm']").find_element(By.TAG_NAME, 'button').click()
            time.sleep(random.randrange(2, 4))

        button_next = browser.find_element(By.XPATH, "//div[@class='_aagz']")
        time.sleep(2)
        button_next.click()
        time.sleep(4)

        if message:
            message_text_area = browser.find_element(By.TAG_NAME, "textarea")
            message_text_area.clear()
            message_text_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            message_text_area.send_keys(Keys.ENTER)

            print(f'Message for {usernames} sent successfully.')
            time.sleep(random.randrange(2, 4))

        self.close_browser()




my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.send_direct_message(direct_users_list, 'Hey! I am your husband! Show tits! (.)(.)')






