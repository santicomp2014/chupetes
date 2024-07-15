from elevenlabs import generate, set_api_key, Voice, voices
from elevenlabs.api import APIError

def get_available_voices(api_key, lang):
    set_api_key(api_key)
    try:
        available_voices = voices()
        return [(voice.voice_id, voice.name) for voice in available_voices]
    except APIError as e:
        raise ValueError(f"{lang['error_fetching_voices']}: {str(e)}")

def text_to_speech(text, voice_id, settings, lang):
    api_key = settings.get('api_key')
    
    if not api_key:
        raise ValueError(lang["error_api_key_not_set"])

    # Set the API key for this request
    set_api_key(api_key)

    # Create a Voice object with the specified settings
    voice = Voice(
        voice_id=voice_id,
        settings={
            "stability": settings.get('stability', 0.5),
            "similarity_boost": settings.get('similarity_boost', 0.5)
        }
    )

    try:
        # Generate the audio
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        return audio
    except APIError as e:
        if "Invalid API key" in str(e):
            raise ValueError(lang["error_invalid_api_key"])
        else:
            raise ValueError(f"{lang['error_api']}: {str(e)}")