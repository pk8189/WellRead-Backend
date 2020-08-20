from fastapi.testclient import TestClient

DEFAULT_EMAIL = "pmkelly4444@gmail.com"
DEFAULT_PASSWORD = "string"


class MockApiRequests:
    """
    API TestClient class with mock requests with kwargs
    for changing the data in the request
    """

    def __init__(self, client: TestClient):
        self.client = client

    def create_user_and_authenticate(self):
        self.create_user()
        return self.authenticate()

    def create_user2_and_authenticate(self):
        self.create_user(
            email="anotheruser@gmail.com",
            password="password2",
            full_name="Patrick Star",
        )
        return self.authenticate(email="anotheruser@gmail.com", password="password2",)

    def authenticate(
        self, email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD
    ):
        res = self.client.post("/token", data={"username": email, "password": password})
        token = res.json()["access_token"]
        return self.client.headers.update({"Authorization": f"Bearer {token}"})

    def prep_kwargs(self, locals: dict) -> dict:
        copied_locals = locals.copy()
        copied_locals.pop("self")
        return copied_locals

    def create_user(
        self,
        full_name="Patrick M Kelly",
        email=DEFAULT_EMAIL,
        password=DEFAULT_PASSWORD,
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/user/", json=body,)

    def create_club(self, name="A merry club"):
        body = self.prep_kwargs(locals())
        return self.client.post("/club/", json=body,)

    def create_book(self, book_title="Book title", author_name="Chinua Acb"):
        body = self.prep_kwargs(locals())
        return self.client.post("/book/", json=body,)

    def create_note(
        self, content="Oh my, such a lovely note!", book_id=1, private=False
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/note/", json=body,)

    def update_note(
        self, note_id=1, content="A new type of note!", private=False, archived=False
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/note/{note_id}/", json=body,)

    def add_tags_to_note(
        self, note_id=1, tags=[1], club_tags=[2],
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/note/{note_id}/tag/", json=body)

    def create_tag(
        self, name="taggy boy",
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/tag/", json=body)

    def update_tag(
        self, name="a new tag name", tag_id=1, archived=False,
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/tag/{tag_id}/", json=body)
