import time
import csv
import datetime
import traceback
import unidecode
from selenium import webdriver

def generate_file_name(title):
	title_url = title#.lower()
	title_url = title_url.replace(' ', '-').replace('.', '-').replace(',', '-').replace('!', '-').replace('?', '-').replace("'", '-').replace('"', '-').replace('+', '-').replace(':', '-').replace('--', '-').replace('--', '-')

	return title_url

def extact_csv_file(search_word, apartment_detail, datetime_now):
	with open(generate_file_name(search_word)+'_results_' + datetime_now + '.csv', 'a', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(apartment_detail)

def get_apartment_image_urls(driver,sleep):
	photos = driver.find_elements_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[1]/div/div/a/div[1]')
	photo_list = []

	for photo in photos:
		try:
			if len(photo.get_attribute('style').split('url("')[1][:-3]) > 10:
				photo_list.append(photo.get_attribute('style').split('url("')[1][:-3])
		except:
			continue
	driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-header.white-foreground > div:nth-child(1) > button.section-header-button.section-header-back-button.noprint.maps-sprite-common-arrow-back-white').click()
	
	print("Apartment Images  Page analysed")
	print('Waiting', sleep)
	time.sleep(sleep)
	
	return photo_list

def get_apartment_detail(driver,sleep, sleep_little, sleep_much):
	apartment_detail = []
	try:
		address = driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div:nth-child(7) > div > div.section-info-line > span.section-info-text > span.widget-pane-link').text
	except:
		address = None
	try:
		address_plus = driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div:nth-child(8) > div > div.section-info-line > span.section-info-text > span.widget-pane-link').text
	except:
		address_plus = None
	try:
		web_site = driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-info.section-info-hoverable.section-info-underline > div > div.section-info-line > span.section-info-text > span.widget-pane-link').text
	except:
		web_site = None
	try:		
		phone = driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div:nth-child(13) > div > div.section-info-line > span.section-info-text > span.widget-pane-link').text
	except:
		phone = None
	# photo click
	photos = ''
	try:
		driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header.white-foreground > button.section-hero-header-hero.widget-pane-fading.widget-pane-fade-in.section-hero-header-hero-clickable').click()
		print('Getting Photos')
		print('Waiting', sleep)
		time.sleep(sleep)
		for image in get_apartment_image_urls(driver,sleep):
			photos += image + '\n'
	except:
		# print(traceback.format_exc())
		photos = 'No Have Image'
		print(photos)

	print('Go To Back')
	driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > button > span').click()

	apartment_detail.append(address)
	apartment_detail.append(address_plus)
	apartment_detail.append(web_site)
	apartment_detail.append(phone)
	apartment_detail.append(photos)

	# print(apartment_detail)
	print("Apartment Detail Page analysed")
	return apartment_detail



def get_apartments(search_word, driver, sleep, sleep_little, sleep_much, datetime_now):
	# apartments = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[2]/h3[contains(@class, "section-result-title")]')
	apartments = driver.find_elements_by_class_name('section-result-title')
	
	apartment_list = []
	for i in range(len(apartments)):
		apartment_list.append(apartments[i].text)


	for i in range(len(apartments)):
		# print('Apartment -- ', apartments[i].text)
		apartment_detail = []
		try:
			category = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[' + str(2*i+1) +']/div[1]/div[1]/div[2]/span[4]').text
		except:
			category = None
		try:	
			review = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[' + str(2*i+1) +']/div[1]/div[1]/div[1]/div[2]/span[3]/span[1]/span').text
		except:
			review = None
		try:
			review_count = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[' + str(2*i+1) +']/div[1]/div[1]/div[1]/div[2]/span[3]/span[2]').text[1:-1]
		except:
			review_count = None
		try:
			price = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[' + str(2*i+1) +']/div[1]/div[1]/div[1]/div[3]').text
		except:
			price = None
		apartment_detail.append(apartment_list[i])
		apartment_detail.append(category)
		apartment_detail.append(review)
		apartment_detail.append(review_count)
		apartment_detail.append(price)

		driver.find_elements_by_class_name('section-result-title')[i].click()
		print('Go to Application Detail Page')
		print('Waiting', sleep)
		time.sleep(sleep)
		for detail in get_apartment_detail(driver,sleep, sleep_little, sleep_much):
			apartment_detail.append(detail)
		extact_csv_file(search_word, apartment_detail, datetime_now)
		print('Name:', apartment_detail[0], 'Category:', apartment_detail[1], 'Review:', apartment_detail[2], 'Review Count:', apartment_detail[3], 'Price:', apartment_detail[4], 'Address:',apartment_detail[5], 'Address Plus:',apartment_detail[6], 'Website:', apartment_detail[7],'Phone:', apartment_detail[8],'Photos:', apartment_detail[9])
		print('Waiting', sleep)
		time.sleep(sleep)




def scrape_apartment(search_word):
	# search_word = "Baku, Azerbaijan"
	sleep_little = 3
	sleep = 15
	sleep_much = 25
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference('permissions.default.image', 2)
	firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
	# driver = webdriver.Firefox(firefox_profile=firefox_profile)
	driver = webdriver.Firefox()
	# UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
	# PHANTOMJS_ARG = {'phantomjs.page.settings.userAgent': UA}
	# driver = webdriver.PhantomJS(desired_capabilities=PHANTOMJS_ARG)
	print("Page opened ...")

	driver.get('https://google.com/maps')
	driver.find_element_by_css_selector('#searchboxinput').send_keys('apartments near ' + search_word)
	print('Waited', sleep_little)
	time.sleep(sleep_little)
	driver.find_element_by_css_selector('#searchbox-searchbutton').click()
	print('Searching nearly apartments in', search_word)
	
	print('Waited', sleep_much)
	time.sleep(sleep_much)
	print('Founded Apartments nearly', search_word)
	datetime_now = str(datetime.datetime.now())
	apartment_detail = ['Name', 'Category', 'Review', 'Review Count', 'Price', 'Address', 'Address Plus', 'Website', 'Phone', 'Photos']
	extact_csv_file(search_word, apartment_detail, datetime_now)
	while not 'n7lv7yjyC35__button-disabled' in driver.find_element_by_css_selector('#n7lv7yjyC35__section-pagination-button-next').get_attribute('class'):
		get_apartments(search_word, driver, sleep, sleep_little, sleep_much, datetime_now)
		print('Apartment analysed')
		driver.find_element_by_css_selector('#n7lv7yjyC35__section-pagination-button-next').click()
		print('Waited')
		time.sleep(sleep)

	driver.close()

