import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SOURCE_PLAYLISTS = ["4b7RbxLP6DoNE2IAUG9YVK"]
TARGET_PLAYLIST_ID = "2VR8EeOC3QYL8JudM4BLEl"

artist_cache = {}


def is_japanese_genre(artist_id, sp):
    if artist_id in artist_cache:
        return artist_cache[artist_id]
    try:
        artist_info = sp.artist(artist_id)
        genres = artist_info.get("genres", [])
        target_keywords = [
            "japanese",
            "j-pop",
            "j-rock",
            "anime",
            "j-metal",
            "city pop",
            "visual kei",
        ]

        is_match = False
        for genre in genres:
            for keyword in target_keywords:
                if keyword in genre.lower():
                    is_match = True
                    break
            if is_match:
                break

        return is_match
    except Exception as e:
        print(f"Error fetching artist {artist_id}: {e}")
        return False


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
    songs_to_add = []
    seen_uris = set()
    print("--- Starting Scan ---")

    for playlist_id in SOURCE_PLAYLISTS:
        print(f"Reading playlist: {playlist_id}...")
        tracks = get_all_playlist_tracks(sp, playlist_id)
        for item in tracks:
            track = item["track"]
            if not track:
                continue
            track_uri = track["uri"]
            if track_uri in seen_uris:
                continue
            track_name = track["name"]
            if not track["artists"] or "id" not in track["artists"][0]:
                continue
            artist_name = track["artists"][0]["name"]
            artist_id = track["artists"][0]["id"]

            if is_japanese_genre(artist_id, sp):
                print(f"Match (genre): {track_name} - {artist_name}")
                songs_to_add.append(track_uri)
                seen_uris.add(track_uri)

    if songs_to_add:
        print(f"--- Adding {len(songs_to_add)} songs to target ---")
        for i in range(0, len(songs_to_add), 100):
            chunk = songs_to_add[i : i + 100]
            sp.playlist_add_items(TARGET_PLAYLIST_ID, chunk)
        print("Done")
    else:
        print("No matches found")


if __name__ == "__main__":
    main()
