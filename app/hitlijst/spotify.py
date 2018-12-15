from flask import current_app as app

def search_spotify(q):
    type='track'
    market='BE'
    limit=5
    response = app.spotify.search(q=q, type=type, market=market, limit=limit)
    result=[]
    for track in response['tracks']['items']:
        name=track["name"]
        id = track["id"]
        uri = track["uri"]
        artists = []
        for artist in track["artists"]:
            artists.append(artist['name'])

        result.append({"id": id, "name": name, "artists": ",".join(artists), "uri": uri})

    return result