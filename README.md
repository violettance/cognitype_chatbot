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

```mermaid
graph TD
    %% User Layer
    User[👤 User Input<br/>• Question<br/>• Personality Type] 
    
    %% Storage Layer
    subgraph Storage ["💾 Storage Layer"]
        LocalStorage[📱 Browser Storage<br/>• User Name<br/>• Browser ID<br/>• Session Data]
        CloudMemory[☁️ Cloud Memory<br/>• Chat History<br/>• User Context<br/>• Profile Data]
    end
    
    %% Processing Layer
    subgraph AILayer ["🤖 AI Processing Layer"]
        MemoryRetrieval[🧠 Memory Context<br/>Retrieval]
        PromptBuilder[🔧 Prompt Builder<br/>+ Personality<br/>+ User History]
        TogetherAPI[🚀 Together.ai API<br/>Mistral-7B Model]
    end
    
    %% Response Layer
    subgraph ResponseLayer ["📤 Response & Storage"]
        AIResponse[✨ Personality<br/>AI Response]
        ChatUI[💬 Chat UI<br/>Display]
        SaveDecision{💾 Save to Memory?<br/>Manual Choice}
        CloudSave[☁️ Save to Cloud]
        SessionOnly[📱 Session Only]
    end
    
    %% Data Flow Connections
    User --> LocalStorage
    User --> MemoryRetrieval
    LocalStorage <--> CloudMemory
    CloudMemory --> MemoryRetrieval
    MemoryRetrieval --> PromptBuilder
    PromptBuilder --> TogetherAPI
    TogetherAPI --> AIResponse
    AIResponse --> ChatUI
    ChatUI --> SaveDecision
    SaveDecision -->|Yes| CloudSave
    SaveDecision -->|No| SessionOnly
    CloudSave --> CloudMemory
    
    %% Styling
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef storageClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef aiClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef responseClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class User userClass
    class LocalStorage,CloudMemory storageClass
    class MemoryRetrieval,PromptBuilder,TogetherAPI aiClass
    class AIResponse,ChatUI,SaveDecision,CloudSave,SessionOnly responseClass
```

### ⚡ Data Flow Steps:

1. **👤 User Input** - User enters question & selects personality type
2. **📱 Local Storage** - localStorage saves user name and browser mapping instantly  
3. **☁️ Memory Retrieval** - Memobase retrieves relevant conversation history
4. **🔧 Prompt Building** - System builds personality-specific prompt with context
5. **🤖 AI Processing** - Together.ai API processes with Mistral-7B model
6. **✨ Response Generation** - AI generates response matching selected personality type
7. **💬 UI Display** - Response displayed in chat interface
8. **💾 Storage Decision** - User manually decides to save to long-term memory

### 🔄 Memory Architecture:
```mermaid
graph LR
    subgraph Browser ["🌐 Browser"]
        LS[📱 localStorage<br/>Fast Access]
    end
    
    subgraph Cloud ["☁️ Cloud"]
        MB[🧠 Memobase<br/>Persistent Storage]
    end
    
    LS <-->|Sync| MB
    
    LS --> UI[👤 User Identity<br/>📊 Session Data]
    MB --> CH[💬 Conversation History<br/>🔄 Cross-Device Sync]
    
    classDef browserClass fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef cloudClass fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef dataClass fill:#fce4ec,stroke:#ad1457,stroke-width:2px
    
    class LS,Browser browserClass
    class MB,Cloud cloudClass
    class UI,CH dataClass
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