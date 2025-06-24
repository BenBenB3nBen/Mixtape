
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Mixtape Generator", page_icon="🎶")

st.title("🎶 Mixtape Generator")
st.markdown("Gib einen Song oder Künstler ein, um ähnliche Musik zu entdecken!")

client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-public"
))

query = st.text_input("🎧 Künstler oder Song eingeben", "")

if query:
    results = sp.search(q=query, limit=1, type="track")
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_id = track["id"]
        st.success(f"Gefunden: {track['name']} von {track['artists'][0]['name']}")
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        st.subheader("🎵 Ähnliche Songs")
        for rec in recommendations["tracks"]:
            name = rec["name"]
            artist = rec["artists"][0]["name"]
            url = rec["external_urls"]["spotify"]
            st.markdown(f"- [{name} – {artist}]({url})")
    else:
        st.error("Kein passender Song gefunden.")
