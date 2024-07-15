from elevenlabs import generate, set_api_key, Voice

def text_to_speech(text, voice_id, settings):
    # Set the API key for this request
    set_api_key(settings['api_key'])

    # Create a Voice object with the specified settings
    voice = Voice(
        voice_id=voice_id,
        settings={
            "stability": settings.get('stability', 0.5),
            "similarity_boost": settings.get('similarity_boost', 0.5)
        }
    )

    # Generate the audio
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v1"
    )
    return audio

# You can add more TTS-related functions here as needed