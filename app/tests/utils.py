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
        self,
        slack_id_team_id="U014YSCLQ2X_T0140PRK962",
        name="Patrick M Kelly",
        tz="Eastern Daylight Time",
        locale="en-US",
        team_id="T0140PRK962",
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/user/", json=body,)

    def update_user(
        self, slack_id_team_id: str, **kwargs,
    ):
        return self.client.put(f"/user/{slack_id_team_id}/", json=kwargs,)

    def create_team(
        self,
        team_id="T0140PRK962",
        name="WellRead",
        domain="www.domain.com",
        email_domain="",
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/team/", json=body,)

    def create_club(
        self,
        book_title="A merry book",
        admin_user_id="U014YSCLQ2X_T0140PRK962",  # default user in tests
        channel_id="19WEWFJEW1425W",
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/club/", json=body,)

    def create_note(
        self,
        content="Oh my, such a lovely note!",
        slack_user_id="U014YSCLQ2X_T0140PRK962",  # default user in tests
        slack_club_id=1,
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
        self, name="taggy boy", slack_club_id=1,
    ):
        body = self.prep_kwargs(locals())
        return self.client.post("/tag/", json=body)

    def update_tag(
        self, name="a new tag name", tag_id=1, archived=False,
    ):
        body = self.prep_kwargs(locals())
        return self.client.put(f"/tag/{tag_id}/", json=body)
