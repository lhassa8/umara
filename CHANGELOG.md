# Changelog

All notable changes to Umara will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-11-27

### Fixed

- **`markdown()` component now properly renders GitHub Flavored Markdown**
  - Tables, bold, italic, strikethrough, lists, and code blocks now render correctly
  - Added `react-markdown` and `remark-gfm` dependencies to the frontend
  - Previously displayed raw markdown text instead of formatted content

- **`date_input()` now accepts Python `date` objects**
  - Previously threw "Object of type date is not JSON serializable" error
  - Now properly converts `date` objects to ISO format strings
  - `min_date` and `max_date` parameters also accept `date` objects

- **`file_uploader()` now renders properly with full functionality**
  - Fixed component type mismatch between Python (`fileuploader`) and frontend (`file_uploader`)
  - Added proper FileUploader React component with drag & drop support
  - Supports file type filtering, multiple file selection, and max file size validation
  - Shows uploaded file names and sizes after selection

- **`time_input()` now accepts Python `time` objects**
  - Previously threw "Object of type time is not JSON serializable" error
  - Now properly converts `datetime.time` objects to "HH:MM" format strings

- **`progress()` now auto-detects value range (0-1 or 0-100)**
  - Streamlit uses 0-1 range, Umara internally uses 0-100
  - Now automatically converts values in 0-1 range to percentages
  - Fixes progress bars showing 0%, 1%, 1% instead of 30%, 60%, 90%

- **Style dict handling in components**
  - Components now accept plain Python dicts for styling in addition to `Style` objects
  - Fixes crashes when passing `{"color": "red"}` instead of `Style(color="red")`

### Added

- 120+ UI components for building web applications
- 12 built-in themes (light, dark, ocean, forest, slate, nord, midnight, rose, copper, lavender, sunset, mint)
- Chat/conversation components (`chat`, `chat_message`, `chat_input`, `chat_container`)
- Navigation components (`sidebar`, `nav_link`, `breadcrumbs`, `pagination`, `steps`)
- Advanced input components (`rating`, `tag_input`, `color_picker`, `search_input`)
- Data display components (`dataframe`, `table`, `metric`, `stat_card`, `json_viewer`)
- Chart components (`line_chart`, `bar_chart`, `area_chart`, `pie_chart`, `scatter_chart`, `plotly_chart`)
- Layout components (`columns`, `grid`, `card`, `tabs`, `expander`, `accordion`, `modal`)
- Utility components (`copy_button`, `badge`, `avatar`, `timeline`, `loading_skeleton`)

### Known Issues

- `expander()` / `accordion()` - May cause blank pages in certain complex test configurations
- Modal content displays inline rather than as overlay (styling improvement needed)

## [0.2.0] - 2024-11-15

### Added

- Initial public release
- Core framework with WebSocket-based communication
- Basic UI components (buttons, inputs, text, etc.)
- 4 built-in themes (light, dark, ocean, forest)
- CLI for running apps (`umara run app.py`)
- Hot reload during development
- State management with `session_state`
- Form handling with batched submission

## [0.1.0] - 2024-10-01

### Added

- Initial development release
- Proof of concept for Python-to-React UI framework
