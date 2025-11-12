# 🛍️ AI Shopping Assistant

An intelligent shopping assistant powered by Google's Gemini AI that helps you compare products, find deals, and get expert shopping advice.

## ✨ Features

- **Natural Conversational AI**: Get detailed, human-like responses to your shopping queries
- **Product Comparisons**: Compare specifications, features, and prices
- **Expert Advice**: Technical details and recommendations from AI
- **Real-time Search**: Integration with Serper API for up-to-date information
- **Clean Chat Interface**: Modern, user-friendly Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-shopping-assistant.git
   cd ai-shopping-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   
   Edit the `app.py` file and replace the API keys with your own:
   - **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Serper API Key**: Get from [Serper.dev](https://serper.dev/)
   - **AliExpress API Key**: Get from [RapidAPI](https://rapidapi.com/)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The app will automatically open at `http://localhost:8501`

## 📋 Requirements

- streamlit
- google-generativeai
- aiohttp
- requests

## 🛠️ Configuration

### API Keys Setup

```python
GEMINI_API_KEY = "your-gemini-api-key"
SERPER_KEY = "your-serper-api-key"
ALIEXPRESS_KEY = "your-rapidapi-key"
```

**⚠️ Security Note**: For production, use environment variables instead of hardcoding API keys.

## 💡 Usage Examples

- "Compare iPhone 15 vs Samsung Galaxy S24"
- "What are the best budget laptops under $500?"
- "Tell me about the latest gaming headsets"
- "Which smartwatch is better for fitness tracking?"

## 🏗️ Project Structure

```
ai-shopping-assistant/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore rules
└── LICENSE            # License file (optional)
```

## 🔧 Troubleshooting

### Gemini API Issues
- Verify your API key is correct
- Check if you have API quota remaining
- Ensure internet connection is stable

### Installation Issues
- Make sure Python 3.8+ is installed
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment to avoid conflicts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- Streamlit for the web interface
- Serper.dev for search capabilities

## 📧 Contact

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/ai-shopping-assistant](https://github.com/yourusername/ai-shopping-assistant)

---

**Note**: Remember to replace API keys with environment variables before deploying to production!
