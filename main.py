import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SOURCE_PLAYLISTS = [
    "4b7RbxLP6DoNE2IAUG9YVK",
    "1tMv5HL5sHfSJpE6ChdBR3",
    "7MXuwUl9SqxNa9EonYgJ0a",
    "20vMMzo0AGe55fvIaBIP5z",
    "3z0UND2T2LL8zOebTAiqg1",
    "3IhnDGoeRYyHssF6N5iPJo",
    "233LJVKVqnF7HtaRwrH4lO",
    "6yD2igx3Wvo5KcX8GQCCH7",
    "2vhbjheMvUKR3OyX4FQrN8",
    "1KzJILWuReQ8OSjQanI5LG",
    "1WOV25D9VCORXkjDwJ4oHq",
]
TARGET_PLAYLIST_ID = "2VR8EeOC3QYL8JudM4BLEl"

artist_cache = {}


def get_japanese_artist_genres(artist_ids, sp):
    artist_genres_map = {}
    target_keywords = [
        "japanese",
        "j-",
        "anime",
        "city pop",
        "visual kei",
        "vocaloid",
        "bemani",
        "doujin",
        "enka",
        "japanoise",
        "oshare kei",
        "shibuya-kei",
    ]
    unique_ids = [uid for uid in list(set(artist_ids)) if uid]
    for i in range(0, len(unique_ids), 50):
        chunk = unique_ids[i : i + 50]
        try:
            response = sp.artists(chunk)
            for artist in response["artists"]:
                if not artist:
                    continue
                genres = artist.get("genres", [])
                for genre in genres:
                    if any(keyword in genre.lower() for keyword in target_keywords):
                        artist_genres_map[artist["id"]] = genre
                        break

        except Exception as e:
            print(f"Error fetching artists {e}")
    return artist_genres_map


def get_all_playlist_tracks(sp, playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def main():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public playlist-modify-private"
        )
    )

    print("--- Scanning target playlist (prevent duplicates) ---")
    existing_tracks = get_all_playlist_tracks(sp, TARGET_PLAYLIST_ID)
    existing_uris = set()
    for item in existing_tracks:
        if item["track"]:
            existing_uris.add(item["track"]["uri"])
    print(f"Found {len(existing_uris)} songs already in target playlist.")

    print("--- Scanning source playlists ---")
    songs_to_add = []
    candidate_artists = {}

    for playlist_id in SOURCE_PLAYLISTS:
        print(f"Reading playlist: {playlist_id}...")
        tracks = get_all_playlist_tracks(sp, playlist_id)

        for item in tracks:
            track = item["track"]
            if not track:
                continue
            track_uri = track["uri"]
            track_name = track["name"]
            if track_uri in existing_uris or track_uri in songs_to_add:
                continue
            if not track["artists"] or "id" not in track["artists"][0]:
                continue
            artist_name = track["artists"][0]["name"]
            artist_id = track["artists"][0]["id"]

            if artist_id not in candidate_artists:
                candidate_artists[artist_id] = []
            candidate_artists[artist_id].append(
                {"uri": track_uri, "track_name": track_name, "artist_name": artist_name}
            )

    print(f"--- Checking genres for {len(candidate_artists)} artists ---")
    ids_to_check = list(candidate_artists.keys())
    valid_japanese_artist_genres = get_japanese_artist_genres(ids_to_check, sp)

    for artist_id, matched_genre in valid_japanese_artist_genres.items():
        tracks_data = candidate_artists[artist_id]
        for track_data in tracks_data:
            if (
                track_data["uri"] not in existing_uris
                and track_data["uri"] not in songs_to_add
            ):
                songs_to_add.append(track_data["uri"])
                existing_uris.add(track_data["uri"])
                print(
                    f"Match ({matched_genre}): {track_data['track_name']} by {track_data['artist_name']}"
                )

    if songs_to_add:
        print(f"--- Adding {len(songs_to_add)} songs to target ---")
        songs_to_add = list(set(songs_to_add))
        for i in range(0, len(songs_to_add), 100):
            chunk = songs_to_add[i : i + 100]
            sp.playlist_add_items(TARGET_PLAYLIST_ID, chunk)
        print("Done!")
    else:
        print("No matches found")


if __name__ == "__main__":
    main()
