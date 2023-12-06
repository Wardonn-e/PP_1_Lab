import os
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver


def create_directories(name: str) -> None:
    for i in range(1, 6):
        dir_name = f'{name}/{i}'
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, exist_ok=True)


def get_review(driver, links: str) -> str:
    driver.get("https://www.livelib.ru" + links.get("href"))
    sleep(2.5)
    soup_review = BeautifulSoup(driver.page_source, "lxml")
    return soup_review.find("div", {"id": "lenta-card__text-review-full"}).text.strip()


def save_review_to_file(review_number: int, review_title: str, review_links: str, review_rating: int, driver,
                        reviewer_name: str) -> None:
    file_name = f'{reviewer_name}/{review_rating}/{str(review_number).zfill(4)}.txt'
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(review_title.text.strip() + '\n' + get_review(driver, review_links))


def download_reviews(count: int, name: str) -> None:
    number_list = 1
    rating_review = [0] * 5
    driver = webdriver.Chrome()
    driver.maximize_window()
    while rating_review[4] < count or rating_review[3] < count or rating_review[2] < count or rating_review[
        1] < count or rating_review[0] < count:
        URL = f"https://www.livelib.ru/reviews/~{number_list}#reviews"
        driver.get(URL)
        sleep(2)
        number_list += 1
        soup = BeautifulSoup(driver.page_source, "lxml")

        rating = soup.find_all("span", {"class": "lenta-card__mymark"})
        title = soup.find_all("a", "lenta-card__book-title")
        links = soup.find_all("a", {"class": "footer-card__link"})

        for i in range(len(rating) - 1):
            rating_value = float(rating[i].text)
            if rating_value >= 1.0 and rating_review[int(rating_value) - 1] < count:
                rating_review[int(rating_value) - 1] += 1
                save_review_to_file(rating_review[int(rating_value) - 1], title[i], links[i], int(rating_value), driver,
                                    name)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    create_directories('data')
    download_reviews(100, 'data')
