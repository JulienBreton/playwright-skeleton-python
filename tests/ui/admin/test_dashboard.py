import pytest
from playwright.sync_api import expect

from framework.pages.admin_dashboard_page import AdminDashboardPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_admin_dashboard_opens_with_saved_session(
    admin_dashboard_page: AdminDashboardPage,
) -> None:
    admin_dashboard_page.open()

    expect(admin_dashboard_page.title).to_have_text("Sales over the years")
