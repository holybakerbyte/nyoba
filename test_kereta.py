import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as by
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@allure.title("Test Case - Booking Kereta Api")
@allure.feature("Booking Management")
@allure.story("successfully ticket booking")
@allure.label("owner", "PyAuto ID")
@allure.description(
    """
    Tes ini memverifikasi fungsionalitas pemesanan tiket kereta api di website KAI.
    Langkah-langkah yang diuji meliputi:
    1. Membuka halaman utama booking.kai.id.
    2. Mengisi stasiun keberangkatan dan tujuan (contoh: Gambir ke Yogyakarta).
    3. Memilih tanggal keberangkatan (contoh: tanggal 30).
    4. Mengatur jumlah penumpang dewasa (1 orang) dan bayi (1 orang).
    5. Melanjutkan ke halaman pilihan kereta api.
    6. Memilih kereta api pertama yang tersedia.
    7. Memastikan navigasi berhasil ke halaman data penumpang.
    """
)
def test_booking_kereta(driver):
    def allure_attach(
        description,
        name="Deskripsi Langkah",
        attachment_type=allure.attachment_type.TEXT,
    ):
        allure.attach(description, name=name, attachment_type=attachment_type)

    with allure.step("open Base URL, https://booking.kai.id"):
        allure_attach("Membuka halaman utama booking.kai.id")
        driver.get("https://booking.kai.id/")
        assert (
            "Reservasi Tiket" in driver.title
        ), "page title does not contain 'Reservasi Tiket'"

    origin = driver.find_element(by.XPATH, "//input[@id='origination-flexdatalist']")
    origin.click()
    origin.send_keys("gambir")
    with allure.step("isi stasiun asal"):
        allure_attach(
            "Mengisi field stasiun asal dengan 'gambir' lalu memilih dari dropdown yang muncul.",
        )
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by.XPATH, "//li[@class='item']"))
            )
            driver.find_element(by.XPATH, "//li[@class='item']").click()
        except TimeoutException:
            print("Stasiun asalnya gak muncul Bang, lho kok bisa?")

    destination = driver.find_element(
        by.XPATH, "//input[@id='destination-flexdatalist']"
    )
    destination.click()
    destination.send_keys("yogyakarta")
    with allure.step("isi stasun tujuan"):
        allure_attach(
            "Mengisi field statiun tujuan dengan 'yogyakarta' dan memilih dari dropdown yang muncul."
        )
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by.XPATH, "//li[@class='item']"))
            )
            driver.find_element(by.XPATH, "//li[@class='item']").click()
        except TimeoutException:
            print("Stasiun tujuannya gak muncul Bang, lho kok bisa?")

    with allure.step("pilih tanggal keberangkatan"):
        allure_attach(
            "Mengklik field tanggal keberangkatan dari kalender yaitu tanggal 30."
        )
        driver.find_element(by.XPATH, "//input[@id='departure_dateh']").click()
        # driver.find_element(by.XPATH, "//a[contains(@class,'ui-state-highlight')]/following-sibing::a").click()
        driver.find_element(by.XPATH, "//a[contains(text(),'30')]").click()

    with allure.step("isi jumlah penumpang dewasa"):
        allure_attach("Mengisi jumlah penumpang dewasa dengan 1 orang.")
        try:
            dewasa = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (by.XPATH, "//input[contains(@class, 'input-number')]")
                )
            )
            # dewasa = driver.find_element(by.XPATH, "//input[contains(@class, 'input-number')]")
            dewasa.click()
            dewasa.clear()
            dewasa.send_keys("1")
        except TimeoutException:
            print("Input jumlah penumpang dewasa tidak ditemukan Bang, lho kok bisa?")
        # driver.find_element(by.XPATH, "//input[contains(@class, 'input-number')]").send_keys("2")
    with allure.step("isi jumlah penumpang infants"):
        allure_attach("Mengisi jumlah infant menjadi 1 orang.")
        driver.find_element(by.XPATH, "//input[@id='infant']").send_keys("1")
    with allure.step("pilih dan pesan tiket"):
        allure_attach("Mengklik tombol 'cari & pesan tiket' untuk melanjutkan.")
        driver.find_element(by.XPATH, "//input[@id='submit']").click()

    with allure.step("pilih kereta pada pilihan pertama"):
        allure_attach("Mengklik pilihan kereta pertama yang muncul.")
        driver.find_element(by.XPATH, "//a[@class='card-schedule'][1]").click()

    allure.attach(
        driver.get_screenshot_as_png(),
        name="success_screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    assert (
        "Passenger Data" in driver.title
    ), "page title does not contain 'Passenger Data'"
