import openpyxl
import pytest
from openpyxl.reader import workbook
from playwright.sync_api import Page

test_data=[]

excel=openpyxl.load_workbook("testdata/demo.xlsx")
sheet=excel.active
for row in sheet.iter_rows(min_row=2,values_only=True):

    a,b=row
    test_data.append((a or "",b or ""))
    excel.close()

@pytest.mark.parametrize("a,b" , test_data)
def test_openpyxl(page: Page,a,b):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    page.locator("input[placeholder='Username']").fill(a)
    page.locator("input[placeholder='Password']").fill(b)
    page.wait_for_timeout(2000)
    page.locator("button[type='submit']").click()





