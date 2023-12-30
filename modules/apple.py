from pyicloud import PyiCloudService


class iCloudBuddy:
    def __init__(self):
        self.app = None
        self.logged_in = False
        self.username = None
        self.password = None

    def init_app(self, app, username, password):
        self.app = app
        self.app.extensions['apple'] = self

        try:
            self.apple_login = PyiCloudService(username, password)
        except Exception as e:
            print(e)
            return False

        if self.apple_login.requires_2fa:
            security_code = self.app.create_popup()
            result = self.apple_login.validate_2fa_code(security_code)
            print("Code validation result: %s" % result)
            if not result:
                print("Failed to verify security code")
            if not self.apple_login.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.apple_login.trust_session()
                print("Session trust result %s" % result)
                if not result:
                    print(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        else:
            print("Authentication successful!")


ICB = iCloudBuddy()
