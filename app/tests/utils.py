from fastapi.testclient import TestClient


class MockApiRequests:
    """
    API TestClient class with mock requests with kwargs
    for changing the data in the request
    """

    def __init__(self, client: TestClient):
        self.client = client

    def prep_kwargs(self, locals: dict) -> dict:
        copied_locals = locals.copy()
        copied_locals.pop("self")
        return copied_locals

    def create_user(
        self, full_name="Patrick M Kelly", email="pmkelly4444@gmail.com",
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/user/", json=body,)

    def update_user(
        self, id: int, **kwargs,
    ):
        return self.client.put(f"/user/{id}/", json=kwargs,)

    def create_club(
        self, book_title="A merry book", admin_user_id=1,  # default user in tests
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/club/", json=body,)

    def create_note(
        self,
        content="Oh my, such a lovely note!",
        user_id=1,  # default user in tests
        club_id=1,
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/note/", json=body)

    def update_note(
        self, note_id=1, content="A new type of note!", private=False, archived=False
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/note/{note_id}/", json=body)

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
