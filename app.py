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

with st.form("search_form"):
    query = st.text_input("🎧 Künstler oder Song eingeben", "")
    submitted = st.form_submit_button("🔍 Suche starten")

if submitted and query:
    results = sp.search(q=query, type="track", limit=10)
    found_track = None

    for track in results["tracks"]["items"]:
        name = track["name"].lower()
        artist = track["artists"][0]["name"].lower()
        if all(term in (name + " " + artist) for term in query.lower().split()):
            found_track = track
            break

    if found_track:
        track_id = found_track["id"]
        st.success(f"Gefunden: {found_track['name']} von {found_track['artists'][0]['name']}")
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        st.subheader("🎵 Ähnliche Songs")
        for rec in recommendations["tracks"]:
            name = rec["name"]
            artist = rec["artists"][0]["name"]
            url = rec["external_urls"]["spotify"]
            st.markdown(f"- [{name} – {artist}]({url})")
    else:
        st.error("Kein passender Song gefunden.")
