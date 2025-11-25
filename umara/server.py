"""
WebSocket server for Umara.

Handles communication between Python backend and JavaScript frontend,
with support for hot reload during development.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import importlib
import importlib.util
from pathlib import Path
from typing import Any, Dict, Optional, Callable
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from umara.core import UmaraApp, get_app, Session


def create_fastapi_app(umara_app: UmaraApp) -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title=umara_app.title)

    # Add CORS middleware for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Get the frontend dist directory
    frontend_dist = Path(__file__).parent.parent / "umara_frontend" / "dist"
    frontend_dev = Path(__file__).parent.parent / "umara_frontend"

    @app.get("/")
    async def index():
        """Serve the main HTML page."""
        # Check for production build first
        if frontend_dist.exists() and (frontend_dist / "index.html").exists():
            return FileResponse(frontend_dist / "index.html")

        # Development mode - serve basic HTML that loads from Vite dev server
        return HTMLResponse(get_dev_html(umara_app.title))

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Handle WebSocket connections."""
        await websocket.accept()

        # Create or restore session
        session_id = str(uuid.uuid4())
        session = umara_app.create_session(session_id)
        session.websocket = websocket

        try:
            # Send initial render
            initial_data = await umara_app.render_session(session)
            await websocket.send_json({
                "type": "init",
                "sessionId": session_id,
                "data": initial_data,
            })

            # Handle incoming messages
            while True:
                data = await websocket.receive_json()
                response = await handle_message(umara_app, session, data)
                if response:
                    await websocket.send_json(response)

        except WebSocketDisconnect:
            umara_app.remove_session(session_id)
        except Exception as e:
            try:
                await websocket.send_json({
                    "type": "error",
                    "error": str(e),
                })
            except Exception:
                pass
            umara_app.remove_session(session_id)

    @app.get("/api/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "version": "0.1.0"}

    # Mount static files if available
    if frontend_dist.exists():
        app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

    return app


async def handle_message(
    umara_app: UmaraApp,
    session: Session,
    data: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Handle incoming WebSocket messages."""
    msg_type = data.get("type")

    if msg_type == "event":
        # Handle component event
        result = await umara_app.handle_event(
            session,
            data.get("eventType", "click"),
            data.get("componentId", ""),
            data.get("payload", {}),
        )
        return {"type": "update", "data": result}

    elif msg_type == "state":
        # Handle state update
        result = await umara_app.handle_state_update(
            session,
            data.get("key", ""),
            data.get("value"),
        )
        return {"type": "update", "data": result}

    elif msg_type == "rerender":
        # Force re-render
        result = await umara_app.render_session(session)
        return {"type": "update", "data": result}

    elif msg_type == "ping":
        return {"type": "pong"}

    return None


def get_dev_html(title: str) -> str:
    """Generate HTML for development mode."""
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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            line-height: 1.5;
        }}
        #root {{
            min-height: 100vh;
        }}
        .loading {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            gap: 16px;
        }}
        .loading-spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid #e2e8f0;
            border-top-color: #6366f1;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        .loading-text {{
            color: #64748b;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div id="root">
        <div class="loading">
            <div class="loading-spinner"></div>
            <div class="loading-text">Connecting to Umara...</div>
        </div>
    </div>
    <script type="module">
        // Inline React app for development when frontend isn't built
        const WEBSOCKET_URL = `ws://${{window.location.host}}/ws`;

        class UmaraClient {{
            constructor() {{
                this.ws = null;
                this.sessionId = null;
                this.reconnectAttempts = 0;
                this.maxReconnectAttempts = 5;
                this.listeners = new Set();
            }}

            connect() {{
                this.ws = new WebSocket(WEBSOCKET_URL);

                this.ws.onopen = () => {{
                    console.log('Connected to Umara server');
                    this.reconnectAttempts = 0;
                }};

                this.ws.onmessage = (event) => {{
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                }};

                this.ws.onclose = () => {{
                    console.log('Disconnected from Umara server');
                    this.attemptReconnect();
                }};

                this.ws.onerror = (error) => {{
                    console.error('WebSocket error:', error);
                }};
            }}

            attemptReconnect() {{
                if (this.reconnectAttempts < this.maxReconnectAttempts) {{
                    this.reconnectAttempts++;
                    setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
                }}
            }}

            handleMessage(data) {{
                if (data.type === 'init') {{
                    this.sessionId = data.sessionId;
                    this.render(data.data);
                }} else if (data.type === 'update') {{
                    this.render(data.data);
                }} else if (data.type === 'error') {{
                    console.error('Server error:', data.error);
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
                this.send({{
                    type: 'state',
                    key,
                    value,
                }});
            }}

            render(data) {{
                const root = document.getElementById('root');
                if (data.tree) {{
                    root.innerHTML = '';
                    const element = this.renderComponent(data.tree);
                    root.appendChild(element);
                    this.applyTheme(data.theme);
                }}
            }}

            applyTheme(theme) {{
                if (!theme) return;
                const root = document.documentElement;
                const colors = theme.colors || {{}};
                Object.entries(colors).forEach(([key, value]) => {{
                    root.style.setProperty(`--um-color-${{key.replace(/_/g, '-')}}`, value);
                }});
            }}

            renderComponent(component) {{
                if (!component) return document.createTextNode('');

                const {{ id, type, props, children, style, events }} = component;

                // Handle different component types
                switch (type) {{
                    case 'root':
                        const container = document.createElement('div');
                        container.className = 'umara-root';
                        container.style.cssText = 'max-width: 1200px; margin: 0 auto; padding: 24px;';
                        children?.forEach(child => {{
                            container.appendChild(this.renderComponent(child));
                        }});
                        return container;

                    case 'text':
                        const text = document.createElement('p');
                        text.textContent = props.content || '';
                        text.className = 'um-text';
                        this.applyStyle(text, style);
                        return text;

                    case 'header':
                        const header = document.createElement(props.level ? `h${{props.level}}` : 'h1');
                        header.textContent = props.content || '';
                        header.className = 'um-header';
                        header.style.cssText = 'font-weight: 700; margin-bottom: 16px; color: var(--um-color-text, #0f172a);';
                        if (!props.level || props.level === 1) header.style.fontSize = '2.25rem';
                        else if (props.level === 2) header.style.fontSize = '1.875rem';
                        else header.style.fontSize = '1.5rem';
                        this.applyStyle(header, style);
                        return header;

                    case 'subheader':
                        const subheader = document.createElement('h3');
                        subheader.textContent = props.content || '';
                        subheader.className = 'um-subheader';
                        subheader.style.cssText = 'font-weight: 600; font-size: 1.25rem; margin-bottom: 12px; color: var(--um-color-text, #0f172a);';
                        this.applyStyle(subheader, style);
                        return subheader;

                    case 'button':
                        const button = document.createElement('button');
                        button.textContent = props.label || 'Button';
                        button.className = `um-button um-button-${{props.variant || 'primary'}}`;
                        button.style.cssText = this.getButtonStyle(props.variant || 'primary');
                        button.disabled = props.disabled || false;
                        button.onclick = () => this.sendEvent(id, 'click', {{}});
                        this.applyStyle(button, style);
                        return button;

                    case 'input':
                        const inputWrapper = document.createElement('div');
                        inputWrapper.className = 'um-input-wrapper';
                        inputWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const label = document.createElement('label');
                            label.textContent = props.label;
                            label.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px; color: var(--um-color-text, #0f172a);';
                            inputWrapper.appendChild(label);
                        }}

                        const input = document.createElement('input');
                        input.type = props.type || 'text';
                        input.value = props.value || '';
                        input.placeholder = props.placeholder || '';
                        input.className = 'um-input';
                        input.style.cssText = 'width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; transition: all 0.2s; outline: none;';
                        input.onfocus = () => input.style.borderColor = 'var(--um-color-primary, #6366f1)';
                        input.onblur = () => input.style.borderColor = 'var(--um-color-border, #e2e8f0)';
                        input.oninput = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                        inputWrapper.appendChild(input);
                        this.applyStyle(inputWrapper, style);
                        return inputWrapper;

                    case 'slider':
                        const sliderWrapper = document.createElement('div');
                        sliderWrapper.className = 'um-slider-wrapper';
                        sliderWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const sliderLabel = document.createElement('div');
                            sliderLabel.style.cssText = 'display: flex; justify-content: space-between; font-size: 14px; font-weight: 500; margin-bottom: 8px;';
                            sliderLabel.innerHTML = `<span>${{props.label}}</span><span id="slider-value-${{id}}">${{props.value || props.min || 0}}</span>`;
                            sliderWrapper.appendChild(sliderLabel);
                        }}

                        const slider = document.createElement('input');
                        slider.type = 'range';
                        slider.min = props.min || 0;
                        slider.max = props.max || 100;
                        slider.value = props.value || props.min || 0;
                        slider.step = props.step || 1;
                        slider.className = 'um-slider';
                        slider.style.cssText = 'width: 100%; height: 6px; -webkit-appearance: none; appearance: none; background: var(--um-color-border, #e2e8f0); border-radius: 3px; outline: none;';
                        slider.oninput = (e) => {{
                            const valueEl = document.getElementById(`slider-value-${{id}}`);
                            if (valueEl) valueEl.textContent = e.target.value;
                            this.sendStateUpdate(props.stateKey || id, parseFloat(e.target.value));
                        }};
                        sliderWrapper.appendChild(slider);
                        this.applyStyle(sliderWrapper, style);
                        return sliderWrapper;

                    case 'select':
                        const selectWrapper = document.createElement('div');
                        selectWrapper.className = 'um-select-wrapper';
                        selectWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const selectLabel = document.createElement('label');
                            selectLabel.textContent = props.label;
                            selectLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            selectWrapper.appendChild(selectLabel);
                        }}

                        const select = document.createElement('select');
                        select.className = 'um-select';
                        select.style.cssText = 'width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; background: white; outline: none;';
                        (props.options || []).forEach(opt => {{
                            const option = document.createElement('option');
                            option.value = typeof opt === 'object' ? opt.value : opt;
                            option.textContent = typeof opt === 'object' ? opt.label : opt;
                            if (props.value === option.value) option.selected = true;
                            select.appendChild(option);
                        }});
                        select.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                        selectWrapper.appendChild(select);
                        this.applyStyle(selectWrapper, style);
                        return selectWrapper;

                    case 'checkbox':
                        const checkWrapper = document.createElement('label');
                        checkWrapper.className = 'um-checkbox-wrapper';
                        checkWrapper.style.cssText = 'display: flex; align-items: center; gap: 10px; cursor: pointer; margin-bottom: 12px;';

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.checked = props.value || false;
                        checkbox.style.cssText = 'width: 18px; height: 18px; accent-color: var(--um-color-primary, #6366f1);';
                        checkbox.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.checked);

                        const checkLabel = document.createElement('span');
                        checkLabel.textContent = props.label || '';
                        checkLabel.style.cssText = 'font-size: 14px;';

                        checkWrapper.appendChild(checkbox);
                        checkWrapper.appendChild(checkLabel);
                        this.applyStyle(checkWrapper, style);
                        return checkWrapper;

                    case 'card':
                        const card = document.createElement('div');
                        card.className = 'um-card';
                        card.style.cssText = 'background: var(--um-color-surface, #fff); border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 16px;';
                        children?.forEach(child => {{
                            card.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(card, style);
                        return card;

                    case 'container':
                        const cont = document.createElement('div');
                        cont.className = 'um-container';
                        cont.style.cssText = 'margin-bottom: 16px;';
                        children?.forEach(child => {{
                            cont.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(cont, style);
                        return cont;

                    case 'columns':
                        const cols = document.createElement('div');
                        cols.className = 'um-columns';
                        cols.style.cssText = `display: grid; grid-template-columns: repeat(${{props.count || 2}}, 1fr); gap: ${{props.gap || '16px'}}; margin-bottom: 16px;`;
                        children?.forEach(child => {{
                            cols.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(cols, style);
                        return cols;

                    case 'column':
                        const col = document.createElement('div');
                        col.className = 'um-column';
                        children?.forEach(child => {{
                            col.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(col, style);
                        return col;

                    case 'success':
                        const success = document.createElement('div');
                        success.className = 'um-alert um-alert-success';
                        success.style.cssText = 'padding: 12px 16px; border-radius: 8px; background: var(--um-color-success-light, #d1fae5); color: var(--um-color-success-dark, #047857); margin-bottom: 16px; font-size: 14px;';
                        success.textContent = props.message || '';
                        this.applyStyle(success, style);
                        return success;

                    case 'error':
                        const errorEl = document.createElement('div');
                        errorEl.className = 'um-alert um-alert-error';
                        errorEl.style.cssText = 'padding: 12px 16px; border-radius: 8px; background: var(--um-color-error-light, #fee2e2); color: var(--um-color-error-dark, #b91c1c); margin-bottom: 16px; font-size: 14px;';
                        errorEl.textContent = props.message || '';
                        if (props.traceback) {{
                            const trace = document.createElement('pre');
                            trace.style.cssText = 'margin-top: 8px; font-size: 12px; overflow-x: auto; font-family: monospace;';
                            trace.textContent = props.traceback;
                            errorEl.appendChild(trace);
                        }}
                        this.applyStyle(errorEl, style);
                        return errorEl;

                    case 'warning':
                        const warning = document.createElement('div');
                        warning.className = 'um-alert um-alert-warning';
                        warning.style.cssText = 'padding: 12px 16px; border-radius: 8px; background: var(--um-color-warning-light, #fef3c7); color: var(--um-color-warning-dark, #b45309); margin-bottom: 16px; font-size: 14px;';
                        warning.textContent = props.message || '';
                        this.applyStyle(warning, style);
                        return warning;

                    case 'info':
                        const infoEl = document.createElement('div');
                        infoEl.className = 'um-alert um-alert-info';
                        infoEl.style.cssText = 'padding: 12px 16px; border-radius: 8px; background: var(--um-color-info-light, #dbeafe); color: var(--um-color-info-dark, #1d4ed8); margin-bottom: 16px; font-size: 14px;';
                        infoEl.textContent = props.message || '';
                        this.applyStyle(infoEl, style);
                        return infoEl;

                    case 'divider':
                        const divider = document.createElement('hr');
                        divider.className = 'um-divider';
                        divider.style.cssText = 'border: none; border-top: 1px solid var(--um-color-border, #e2e8f0); margin: 24px 0;';
                        this.applyStyle(divider, style);
                        return divider;

                    case 'spacer':
                        const spacer = document.createElement('div');
                        spacer.className = 'um-spacer';
                        spacer.style.cssText = `height: ${{props.height || '24px'}};`;
                        return spacer;

                    case 'metric':
                        const metric = document.createElement('div');
                        metric.className = 'um-metric';
                        metric.style.cssText = 'margin-bottom: 16px;';
                        metric.innerHTML = `
                            <div style="font-size: 14px; color: var(--um-color-text-secondary, #64748b); margin-bottom: 4px;">${{props.label || ''}}</div>
                            <div style="font-size: 32px; font-weight: 700; color: var(--um-color-text, #0f172a);">${{props.value || '0'}}</div>
                            ${{props.delta ? `<div style="font-size: 14px; color: ${{props.delta > 0 ? 'var(--um-color-success, #10b981)' : 'var(--um-color-error, #ef4444)'}};">${{props.delta > 0 ? '+' : ''}}${{props.delta}}${{props.deltaLabel || ''}}</div>` : ''}}
                        `;
                        this.applyStyle(metric, style);
                        return metric;

                    case 'progress':
                        const progressWrapper = document.createElement('div');
                        progressWrapper.className = 'um-progress-wrapper';
                        progressWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const pLabel = document.createElement('div');
                            pLabel.style.cssText = 'display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px;';
                            pLabel.innerHTML = `<span>${{props.label}}</span><span>${{Math.round(props.value || 0)}}%</span>`;
                            progressWrapper.appendChild(pLabel);
                        }}

                        const progressTrack = document.createElement('div');
                        progressTrack.style.cssText = 'height: 8px; background: var(--um-color-border, #e2e8f0); border-radius: 4px; overflow: hidden;';

                        const progressBar = document.createElement('div');
                        progressBar.style.cssText = `width: ${{props.value || 0}}%; height: 100%; background: var(--um-color-primary, #6366f1); border-radius: 4px; transition: width 0.3s ease;`;

                        progressTrack.appendChild(progressBar);
                        progressWrapper.appendChild(progressTrack);
                        this.applyStyle(progressWrapper, style);
                        return progressWrapper;

                    case 'tabs':
                        const tabsContainer = document.createElement('div');
                        tabsContainer.className = 'um-tabs';
                        tabsContainer.style.cssText = 'margin-bottom: 16px;';

                        const tabList = document.createElement('div');
                        tabList.className = 'um-tab-list';
                        tabList.style.cssText = 'display: flex; gap: 4px; border-bottom: 1px solid var(--um-color-border, #e2e8f0); margin-bottom: 16px;';

                        const tabContents = document.createElement('div');
                        tabContents.className = 'um-tab-contents';

                        const activeTab = props.activeTab || 0;
                        (props.tabs || []).forEach((tabName, index) => {{
                            const tabBtn = document.createElement('button');
                            tabBtn.textContent = tabName;
                            tabBtn.className = `um-tab-btn ${{index === activeTab ? 'active' : ''}}`;
                            tabBtn.style.cssText = `padding: 10px 16px; border: none; background: transparent; cursor: pointer; font-size: 14px; font-weight: 500; color: ${{index === activeTab ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-text-secondary, #64748b)'}}; border-bottom: 2px solid ${{index === activeTab ? 'var(--um-color-primary, #6366f1)' : 'transparent'}}; margin-bottom: -1px; transition: all 0.2s;`;
                            tabBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, index);
                            tabList.appendChild(tabBtn);
                        }});

                        if (children && children[activeTab]) {{
                            tabContents.appendChild(this.renderComponent(children[activeTab]));
                        }}

                        tabsContainer.appendChild(tabList);
                        tabsContainer.appendChild(tabContents);
                        this.applyStyle(tabsContainer, style);
                        return tabsContainer;

                    case 'tab':
                        const tabContent = document.createElement('div');
                        tabContent.className = 'um-tab-content';
                        children?.forEach(child => {{
                            tabContent.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(tabContent, style);
                        return tabContent;

                    case 'dataframe':
                        const tableWrapper = document.createElement('div');
                        tableWrapper.className = 'um-dataframe-wrapper';
                        tableWrapper.style.cssText = 'overflow-x: auto; margin-bottom: 16px;';

                        const table = document.createElement('table');
                        table.className = 'um-dataframe';
                        table.style.cssText = 'width: 100%; border-collapse: collapse; font-size: 14px;';

                        // Header
                        if (props.columns) {{
                            const thead = document.createElement('thead');
                            const headerRow = document.createElement('tr');
                            props.columns.forEach(col => {{
                                const th = document.createElement('th');
                                th.textContent = col;
                                th.style.cssText = 'padding: 12px 16px; text-align: left; font-weight: 600; background: var(--um-color-background-secondary, #f8fafc); border-bottom: 2px solid var(--um-color-border, #e2e8f0);';
                                headerRow.appendChild(th);
                            }});
                            thead.appendChild(headerRow);
                            table.appendChild(thead);
                        }}

                        // Body
                        if (props.data) {{
                            const tbody = document.createElement('tbody');
                            props.data.forEach((row, i) => {{
                                const tr = document.createElement('tr');
                                tr.style.cssText = i % 2 === 0 ? '' : 'background: var(--um-color-background-secondary, #f8fafc);';
                                Object.values(row).forEach(cell => {{
                                    const td = document.createElement('td');
                                    td.textContent = cell;
                                    td.style.cssText = 'padding: 12px 16px; border-bottom: 1px solid var(--um-color-border, #e2e8f0);';
                                    tr.appendChild(td);
                                }});
                                tbody.appendChild(tr);
                            }});
                            table.appendChild(tbody);
                        }}

                        tableWrapper.appendChild(table);
                        this.applyStyle(tableWrapper, style);
                        return tableWrapper;

                    default:
                        const generic = document.createElement('div');
                        generic.className = `um-${{type}}`;
                        if (props.content) generic.textContent = props.content;
                        children?.forEach(child => {{
                            generic.appendChild(this.renderComponent(child));
                        }});
                        this.applyStyle(generic, style);
                        return generic;
                }}
            }}

            getButtonStyle(variant) {{
                const base = 'padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; border: none;';
                switch (variant) {{
                    case 'secondary':
                        return base + 'background: var(--um-color-secondary-light, #f1f5f9); color: var(--um-color-secondary, #64748b);';
                    case 'outline':
                        return base + 'background: transparent; color: var(--um-color-primary, #6366f1); border: 1px solid var(--um-color-primary, #6366f1);';
                    case 'ghost':
                        return base + 'background: transparent; color: var(--um-color-text, #0f172a);';
                    case 'danger':
                        return base + 'background: var(--um-color-error, #ef4444); color: white;';
                    default: // primary
                        return base + 'background: var(--um-color-primary, #6366f1); color: white;';
                }}
            }}

            applyStyle(element, style) {{
                if (style) {{
                    Object.entries(style).forEach(([key, value]) => {{
                        element.style[key] = value;
                    }});
                }}
            }}
        }}

        // Initialize
        const client = new UmaraClient();
        client.connect();
    </script>
</body>
</html>"""


def start_server(
    app: UmaraApp,
    host: str = "127.0.0.1",
    port: int = 8501,
    debug: bool = False,
    reload: bool = False,
) -> None:
    """Start the Umara server."""
    fastapi_app = create_fastapi_app(app)

    # Configure uvicorn
    config = uvicorn.Config(
        fastapi_app,
        host=host,
        port=port,
        log_level="debug" if debug else "info",
        reload=False,  # We handle reload ourselves
    )

    server = uvicorn.Server(config)
    server.run()


def run_with_reload(
    script_path: str,
    host: str = "127.0.0.1",
    port: int = 8501,
    debug: bool = False,
) -> None:
    """Run server with file watching for hot reload."""
    import subprocess
    from watchfiles import watch

    script_path = Path(script_path).resolve()
    script_dir = script_path.parent

    def run_server():
        """Run the server in a subprocess."""
        env = os.environ.copy()
        env["UMARA_SCRIPT"] = str(script_path)
        return subprocess.Popen(
            [sys.executable, "-m", "umara.server", str(script_path), host, str(port)],
            env=env,
            cwd=str(script_dir),
        )

    process = run_server()

    try:
        # Watch for file changes
        for changes in watch(script_dir, recursive=True):
            for change_type, changed_path in changes:
                if changed_path.endswith(".py"):
                    print(f"\n🔄 File changed: {changed_path}")
                    print("Reloading...")
                    process.terminate()
                    process.wait()
                    process = run_server()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        process.terminate()
        process.wait()


if __name__ == "__main__":
    # Called as subprocess for reload functionality
    import sys

    if len(sys.argv) >= 4:
        script_path = sys.argv[1]
        host = sys.argv[2]
        port = int(sys.argv[3])

        # Load the user's script
        spec = importlib.util.spec_from_file_location("user_app", script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["user_app"] = module

            # Get the app before running
            app = get_app()

            # Create a wrapper function that loads and runs the module
            def run_user_app():
                # Reload the module
                spec.loader.exec_module(module)

            app.set_app_function(run_user_app)

            # Start the server
            start_server(app, host=host, port=port)
