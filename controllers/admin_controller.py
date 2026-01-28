from views.admin_view import AdminView

class AdminController:
    def __init__(self, app):
        self.app = app

    def show_admin_dashboard(self):
        self.app.clear_screen()
        self.app.render_header("Admin Dashboard")
        AdminView(self.app.root, self.app).pack(fill="both", expand=True)
