import requests
from selenium import webdriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from selenium.common.exceptions import TimeoutException
 
# Get the player_gamertag from the user message (assuming it's in the format "/location PLAYER_GAMERTAG")
player_gamertag = input("Enter player gamertag: ")
 
api_token = "YOUR_API_KEY_HERE"
 
auth_url = "https://x-bot.live/api/postman/auth"
auth_headers = {"Authorization": api_token}
auth_response = requests.get(auth_url, headers=auth_headers)
auth_data = auth_response.json()
 
xbl_auth = f"XBL3.0 x={auth_data['userHash']};{auth_data['XSTSToken']}"
 
profile_url = f"https://profile.xboxlive.com/users/gt({player_gamertag})/profile/settings"
profile_headers = {
    "X-XBL-Contract-Version": "2",
    "Authorization": xbl_auth,
    "Accept-Language": "en-US",
}
profile_response = requests.get(profile_url, headers=profile_headers)
profile_data = profile_response.json()
player_xuid = profile_data["profileUsers"][0]["id"]
 
friends_url = f"https://peoplehub.xboxlive.com/users/xuid({player_xuid})/people/social"
friends_headers = {
    "X-XBL-Contract-Version": "5",
    "Authorization": xbl_auth,
    "Accept-Language": "en-US",
}
friends_response = requests.get(friends_url, headers=friends_headers)
friends_data = friends_response.json()
 
# Print the friend list
friend_count = len(friends_data["people"])
print("Friends: " + str(friend_count))
 
# Create a chrome_options object
chrome_options = uc.ChromeOptions()
 
# Add the --headless argument
chrome_options.add_argument("--headless")
 
# Initialize the Chrome WebDriver with chrome_options
driver = uc.Chrome(options=chrome_options)
 
while True:
    driver.get('https://beta.octosniff.net/auth')
    time.sleep(5)
    # Wait for the login credentials box to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/form/div[1]/input'))
    )
 
    # Enter username
    element.send_keys('YOUR_OCTO_USER_HERE')
 
    # Find password
    element2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/form/div[2]/input')
    element2.send_keys('YOUR_OCTO_PASS_HERE')
 
    # Find a button by XPath and click it
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/form/button')
    button.click()
 
    try:
        # Check for button2 presence
        button2 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/nav/ul/li[5]/a'))
        )
        button2.click()
        break  # Exit the loop if button2 is found
    except TimeoutException:
        # Repeat the process if button2 is not found within 5 seconds
        continue
# Clear the contents of ip.txt before the loop starts
with open('ip.txt', 'w') as file:
    pass
button3 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/nav/ul/li[5]/ul/li[1]/a'))
)
button3.click()
 
button4 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div/div/div[2]/div[1]/div/ul/li[3]/a'))
)
button4.click()
 
element3 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/form/input'))
)
 
friend_usernames = []
for friend in friends_data["people"]:
    friend_usernames.append(friend["gamertag"])
 
ip_list = []
# Loop through friend_usernames to get IP addresses
for gamertag in friend_usernames:
    element3.clear()  # Clear the input field
    element3.send_keys(gamertag)
 
    button5 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/form/button'))
    )
    button5.click()
 
    element4 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/div/div/div'))
    )
 
 
    if element4.text.startswith('L'):
        ip_address = element4.text[26:]
        print(ip_address)
 
        # Save IP addresses into ip.txt, one IP per line
        with open('ip.txt', 'a') as file:
            file.write(f'{ip_address}\n')
    else:
        # Handle other cases here
        pass
 
def get_location(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country")
    }
    return f"{location_data['city']}, {location_data['region']}, {location_data['country']}"
 
 
if __name__ == "__main__":
    locations = []
 
    with open('ip.txt', 'r') as f:
        for line in f:
            ip_address = line.strip()
            location_data = get_location(ip_address)
            locations.append(location_data)
 
    # Clear the contents of the loco.txt file
    with open('loco.txt', 'w') as f:
        pass
 
    with open('loco.txt', 'w') as f:
        for location in locations:
            f.write(f"{location}\n")
 
    with open('loco.txt', 'r') as f:
        lines = f.readlines()
 
    # Count the number of occurrences of each location
    location_counts = {}
    for line in lines:
        if line in location_counts:
            location_counts[line] += 1
        else:
            location_counts[line] = 1
 
    # Find the location with the most occurrences
    most_common_location = max(location_counts, key=location_counts.get)
 
    # Print the conclusive location if there are duplicates, or "No conclusive location found" otherwise
    if location_counts[most_common_location] > 1:
        print(f"Conclusive location - {most_common_location.strip()}")
    else:
        print("No conclusive location found")
