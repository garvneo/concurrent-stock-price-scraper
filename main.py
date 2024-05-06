import os
import time

from dotenv import load_dotenv

from yaml_scanner import YamlScanner


def main():
    load_dotenv()
    PIPELINE_PATH = os.environ.get("PIPELINE_PATH")
    if PIPELINE_PATH is None:
        print("Could not find pipeline path!")
        exit(1)
    scraper_start_time = time.time()

    yaml_scanner = YamlScanner(PIPELINE_PATH=PIPELINE_PATH)
    yaml_scanner.start()
    yaml_scanner.join()
    print("Data extraction took", round(time.time() - scraper_start_time, 1))


if __name__ == "__main__":
    main()
