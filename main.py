from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

TIMEOUT_SECONDS = 60

# ----------------------- Enter parameters here ----------------------------
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"

# this is all fridays in jul - sept. add/remove/modify as needed
DATES = [
  ("Jul", "2nd"), 
  ("Jul", "9th"),
  ("Jul", "16th"),
  ("Jul", "23rd"),
  ("Jul", "30th"),
  ("Aug", "6th"),
  ("Aug", "13th"),
  ("Aug", "20th"),
  ("Aug", "27th"),
  ("Sep", "3rd")]

NUMNIGHTS = "2"

PARTYSIZE = "2"

# The names need to match exactly with the link names!
CAMPGROUND = "Two Jack Lakeside"
CAMPGROUNDAREAS = ["Two Jack Lakeside 1-13", "Two Jack Lakeside 14-35", "Two Jack Lakeside 36-74"]
# ----------------------- End parameters ----------------------------------

def clickReserve(dateChoiceIdx, campgroundAreaIdx):
  print("Trying " + DATES[dateChoiceIdx][0] + " " + DATES[dateChoiceIdx][1] + " for " + CAMPGROUNDAREAS[campgroundAreaIdx])
  driver.find_element_by_id("MainContentPlaceHolder_ListLink").click()
  waitPageLoadForId("viewPort", TIMEOUT_SECONDS)
  driver.find_element_by_link_text(CAMPGROUNDAREAS[campgroundAreaIdx]).click()
  waitPageLoadForId("viewPort", TIMEOUT_SECONDS)
  reserveLinks = driver.find_elements_by_link_text("Reserve!")
  if(len(reserveLinks) == 0):
    return False
  print(len(reserveLinks) + " available!")
  random.choice(reserveLinks).click()
  return True

def selectDropdown(dropdownId, visibleText):
  dropdown = Select(driver.find_element_by_id(dropdownId))
  dropdown.select_by_visible_text(visibleText)
  while(dropdown.first_selected_option.text != visibleText):
    time.sleep(0.2)

def waitPageLoadForId(elementId, seconds):
  WebDriverWait(driver, seconds).until(
      EC.presence_of_element_located((By.ID, elementId))
  )

def signIn():
  login = driver.find_element_by_id("LoginView1_SignIn")
  login.click()

  driver.find_element_by_id("MainContentPlaceHolder_btnGCKeyLogIn").click()
  driver.find_element_by_id("token1").send_keys(USERNAME)
  driver.find_element_by_id("token2").send_keys(PASSWORD)
  driver.find_element(By.XPATH, '//button[text()="Sign In"]').click()
  driver.find_element_by_id("continue").click()


# main driver code
driver = webdriver.Firefox()
driver.implicitly_wait(1)
driver.get("https://reservation.pc.gc.ca/Banff/TwoJackLakeside?List")

signIn()

selectDropdown("selEquipmentSub", "Small Tent")
selectDropdown("selPartySize", PARTYSIZE)
selectDropdown("selNumNights", NUMNIGHTS)

isAckMessage = False
campgroundAreaIdx = 0
dateChoiceIdx = 0
selectDropdown("selArrMth", DATES[0][0])
selectDropdown("selArrDay", DATES[0][1])

driver.close()

while(True):
  while(clickReserve(dateChoiceIdx, campgroundAreaIdx) == False and dateChoiceIdx < len(DATES)):
    print("No campgrounds in " + CAMPGROUNDAREAS[campgroundAreaIdx])
    selectDropdown("selNumNights", "2")
    campgroundAreaIdx += 1
    if(campgroundAreaIdx == len(CAMPGROUNDAREAS)):
      campgroundAreaIdx = 0
      dateChoiceIdx += 1
      if(dateChoiceIdx == len(DATES)):
        print("No campsites in date range :(")
        exit()
      else:
        selectDropdown("selArrMth", DATES[dateChoiceIdx][0])
        selectDropdown("selArrDay", DATES[dateChoiceIdx][1])
    driver.find_element_by_link_text(CAMPGROUND).click()
  # for if the site wont load in 60s, try again
  try:
    waitPageLoadForId("MainContentPlaceHolder_MessagesPanel", TIMEOUT_SECONDS)
  except:
    continue
  isAckMessage = "Please read and acknowledge all messages below" in driver.page_source
  if(isAckMessage == True):
    break
  driver.find_element_by_id("MainContentPlaceHolder_CancelButton").click()
  driver.find_element_by_link_text(CAMPGROUND).click()

ackCheckbox = driver.find_element_by_id("MainContentPlaceHolder_MessageControl1_AcknowledgeAllCheckBox")
ackCheckbox.click()

continueButton = driver.find_element_by_name("ctl00$MainContentPlaceHolder$ContinueButton")
continueButton.click()

x = input("Press any key to exit. WARNING: WILL CLOSE THE BROWSER. FINISH BOOKING IN BROWSER FIRST!!!!....")

driver.close()