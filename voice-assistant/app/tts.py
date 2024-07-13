from elevenlabs import generate, set_api_key

def text_to_speech(text, voice_id, settings):
    # Set the API key for this request
    set_api_key(settings['api_key'])

    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v1",
        stability=settings.get('stability', 0.5),
        similarity_boost=settings.get('similarity_boost', 0.5)
    )
    return audio

# You can add more TTS-related functions here as needed