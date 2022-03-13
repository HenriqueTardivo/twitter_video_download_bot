from  selenium import webdriver
import validators
import tweepy
import apikeys

PATH_CHROME = "C:\Program Files (x86)\chromedriver.exe"

auth = tweepy.OAuthHandler(apikeys.API_KEY,apikeys.API_SECRET)
auth.set_access_token(apikeys.ACCESS_TOKEN,apikeys.API_SECRET)
api = tweepy.API(auth=auth, wait_on_rate_limit=True)

async def downloadUrl(url):
    driver = webdriver.Chrome(PATH_CHROME)
    driver.get("https://twittervideodownloader.com/")
    driver.find_element_by_class_name("input-group-field").send_keys(url)
    driver.find_element_by_class_name("button").click()
    driver.find_element_by_xpath("/html/body/div[2]/div/center/div[6]/div[1]/a").click()
    print(driver.current_url)
    return driver.current_url

class MyStreamListener(tweepy.Stream):
    async def on_status(self, status):
        print(status)
        if validators.url(status.text):
            urlDownload = await downloadUrl(status.text)
            api.update_status('@' + status.user.screen_name + ' ' + urlDownload , in_reply_to_status_id=status.id )

stream = MyStreamListener(apikeys.API_KEY,apikeys.API_SECRET,apikeys.ACCESS_TOKEN,apikeys.ACCESS_TOKEN_SECRET)
stream.filter(track="@bolsominion_cry")




