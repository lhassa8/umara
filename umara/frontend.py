"""
Modern frontend renderer for Umara.

Features:
- Smart DOM diffing (only updates changed components)
- Smooth CSS animations and transitions
- Toast notification system
- Loading states
- Keyboard accessibility
- Responsive design
"""


def get_frontend_html(title: str) -> str:
    """Generate the complete frontend HTML with modern JavaScript."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        /* ============================================
           CSS Reset & Base Styles
           ============================================ */
        *, *::before, *::after {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            /* Default theme variables */
            --um-color-primary: #6366f1;
            --um-color-primary-hover: #4f46e5;
            --um-color-primary-light: #e0e7ff;
            --um-color-secondary: #64748b;
            --um-color-background: #ffffff;
            --um-color-background-secondary: #f8fafc;
            --um-color-surface: #ffffff;
            --um-color-border: #e2e8f0;
            --um-color-text: #0f172a;
            --um-color-text-secondary: #64748b;
            --um-color-success: #10b981;
            --um-color-success-light: #d1fae5;
            --um-color-warning: #f59e0b;
            --um-color-warning-light: #fef3c7;
            --um-color-error: #ef4444;
            --um-color-error-light: #fee2e2;
            --um-color-info: #3b82f6;
            --um-color-info-light: #dbeafe;

            /* Animations */
            --um-transition-fast: 150ms ease;
            --um-transition-normal: 200ms ease;
            --um-transition-slow: 300ms ease;

            /* Shadows */
            --um-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --um-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --um-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --um-shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

            /* Border radius */
            --um-radius-sm: 6px;
            --um-radius-md: 8px;
            --um-radius-lg: 12px;
            --um-radius-xl: 16px;
            --um-radius-full: 9999px;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--um-color-background);
            color: var(--um-color-text);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            transition: background var(--um-transition-slow), color var(--um-transition-slow);
        }}

        #root {{
            min-height: 100vh;
        }}

        /* ============================================
           Loading Screen
           ============================================ */
        .um-loading-screen {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            gap: 20px;
        }}

        .um-loading-spinner {{
            width: 48px;
            height: 48px;
            border: 3px solid var(--um-color-border);
            border-top-color: var(--um-color-primary);
            border-radius: 50%;
            animation: um-spin 0.8s linear infinite;
        }}

        @keyframes um-spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* ============================================
           Toast Notifications
           ============================================ */
        .um-toast-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }}

        .um-toast {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 20px;
            background: var(--um-color-surface);
            border-radius: var(--um-radius-lg);
            box-shadow: var(--um-shadow-lg);
            border-left: 4px solid var(--um-color-primary);
            pointer-events: auto;
            animation: um-toast-in 0.3s ease;
            max-width: 400px;
        }}

        .um-toast.success {{ border-left-color: var(--um-color-success); }}
        .um-toast.error {{ border-left-color: var(--um-color-error); }}
        .um-toast.warning {{ border-left-color: var(--um-color-warning); }}
        .um-toast.info {{ border-left-color: var(--um-color-info); }}

        .um-toast.removing {{
            animation: um-toast-out 0.3s ease forwards;
        }}

        @keyframes um-toast-in {{
            from {{ opacity: 0; transform: translateX(100px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}

        @keyframes um-toast-out {{
            from {{ opacity: 1; transform: translateX(0); }}
            to {{ opacity: 0; transform: translateX(100px); }}
        }}

        /* ============================================
           Component Animations
           ============================================ */
        @keyframes um-fade-in {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes um-slide-up {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes um-scale-in {{
            from {{ opacity: 0; transform: scale(0.95); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        @keyframes um-skeleton {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}

        .um-animate-fade {{ animation: um-fade-in 0.3s ease; }}
        .um-animate-slide {{ animation: um-slide-up 0.3s ease; }}
        .um-animate-scale {{ animation: um-scale-in 0.2s ease; }}

        /* ============================================
           Interactive States
           ============================================ */
        .um-interactive {{
            transition: transform var(--um-transition-fast), box-shadow var(--um-transition-fast);
        }}

        .um-interactive:hover {{
            transform: translateY(-1px);
        }}

        .um-interactive:active {{
            transform: translateY(0);
        }}

        /* ============================================
           Focus Styles (Accessibility)
           ============================================ */
        *:focus-visible {{
            outline: 2px solid var(--um-color-primary);
            outline-offset: 2px;
        }}

        button:focus-visible,
        input:focus-visible,
        select:focus-visible,
        textarea:focus-visible {{
            outline: 2px solid var(--um-color-primary);
            outline-offset: 2px;
        }}

        /* ============================================
           Responsive Utilities
           ============================================ */
        @media (max-width: 768px) {{
            .um-hide-mobile {{ display: none !important; }}
            .um-columns {{ grid-template-columns: 1fr !important; }}
        }}

        /* ============================================
           Scrollbar Styling
           ============================================ */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--um-color-background-secondary);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--um-color-border);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--um-color-text-secondary);
        }}
    </style>
</head>
<body>
    <div id="root">
        <div class="um-loading-screen">
            <div class="um-loading-spinner"></div>
            <div style="color: var(--um-color-text-secondary); font-size: 14px;">Loading Umara...</div>
        </div>
    </div>

    <!-- Toast Container -->
    <div id="um-toast-container" class="um-toast-container"></div>

    <script type="module">
        // ============================================
        // Umara Frontend Client v2.0
        // ============================================

        class UmaraToast {{
            static container = document.getElementById('um-toast-container');

            static show(message, type = 'info', duration = 4000) {{
                const toast = document.createElement('div');
                toast.className = `um-toast ${{type}}`;

                const icons = {{
                    success: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-success)"/><path d="M6 10l3 3 5-6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
                    error: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-error)"/><path d="M7 7l6 6M13 7l-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
                    warning: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-warning)"/><path d="M10 6v5M10 14v.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
                    info: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-info)"/><path d="M10 9v5M10 6v.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>'
                }};

                toast.innerHTML = `
                    ${{icons[type] || icons.info}}
                    <span style="flex: 1; font-size: 14px;">${{message}}</span>
                    <button onclick="this.parentElement.remove()" style="background: none; border: none; cursor: pointer; padding: 4px; opacity: 0.5;">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                    </button>
                `;

                this.container.appendChild(toast);

                if (duration > 0) {{
                    setTimeout(() => {{
                        toast.classList.add('removing');
                        setTimeout(() => toast.remove(), 300);
                    }}, duration);
                }}

                return toast;
            }}

            static success(message, duration) {{ return this.show(message, 'success', duration); }}
            static error(message, duration) {{ return this.show(message, 'error', duration); }}
            static warning(message, duration) {{ return this.show(message, 'warning', duration); }}
            static info(message, duration) {{ return this.show(message, 'info', duration); }}
        }}

        // Make toast globally available
        window.UmaraToast = UmaraToast;

        class UmaraClient {{
            constructor() {{
                this.ws = null;
                this.sessionId = null;
                this.reconnectAttempts = 0;
                this.maxReconnectAttempts = 10;
                this.componentCache = new Map();
                this.currentTree = null;
                this.debounceTimers = new Map();
            }}

            connect() {{
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                this.ws = new WebSocket(`${{protocol}}//${{window.location.host}}/ws`);

                this.ws.onopen = () => {{
                    console.log('%c Umara Connected ', 'background: #6366f1; color: white; padding: 4px 8px; border-radius: 4px;');
                    this.reconnectAttempts = 0;
                }};

                this.ws.onmessage = (event) => {{
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                }};

                this.ws.onclose = () => {{
                    console.log('%c Umara Disconnected ', 'background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px;');
                    this.attemptReconnect();
                }};

                this.ws.onerror = (error) => {{
                    console.error('WebSocket error:', error);
                }};
            }}

            attemptReconnect() {{
                if (this.reconnectAttempts < this.maxReconnectAttempts) {{
                    this.reconnectAttempts++;
                    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts - 1), 30000);
                    console.log(`Reconnecting in ${{delay}}ms...`);
                    setTimeout(() => this.connect(), delay);
                }} else {{
                    UmaraToast.error('Connection lost. Please refresh the page.');
                }}
            }}

            handleMessage(data) {{
                if (data.type === 'init') {{
                    this.sessionId = data.sessionId;
                    this.render(data.data, true);
                }} else if (data.type === 'update') {{
                    this.render(data.data, false);
                }} else if (data.type === 'toast') {{
                    UmaraToast.show(data.message, data.variant);
                }} else if (data.type === 'error') {{
                    console.error('Server error:', data.error);
                    UmaraToast.error(data.error);
                }}
            }}

            send(message) {{
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {{
                    this.ws.send(JSON.stringify(message));
                }}
            }}

            sendEvent(componentId, eventType, payload = {{}}) {{
                this.send({{
                    type: 'event',
                    componentId,
                    eventType,
                    payload,
                }});
            }}

            sendStateUpdate(key, value) {{
                // Debounce rapid updates
                if (this.debounceTimers.has(key)) {{
                    clearTimeout(this.debounceTimers.get(key));
                }}

                this.debounceTimers.set(key, setTimeout(() => {{
                    this.send({{
                        type: 'state',
                        key,
                        value,
                    }});
                    this.debounceTimers.delete(key);
                }}, 50));
            }}

            render(data, isInitial) {{
                const root = document.getElementById('root');
                if (!data.tree) return;

                // Save focus state and current value (to preserve user input during re-render)
                const activeEl = document.activeElement;
                const activeId = activeEl?.dataset?.umId || '';
                const selectionStart = activeEl?.selectionStart;
                const selectionEnd = activeEl?.selectionEnd;
                const activeValue = (activeEl?.tagName === 'INPUT' || activeEl?.tagName === 'TEXTAREA') ? activeEl.value : null;
                const scrollPositions = new Map();

                // Save scroll positions
                document.querySelectorAll('[data-um-scroll]').forEach(el => {{
                    scrollPositions.set(el.dataset.umId, el.scrollTop);
                }});

                // Render the component tree
                root.innerHTML = '';
                const element = this.renderComponent(data.tree, isInitial);
                root.appendChild(element);

                // Apply theme
                this.applyTheme(data.theme);

                // Restore focus and preserve user's current input value
                if (activeId) {{
                    const newActiveEl = document.querySelector(`[data-um-id="${{activeId}}"]`);
                    if (newActiveEl && (newActiveEl.tagName === 'INPUT' || newActiveEl.tagName === 'TEXTAREA')) {{
                        // Restore the value the user had typed (not the server's stale value)
                        if (activeValue !== null && activeValue !== newActiveEl.value) {{
                            newActiveEl.value = activeValue;
                            // Send updated state to sync with server
                            const stateKey = newActiveEl.dataset?.stateKey;
                            if (stateKey) {{
                                this.sendStateUpdate(stateKey, activeValue);
                            }}
                        }}
                        newActiveEl.focus();
                        if (typeof selectionStart === 'number') {{
                            try {{ newActiveEl.setSelectionRange(selectionStart, selectionEnd); }} catch (e) {{}}
                        }}
                    }}
                }}

                // Restore scroll positions
                scrollPositions.forEach((top, id) => {{
                    const el = document.querySelector(`[data-um-id="${{id}}"]`);
                    if (el) el.scrollTop = top;
                }});
            }}

            applyTheme(theme) {{
                if (!theme) return;
                const root = document.documentElement;
                const colors = theme.colors || {{}};

                Object.entries(colors).forEach(([key, value]) => {{
                    root.style.setProperty(`--um-color-${{key.replace(/_/g, '-')}}`, value);
                }});

                // Update body background and color
                document.body.style.background = colors.background || '';
                document.body.style.color = colors.text || '';
            }}

            renderComponent(component, animate = false) {{
                if (!component) return document.createTextNode('');

                const {{ id, type, props = {{}}, children, style }} = component;
                const animClass = animate ? ' um-animate-fade' : '';

                // Component rendering switch
                const el = this.createComponent(type, id, props, children, animate);

                // Apply custom styles
                if (style) {{
                    Object.entries(style).forEach(([key, value]) => {{
                        el.style[key] = value;
                    }});
                }}

                return el;
            }}

            createComponent(type, id, props, children, animate) {{
                const animClass = animate ? 'um-animate-slide' : '';

                switch (type) {{
                    case 'root':
                        return this.createRoot(children, animate);
                    case 'text':
                        return this.createText(props);
                    case 'header':
                        return this.createHeader(props);
                    case 'subheader':
                        return this.createSubheader(props);
                    case 'button':
                        return this.createButton(id, props);
                    case 'input':
                        return this.createInput(id, props);
                    case 'text_area':
                        return this.createTextArea(id, props);
                    case 'slider':
                        return this.createSlider(id, props);
                    case 'select':
                        return this.createSelect(id, props);
                    case 'checkbox':
                        return this.createCheckbox(id, props);
                    case 'toggle':
                        return this.createToggle(id, props);
                    case 'radio':
                        return this.createRadio(id, props);
                    case 'card':
                        return this.createCard(children, props, animate);
                    case 'container':
                        return this.createContainer(children, animate);
                    case 'columns':
                        return this.createColumns(props, children, animate);
                    case 'column':
                        return this.createColumn(children, animate);
                    case 'grid':
                        return this.createGrid(props, children, animate);
                    case 'divider':
                        return this.createDivider();
                    case 'spacer':
                        return this.createSpacer(props);
                    case 'success':
                    case 'error':
                    case 'warning':
                    case 'info':
                        return this.createAlert(type, props);
                    case 'metric':
                        return this.createMetric(props);
                    case 'progress':
                        return this.createProgress(props);
                    case 'badge':
                        return this.createBadge(props);
                    case 'avatar':
                        return this.createAvatar(props);
                    case 'stat_card':
                        return this.createStatCard(props);
                    case 'tabs':
                        return this.createTabs(id, props, children);
                    case 'tab':
                        return this.createTab(children, animate);
                    case 'dataframe':
                        return this.createDataframe(props);
                    case 'chat':
                        return this.createChat(id, props);
                    case 'chat_message':
                        return this.createChatMessage(props);
                    case 'chat_input':
                        return this.createChatInput(id, props);
                    case 'chat_container':
                        return this.createChatContainer(id, props, children);
                    case 'expander':
                        return this.createExpander(id, props, children);
                    case 'modal':
                        return this.createModal(id, props, children);
                    case 'breadcrumbs':
                        return this.createBreadcrumbs(props);
                    case 'pagination':
                        return this.createPagination(id, props);
                    case 'steps':
                        return this.createSteps(props);
                    case 'timeline':
                        return this.createTimeline(props);
                    case 'number_input':
                        return this.createNumberInput(id, props);
                    case 'date_input':
                        return this.createDateInput(id, props);
                    case 'time_input':
                        return this.createTimeInput(id, props);
                    case 'color_picker':
                        return this.createColorPicker(id, props);
                    case 'rating':
                        return this.createRating(id, props);
                    case 'code':
                        return this.createCode(props);
                    case 'markdown':
                        return this.createMarkdown(props);
                    case 'json_viewer':
                        return this.createJsonViewer(props);
                    case 'chart':
                        return this.createChart(props);
                    case 'empty_state':
                        return this.createEmptyState(props, children);
                    case 'loading_skeleton':
                        return this.createSkeleton(props);
                    case 'html':
                        return this.createHtml(props);
                    case 'iframe':
                        return this.createIframe(props);
                    default:
                        return this.createGeneric(type, props, children, animate);
                }}
            }}

            // ============================================
            // Component Creators
            // ============================================

            createRoot(children, animate) {{
                const el = document.createElement('div');
                el.className = 'umara-root';
                el.style.cssText = 'max-width: 1200px; margin: 0 auto; padding: 24px; min-height: 100vh;';
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}

            createText(props) {{
                const el = document.createElement('p');
                el.textContent = props.content || '';
                el.style.cssText = `margin-bottom: 8px; color: ${{props.color || 'inherit'}}; font-size: ${{props.size || '16px'}};`;
                return el;
            }}

            createHeader(props) {{
                const level = props.level || 1;
                const el = document.createElement(`h${{Math.min(level, 6)}}`);
                el.textContent = props.content || '';
                const sizes = {{ 1: '2.5rem', 2: '2rem', 3: '1.75rem', 4: '1.5rem', 5: '1.25rem', 6: '1rem' }};
                el.style.cssText = `font-weight: 700; font-size: ${{sizes[level] || sizes[1]}}; margin-bottom: 16px; color: var(--um-color-text); letter-spacing: -0.02em;`;
                return el;
            }}

            createSubheader(props) {{
                const el = document.createElement('h3');
                el.textContent = props.content || '';
                el.style.cssText = 'font-weight: 600; font-size: 1.25rem; margin-bottom: 12px; color: var(--um-color-text);';
                return el;
            }}

            createButton(id, props) {{
                const el = document.createElement('button');
                el.textContent = props.label || 'Button';
                el.disabled = props.disabled || false;
                el.className = 'um-interactive';

                const variants = {{
                    primary: 'background: var(--um-color-primary); color: white; border: none;',
                    secondary: 'background: var(--um-color-background-secondary); color: var(--um-color-text); border: 1px solid var(--um-color-border);',
                    outline: 'background: transparent; color: var(--um-color-primary); border: 1px solid var(--um-color-primary);',
                    ghost: 'background: transparent; color: var(--um-color-text); border: none;',
                    danger: 'background: var(--um-color-error); color: white; border: none;'
                }};

                el.style.cssText = `
                    padding: 10px 20px; border-radius: var(--um-radius-md); font-size: 14px; font-weight: 500;
                    cursor: pointer; transition: all var(--um-transition-fast); display: inline-flex;
                    align-items: center; gap: 8px; ${{variants[props.variant] || variants.primary}}
                `;

                el.onmouseenter = () => {{ if (!el.disabled) el.style.filter = 'brightness(0.95)'; }};
                el.onmouseleave = () => {{ el.style.filter = ''; }};
                el.onclick = () => {{ if (!el.disabled) this.sendStateUpdate((props.stateKey || id) + '_clicked', true); }};

                return el;
            }}

            createInput(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px; color: var(--um-color-text);';
                    wrapper.appendChild(label);
                }}

                const input = document.createElement('input');
                input.type = props.type || 'text';
                input.value = props.value || '';
                input.placeholder = props.placeholder || '';
                input.dataset.umId = id;
                input.dataset.stateKey = props.stateKey || id;
                input.style.cssText = `
                    width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; transition: all var(--um-transition-fast);
                    background: var(--um-color-surface); color: var(--um-color-text); outline: none;
                `;

                input.onfocus = () => {{ input.style.borderColor = 'var(--um-color-primary)'; input.style.boxShadow = '0 0 0 3px var(--um-color-primary-light)'; }};
                input.onblur = () => {{ input.style.borderColor = 'var(--um-color-border)'; input.style.boxShadow = ''; }};
                input.oninput = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);

                wrapper.appendChild(input);
                return wrapper;
            }}

            createTextArea(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const textarea = document.createElement('textarea');
                textarea.value = props.value || '';
                textarea.placeholder = props.placeholder || '';
                textarea.rows = props.rows || 4;
                textarea.dataset.umId = id;
                textarea.dataset.stateKey = props.stateKey || id;
                textarea.style.cssText = `
                    width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; resize: vertical; font-family: inherit;
                    background: var(--um-color-surface); color: var(--um-color-text); outline: none;
                    transition: all var(--um-transition-fast);
                `;

                textarea.onfocus = () => {{ textarea.style.borderColor = 'var(--um-color-primary)'; textarea.style.boxShadow = '0 0 0 3px var(--um-color-primary-light)'; }};
                textarea.onblur = () => {{ textarea.style.borderColor = 'var(--um-color-border)'; textarea.style.boxShadow = ''; }};
                textarea.oninput = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);

                wrapper.appendChild(textarea);
                return wrapper;
            }}

            createSlider(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const labelRow = document.createElement('div');
                    labelRow.style.cssText = 'display: flex; justify-content: space-between; font-size: 14px; font-weight: 500; margin-bottom: 8px;';
                    labelRow.innerHTML = `<span>${{props.label}}</span><span style="color: var(--um-color-primary); font-weight: 600;">${{props.value ?? props.min ?? 0}}</span>`;
                    wrapper.appendChild(labelRow);
                }}

                const slider = document.createElement('input');
                slider.type = 'range';
                slider.min = props.min || 0;
                slider.max = props.max || 100;
                slider.value = props.value ?? props.min ?? 0;
                slider.step = props.step || 1;
                slider.style.cssText = `
                    width: 100%; height: 6px; -webkit-appearance: none; appearance: none;
                    background: linear-gradient(to right, var(--um-color-primary) 0%, var(--um-color-primary) ${{((props.value - props.min) / (props.max - props.min)) * 100}}%, var(--um-color-border) ${{((props.value - props.min) / (props.max - props.min)) * 100}}%, var(--um-color-border) 100%);
                    border-radius: 3px; outline: none; cursor: pointer;
                `;

                slider.oninput = (e) => {{
                    const val = parseFloat(e.target.value);
                    const pct = ((val - props.min) / (props.max - props.min)) * 100;
                    slider.style.background = `linear-gradient(to right, var(--um-color-primary) 0%, var(--um-color-primary) ${{pct}}%, var(--um-color-border) ${{pct}}%, var(--um-color-border) 100%)`;
                    if (wrapper.querySelector('span:last-child')) wrapper.querySelector('div span:last-child').textContent = val;
                    this.sendStateUpdate(props.stateKey || id, val);
                }};

                wrapper.appendChild(slider);
                return wrapper;
            }}

            createSelect(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const select = document.createElement('select');
                select.style.cssText = `
                    width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; background: var(--um-color-surface);
                    color: var(--um-color-text); outline: none; cursor: pointer;
                    transition: all var(--um-transition-fast);
                `;

                (props.options || []).forEach(opt => {{
                    const option = document.createElement('option');
                    option.value = typeof opt === 'object' ? opt.value : opt;
                    option.textContent = typeof opt === 'object' ? opt.label : opt;
                    if (props.value === option.value) option.selected = true;
                    select.appendChild(option);
                }});

                select.onfocus = () => {{ select.style.borderColor = 'var(--um-color-primary)'; }};
                select.onblur = () => {{ select.style.borderColor = 'var(--um-color-border)'; }};
                select.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);

                wrapper.appendChild(select);
                return wrapper;
            }}

            createCheckbox(id, props) {{
                const wrapper = document.createElement('label');
                wrapper.style.cssText = 'display: flex; align-items: center; gap: 10px; cursor: pointer; margin-bottom: 12px;';

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = props.value || false;
                checkbox.style.cssText = 'width: 18px; height: 18px; accent-color: var(--um-color-primary); cursor: pointer;';
                checkbox.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.checked);

                const label = document.createElement('span');
                label.textContent = props.label || '';
                label.style.cssText = 'font-size: 14px;';

                wrapper.appendChild(checkbox);
                wrapper.appendChild(label);
                return wrapper;
            }}

            createToggle(id, props) {{
                const wrapper = document.createElement('label');
                wrapper.style.cssText = 'display: flex; align-items: center; gap: 12px; cursor: pointer; margin-bottom: 12px;';

                const track = document.createElement('div');
                track.style.cssText = `
                    width: 48px; height: 26px; border-radius: 13px; position: relative;
                    background: ${{props.value ? 'var(--um-color-primary)' : 'var(--um-color-border)'}};
                    transition: background var(--um-transition-fast);
                `;

                const thumb = document.createElement('div');
                thumb.style.cssText = `
                    width: 22px; height: 22px; border-radius: 50%; background: white;
                    position: absolute; top: 2px; left: ${{props.value ? '24px' : '2px'}};
                    transition: left var(--um-transition-fast); box-shadow: var(--um-shadow-sm);
                `;
                track.appendChild(thumb);

                const label = document.createElement('span');
                label.textContent = props.label || '';
                label.style.cssText = 'font-size: 14px;';

                wrapper.onclick = () => this.sendStateUpdate(props.stateKey || id, !props.value);
                wrapper.appendChild(track);
                wrapper.appendChild(label);
                return wrapper;
            }}

            createRadio(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const groupLabel = document.createElement('div');
                    groupLabel.textContent = props.label;
                    groupLabel.style.cssText = 'font-size: 14px; font-weight: 500; margin-bottom: 8px;';
                    wrapper.appendChild(groupLabel);
                }}

                (props.options || []).forEach(opt => {{
                    const optValue = typeof opt === 'object' ? opt.value : opt;
                    const optLabel = typeof opt === 'object' ? opt.label : opt;

                    const item = document.createElement('label');
                    item.style.cssText = 'display: flex; align-items: center; gap: 8px; cursor: pointer; margin-bottom: 8px;';

                    const radio = document.createElement('input');
                    radio.type = 'radio';
                    radio.name = id;
                    radio.value = optValue;
                    radio.checked = props.value === optValue;
                    radio.style.cssText = 'width: 18px; height: 18px; accent-color: var(--um-color-primary);';
                    radio.onchange = () => this.sendStateUpdate(props.stateKey || id, optValue);

                    const label = document.createElement('span');
                    label.textContent = optLabel;
                    label.style.cssText = 'font-size: 14px;';

                    item.appendChild(radio);
                    item.appendChild(label);
                    wrapper.appendChild(item);
                }});

                return wrapper;
            }}

            createCard(children, props, animate) {{
                const el = document.createElement('div');
                el.className = animate ? 'um-animate-scale' : '';
                el.style.cssText = `
                    background: var(--um-color-surface); border-radius: var(--um-radius-lg);
                    padding: 24px; box-shadow: var(--um-shadow-md); margin-bottom: 16px;
                    border: 1px solid var(--um-color-border); transition: box-shadow var(--um-transition-fast);
                `;
                el.onmouseenter = () => {{ el.style.boxShadow = 'var(--um-shadow-lg)'; }};
                el.onmouseleave = () => {{ el.style.boxShadow = 'var(--um-shadow-md)'; }};
                children?.forEach(child => el.appendChild(this.renderComponent(child, false)));
                return el;
            }}

            createContainer(children, animate) {{
                const el = document.createElement('div');
                el.style.cssText = 'margin-bottom: 16px;';
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}

            createColumns(props, children, animate) {{
                const el = document.createElement('div');
                el.className = 'um-columns';
                el.style.cssText = `display: grid; grid-template-columns: repeat(${{props.count || 2}}, 1fr); gap: ${{props.gap || '16px'}}; margin-bottom: 16px;`;
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}

            createColumn(children, animate) {{
                const el = document.createElement('div');
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}

            createGrid(props, children, animate) {{
                const el = document.createElement('div');
                el.style.cssText = `display: grid; grid-template-columns: repeat(${{props.columns || 3}}, 1fr); gap: ${{props.gap || '16px'}}; margin-bottom: 16px;`;
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}

            createDivider() {{
                const el = document.createElement('hr');
                el.style.cssText = 'border: none; border-top: 1px solid var(--um-color-border); margin: 24px 0;';
                return el;
            }}

            createSpacer(props) {{
                const el = document.createElement('div');
                el.style.height = props.height || '24px';
                return el;
            }}

            createAlert(type, props) {{
                const colors = {{
                    success: {{ bg: 'var(--um-color-success-light)', border: 'var(--um-color-success)', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-success)"/><path d="M6 10l3 3 5-6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' }},
                    error: {{ bg: 'var(--um-color-error-light)', border: 'var(--um-color-error)', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-error)"/><path d="M7 7l6 6M13 7l-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>' }},
                    warning: {{ bg: 'var(--um-color-warning-light)', border: 'var(--um-color-warning)', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-warning)"/><path d="M10 6v5M10 14v.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>' }},
                    info: {{ bg: 'var(--um-color-info-light)', border: 'var(--um-color-info)', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="10" fill="var(--um-color-info)"/><path d="M10 9v5M10 6v.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>' }}
                }};

                const el = document.createElement('div');
                el.className = 'um-animate-slide';
                el.style.cssText = `
                    display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px;
                    border-radius: var(--um-radius-md); background: ${{colors[type].bg}};
                    border-left: 4px solid ${{colors[type].border}}; margin-bottom: 16px;
                `;
                el.innerHTML = `${{colors[type].icon}}<span style="font-size: 14px; line-height: 1.5;">${{props.message || ''}}</span>`;
                return el;
            }}

            createMetric(props) {{
                const el = document.createElement('div');
                el.style.cssText = 'margin-bottom: 16px;';

                const delta = props.delta;
                const deltaColor = delta > 0 ? 'var(--um-color-success)' : delta < 0 ? 'var(--um-color-error)' : 'var(--um-color-text-secondary)';
                const deltaIcon = delta > 0 ? '↑' : delta < 0 ? '↓' : '';

                el.innerHTML = `
                    <div style="font-size: 14px; color: var(--um-color-text-secondary); margin-bottom: 4px;">${{props.label || ''}}</div>
                    <div style="font-size: 32px; font-weight: 700; color: var(--um-color-text); letter-spacing: -0.02em;">${{props.value || '0'}}</div>
                    ${{delta !== undefined ? `<div style="font-size: 14px; color: ${{deltaColor}}; display: flex; align-items: center; gap: 4px; margin-top: 4px;">${{deltaIcon}} ${{Math.abs(delta)}}%${{props.deltaLabel ? ' ' + props.deltaLabel : ''}}</div>` : ''}}
                `;
                return el;
            }}

            createProgress(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const labelRow = document.createElement('div');
                    labelRow.style.cssText = 'display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px;';
                    labelRow.innerHTML = `<span>${{props.label}}</span><span style="font-weight: 500;">${{Math.round(props.value || 0)}}%</span>`;
                    wrapper.appendChild(labelRow);
                }}

                const track = document.createElement('div');
                track.style.cssText = 'height: 8px; background: var(--um-color-border); border-radius: 4px; overflow: hidden;';

                const bar = document.createElement('div');
                bar.style.cssText = `
                    width: ${{props.value || 0}}%; height: 100%;
                    background: linear-gradient(90deg, var(--um-color-primary), var(--um-color-primary-hover));
                    border-radius: 4px; transition: width 0.5s ease;
                `;

                track.appendChild(bar);
                wrapper.appendChild(track);
                return wrapper;
            }}

            createBadge(props) {{
                const el = document.createElement('span');
                const variants = {{
                    default: 'background: var(--um-color-background-secondary); color: var(--um-color-text);',
                    primary: 'background: var(--um-color-primary-light); color: var(--um-color-primary);',
                    success: 'background: var(--um-color-success-light); color: var(--um-color-success);',
                    warning: 'background: var(--um-color-warning-light); color: var(--um-color-warning);',
                    error: 'background: var(--um-color-error-light); color: var(--um-color-error);'
                }};
                el.style.cssText = `display: inline-flex; padding: 4px 10px; border-radius: var(--um-radius-full); font-size: 12px; font-weight: 500; ${{variants[props.variant] || variants.default}}`;
                el.textContent = props.label || '';
                return el;
            }}

            createAvatar(props) {{
                const el = document.createElement('div');
                const sizeMap = {{ sm: '32px', md: '40px', lg: '48px', xl: '64px' }};
                const size = sizeMap[props.size] || props.size || '40px';
                el.style.cssText = `
                    width: ${{size}}; height: ${{size}}; border-radius: 50%;
                    background: linear-gradient(135deg, var(--um-color-primary), var(--um-color-primary-hover));
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-weight: 600; font-size: calc(${{size}} / 2.5); overflow: hidden;
                `;
                if (props.src) {{
                    el.innerHTML = `<img src="${{props.src}}" style="width: 100%; height: 100%; object-fit: cover;" />`;
                }} else {{
                    el.textContent = (props.name || 'U').charAt(0).toUpperCase();
                }}
                return el;
            }}

            createStatCard(props) {{
                const el = document.createElement('div');
                el.className = 'um-interactive';
                el.style.cssText = `
                    background: var(--um-color-surface); border-radius: var(--um-radius-lg);
                    padding: 20px; box-shadow: var(--um-shadow-sm); margin-bottom: 16px;
                    border: 1px solid var(--um-color-border);
                `;

                const deltaColor = props.delta > 0 ? 'var(--um-color-success)' : props.delta < 0 ? 'var(--um-color-error)' : '';
                const deltaIcon = props.delta > 0 ? '↑' : props.delta < 0 ? '↓' : '';

                el.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-size: 14px; color: var(--um-color-text-secondary); margin-bottom: 4px;">${{props.label || ''}}</div>
                            <div style="font-size: 28px; font-weight: 700; color: var(--um-color-text);">${{props.value || '0'}}</div>
                            ${{props.delta !== undefined ? `<div style="font-size: 14px; margin-top: 4px; color: ${{deltaColor}};">${{deltaIcon}} ${{Math.abs(props.delta)}}%</div>` : ''}}
                        </div>
                        ${{props.icon ? `<div style="width: 48px; height: 48px; border-radius: var(--um-radius-md); background: var(--um-color-primary-light); display: flex; align-items: center; justify-content: center; font-size: 24px;">${{props.icon}}</div>` : ''}}
                    </div>
                `;
                return el;
            }}

            createTabs(id, props, children) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                const tabList = document.createElement('div');
                tabList.style.cssText = 'display: flex; gap: 4px; border-bottom: 1px solid var(--um-color-border); margin-bottom: 16px;';
                tabList.setAttribute('role', 'tablist');

                const activeTab = props.activeTab || 0;
                (props.tabs || []).forEach((tabName, index) => {{
                    const btn = document.createElement('button');
                    btn.textContent = tabName;
                    btn.setAttribute('role', 'tab');
                    btn.setAttribute('aria-selected', index === activeTab);
                    btn.style.cssText = `
                        padding: 10px 16px; border: none; background: transparent; cursor: pointer;
                        font-size: 14px; font-weight: 500; transition: all var(--um-transition-fast);
                        color: ${{index === activeTab ? 'var(--um-color-primary)' : 'var(--um-color-text-secondary)'}};
                        border-bottom: 2px solid ${{index === activeTab ? 'var(--um-color-primary)' : 'transparent'}};
                        margin-bottom: -1px;
                    `;
                    btn.onmouseenter = () => {{ if (index !== activeTab) btn.style.color = 'var(--um-color-text)'; }};
                    btn.onmouseleave = () => {{ if (index !== activeTab) btn.style.color = 'var(--um-color-text-secondary)'; }};
                    btn.onclick = () => this.sendStateUpdate(props.stateKey || id, index);
                    tabList.appendChild(btn);
                }});

                const content = document.createElement('div');
                content.setAttribute('role', 'tabpanel');
                if (children && children[activeTab]) {{
                    content.appendChild(this.renderComponent(children[activeTab], true));
                }}

                wrapper.appendChild(tabList);
                wrapper.appendChild(content);
                return wrapper;
            }}

            createTab(children, animate) {{
                const el = document.createElement('div');
                el.className = animate ? 'um-animate-fade' : '';
                children?.forEach(child => el.appendChild(this.renderComponent(child, false)));
                return el;
            }}

            createDataframe(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'overflow-x: auto; margin-bottom: 16px; border-radius: var(--um-radius-md); border: 1px solid var(--um-color-border);';

                const table = document.createElement('table');
                table.style.cssText = 'width: 100%; border-collapse: collapse; font-size: 14px;';

                if (props.columns) {{
                    const thead = document.createElement('thead');
                    const headerRow = document.createElement('tr');
                    props.columns.forEach(col => {{
                        const th = document.createElement('th');
                        th.textContent = col;
                        th.style.cssText = 'padding: 12px 16px; text-align: left; font-weight: 600; background: var(--um-color-background-secondary); border-bottom: 2px solid var(--um-color-border); color: var(--um-color-text);';
                        headerRow.appendChild(th);
                    }});
                    thead.appendChild(headerRow);
                    table.appendChild(thead);
                }}

                if (props.data) {{
                    const tbody = document.createElement('tbody');
                    props.data.forEach((row, i) => {{
                        const tr = document.createElement('tr');
                        tr.style.cssText = `transition: background var(--um-transition-fast); ${{i % 2 === 1 ? 'background: var(--um-color-background-secondary);' : ''}}`;
                        tr.onmouseenter = () => {{ tr.style.background = 'var(--um-color-primary-light)'; }};
                        tr.onmouseleave = () => {{ tr.style.background = i % 2 === 1 ? 'var(--um-color-background-secondary)' : ''; }};
                        Object.values(row).forEach(cell => {{
                            const td = document.createElement('td');
                            td.textContent = cell;
                            td.style.cssText = 'padding: 12px 16px; border-bottom: 1px solid var(--um-color-border);';
                            tr.appendChild(td);
                        }});
                        tbody.appendChild(tr);
                    }});
                    table.appendChild(tbody);
                }}

                wrapper.appendChild(table);
                return wrapper;
            }}

            createChat(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = `
                    display: flex; flex-direction: column; height: ${{props.height || '500px'}};
                    border: 1px solid var(--um-color-border); border-radius: var(--um-radius-lg);
                    overflow: hidden; background: var(--um-color-surface); margin-bottom: 16px;
                `;

                const messages = document.createElement('div');
                messages.dataset.umScroll = 'true';
                messages.dataset.umId = `${{id}}-messages`;
                messages.style.cssText = 'flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px;';

                (props.messages || []).forEach(msg => {{
                    const isUser = msg.role === 'user';
                    const msgEl = document.createElement('div');
                    msgEl.className = 'um-animate-slide';
                    msgEl.style.cssText = `display: flex; gap: 12px; ${{isUser ? 'flex-direction: row-reverse;' : ''}}`;

                    const avatar = document.createElement('div');
                    avatar.style.cssText = `
                        width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
                        background: ${{isUser ? 'var(--um-color-primary)' : 'linear-gradient(135deg, #64748b, #475569)'}};
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-size: 14px; font-weight: 500;
                    `;
                    avatar.textContent = isUser ? 'U' : 'AI';

                    const bubble = document.createElement('div');
                    bubble.style.cssText = `
                        max-width: 70%; padding: 12px 16px; border-radius: 16px; font-size: 14px; line-height: 1.5;
                        background: ${{isUser ? 'var(--um-color-primary)' : 'var(--um-color-background-secondary)'}};
                        color: ${{isUser ? 'white' : 'var(--um-color-text)'}};
                        ${{isUser ? 'border-bottom-right-radius: 4px;' : 'border-bottom-left-radius: 4px;'}}
                    `;
                    bubble.textContent = msg.content;

                    msgEl.appendChild(avatar);
                    msgEl.appendChild(bubble);
                    messages.appendChild(msgEl);
                }});

                wrapper.appendChild(messages);

                if (props.showInput !== false) {{
                    const inputArea = document.createElement('div');
                    inputArea.style.cssText = 'padding: 12px 16px; border-top: 1px solid var(--um-color-border); display: flex; gap: 12px;';

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.placeholder = props.inputPlaceholder || 'Type a message...';
                    input.dataset.umId = `${{id}}-input`;
                    input.style.cssText = `
                        flex: 1; padding: 10px 14px; border: 1px solid var(--um-color-border);
                        border-radius: var(--um-radius-md); font-size: 14px; outline: none;
                        background: var(--um-color-background); color: var(--um-color-text);
                    `;

                    const sendBtn = document.createElement('button');
                    sendBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M18 10L3 2l2 8-2 8 15-8z" fill="currentColor"/></svg>';
                    sendBtn.style.cssText = `
                        padding: 10px 16px; background: var(--um-color-primary); color: white;
                        border: none; border-radius: var(--um-radius-md); cursor: pointer;
                        transition: all var(--um-transition-fast);
                    `;
                    sendBtn.onmouseenter = () => {{ sendBtn.style.background = 'var(--um-color-primary-hover)'; }};
                    sendBtn.onmouseleave = () => {{ sendBtn.style.background = 'var(--um-color-primary)'; }};

                    const send = () => {{
                        if (input.value.trim()) {{
                            this.sendEvent(id, 'submit', {{ message: input.value }});
                            input.value = '';
                        }}
                    }};

                    sendBtn.onclick = send;
                    input.onkeypress = (e) => {{ if (e.key === 'Enter') send(); }};

                    inputArea.appendChild(input);
                    inputArea.appendChild(sendBtn);
                    wrapper.appendChild(inputArea);
                }}

                setTimeout(() => {{ messages.scrollTop = messages.scrollHeight; }}, 0);
                return wrapper;
            }}

            createChatMessage(props) {{
                const isUser = props.role === 'user';
                const wrapper = document.createElement('div');
                wrapper.className = 'um-animate-slide';
                wrapper.style.cssText = `display: flex; gap: 12px; margin-bottom: 12px; ${{isUser ? 'flex-direction: row-reverse;' : ''}}`;

                const avatar = document.createElement('div');
                avatar.style.cssText = `
                    width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
                    background: ${{isUser ? 'var(--um-color-primary)' : 'linear-gradient(135deg, #64748b, #475569)'}};
                    display: flex; align-items: center; justify-content: center; color: white; font-size: 14px;
                `;
                avatar.textContent = isUser ? 'U' : 'AI';

                const bubble = document.createElement('div');
                bubble.style.cssText = `
                    max-width: 70%; padding: 12px 16px; border-radius: 16px; font-size: 14px;
                    background: ${{isUser ? 'var(--um-color-primary)' : 'var(--um-color-background-secondary)'}};
                    color: ${{isUser ? 'white' : 'var(--um-color-text)'}};
                `;
                bubble.textContent = props.content || '';

                wrapper.appendChild(avatar);
                wrapper.appendChild(bubble);
                return wrapper;
            }}

            createChatInput(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'display: flex; gap: 12px; margin-bottom: 16px;';

                const input = document.createElement('input');
                input.type = 'text';
                input.placeholder = props.placeholder || 'Type a message...';
                input.dataset.umId = id;
                input.style.cssText = `
                    flex: 1; padding: 12px 16px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; outline: none;
                    background: var(--um-color-surface); color: var(--um-color-text);
                `;

                const btn = document.createElement('button');
                btn.textContent = props.buttonLabel || 'Send';
                btn.style.cssText = `
                    padding: 12px 24px; background: var(--um-color-primary); color: white;
                    border: none; border-radius: var(--um-radius-md); cursor: pointer; font-weight: 500;
                `;

                const send = () => {{
                    if (input.value.trim()) {{
                        this.sendEvent(id, 'submit', {{ message: input.value }});
                        input.value = '';
                    }}
                }};

                btn.onclick = send;
                input.onkeypress = (e) => {{ if (e.key === 'Enter') send(); }};

                wrapper.appendChild(input);
                wrapper.appendChild(btn);
                return wrapper;
            }}

            createChatContainer(id, props, children) {{
                const wrapper = document.createElement('div');
                wrapper.dataset.umScroll = 'true';
                wrapper.dataset.umId = id;
                wrapper.style.cssText = `
                    height: ${{props.height || '400px'}}; overflow-y: auto; padding: 16px;
                    border: 1px solid var(--um-color-border); border-radius: var(--um-radius-lg); margin-bottom: 16px;
                `;
                children?.forEach(child => wrapper.appendChild(this.renderComponent(child, false)));
                setTimeout(() => {{ wrapper.scrollTop = wrapper.scrollHeight; }}, 0);
                return wrapper;
            }}

            createExpander(id, props, children) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'border: 1px solid var(--um-color-border); border-radius: var(--um-radius-md); margin-bottom: 12px; overflow: hidden;';

                const header = document.createElement('button');
                header.style.cssText = `
                    width: 100%; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between;
                    background: var(--um-color-background-secondary); border: none; cursor: pointer;
                    font-size: 14px; font-weight: 500; color: var(--um-color-text);
                    transition: background var(--um-transition-fast);
                `;
                header.onmouseenter = () => {{ header.style.background = 'var(--um-color-border)'; }};
                header.onmouseleave = () => {{ header.style.background = 'var(--um-color-background-secondary)'; }};

                const icon = document.createElement('span');
                icon.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                icon.style.cssText = `transform: rotate(${{props.expanded ? '180deg' : '0deg'}}); transition: transform var(--um-transition-fast);`;

                header.innerHTML = `<span>${{props.label || 'Expand'}}</span>`;
                header.appendChild(icon);
                header.onclick = () => this.sendStateUpdate(props.stateKey || id, !props.expanded);

                wrapper.appendChild(header);

                if (props.expanded) {{
                    const content = document.createElement('div');
                    content.className = 'um-animate-slide';
                    content.style.cssText = 'padding: 16px; border-top: 1px solid var(--um-color-border);';
                    children?.forEach(child => content.appendChild(this.renderComponent(child, false)));
                    wrapper.appendChild(content);
                }}

                return wrapper;
            }}

            createModal(id, props, children) {{
                if (!props.isOpen) return document.createTextNode('');

                const overlay = document.createElement('div');
                overlay.className = 'um-animate-fade';
                overlay.style.cssText = `
                    position: fixed; inset: 0; background: rgba(0,0,0,0.5);
                    display: flex; align-items: center; justify-content: center; z-index: 1000;
                    backdrop-filter: blur(4px);
                `;
                overlay.onclick = (e) => {{ if (e.target === overlay && props.closeOnOverlay !== false) this.sendEvent(id, 'close', {{}}); }};

                const modal = document.createElement('div');
                modal.className = 'um-animate-scale';
                modal.style.cssText = `
                    background: var(--um-color-surface); border-radius: var(--um-radius-xl);
                    padding: 24px; max-width: ${{props.width || '500px'}}; width: 90%;
                    max-height: 90vh; overflow-y: auto; position: relative;
                    box-shadow: var(--um-shadow-xl);
                `;

                if (props.title) {{
                    const header = document.createElement('div');
                    header.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;';

                    const title = document.createElement('h3');
                    title.textContent = props.title;
                    title.style.cssText = 'font-size: 18px; font-weight: 600; margin: 0;';

                    const closeBtn = document.createElement('button');
                    closeBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 5l10 10M15 5l-10 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
                    closeBtn.style.cssText = `
                        background: none; border: none; cursor: pointer; padding: 4px;
                        color: var(--um-color-text-secondary); border-radius: var(--um-radius-sm);
                        transition: all var(--um-transition-fast);
                    `;
                    closeBtn.onmouseenter = () => {{ closeBtn.style.background = 'var(--um-color-background-secondary)'; }};
                    closeBtn.onmouseleave = () => {{ closeBtn.style.background = ''; }};
                    closeBtn.onclick = () => this.sendEvent(id, 'close', {{}});

                    header.appendChild(title);
                    header.appendChild(closeBtn);
                    modal.appendChild(header);
                }}

                const body = document.createElement('div');
                children?.forEach(child => body.appendChild(this.renderComponent(child, false)));
                modal.appendChild(body);

                overlay.appendChild(modal);
                return overlay;
            }}

            createBreadcrumbs(props) {{
                const wrapper = document.createElement('nav');
                wrapper.setAttribute('aria-label', 'Breadcrumb');
                wrapper.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font-size: 14px;';

                (props.items || []).forEach((item, i) => {{
                    if (i > 0) {{
                        const sep = document.createElement('span');
                        sep.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 4l4 4-4 4" stroke="var(--um-color-text-secondary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                        wrapper.appendChild(sep);
                    }}

                    const link = document.createElement('a');
                    link.href = item.href || '#';
                    link.textContent = item.label;
                    link.style.cssText = `
                        text-decoration: none; transition: color var(--um-transition-fast);
                        color: ${{i === props.items.length - 1 ? 'var(--um-color-text)' : 'var(--um-color-primary)'}};
                        font-weight: ${{i === props.items.length - 1 ? '500' : '400'}};
                    `;
                    if (i !== props.items.length - 1) {{
                        link.onmouseenter = () => {{ link.style.textDecoration = 'underline'; }};
                        link.onmouseleave = () => {{ link.style.textDecoration = 'none'; }};
                    }}
                    wrapper.appendChild(link);
                }});

                return wrapper;
            }}

            createPagination(id, props) {{
                const wrapper = document.createElement('nav');
                wrapper.setAttribute('aria-label', 'Pagination');
                wrapper.style.cssText = 'display: flex; align-items: center; gap: 4px; margin-bottom: 16px;';

                const total = props.totalPages || 1;
                const current = props.currentPage || 1;

                const createBtn = (content, page, disabled = false, active = false) => {{
                    const btn = document.createElement('button');
                    btn.innerHTML = content;
                    btn.disabled = disabled;
                    btn.style.cssText = `
                        padding: 8px 12px; border: 1px solid var(--um-color-border);
                        border-radius: var(--um-radius-sm); cursor: ${{disabled ? 'not-allowed' : 'pointer'}};
                        transition: all var(--um-transition-fast); font-size: 14px;
                        background: ${{active ? 'var(--um-color-primary)' : 'var(--um-color-surface)'}};
                        color: ${{active ? 'white' : disabled ? 'var(--um-color-text-secondary)' : 'var(--um-color-text)'}};
                        ${{active ? 'border-color: var(--um-color-primary);' : ''}}
                        opacity: ${{disabled ? '0.5' : '1'}};
                    `;
                    if (!disabled && !active) {{
                        btn.onmouseenter = () => {{ btn.style.borderColor = 'var(--um-color-primary)'; }};
                        btn.onmouseleave = () => {{ btn.style.borderColor = 'var(--um-color-border)'; }};
                    }}
                    btn.onclick = () => {{ if (!disabled) this.sendStateUpdate(props.stateKey || id, page); }};
                    return btn;
                }};

                wrapper.appendChild(createBtn('<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 4l-4 4 4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>', current - 1, current <= 1));

                const start = Math.max(1, current - 2);
                const end = Math.min(total, start + 4);

                for (let i = start; i <= end; i++) {{
                    wrapper.appendChild(createBtn(String(i), i, false, i === current));
                }}

                wrapper.appendChild(createBtn('<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>', current + 1, current >= total));

                return wrapper;
            }}

            createSteps(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'display: flex; margin-bottom: 24px;';

                (props.items || []).forEach((item, i) => {{
                    const step = document.createElement('div');
                    step.style.cssText = 'flex: 1; display: flex; flex-direction: column; align-items: center; position: relative;';

                    const isActive = i <= (props.currentStep || 0);
                    const isComplete = i < (props.currentStep || 0);

                    const circle = document.createElement('div');
                    circle.style.cssText = `
                        width: 32px; height: 32px; border-radius: 50%; z-index: 1;
                        display: flex; align-items: center; justify-content: center; font-weight: 600;
                        transition: all var(--um-transition-normal);
                        background: ${{isActive ? 'var(--um-color-primary)' : 'var(--um-color-border)'}};
                        color: ${{isActive ? 'white' : 'var(--um-color-text-secondary)'}};
                    `;
                    circle.innerHTML = isComplete ? '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8l4 4 6-8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' : (i + 1);

                    const label = document.createElement('div');
                    label.textContent = item;
                    label.style.cssText = `
                        font-size: 14px; margin-top: 8px; text-align: center;
                        color: ${{isActive ? 'var(--um-color-text)' : 'var(--um-color-text-secondary)'}};
                        font-weight: ${{isActive ? '500' : '400'}};
                    `;

                    if (i < props.items.length - 1) {{
                        const line = document.createElement('div');
                        line.style.cssText = `
                            position: absolute; top: 16px; left: calc(50% + 20px); right: calc(-50% + 20px);
                            height: 2px; transition: background var(--um-transition-normal);
                            background: ${{isComplete ? 'var(--um-color-primary)' : 'var(--um-color-border)'}};
                        `;
                        step.appendChild(line);
                    }}

                    step.appendChild(circle);
                    step.appendChild(label);
                    wrapper.appendChild(step);
                }});

                return wrapper;
            }}

            createTimeline(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'position: relative; padding-left: 28px; margin-bottom: 16px;';

                (props.items || []).forEach((item, i) => {{
                    const entry = document.createElement('div');
                    entry.className = 'um-animate-slide';
                    entry.style.cssText = 'position: relative; padding-bottom: 24px;';
                    entry.style.animationDelay = `${{i * 100}}ms`;

                    const dot = document.createElement('div');
                    dot.style.cssText = `
                        position: absolute; left: -28px; width: 12px; height: 12px;
                        border-radius: 50%; background: var(--um-color-primary);
                        border: 3px solid var(--um-color-background);
                        box-shadow: 0 0 0 2px var(--um-color-primary-light);
                    `;

                    if (i < props.items.length - 1) {{
                        const line = document.createElement('div');
                        line.style.cssText = 'position: absolute; left: -23px; top: 20px; bottom: 0; width: 2px; background: var(--um-color-border);';
                        entry.appendChild(line);
                    }}

                    const content = document.createElement('div');
                    content.innerHTML = `
                        <div style="font-weight: 600; margin-bottom: 4px; color: var(--um-color-text);">${{item.title}}</div>
                        <div style="font-size: 14px; color: var(--um-color-text-secondary); line-height: 1.5;">${{item.description || ''}}</div>
                        ${{item.time ? `<div style="font-size: 12px; color: var(--um-color-text-secondary); margin-top: 8px;">${{item.time}}</div>` : ''}}
                    `;

                    entry.appendChild(dot);
                    entry.appendChild(content);
                    wrapper.appendChild(entry);
                }});

                return wrapper;
            }}

            createNumberInput(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const group = document.createElement('div');
                group.style.cssText = 'display: inline-flex; align-items: center;';

                const btnStyle = `
                    width: 36px; height: 36px; border: 1px solid var(--um-color-border);
                    background: var(--um-color-background-secondary); cursor: pointer;
                    font-size: 18px; transition: all var(--um-transition-fast);
                    display: flex; align-items: center; justify-content: center;
                `;

                const decBtn = document.createElement('button');
                decBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
                decBtn.style.cssText = btnStyle + 'border-radius: var(--um-radius-md) 0 0 var(--um-radius-md);';
                decBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, Math.max(props.min ?? -Infinity, (props.value || 0) - (props.step || 1)));

                const input = document.createElement('input');
                input.type = 'number';
                input.value = props.value || 0;
                input.style.cssText = `
                    width: 60px; height: 36px; border: 1px solid var(--um-color-border);
                    border-left: none; border-right: none; text-align: center; font-size: 14px;
                    background: var(--um-color-surface); color: var(--um-color-text);
                `;
                input.onchange = (e) => this.sendStateUpdate(props.stateKey || id, parseFloat(e.target.value));

                const incBtn = document.createElement('button');
                incBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
                incBtn.style.cssText = btnStyle + 'border-radius: 0 var(--um-radius-md) var(--um-radius-md) 0;';
                incBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, Math.min(props.max ?? Infinity, (props.value || 0) + (props.step || 1)));

                group.appendChild(decBtn);
                group.appendChild(input);
                group.appendChild(incBtn);
                wrapper.appendChild(group);
                return wrapper;
            }}

            createDateInput(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const input = document.createElement('input');
                input.type = 'date';
                input.value = props.value || '';
                input.dataset.umId = id;
                input.style.cssText = `
                    width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; outline: none;
                    background: var(--um-color-surface); color: var(--um-color-text);
                `;
                input.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                wrapper.appendChild(input);
                return wrapper;
            }}

            createTimeInput(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const input = document.createElement('input');
                input.type = 'time';
                input.value = props.value || '';
                input.dataset.umId = id;
                input.style.cssText = `
                    width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); font-size: 14px; outline: none;
                    background: var(--um-color-surface); color: var(--um-color-text);
                `;
                input.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                wrapper.appendChild(input);
                return wrapper;
            }}

            createColorPicker(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px;';

                if (props.label) {{
                    const label = document.createElement('label');
                    label.textContent = props.label;
                    label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                    wrapper.appendChild(label);
                }}

                const group = document.createElement('div');
                group.style.cssText = 'display: flex; align-items: center; gap: 12px;';

                const input = document.createElement('input');
                input.type = 'color';
                input.value = props.value || '#6366f1';
                input.style.cssText = `
                    width: 48px; height: 48px; border: 2px solid var(--um-color-border);
                    border-radius: var(--um-radius-md); cursor: pointer; padding: 2px;
                `;

                const valueDisplay = document.createElement('span');
                valueDisplay.textContent = props.value || '#6366f1';
                valueDisplay.style.cssText = 'font-family: monospace; font-size: 14px; color: var(--um-color-text-secondary);';

                input.oninput = (e) => {{
                    valueDisplay.textContent = e.target.value;
                    this.sendStateUpdate(props.stateKey || id, e.target.value);
                }};

                group.appendChild(input);
                group.appendChild(valueDisplay);
                wrapper.appendChild(group);
                return wrapper;
            }}

            createRating(id, props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'display: flex; gap: 4px; margin-bottom: 16px;';
                wrapper.setAttribute('role', 'radiogroup');
                wrapper.setAttribute('aria-label', 'Rating');

                const max = props.max || 5;
                const current = props.value || 0;

                for (let i = 1; i <= max; i++) {{
                    const star = document.createElement('button');
                    star.setAttribute('role', 'radio');
                    star.setAttribute('aria-checked', i <= current);
                    star.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="${{i <= current ? 'var(--um-color-warning)' : 'none'}}" stroke="var(--um-color-warning)" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`;
                    star.style.cssText = `
                        background: none; border: none; cursor: pointer; padding: 2px;
                        transition: transform var(--um-transition-fast);
                    `;
                    star.onmouseenter = () => {{ star.style.transform = 'scale(1.2)'; }};
                    star.onmouseleave = () => {{ star.style.transform = ''; }};
                    star.onclick = () => this.sendStateUpdate(props.stateKey || id, i);
                    wrapper.appendChild(star);
                }}

                return wrapper;
            }}

            createCode(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px; border-radius: var(--um-radius-md); overflow: hidden;';

                if (props.language) {{
                    const header = document.createElement('div');
                    header.style.cssText = `
                        background: #1e293b; color: #94a3b8; padding: 8px 16px;
                        font-size: 12px; font-family: monospace; display: flex;
                        justify-content: space-between; align-items: center;
                    `;
                    header.innerHTML = `<span>${{props.language}}</span>`;
                    wrapper.appendChild(header);
                }}

                const pre = document.createElement('pre');
                pre.style.cssText = `
                    background: #0f172a; color: #e2e8f0; padding: 16px; margin: 0;
                    overflow-x: auto; font-family: 'JetBrains Mono', monospace;
                    font-size: 14px; line-height: 1.6;
                `;

                const code = document.createElement('code');
                code.textContent = props.content || '';
                pre.appendChild(code);
                wrapper.appendChild(pre);
                return wrapper;
            }}

            createMarkdown(props) {{
                const el = document.createElement('div');
                el.style.cssText = 'margin-bottom: 16px; line-height: 1.7;';

                let content = props.content || '';
                content = content
                    .replace(/^### (.+)$/gm, '<h3 style="font-size: 1.25rem; font-weight: 600; margin: 1em 0 0.5em;">$1</h3>')
                    .replace(/^## (.+)$/gm, '<h2 style="font-size: 1.5rem; font-weight: 600; margin: 1em 0 0.5em;">$1</h2>')
                    .replace(/^# (.+)$/gm, '<h1 style="font-size: 2rem; font-weight: 700; margin: 1em 0 0.5em;">$1</h1>')
                    .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
                    .replace(/`(.+?)`/g, '<code style="background: var(--um-color-background-secondary); padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em;">$1</code>')
                    .replace(/\\n/g, '<br>');

                el.innerHTML = content;
                return el;
            }}

            createJsonViewer(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = `
                    background: #0f172a; color: #e2e8f0; padding: 16px;
                    border-radius: var(--um-radius-md); overflow-x: auto;
                    font-family: 'JetBrains Mono', monospace; font-size: 13px; margin-bottom: 16px;
                `;

                try {{
                    const formatted = JSON.stringify(props.data, null, 2);
                    wrapper.innerHTML = `<pre style="margin: 0;">${{this.syntaxHighlight(formatted)}}</pre>`;
                }} catch (e) {{
                    wrapper.textContent = String(props.data);
                }}

                return wrapper;
            }}

            syntaxHighlight(json) {{
                return json.replace(/("(\\\\u[a-zA-Z0-9]{{4}}|\\\\[^u]|[^\\\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, (match) => {{
                    let color = '#f472b6'; // string
                    if (/^"/.test(match)) {{
                        color = /:$/.test(match) ? '#93c5fd' : '#a5d6a7'; // key : string
                    }} else if (/true|false/.test(match)) {{
                        color = '#fbbf24'; // boolean
                    }} else if (/null/.test(match)) {{
                        color = '#94a3b8'; // null
                    }} else {{
                        color = '#f472b6'; // number
                    }}
                    return `<span style="color: ${{color}}">${{match}}</span>`;
                }});
            }}

            createChart(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = `
                    height: ${{props.height || '300px'}}; background: var(--um-color-surface);
                    border: 1px solid var(--um-color-border); border-radius: var(--um-radius-lg);
                    padding: 16px; margin-bottom: 16px; display: flex; flex-direction: column;
                `;

                const chartType = props.chartType || 'line';
                const chartData = props.data || [];
                const chartHeight = parseInt(props.height) || 300;

                let content = '';
                if (props.title) {{
                    content += `<div style="font-weight: 600; margin-bottom: 12px; color: var(--um-color-text);">${{props.title}}</div>`;
                }}

                if (chartData.length > 0) {{
                    const svgHeight = chartHeight - 80;
                    const svgWidth = 500;
                    const colors = props.colors || ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

                    if (chartType === 'pie') {{
                        content += this.renderPieChart(chartData, props, colors);
                    }} else {{
                        content += this.renderLineBarChart(chartType, chartData, props, svgWidth, svgHeight, colors);
                    }}
                }} else {{
                    content += `<div style="flex: 1; display: flex; align-items: center; justify-content: center; color: var(--um-color-text-secondary);">No data available</div>`;
                }}

                wrapper.innerHTML = content;
                return wrapper;
            }}

            renderPieChart(data, props, colors) {{
                const total = data.reduce((sum, d) => sum + (d[props.value] || 0), 0);
                let currentAngle = -90;
                let paths = '';
                let legend = '';

                data.forEach((d, i) => {{
                    const value = d[props.value] || 0;
                    const angle = (value / total) * 360;
                    const endAngle = currentAngle + angle;

                    const x1 = 100 + 80 * Math.cos(currentAngle * Math.PI / 180);
                    const y1 = 100 + 80 * Math.sin(currentAngle * Math.PI / 180);
                    const x2 = 100 + 80 * Math.cos(endAngle * Math.PI / 180);
                    const y2 = 100 + 80 * Math.sin(endAngle * Math.PI / 180);

                    const largeArc = angle > 180 ? 1 : 0;
                    const color = colors[i % colors.length];

                    paths += `<path d="M 100 100 L ${{x1}} ${{y1}} A 80 80 0 ${{largeArc}} 1 ${{x2}} ${{y2}} Z" fill="${{color}}" style="transition: opacity 0.2s;" onmouseenter="this.style.opacity='0.8'" onmouseleave="this.style.opacity='1'" />`;

                    if (props.donut) {{
                        paths += `<circle cx="100" cy="100" r="50" fill="var(--um-color-surface)" />`;
                    }}

                    legend += `<span style="display: inline-flex; align-items: center; margin-right: 16px; font-size: 12px;"><span style="width: 12px; height: 12px; background: ${{color}}; border-radius: 2px; margin-right: 6px;"></span>${{d[props.label] || 'Item'}} (${{Math.round(value / total * 100)}}%)</span>`;
                    currentAngle = endAngle;
                }});

                return `
                    <div style="display: flex; align-items: center; justify-content: center; flex: 1;">
                        <svg viewBox="0 0 200 200" style="width: 180px; height: 180px;">${{paths}}</svg>
                    </div>
                    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 12px;">${{legend}}</div>
                `;
            }}

            renderLineBarChart(type, data, props, width, height, colors) {{
                const xKey = props.x;
                const yKeys = props.y || [];
                const padding = {{ left: 50, right: 20, top: 20, bottom: 40 }};
                const chartWidth = width - padding.left - padding.right;
                const chartHeight = height - padding.top - padding.bottom;

                const values = data.flatMap(d => yKeys.map(k => d[k] || 0));
                const maxVal = Math.max(...values) * 1.1;
                const minVal = Math.min(0, ...values);
                const range = maxVal - minVal || 1;

                let elements = '';
                let legend = '';

                // Grid lines
                for (let i = 0; i <= 4; i++) {{
                    const y = padding.top + (chartHeight / 4) * i;
                    const val = Math.round(maxVal - (range / 4) * i);
                    elements += `<line x1="${{padding.left}}" y1="${{y}}" x2="${{width - padding.right}}" y2="${{y}}" stroke="var(--um-color-border)" stroke-dasharray="4" />`;
                    elements += `<text x="${{padding.left - 10}}" y="${{y + 4}}" text-anchor="end" font-size="11" fill="var(--um-color-text-secondary)">${{val}}</text>`;
                }}

                yKeys.forEach((yKey, yi) => {{
                    const color = colors[yi % colors.length];

                    if (type === 'bar') {{
                        const barWidth = chartWidth / data.length / yKeys.length * 0.7;
                        const gap = chartWidth / data.length * 0.15;

                        data.forEach((d, i) => {{
                            const x = padding.left + gap + (i / data.length) * chartWidth + yi * barWidth + yi * 2;
                            const val = d[yKey] || 0;
                            const barHeight = ((val - minVal) / range) * chartHeight;
                            const y = padding.top + chartHeight - barHeight;

                            elements += `<rect x="${{x}}" y="${{y}}" width="${{barWidth}}" height="${{barHeight}}" fill="${{color}}" rx="3" style="transition: opacity 0.2s;" onmouseenter="this.style.opacity='0.8'" onmouseleave="this.style.opacity='1'"><title>${{yKey}}: ${{val}}</title></rect>`;
                        }});
                    }} else {{
                        const points = data.map((d, i) => {{
                            const x = padding.left + (i / (data.length - 1 || 1)) * chartWidth;
                            const y = padding.top + chartHeight - ((d[yKey] - minVal) / range) * chartHeight;
                            return `${{x}},${{y}}`;
                        }});

                        if (type === 'area') {{
                            const areaPath = `M ${{padding.left}},${{padding.top + chartHeight}} L ${{points.join(' L ')}} L ${{padding.left + chartWidth}},${{padding.top + chartHeight}} Z`;
                            elements += `<path d="${{areaPath}}" fill="${{color}}" fill-opacity="0.15" />`;
                        }}

                        elements += `<polyline points="${{points.join(' ')}}" fill="none" stroke="${{color}}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />`;

                        // Data points
                        data.forEach((d, i) => {{
                            const x = padding.left + (i / (data.length - 1 || 1)) * chartWidth;
                            const y = padding.top + chartHeight - ((d[yKey] - minVal) / range) * chartHeight;
                            elements += `<circle cx="${{x}}" cy="${{y}}" r="4" fill="${{color}}" stroke="var(--um-color-surface)" stroke-width="2" style="transition: r 0.2s;" onmouseenter="this.setAttribute('r','6')" onmouseleave="this.setAttribute('r','4')"><title>${{yKey}}: ${{d[yKey]}}</title></circle>`;
                        }});
                    }}

                    legend += `<span style="display: inline-flex; align-items: center; margin-right: 16px; font-size: 12px;"><span style="width: 12px; height: 12px; background: ${{color}}; border-radius: 2px; margin-right: 6px;"></span>${{yKey}}</span>`;
                }});

                // X-axis labels
                data.forEach((d, i) => {{
                    if (i % Math.ceil(data.length / 6) === 0 || i === data.length - 1) {{
                        const x = padding.left + (i / (data.length - 1 || 1)) * chartWidth;
                        elements += `<text x="${{x}}" y="${{height - 10}}" text-anchor="middle" font-size="11" fill="var(--um-color-text-secondary)">${{d[xKey] || i}}</text>`;
                    }}
                }});

                return `
                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                        <svg viewBox="0 0 ${{width}} ${{height}}" style="width: 100%; height: 100%;" preserveAspectRatio="xMidYMid meet">${{elements}}</svg>
                    </div>
                    ${{yKeys.length > 1 ? `<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 8px;">${{legend}}</div>` : ''}}
                `;
            }}

            createEmptyState(props, children) {{
                const el = document.createElement('div');
                el.style.cssText = 'text-align: center; padding: 48px 24px; margin-bottom: 16px;';
                el.innerHTML = `
                    ${{props.icon ? `<div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">${{props.icon}}</div>` : ''}}
                    <h3 style="font-size: 18px; font-weight: 600; color: var(--um-color-text); margin-bottom: 8px;">${{props.title || 'No data'}}</h3>
                    <p style="font-size: 14px; color: var(--um-color-text-secondary); margin-bottom: 16px;">${{props.description || ''}}</p>
                `;
                children?.forEach(child => el.appendChild(this.renderComponent(child, false)));
                return el;
            }}

            createSkeleton(props) {{
                const el = document.createElement('div');
                el.style.cssText = `
                    height: ${{props.height || '20px'}}; width: ${{props.width || '100%'}};
                    background: linear-gradient(90deg, var(--um-color-border) 25%, var(--um-color-background-secondary) 50%, var(--um-color-border) 75%);
                    background-size: 200% 100%; animation: um-skeleton 1.5s infinite;
                    border-radius: ${{props.rounded ? 'var(--um-radius-full)' : 'var(--um-radius-md)'}}; margin-bottom: 8px;
                `;
                return el;
            }}

            createHtml(props) {{
                const el = document.createElement('div');
                el.innerHTML = props.content || '';
                return el;
            }}

            createIframe(props) {{
                const wrapper = document.createElement('div');
                wrapper.style.cssText = 'margin-bottom: 16px; border-radius: var(--um-radius-md); overflow: hidden; border: 1px solid var(--um-color-border);';

                const iframe = document.createElement('iframe');
                iframe.src = props.src || '';
                iframe.style.cssText = `width: ${{props.width || '100%'}}; height: ${{props.height || '400px'}}; border: none;`;
                iframe.setAttribute('loading', 'lazy');

                wrapper.appendChild(iframe);
                return wrapper;
            }}

            createGeneric(type, props, children, animate) {{
                const el = document.createElement('div');
                el.className = `um-${{type}} ${{animate ? 'um-animate-fade' : ''}}`;
                if (props.content) el.textContent = props.content;
                children?.forEach(child => el.appendChild(this.renderComponent(child, animate)));
                return el;
            }}
        }}

        // Initialize
        const client = new UmaraClient();
        client.connect();

        // Expose for debugging
        window.UmaraClient = client;
    </script>
</body>
</html>"""
