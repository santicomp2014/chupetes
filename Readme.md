# Voice Assistant for Text-to-Speech Communication

This project is an open-source Streamlit application designed to assist individuals with vocal impairments in communicating through text-to-speech technology. It's a tribute to a friend facing vocal cancer El Chupete, aiming to help them maintain their ability to communicate effectively.

## Project Structure

```
voice-assistant/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── tts.py
│   ├── ui.py
│   └── utils.py
│
├── config/
│   └── languages.json
│
├── requirements.txt
│
└── README.md
```

## Files Description

- `app/main.py`: The main Streamlit application entry point.
- `app/auth.py`: Handles authentication using Auth0.
- `app/tts.py`: Manages text-to-speech functionality using ElevenLabs API.
- `app/ui.py`: Contains UI-related functions and layouts.
- `app/utils.py`: Utility functions used across the application.
- `config/languages.json`: Configuration file for multilingual support.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This file, containing project information and setup instructions.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following contents:
   ```
   AUTH0_CLIENT_ID=your_auth0_client_id
   AUTH0_CLIENT_SECRET=your_auth0_client_secret
   AUTH0_DOMAIN=your_auth0_domain
   AUTH0_CALLBACK_URL=http://localhost:8501/callback
   ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

   Note: The API keys in the `.env` file will be used as default values. Users can override these in the application settings.

5. Run the Streamlit app:
   ```
   streamlit run app/main.py
   ```

## Features

- User authentication with Auth0
- Text-to-speech functionality using ElevenLabs API
- Multilingual support
- Customizable voice settings
- Chat history with replay function
- Mobile-friendly UI
- User-configurable API keys for ElevenLabs, OpenAI, and Anthropic

## Future Enhancements

- Voice cloning from audio files
- Integration with OpenAI or Anthropic for AI-assisted communication
- Phrase bank for quick access to common expressions
- Integration with alternative input methods
- Emotion conveying in speech
- Offline mode support

## Contributing

We welcome contributions to this project. Please feel free to submit issues and pull requests.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

This project is dedicated to our friend and all individuals facing challenges with vocal communication. Your strength and resilience inspire us.