# 🧠 Personality AI Chat

A modern Streamlit chatbot where you can choose the AI's personality type to get responses tailored to different cognitive styles and communication patterns.

## ✨ Features

- **Personalized AI Responses** - Get answers tailored to your cognitive preferences
- **Modern UI Design** - Clean, minimalist interface with smooth animations
- **Chat History** - Keep track of your conversations
- **localStorage Integration** - Persistent user data across browser sessions
- **Memory System (Memobase)** - Long-term conversation memory with cloud sync
- **Powered by Mistral-7B** - Using Together.ai's advanced language model

## 📱 localStorage System

The application uses browser localStorage for immediate data persistence:

- **User Name Storage** - Remembers your name across browser sessions
- **Session Management** - Maintains user identity locally  
- **Browser ID Mapping** - Links browser sessions to cloud memory
- **Fast Access** - Instant loading without API calls
- **Privacy First** - Data stays on your device

```javascript
// localStorage functions currently used
saveNameToLocalStorage(name)
getNameFromLocalStorage()
saveBrowserIdToLocalStorage(browserId)
getBrowserIdFromLocalStorage()
saveMemobaseMappingForBrowser(browserId, memobaseId)
getMemobaseMappingForBrowser(browserId)
```

## 🧠 Memory (Hafıza) Sistemi - Memobase Entegrasyonu

Advanced cloud-based memory system for long-term conversation storage:

### Key Features:
- **Long-term Memory** - Conversations saved to cloud storage
- **Cross-Device Sync** - Access your history from any device  
- **Context Awareness** - AI remembers previous conversations
- **Manual Save Control** - Choose what to save to preserve API credits
- **Profile Building** - System learns about user preferences over time

### How It Works:
1. **Browser Identity** - Unique ID generated and stored in localStorage
2. **Cloud Mapping** - Browser ID mapped to Memobase user account
3. **Conversation Storage** - Chat history saved as ChatBlob format
4. **Context Retrieval** - Relevant past conversations inform AI responses
5. **Memory Flush** - Triggers profile and event extraction

### Memory Architecture:
```
localStorage (Fast) ←→ Memobase Cloud (Persistent)
      ↓                       ↓
 User Identity          Conversation History
 Session Data           Cross-Device Sync
```

## 🏗️ System Architecture Diagram

Complete data flow architecture of the Personality AI Chat system:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              🧠 Personality AI Chat                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    👤 User Input                   📱 Browser Storage              ☁️  Cloud Memory
    ┌─────────────┐                ┌─────────────────┐             ┌─────────────────┐
    │             │                │                 │             │                 │
    │ • Question  │───────────────▶│ • User Name     │◀───────────▶│ • Chat History  │
    │ • Personality│                │ • Browser ID    │             │ • User Context  │
    │   Type       │                │ • Session Data  │             │ • Profile Data  │
    │             │                │                 │             │                 │
    └─────────────┘                └─────────────────┘             └─────────────────┘
           │                                │                              ▲
           │                                │                              │
           ▼                                ▼                              │
    ┌─────────────────────────────────────────────────────────────────────┴─────────┐
    │                          🤖 AI Processing Layer                              │
    │                                                                              │
    │  ┌─────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
    │  │   Memory    │───▶│ Prompt Builder  │───▶│     Together.ai API         │  │
    │  │  Context    │    │ + Personality   │    │     (Mistral-7B)           │  │
    │  │ Retrieval   │    │ + User History  │    │                             │  │
    │  └─────────────┘    └─────────────────┘    └─────────────────────────────┘  │
    │                                                           │                  │
    └───────────────────────────────────────────────────────────┼──────────────────┘
                                                                │
                                                                ▼
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                           📤 Response & Storage                                │
    │                                                                               │
    │ ┌─────────────────┐    ┌──────────────┐    ┌────────────────────────────────┐ │
    │ │ ✨ Personality  │───▶│ 💬 Chat UI   │───▶│ 💾 Save to Memory? (Manual)   │ │
    │ │ AI Response     │    │ Display      │    │                                │ │
    │ │                 │    │              │    │ ├─ Yes → Cloud Storage        │ │
    │ └─────────────────┘    └──────────────┘    │ └─ No  → Session Only         │ │
    │                                            └────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────────────────┘

                                ⚡ Data Flow:
    
    1. 👤 User enters question & selects personality type
    2. 📱 localStorage saves user name and browser mapping instantly  
    3. ☁️  Memobase retrieves relevant conversation history
    4. 🔧 System builds personality-specific prompt with context
    5. 🤖 Together.ai API processes with Mistral-7B model
    6. ✨ AI generates response matching selected personality type
    7. 💬 Response displayed in chat interface
    8. 💾 User manually decides to save to long-term memory
```

## 🛠️ Technologies Used

- **Streamlit** - Web application framework
- **Together.ai API** - AI language model (Mistral-7B)
- **Memobase** - Cloud memory and context management
- **JavaScript localStorage** - Browser-based data persistence
- **Python** - Backend logic
- **CSS** - Custom styling and animations

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cognitype-chatbot.git
   cd cognitype-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env.local` file:
   ```bash
   TOGETHER_API_KEY="your-together-ai-api-key"
   MEMOBASE_API_KEY="your-memobase-api-key"
   MEMOBASE_URL="https://api.memobase.dev"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment

This application can be deployed on various platforms:

- **Streamlit Community Cloud** (Free)
- **Railway** ($5/month, no sleep mode)
- **Render** (Free tier with sleep mode)
- **DigitalOcean App Platform** ($5/month)


## 🤖 AI Integration

The chatbot uses Together.ai's Mistral-7B model with personality-specific prompts:

- **Personalized Responses** - Each personality type gets tailored communication style
- **Context Awareness** - Considers cognitive preferences and decision-making patterns
- **Error Handling** - Robust API error management
- **Rate Limiting** - Handles API limits gracefully

## 🔒 Environment Variables

```bash
TOGETHER_API_KEY=your-together-ai-api-key-here
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit • Powered by Together.ai & Mistral-7B** 