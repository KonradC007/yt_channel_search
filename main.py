import python_package


def main():

    sheet_id = "1-yrmb5N14niNwgGKOF5zK3jyCB4zla_EjBg2Z2oIal4"
    keyword_range = "Keyword list!B4:B"
    lang_range = "Keyword list!C5"
    country_range = "Keyword list!C2"
    file_path = "tmp/results.json"
    table_id = "thunderz-344909.youtube_search.search_results"
    google_sheets_client = python_package.GoogleSheetsConnection()
    keywords = google_sheets_client.import_range(sheet_id=sheet_id, sheet_range=keyword_range)
    lang = google_sheets_client.import_range(sheet_id=sheet_id, sheet_range=lang_range)[0][0]
    country = google_sheets_client.import_range(sheet_id=sheet_id, sheet_range=country_range)[0][0]

    for keyword in keywords:
        process_keyword(keyword=keyword, lang=lang, country=country, file_path=file_path, table_id=table_id)


def process_keyword(keyword, lang, country, file_path, table_id):

    # Load modules
    webdriver = python_package.webdriver_functions()
    transform = python_package.Transform()
    bq_client = python_package.Bigquery_connection()

    # Open website
    webdriver.open_website(link="https://www.youtube.com/")

    # Accept cookies etc.
    webdriver.click_on_xpath("//*[@id='content']/div/div[6]/div[1]/ytd-button-renderer[2]/a")

    # Change language to select location
    webdriver.click_on_xpath("(//*[@class='style-scope ytd-topbar-menu-button-renderer' and @id='button'])[2]")
    webdriver.click_on_xpath("(//*[@class='style-scope yt-multi-page-menu-section-renderer']/*[@id='endpoint'])[1]")
    webdriver.click_on_xpath(f"//*[contains(text(),'English (UK)')]")

    # Change location
    webdriver.click_on_xpath("(//*[@class='style-scope ytd-topbar-menu-button-renderer' and @id='button'])[2]")
    webdriver.click_on_xpath("(//*[@class='style-scope yt-multi-page-menu-section-renderer']/*[@id='endpoint'])[2]")
    webdriver.click_on_xpath(f"//*[contains(text(),'{country}')]")

    # Change language
    webdriver.click_on_xpath("(//*[@class='style-scope ytd-topbar-menu-button-renderer' and @id='button'])[2]")
    webdriver.click_on_xpath("(//*[@class='style-scope yt-multi-page-menu-section-renderer']/*[@id='endpoint'])[1]")
    webdriver.click_on_xpath(f"//*[contains(text(),'{lang}')]")

    # search keyword
    webdriver.send_keys_to_text_box(text=keyword, xpath="//*[@name='search_query']")
    webdriver.click_on_xpath("//*[@id='search-icon-legacy']", interval=2)
    xpath_count = webdriver.count_xpath(xpath="//*[contains(@href, '/c/') and @class='style-scope "
                                              f"ytd-video-renderer']", interval=2)

    channel_list = []
    for i in range(1, xpath_count):
        channel_list.append(webdriver.get_xpath_attribute(xpath=f"(//*[contains(@href, '/c/') and @class='style-scope "
                                                                f"ytd-video-renderer'])[{i}]",
                                                          attribute="href"))

    xpath_count = webdriver.count_xpath(
        xpath="//*[@id='video-title' and @class='yt-simple-endpoint style-scope ytd-video-renderer']", interval=2)

    videos_list = []
    for i in range(1, xpath_count):
        videos_list.append(webdriver.get_xpath_attribute(xpath=f"(//*[@id='video-title' and "
                                                               f"@class='yt-simple-endpoint style-scope ytd-video-renderer'])[{i}]",
                                                         attribute="href"))

    videos_list = list(set(videos_list))

    for link in videos_list:
        webdriver.open_website(link=link)
        xpath_count = webdriver.count_xpath(
            xpath="//*[@id='dismissible']/div/div[1]/a", interval=2)

        videos_sublist = []
        for i in range(1, xpath_count):
            videos_sublist.append(webdriver.get_xpath_attribute(xpath=f"(//*[@id='dismissible']/div/div[1]/a)[{i}]",
                                                                attribute="href"))
        for video_link in videos_sublist:
            html = webdriver.get_html_of_link(link=video_link)
            list_of_channels = transform.get_regex_from_html(regex=r'"url":"/c/(.*?)","webPageType"', html=html)
            link_to_channels = transform.convert_to_channel_link(list_of_channels=list_of_channels)
            channel_list = channel_list + link_to_channels

    channel_list = list(set(channel_list))

    results = []

    for channel in channel_list:
        results.append({"channel": channel, "keyword": keyword, "lang": lang, "country": country})

    transform.list_of_dict_to_json(data=results, file_path=file_path)

    bq_client.import_data_to_bq(file_path=file_path, table_id=table_id)

    webdriver.quit_driver()


if __name__ == '__main__':

    main()
