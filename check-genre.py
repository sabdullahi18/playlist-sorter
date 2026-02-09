import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def check_song(url):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public playlist-modify-private"
        )
    )

    try:
        track = sp.track(url)
        print(f"\n🎵 Track: {track['name']}")
        print(f"🔗 URL: {track['external_urls']['spotify']}")
        print("-" * 30)

        for artist in track["artists"]:
            artist_details = sp.artist(artist["id"])
            name = artist_details["name"]
            genres = artist_details["genres"]

            print(f"👤 Artist: {name}")
            if genres:
                print(f"🏷️  Genres: {genres}")
            else:
                print(
                    "⚠️  Genres: [] (Empty! Spotify has no genre data for this artist)"
                )
            print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_genre.py <spotify_track_url>")
    else:
        check_song(sys.argv[1])
