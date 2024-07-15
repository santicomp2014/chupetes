from elevenlabs import generate, set_api_key, Voice
from elevenlabs.api import APIError

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
            model="eleven_multilingual_v1"
        )
        return audio
    except APIError as e:
        if "Invalid API key" in str(e):
            raise ValueError(lang["error_invalid_api_key"])
        else:
            raise ValueError(f"{lang['error_api']}: {str(e)}")

# You can add more TTS-related functions here as needed