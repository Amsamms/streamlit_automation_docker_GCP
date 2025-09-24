import time
from datetime import datetime
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# ── helper ─────────────────────────────────────────────────────────────
def create_driver() -> webdriver.Chrome:
    opts = ChromeOptions()
    opts.add_argument("--headless=new")          # new headless mode
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("window-size=1920x1080")
    service = ChromeService()                   # Selenium Mgr finds driver
    return webdriver.Chrome(service=service, options=opts)

def log_status(url: str, status: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("streamlit_monitor.log", "a") as f:
        f.write(f"{ts} | {url} | {status}\n")

# ── core class ─────────────────────────────────────────────────────────
class StreamlitAppMonitor:
    def __init__(self, urls: List[str], wake_up_wait: int = 120):
        self.urls = urls
        self.wake_up_wait = wake_up_wait

    # ----------------------------------------------------------
    def is_sleeping(self, driver) -> bool:
        try:
            wake_btn = "//button[contains(., 'get this app back up')]"
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, wake_btn))
            )
            return True
        except TimeoutException:
            return False

    # ----------------------------------------------------------
    def wake_up_app(self, driver) -> bool:
        try:
            wake_btn = "//button[contains(., 'get this app back up')]"
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, wake_btn))
            ).click()
            time.sleep(self.wake_up_wait)
            return True
        except Exception:
            return False

    # ----------------------------------------------------------
    def check_app_status(self, url: str) -> Dict:
        driver = None
        try:
            driver = create_driver()
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if self.is_sleeping(driver):
                status = (
                    "ACTIVATED"
                    if self.wake_up_app(driver)
                    else "ERROR"
                )
                details = (
                    "App was sleeping and has been activated"
                    if status == "ACTIVATED"
                    else "Failed to wake up sleeping app"
                )
            else:
                status, details = "ACTIVE", "App is already active"

            return {"url": url, "status": status, "details": details}

        except Exception as e:
            return {"url": url, "status": "ERROR", "details": f"Error: {e}"}

        finally:
            if driver:
                driver.quit()

    # ----------------------------------------------------------
    def monitor_apps(self):
        print(f"\nChecking apps at {datetime.now():%Y-%m-%d %H:%M:%S}")
        print("=" * 50)

        for url in self.urls:
            result = self.check_app_status(url)
            emoji = {"ACTIVE": "✅", "ACTIVATED": "🔄", "ERROR": "❌"}.get(
                result["status"], "❓"
            )
            print(f"{emoji} {url}")
            print(f"   Status : {result['status']}")
            print(f"   Details: {result['details']}")
            print("-" * 50)
            log_status(result["url"], result["status"])


def main():
    urls = [
        "https://amsamms-scatter-plotter-scatter-plotter-f4ojyj.streamlit.app/",
        "https://amsamms-general-machine-learning-algorithm-main-rs6nt9.streamlit.app/",
        "https://datasetanalysis-0.streamlit.app/",
        "https://pdf-table-extract.streamlit.app/",
        "https://images-table-extractor.streamlit.app/",
        "https://unit-converter-engineering.streamlit.app/",
        "https://gas-density-calculator-r.streamlit.app/",
        "https://envelopplotter.streamlit.app/",
        "https://liquid-control-valves-eval.streamlit.app/",
        "https://gas-control-valves-evaluation.streamlit.app/",
        "https://sabri-gpt-chatbot.streamlit.app/",
        "https://assistant-api-sabri.streamlit.app/",
        "https://movie-retriever.streamlit.app/",
        "https://h2-prediction.streamlit.app/",
        "https://ai-league.streamlit.app/",
        "https://fired-heater-calcs.streamlit.app/",
        "https://flow-meter-correction.streamlit.app/",
        "https://rag-demonstration.streamlit.app/"
    ]
    StreamlitAppMonitor(urls).monitor_apps()

if __name__ == "__main__":
    main() 