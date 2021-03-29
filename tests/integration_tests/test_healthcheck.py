def test_healthcheck(client):
    response = client.get('/api/healthcheck')

    assert response.json == {'message': 'OK'}
    assert response.status == '200 OK'
