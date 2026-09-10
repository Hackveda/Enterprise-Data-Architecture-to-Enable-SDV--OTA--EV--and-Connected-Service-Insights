from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'
def test_team_pages():
    for team in ('marketing','sales','support','finance','delivery'):
        assert client.get('/'+team).status_code==200
        payload=client.get('/api/team/'+team+'/data').json()
        assert payload['team']==team
        assert payload['live']['simulated_rps']>=1_600_000
