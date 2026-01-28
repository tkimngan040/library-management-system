from views.member_view import MemberView

class MemberController:
    def __init__(self, app):
        self.app = app

    # màn member
    def show_member_dashboard(self):
        self.app.clear_screen()
        self.app.render_header("Member Dashboard")
        MemberView(self.app.root, self).pack(expand=True)
