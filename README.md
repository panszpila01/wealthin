# Koteria - HTML File Processing Application

A Streamlit application for processing HTML files with a centralized login system.

## 🚀 Features

- **Centralized Login**: Secure login system with session management
- **HTML File Processing**: Upload and process HTML files with intelligent caching
- **Multi-Page Navigation**: Welcome page and file converter with state persistence
- **Session State Management**: Data persists across page navigation using `st.session_state`
- **Performance Optimization**: Cached file processing with `@st.cache_data`
- **Data Analysis**: Process and analyze HTML data with real-time feedback
- **Export Functionality**: Download processed data in CSV format
- **Responsive Design**: Clean, modern UI following Streamlit best practices

## 📁 Project Structure

Following [Streamlit best practices](https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745):

```
Koteria/
├── .streamlit/                   # Streamlit configuration
│   └── config.toml              # Global Streamlit settings
├── app/                          # Core application modules
│   ├── __init__.py              # Package initialization
│   ├── config.py                # App configuration and user management
│   ├── utils.py                 # Utility functions and session state management
│   └── html_processor.py        # HTML file processing functions
├── pages/                        # Multipage application pages
│   ├── 01_🏠_Welcome.py         # Welcome page with overview
│   └── 02_📁_File_Converter.py  # File processing page with caching
├── assets/                       # Static assets (images, styles)
├── data/                         # Data storage
│   ├── raw/                     # Raw data files
│   └── processed/               # Processed data files
├── main.py                       # Main application entry point
├── requirements.txt              # Python dependencies
├── TROUBLESHOOTING.md           # Troubleshooting guide
└── README.md                     # This file
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Koteria
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the main application:
```bash
streamlit run main.py
```

## 📖 Usage

### Running the Application

1. **Start the system:**
   ```bash
   streamlit run main.py
   ```

2. **Login with available users:**
   - **Admin** → Routes to Koteria app (HTML file processing)
   - **Koteria** → Routes to Koteria app (HTML file processing)

### Available Users

| Username | Password | Description |
|----------|----------|-------------|
| Admin | Admin | HTML file processing with wide layout |
| Koteria | Koteria | HTML file processing with wide layout |

## 🎯 Koteria Application

### Features
- **HTML File Processing**: Upload and process HTML files with intelligent caching
- **Multi-Page Navigation**: 
  - Welcome Page: Application overview, data status, and quick actions
  - File Converter: Upload, process, and analyze HTML files
- **Session State Management**: Data persists across page navigation using `st.session_state`
- **Performance Optimization**: Cached file processing prevents re-processing
- **Data Analysis**: Process HTML data and extract structured information
- **Export Functionality**: Download processed data as CSV
- **Layout**: Wide layout for better data visualization
- **Error Handling**: Robust error handling with user-friendly messages

## 🔧 Configuration

### App Configuration

The app can be configured in `app/config.py`:

```python
APP_CONFIGS["koteria"] = AppConfig(
    name="koteria",
    display_name="Koteria",
    layout="wide",
    page_icon="",
    custom_settings={
        "supported_file_types": ["html"],
        "show_dataframe_info": True
    }
)
```

### User Management

Add new users:

```python
USER_APP_MAPPING["NewUser"] = "koteria"
DEFAULT_CREDENTIALS["NewUser"] = "NewUser"
```

## 🛠️ Technical Implementation

### Session State Management
The application uses `st.session_state` to maintain data across page navigation, following [Streamlit best practices](https://discuss.streamlit.io/t/question-about-project-structure/28867/4):

- **Data Persistence**: Uploaded files and processed data persist across page changes
- **State Initialization**: All session variables are properly initialized
- **Cross-Page Communication**: Data can be accessed from any page

### Performance Optimization
Following the [dataprofessor multipage template](https://github.com/dataprofessor/st-multipage) pattern:

- **Caching**: File processing uses `@st.cache_data` to prevent re-processing
- **Efficient Navigation**: Page switching doesn't reload data
- **Memory Management**: Proper cleanup of temporary files

### Code Organization
Following [Streamlit best practices](https://medium.com/@jashuamrita360/best-practices-for-streamlit-development-structuring-code-and-managing-session-state-0bdcfb91a745):

- **Modular Structure**: Clean separation of concerns with dedicated directories
- **App Module**: Core functionality in `app/` directory with proper imports
- **Pages Directory**: Automatic multipage navigation with numbered pages
- **Utilities Module**: Common functions for session state and data management
- **Configuration Management**: Centralized config in `app/config.py`
- **Error Handling**: Robust error handling with user-friendly messages

## 📚 Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit LLM Examples](https://github.com/streamlit/llm-examples)
- [MySnowSight Example](https://github.com/mahanteshimath/mysnowsight)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
