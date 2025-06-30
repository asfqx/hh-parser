class Tokens:
    def __init__(self):
        self.access_token = ""
        self.refresh_token = ""

    def load_tokens(self):
        with open("tokens") as file:
            self.access_token, self.refresh_token = file.readline().strip().split(":")

    def save_tokens(self, ac_token, ref_token):
        with open("tokens", "w") as f:
            f.write(f"{ac_token}:{ref_token}")
        self.access_token, self.refresh_token = ac_token, ref_token


tokens = Tokens()
