# playlist-sorter
organises music library by scanning source playlists and sorting tracks into specific target playlists based on the artist's genres and language-specific keywords

## Getting Started
### 1. Prerequisites

* Python 3.x
* A Spotify Developer account

### 2. Spotify API Setup

Register an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

1. Log in and click **Create app**.
2. Set the **Redirect URI** to `http://127.0.0.1:8000/callback` (or any valid local URL).
3. Note down your **Client ID** and **Client Secret**.

### 3. Installation

```bash
pip install spotipy python-dotenv

```

### 4. Configuration

You need to provide your Spotify credentials via a `.env` file. Create a file named `.env` in the root directory and add the following:

```env
SPOTIPY_CLIENT_ID='your_client_id_here'
SPOTIPY_CLIENT_SECRET='your_client_secret_here'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:8000/callback'

```

### 5. Customising Your Playlists

Edit `main.py` to include your specific Spotify playlist IDs:

* **SOURCE_PLAYLISTS**: Add the IDs of the playlists you want the script to scan for songs.
* **SORTING_RULES**: Update the `target_id` for each rule (e.g., `jp`, `ar`, `zh`) with the ID of the playlist where you want those songs to go.
* **Keywords**: You can refer to `raw_genres.txt` to find more specific Spotify genre keywords to add to your rules.

### Running
To see all configured language/genre rules and their IDs:

```bash
python main.py --list

```
To scan all source playlists and sort songs into every target playlist defined in `SORTING_RULES`:

```bash
python main.py

```
To run only one specific rule (e.g., just for Japanese music):

```bash
python main.py --rule jp

```
