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
        self.client.headers.update(
            {"Authorization": f"Bearer {self.create_user_and_authenticate_client()}"}
        )

    def create_user_and_authenticate_client(self):
        self.create_user()
        res = self.client.post(
            "/token",
            data={"username": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD}
        )
        token = res.json()["access_token"]
        return token


    def prep_kwargs(self, locals: dict) -> dict:
        copied_locals = locals.copy()
        copied_locals.pop("self")
        return copied_locals

    def create_user(
        self,
        full_name="Patrick M Kelly",
        email=DEFAULT_EMAIL,
        password=DEFAULT_PASSWORD
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/user/", json=body,)

    def update_user(
        self, **kwargs,
    ):
        return self.client.put(
            f"/user/",
            json=kwargs,
        )

    def create_club(
        self, token, book_title="A merry book"
    ):
        body = self.prep_kwargs(locals())
        return self.client.post(
            "/club/",
            headers={"Authorization": f"Bearer {token}"},
            json=body,
        )

    def create_note(
        self,
        token,
        content="Oh my, such a lovely note!",
        club_id=1,
    ):
        body = self.prep_kwargs(locals())
        return self.client.post(
            "/note/",
            headers={"Authorization": f"Bearer {token}"},
            json=body,
        )

    def update_note(
        self, token, note_id=1, content="A new type of note!", private=False, archived=False
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(
            f"/note/{note_id}/",
            headers={"Authorization": f"Bearer {token}"},
            json=body,
        )

    def add_tags_to_note(
        self, note_id=1, tags=[1],
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/note/{note_id}/tag/", json=body)

    def create_tag(
        self, name="taggy boy", club_id=1,
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/tag/", json=body)

    def update_tag(
        self, name="a new tag name", tag_id=1, archived=False,
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/tag/{tag_id}/", json=body)
