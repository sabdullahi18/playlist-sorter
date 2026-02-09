import spotipy
import argparse
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
    "4Eq9CvOurX3fUwLs3itjJi",
    "02YU2H202FR4WvKUwJJ29M",
    "6iMfJfX3hDFtbMe0koHh0B",
    "2VR8EeOC3QYL8JudM4BLEl",
    "7u6ru8egT8bFqxwHyxAt9o",
    "0nhh0RUd0JvboUAgO76OdH",
    "7bfiiRryBWurKNfwq8dWLc",
    "02aLUpGZTZ8CX6LMgScgUR",
    "1s3OL6khnDRW5nOvgY6DvN",
    "0D96bhlUcO1GMnGmFCECCV",
    "2xZesaH6DrK6YJpI48Hs0B",
]
SORTING_RULES = [
    {
        "id": "jp",
        "name": "japanese (日本語)",
        "target_id": "2VR8EeOC3QYL8JudM4BLEl",
        "keywords": [
            # Broad Terms
            "japanese",
            "j-",
            # Anime & Otaku
            "anime",
            "anisong",
            "vocaloid",
            "touhou",
            "doujin",
            "denpa-kei",
            "bemani",
            "kawaii",
            "seiyu",
            "vtuber",
            # City Pop & Jazz
            "city pop",
            "shibuya-kei",
            # Visual Kei & Subcultures
            "visual kei",
            "oshare kei",
            "men chika",
            "jirai kei",
            "japanoise",
            "nagoya kei",
            # Traditional & Folk
            "enka",
            "kayokyoku",
            "ryukyu ongaku",
            "okinawan",
            "min'yo",
            "shamisen",
            "koto",
            "taiko",
            "shakuhachi",
            "gagaku",
        ],
    },
    {
        "id": "ar",
        "name": "arabic (عربي)",
        "target_id": "02YU2H202FR4WvKUwJJ29M",
        "keywords": [
            # General Arab
            "arab",
            "middle east",
            # Egyptian (Masri)
            "egyptian",
            "mahraganat",
            "shaabi",
            # North African (Maghreb)
            "maghreb",
            "deep rai",
            "rai algerien",
            "moroccan",
            "maroc",
            "algerian",
            "algerien",
            "tunisian",
            "tunisien",
            "libyan",
            "gnawa",
            # Levantine (Sham)
            "lebanese",
            "dabke",
            "syrian",
            "jordanian",
            "palestinian",
            # Gulf (Khaleeji) & Iraqi
            "khaleeji",
            "khaliji",
            "sheilat",
            "gulf",
            "iraqi",
            "yemeni",
            # Sudan
            "sudanese",
            # Religious & Traditional
            "islamic recitation",
            "nasheed",
            "quran",
            "sufi",
            "oud",
            "belly dance",
        ],
    },
    {
        "id": "zh",
        "name": "chinese (中文)",
        "target_id": "6iMfJfX3hDFtbMe0koHh0B",
        "keywords": [
            # Mainstream Pop
            "c-",
            "chinese",
            "mandopop",
            "cantopop",
            "hk-pop",
            "taiwan",
            "taiwanese",
            "hokkien",
            "hakkapop",
            # Indie & Rock
            "hong kong",
            "shanghai",
            "wuhan",
            # Hip Hop & R&B
            "sichuanese",
            # Traditional & Instruments
            "cantonese",
            "zhongguo",
            "guqin",
            "guzheng",
            "pipa",
            "erhu",
            "dizi",
            # Specific Scenes
            "xinyao",
        ],
    },
    {
        "id": "ru",
        "name": "russian (русский)",
        "target_id": "0nhh0RUd0JvboUAgO76OdH",
        "keywords": [
            # Pop & Dance
            "russian",
            # Hip Hop & Trap
            # Rock, Post-Punk & Doomer
            "soviet",
            # Metal
            "slavic",
            # Folk & Regional
            "tatar",
            "yakut",
            "chechen",
            "siberian",
            "tuvan",
            "circassian",
            "balalaika",
        ],
    },
    {
        "id": "ir",
        "name": "persian (فارسی)",
        "target_id": "1s3OL6khnDRW5nOvgY6DvN",
        "keywords": [
            # Mainstream Pop
            "persian",
            # Hip Hop & Rap (The biggest modern scene)
            # Rock & Alternative
            "iranian",
            # Traditional & Classical
            "musiqi-ye zanan",
            # Regional (Iranian ethnic groups)
            "mazandarani",
            "balochi",
            "kurdish",
        ],
    },
    {
        "id": "ca",
        "name": "caucasian",
        "target_id": "7Bonps8o4YrvnRZbUqCpNV",
        "keywords": [
            "azeri",
            "meyxana",
            "armenian",
            "georgian",
            "caucasian",
            "ossetian",
            "circassian",
            "chechen",
        ],
    },
    {
        "id": "br",
        "name": "brazilian portuguese",
        "target_id": "0D96bhlUcO1GMnGmFCECCV",
        "keywords": [
            # Bossa Nova & MPB
            "bossa nova",
            "mpb",
            "tropicalia",
            "choro",
            "manguebeat",
            "jovem guarda",
            # Samba & Pagode
            "samba",
            "pagode",
            "partido alto",
            # Funk Brasileiro (Rio/Baile Funk)
            "carioca",
            "ostentacao",
            "paulista",
            "mtg",
            "consciente",
            "mandelao",
            "brega funk",
            "funk 150 bpm",
            "funk viral",
            # Sertanejo & Forro
            "sertanejo",
            "agronejo",
            "arrocha",
            "forro",
            "piseiro",
            "tecnobrega",
            "brega",
            "axe",
            "frevo",
            "carimbo",
            # Rock & Pop
            "pop nacional",
            "rock nacional",
            "brazilian",
            "brasileiro",
        ],
    },
    {
        "id": "rap",
        "name": "american rap",
        "target_id": "7u6ru8egT8bFqxwHyxAt9o",
        "keywords": [
            # Regional: South (Atlanta, Memphis, Florida, Texas)
            "southern hip hop",
            "dirty south rap",
            "atl hip hop",
            "atl trap",
            "memphis hip hop",
            "miami hip hop",
            "florida rap",
            "houston rap",
            "new orleans rap",
            "crunk",
            "trap music",
            "baton rouge rap",
            # Regional: East Coast (NY, Philly)
            "east coast hip hop",
            "nyc rap",
            "brooklyn drill",
            "bronx drill",
            "philly rap",
            "queens hip hop",
            "harlem hip hop",
            "boom bap",
            # Regional: West Coast (LA, Bay Area)
            "west coast rap",
            "cali rap",
            "g funk",
            "hyphy",
            "oakland hip hop",
            "bay area hip hop",
            "sacramento hip hop",
            # Regional: Midwest (Chicago, Detroit)
            "chicago rap",
            "chicago drill",
            "detroit hip hop",
            "detroit trap",
            # Modern Styles & Subgenres
            "melodic rap",
            "cloud rap",
            "emo rap",
            "sad rap",
            "rage rap",
            "plugg",
            "pluggnb",
            "conscious hip hop",
            "jazz rap",
            "experimental hip hop",
            "industrial hip hop",
        ],
    },
    {
        "id": "uk-rap",
        "name": "uk rap",
        "target_id": "208lHwlrPzMwuGVlT444Ws",
        "keywords": [
            # Core UK Rap & Hip Hop
            "uk hip hop",
            "british hip hop",
            "uk melodic rap",
            "uk alternative hip hop",
            "uk christian rap",
            # Grime & Drill
            "grime",
            "uk drill",
            "grimewave",
            "birmingham grime",
            # Afroswing (Crucial for modern UK Rap)
            "afroswing",
            # Regional Scenes
            "london",
            "manchester",
            "birmingham",
            "nottingham",
            "scottish",
            "welsh",
            # Adjacent / Origins (Garage & Bass often feature MCs)
            "uk garage",
            "bassline",
            "uk bass",
            "uk funky",
        ],
    },
    {
        "id": "kr",
        "name": "korean (한국인)",
        "target_id": "2X5jXqhcVInsJVNnSFhqWX",
        "keywords": [
            # Mainstream K-Pop
            "k-pop",
            "korean",
            # Hip Hop & R&B
            "k-rap",
            # Indie & Rock
            "k-indie",
            "k-rock",
            # Traditional & Classical
            "pansori",
        ],
    },
]

artist_cache = {}


def get_artist_genre_map(artist_ids, sp):
    artist_genre_map = {}
    unique_ids = [uid for uid in list(set(artist_ids)) if uid]

    for i in range(0, len(unique_ids), 50):
        chunk = unique_ids[i : i + 50]
        try:
            response = sp.artists(chunk)
            for artist in response["artists"]:
                if not artist:
                    continue
                artist_genre_map[artist["id"]] = artist.get("genres", [])
        except Exception as e:
            print(f"Error fetching artists {e}")
    return artist_genre_map


def get_all_playlist_tracks(sp, playlist_id):
    tracks = []
    try:
        results = sp.playlist_items(playlist_id)
        tracks.extend(results["items"])
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])
    except Exception as e:
        print(f"Couldn't read playlist {playlist_id}: {e}")
    return tracks


def main():
    parser = argparse.ArgumentParser(description="Spotify Playlist Sorter")
    parser.add_argument(
        "--rule", type=str, help="Run a specific rule by its ID (e.g., --rule jp)"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available rule IDs"
    )
    args = parser.parse_args()

    if args.list:
        print("\nAvailable rules:")
        for rule in SORTING_RULES:
            print(f" - {rule['id']} : {rule['name']}")
        return

    active_rules = SORTING_RULES
    if args.rule:
        active_rules = [r for r in SORTING_RULES if r["id"] == args.rule]
        if not active_rules:
            print(f"Error: No rule found with ID {args.rule}")
            print("Use --list to see available options")
            return

    print(f"Running {len(active_rules)} rule(s)...")

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public playlist-modify-private"
        )
    )

    print("--- 1. Scanning target playlist (prevent duplicates) ---")
    existing_tracks = {}
    for rule in active_rules:
        pid = rule["target_id"]
        tracks = get_all_playlist_tracks(sp, pid)
        uris = set()
        for item in tracks:
            if item["track"]:
                uris.add(item["track"]["uri"])
        existing_tracks[pid] = uris
    print(f"Found {len(existing_tracks[pid])} songs already in target playlist.")

    print("--- 2. Scanning source playlists ---")
    candidate_tracks = []
    candidate_artists = set()

    for i, playlist_id in enumerate(SOURCE_PLAYLISTS):
        print(f"Reading playlist {i+1}/{len(SOURCE_PLAYLISTS)}: {playlist_id}...")
        items = get_all_playlist_tracks(sp, playlist_id)
        print(f"Found {len(items)} tracks")

        for item in items:
            track = item["track"]
            if not track or not track["artists"]:
                continue
            track_data = {
                "uri": track["uri"],
                "name": track["name"],
                "artist_name": track["artists"][0]["name"],
                "artist_id": track["artists"][0].get("id"),
            }
            if track_data["artist_id"]:
                candidate_tracks.append(track_data)
                candidate_artists.add(track_data["artist_id"])

    print(f" > Total unique artists found: {len(candidate_artists)}")
    print(f" > Total tracks to check: {len(candidate_tracks)}")

    print(f"--- 3. Checking genres for {len(candidate_artists)} artists ---")
    artist_genre_map = get_artist_genre_map(list(candidate_artists), sp)

    print("--- 4. Sorting songs ---")
    songs_to_add_map = {rule["target_id"]: [] for rule in active_rules}

    for track in candidate_tracks:
        artist_id = track["artist_id"]
        track_uri = track["uri"]
        artist_genres = artist_genre_map.get(artist_id, [])

        for rule in active_rules:
            target_id = rule["target_id"]
            match_found = False
            matched_keyword = ""

            for genre in artist_genres:
                for keyword in rule["keywords"]:
                    if keyword in genre.lower():
                        match_found = True
                        matched_keyword = genre
                        break
                if match_found:
                    break

            if match_found:
                if (
                    track_uri not in existing_tracks[target_id]
                    and track_uri not in songs_to_add_map[target_id]
                ):
                    songs_to_add_map[target_id].append(track_uri)
                    print(
                        f"[{rule['id']}] match: {track['name']} - {track['artist_name']} ({matched_keyword})"
                    )

    print("--- 5. Updating playlists ---")
    for rule in active_rules:
        tid = rule["target_id"]
        songs = songs_to_add_map.get(tid, [])

        if songs:
            print(f"Adding {len(songs)} songs to {rule['name']}...")
            for i in range(0, len(songs), 100):
                sp.playlist_add_items(tid, songs[i : i + 100])
        else:
            print(f"No new songs for {rule['name']}")
    print("Done!")


if __name__ == "__main__":
    main()
