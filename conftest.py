import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--my-browser-type", default="chromium", help="Browser type: chromium, firefox, webkit")
    parser.addoption("--my-headed", action="store_true", help="Run in headed (visible) mode")
    parser.addoption("--my-base-url", default="https://tutorialsninja.com/demo/", help="Base URL for tests")
    parser.addoption("--my-video", default="retain-on-failure", help="Record video: on, off, retain-on-failure")
    parser.addoption("--my-screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    parser.addoption("--my-tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")

def get_config_value(config, option_name):
    cmd_value = config.getoption(option_name)
    if cmd_value is not None:
        return cmd_value
    return config.getini(option_name)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

@pytest.fixture(scope="function")
def browser_context(request):
    browser_name = get_config_value(request.config, "my_browser_type")   # ✅ use underscore
    headed_flag = get_config_value(request.config, "my_headed")
    video_option = get_config_value(request.config, "my_video")

    playwright = sync_playwright().start()

    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(headless=not headed_flag)
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=not headed_flag)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=not headed_flag)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    if video_option in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()

    yield context

    context.close()
    browser.close()
    playwright.stop()

@pytest.fixture(scope="function")
def page(request, browser_context):
    base_url = get_config_value(request.config, "my_base_url")   # ✅ use underscore
    screenshot_option = get_config_value(request.config, "my_screenshot")
    tracing_option = get_config_value(request.config, "my_tracing")
    video_option = get_config_value(request.config, "my_video")

    if tracing_option in ["on", "retain-on-failure"]:
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = browser_context.new_page()
    page.goto(base_url)

    yield page

    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        browser_context.tracing.stop(path=trace_path)

    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name=f"{test_name}_screenshot", attachment_type=allure.attachment_type.PNG)

    if test_failed and video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None
        if video_path and Path(video_path).exists():
            allure.attach.file(video_path, name=f"{test_name}_video", attachment_type=allure.attachment_type.WEBM)
