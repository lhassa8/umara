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
        @keyframes skeleton-loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
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

                    case 'toggle':
                        const toggleWrapper = document.createElement('label');
                        toggleWrapper.className = 'um-toggle-wrapper';
                        toggleWrapper.style.cssText = 'display: flex; align-items: center; gap: 12px; cursor: pointer; margin-bottom: 12px;';

                        const toggleTrack = document.createElement('div');
                        toggleTrack.style.cssText = `width: 44px; height: 24px; border-radius: 12px; background: ${{props.value ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-border, #e2e8f0)'}}; position: relative; transition: all 0.2s;`;

                        const toggleThumb = document.createElement('div');
                        toggleThumb.style.cssText = `width: 20px; height: 20px; border-radius: 50%; background: white; position: absolute; top: 2px; left: ${{props.value ? '22px' : '2px'}}; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.2);`;
                        toggleTrack.appendChild(toggleThumb);

                        const toggleLabel = document.createElement('span');
                        toggleLabel.textContent = props.label || '';
                        toggleLabel.style.cssText = 'font-size: 14px;';

                        toggleWrapper.onclick = () => this.sendStateUpdate(props.stateKey || id, !props.value);
                        toggleWrapper.appendChild(toggleTrack);
                        toggleWrapper.appendChild(toggleLabel);
                        this.applyStyle(toggleWrapper, style);
                        return toggleWrapper;

                    case 'chat':
                        const chatContainer = document.createElement('div');
                        chatContainer.className = 'um-chat';
                        chatContainer.style.cssText = `display: flex; flex-direction: column; height: ${{props.height || '500px'}}; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 12px; overflow: hidden; background: var(--um-color-surface, #fff); margin-bottom: 16px;`;

                        const chatMessages = document.createElement('div');
                        chatMessages.className = 'um-chat-messages';
                        chatMessages.style.cssText = 'flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px;';

                        (props.messages || []).forEach(msg => {{
                            const msgEl = document.createElement('div');
                            const isUser = msg.role === 'user';
                            msgEl.className = `um-chat-message um-chat-message-${{msg.role}}`;
                            msgEl.style.cssText = `display: flex; gap: 12px; ${{isUser ? 'flex-direction: row-reverse;' : ''}}`;

                            const avatar = document.createElement('div');
                            avatar.style.cssText = `width: 36px; height: 36px; border-radius: 50%; background: ${{isUser ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-secondary, #64748b)'}}; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; font-weight: 500; flex-shrink: 0;`;
                            avatar.textContent = isUser ? 'U' : 'A';

                            const bubble = document.createElement('div');
                            bubble.style.cssText = `max-width: 70%; padding: 12px 16px; border-radius: 16px; background: ${{isUser ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-background-secondary, #f1f5f9)'}}; color: ${{isUser ? 'white' : 'var(--um-color-text, #0f172a)'}}; font-size: 14px; line-height: 1.5;`;
                            bubble.textContent = msg.content;

                            msgEl.appendChild(avatar);
                            msgEl.appendChild(bubble);
                            chatMessages.appendChild(msgEl);
                        }});

                        chatContainer.appendChild(chatMessages);

                        if (props.showInput !== false) {{
                            const chatInputArea = document.createElement('div');
                            chatInputArea.style.cssText = 'padding: 12px 16px; border-top: 1px solid var(--um-color-border, #e2e8f0); display: flex; gap: 12px;';

                            const chatInput = document.createElement('input');
                            chatInput.type = 'text';
                            chatInput.placeholder = props.inputPlaceholder || 'Type a message...';
                            chatInput.style.cssText = 'flex: 1; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; outline: none;';
                            chatInput.id = `chat-input-${{id}}`;

                            const sendBtn = document.createElement('button');
                            sendBtn.textContent = 'Send';
                            sendBtn.style.cssText = 'padding: 10px 20px; background: var(--um-color-primary, #6366f1); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500;';
                            sendBtn.onclick = () => {{
                                const inputEl = document.getElementById(`chat-input-${{id}}`);
                                if (inputEl && inputEl.value.trim()) {{
                                    this.sendEvent(id, 'submit', {{ message: inputEl.value }});
                                    inputEl.value = '';
                                }}
                            }};

                            chatInput.onkeypress = (e) => {{
                                if (e.key === 'Enter') sendBtn.click();
                            }};

                            chatInputArea.appendChild(chatInput);
                            chatInputArea.appendChild(sendBtn);
                            chatContainer.appendChild(chatInputArea);
                        }}

                        setTimeout(() => {{ chatMessages.scrollTop = chatMessages.scrollHeight; }}, 0);
                        this.applyStyle(chatContainer, style);
                        return chatContainer;

                    case 'chat_message':
                        const cmWrapper = document.createElement('div');
                        const cmIsUser = props.role === 'user';
                        cmWrapper.style.cssText = `display: flex; gap: 12px; margin-bottom: 12px; ${{cmIsUser ? 'flex-direction: row-reverse;' : ''}}`;

                        const cmAvatar = document.createElement('div');
                        cmAvatar.style.cssText = `width: 36px; height: 36px; border-radius: 50%; background: ${{cmIsUser ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-secondary, #64748b)'}}; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; flex-shrink: 0;`;
                        cmAvatar.textContent = cmIsUser ? 'U' : 'A';

                        const cmBubble = document.createElement('div');
                        cmBubble.style.cssText = `max-width: 70%; padding: 12px 16px; border-radius: 16px; background: ${{cmIsUser ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-background-secondary, #f1f5f9)'}}; color: ${{cmIsUser ? 'white' : 'var(--um-color-text, #0f172a)'}}; font-size: 14px;`;
                        cmBubble.textContent = props.content || '';

                        cmWrapper.appendChild(cmAvatar);
                        cmWrapper.appendChild(cmBubble);
                        this.applyStyle(cmWrapper, style);
                        return cmWrapper;

                    case 'chat_input':
                        const ciWrapper = document.createElement('div');
                        ciWrapper.style.cssText = 'display: flex; gap: 12px; margin-bottom: 16px;';

                        const ciInput = document.createElement('input');
                        ciInput.type = 'text';
                        ciInput.placeholder = props.placeholder || 'Type a message...';
                        ciInput.style.cssText = 'flex: 1; padding: 12px 16px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; outline: none;';
                        ciInput.id = `chat-input-${{id}}`;

                        const ciBtn = document.createElement('button');
                        ciBtn.textContent = props.buttonLabel || 'Send';
                        ciBtn.style.cssText = 'padding: 12px 24px; background: var(--um-color-primary, #6366f1); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 500;';
                        ciBtn.onclick = () => {{
                            const el = document.getElementById(`chat-input-${{id}}`);
                            if (el && el.value.trim()) {{
                                this.sendEvent(id, 'submit', {{ message: el.value }});
                                el.value = '';
                            }}
                        }};

                        ciInput.onkeypress = (e) => {{ if (e.key === 'Enter') ciBtn.click(); }};

                        ciWrapper.appendChild(ciInput);
                        ciWrapper.appendChild(ciBtn);
                        this.applyStyle(ciWrapper, style);
                        return ciWrapper;

                    case 'chat_container':
                        const ccWrapper = document.createElement('div');
                        ccWrapper.className = 'um-chat-container';
                        ccWrapper.style.cssText = `height: ${{props.height || '400px'}}; overflow-y: auto; padding: 16px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 12px; margin-bottom: 16px;`;
                        children?.forEach(child => ccWrapper.appendChild(this.renderComponent(child)));
                        setTimeout(() => {{ ccWrapper.scrollTop = ccWrapper.scrollHeight; }}, 0);
                        this.applyStyle(ccWrapper, style);
                        return ccWrapper;

                    case 'sidebar':
                        const sidebarEl = document.createElement('aside');
                        sidebarEl.className = 'um-sidebar';
                        sidebarEl.style.cssText = `position: fixed; left: 0; top: 0; bottom: 0; width: ${{props.width || '280px'}}; background: var(--um-color-surface, #fff); border-right: 1px solid var(--um-color-border, #e2e8f0); padding: 24px; overflow-y: auto; z-index: 100;`;
                        children?.forEach(child => sidebarEl.appendChild(this.renderComponent(child)));
                        this.applyStyle(sidebarEl, style);
                        return sidebarEl;

                    case 'nav_link':
                        const navLink = document.createElement('a');
                        navLink.className = `um-nav-link ${{props.active ? 'active' : ''}}`;
                        navLink.href = props.href || '#';
                        navLink.style.cssText = `display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 8px; text-decoration: none; font-size: 14px; color: ${{props.active ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-text, #0f172a)'}}; background: ${{props.active ? 'var(--um-color-primary-light, #eef2ff)' : 'transparent'}}; margin-bottom: 4px; transition: all 0.2s;`;
                        navLink.textContent = props.label || '';
                        navLink.onclick = (e) => {{ e.preventDefault(); this.sendEvent(id, 'click', {{ href: props.href }}); }};
                        this.applyStyle(navLink, style);
                        return navLink;

                    case 'breadcrumbs':
                        const bcWrapper = document.createElement('nav');
                        bcWrapper.className = 'um-breadcrumbs';
                        bcWrapper.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font-size: 14px;';
                        (props.items || []).forEach((item, i) => {{
                            if (i > 0) {{
                                const sep = document.createElement('span');
                                sep.textContent = props.separator || '/';
                                sep.style.cssText = 'color: var(--um-color-text-secondary, #64748b);';
                                bcWrapper.appendChild(sep);
                            }}
                            const bcItem = document.createElement('a');
                            bcItem.href = item.href || '#';
                            bcItem.textContent = item.label;
                            bcItem.style.cssText = `text-decoration: none; color: ${{i === (props.items.length - 1) ? 'var(--um-color-text, #0f172a)' : 'var(--um-color-primary, #6366f1)'}};`;
                            bcWrapper.appendChild(bcItem);
                        }});
                        this.applyStyle(bcWrapper, style);
                        return bcWrapper;

                    case 'pagination':
                        const pgWrapper = document.createElement('div');
                        pgWrapper.className = 'um-pagination';
                        pgWrapper.style.cssText = 'display: flex; align-items: center; gap: 4px; margin-bottom: 16px;';
                        const total = props.totalPages || 1;
                        const current = props.currentPage || 1;

                        const pgPrev = document.createElement('button');
                        pgPrev.textContent = '←';
                        pgPrev.disabled = current <= 1;
                        pgPrev.style.cssText = 'padding: 8px 12px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 6px; background: white; cursor: pointer;';
                        pgPrev.onclick = () => this.sendStateUpdate(props.stateKey || id, current - 1);
                        pgWrapper.appendChild(pgPrev);

                        for (let i = 1; i <= Math.min(total, 7); i++) {{
                            const pgBtn = document.createElement('button');
                            pgBtn.textContent = i;
                            pgBtn.style.cssText = `padding: 8px 12px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 6px; cursor: pointer; ${{i === current ? 'background: var(--um-color-primary, #6366f1); color: white; border-color: var(--um-color-primary, #6366f1);' : 'background: white;'}}`;
                            pgBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, i);
                            pgWrapper.appendChild(pgBtn);
                        }}

                        const pgNext = document.createElement('button');
                        pgNext.textContent = '→';
                        pgNext.disabled = current >= total;
                        pgNext.style.cssText = 'padding: 8px 12px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 6px; background: white; cursor: pointer;';
                        pgNext.onclick = () => this.sendStateUpdate(props.stateKey || id, current + 1);
                        pgWrapper.appendChild(pgNext);

                        this.applyStyle(pgWrapper, style);
                        return pgWrapper;

                    case 'expander':
                        const expWrapper = document.createElement('div');
                        expWrapper.className = 'um-expander';
                        expWrapper.style.cssText = 'border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; margin-bottom: 12px; overflow: hidden;';

                        const expHeader = document.createElement('button');
                        expHeader.style.cssText = 'width: 100%; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; background: var(--um-color-background-secondary, #f8fafc); border: none; cursor: pointer; font-size: 14px; font-weight: 500;';
                        expHeader.innerHTML = `<span>${{props.label || 'Expand'}}</span><span style="transform: rotate(${{props.expanded ? '180deg' : '0deg'}}); transition: transform 0.2s;">▼</span>`;
                        expHeader.onclick = () => this.sendStateUpdate(props.stateKey || id, !props.expanded);

                        expWrapper.appendChild(expHeader);

                        if (props.expanded) {{
                            const expContent = document.createElement('div');
                            expContent.style.cssText = 'padding: 16px;';
                            children?.forEach(child => expContent.appendChild(this.renderComponent(child)));
                            expWrapper.appendChild(expContent);
                        }}

                        this.applyStyle(expWrapper, style);
                        return expWrapper;

                    case 'accordion':
                        const accWrapper = document.createElement('div');
                        accWrapper.className = 'um-accordion';
                        accWrapper.style.cssText = 'margin-bottom: 16px;';
                        children?.forEach(child => accWrapper.appendChild(this.renderComponent(child)));
                        this.applyStyle(accWrapper, style);
                        return accWrapper;

                    case 'modal':
                        if (!props.isOpen) return document.createTextNode('');

                        const modalOverlay = document.createElement('div');
                        modalOverlay.className = 'um-modal-overlay';
                        modalOverlay.style.cssText = 'position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;';
                        modalOverlay.onclick = (e) => {{ if (e.target === modalOverlay && props.closeOnOverlay !== false) this.sendEvent(id, 'close', {{}}); }};

                        const modalContent = document.createElement('div');
                        modalContent.className = 'um-modal';
                        modalContent.style.cssText = `background: var(--um-color-surface, #fff); border-radius: 16px; padding: 24px; max-width: ${{props.width || '500px'}}; width: 90%; max-height: 90vh; overflow-y: auto; position: relative;`;

                        if (props.title) {{
                            const modalHeader = document.createElement('div');
                            modalHeader.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;';
                            modalHeader.innerHTML = `<h3 style="font-size: 18px; font-weight: 600; margin: 0;">${{props.title}}</h3>`;

                            const closeBtn = document.createElement('button');
                            closeBtn.textContent = '×';
                            closeBtn.style.cssText = 'background: none; border: none; font-size: 24px; cursor: pointer; color: var(--um-color-text-secondary, #64748b);';
                            closeBtn.onclick = () => this.sendEvent(id, 'close', {{}});
                            modalHeader.appendChild(closeBtn);
                            modalContent.appendChild(modalHeader);
                        }}

                        const modalBody = document.createElement('div');
                        children?.forEach(child => modalBody.appendChild(this.renderComponent(child)));
                        modalContent.appendChild(modalBody);

                        modalOverlay.appendChild(modalContent);
                        this.applyStyle(modalContent, style);
                        return modalOverlay;

                    case 'badge':
                        const badgeEl = document.createElement('span');
                        badgeEl.className = `um-badge um-badge-${{props.variant || 'default'}}`;
                        const badgeColors = {{
                            default: 'background: var(--um-color-background-secondary, #f1f5f9); color: var(--um-color-text, #0f172a);',
                            primary: 'background: var(--um-color-primary-light, #eef2ff); color: var(--um-color-primary, #6366f1);',
                            success: 'background: var(--um-color-success-light, #d1fae5); color: var(--um-color-success-dark, #047857);',
                            warning: 'background: var(--um-color-warning-light, #fef3c7); color: var(--um-color-warning-dark, #b45309);',
                            error: 'background: var(--um-color-error-light, #fee2e2); color: var(--um-color-error-dark, #b91c1c);',
                        }};
                        badgeEl.style.cssText = `display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 500; ${{badgeColors[props.variant] || badgeColors.default}}`;
                        badgeEl.textContent = props.label || '';
                        this.applyStyle(badgeEl, style);
                        return badgeEl;

                    case 'avatar':
                        const avatarEl = document.createElement('div');
                        avatarEl.className = 'um-avatar';
                        const avatarSize = props.size || '40px';
                        avatarEl.style.cssText = `width: ${{avatarSize}}; height: ${{avatarSize}}; border-radius: 50%; background: var(--um-color-primary, #6366f1); display: flex; align-items: center; justify-content: center; color: white; font-weight: 500; font-size: calc(${{avatarSize}} / 2.5); overflow: hidden;`;
                        if (props.src) {{
                            const img = document.createElement('img');
                            img.src = props.src;
                            img.style.cssText = 'width: 100%; height: 100%; object-fit: cover;';
                            avatarEl.appendChild(img);
                        }} else {{
                            avatarEl.textContent = (props.name || 'U').charAt(0).toUpperCase();
                        }}
                        this.applyStyle(avatarEl, style);
                        return avatarEl;

                    case 'stat_card':
                        const statCard = document.createElement('div');
                        statCard.className = 'um-stat-card';
                        statCard.style.cssText = 'background: var(--um-color-surface, #fff); border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 16px;';
                        statCard.innerHTML = `
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div>
                                    <div style="font-size: 14px; color: var(--um-color-text-secondary, #64748b); margin-bottom: 4px;">${{props.label || ''}}</div>
                                    <div style="font-size: 28px; font-weight: 700; color: var(--um-color-text, #0f172a);">${{props.value || '0'}}</div>
                                    ${{props.delta ? `<div style="font-size: 14px; margin-top: 4px; color: ${{props.delta > 0 ? 'var(--um-color-success, #10b981)' : 'var(--um-color-error, #ef4444)'}};">${{props.delta > 0 ? '↑' : '↓'}} ${{Math.abs(props.delta)}}%</div>` : ''}}
                                </div>
                                ${{props.icon ? `<div style="width: 48px; height: 48px; border-radius: 12px; background: var(--um-color-primary-light, #eef2ff); display: flex; align-items: center; justify-content: center; font-size: 24px;">${{props.icon}}</div>` : ''}}
                            </div>
                        `;
                        this.applyStyle(statCard, style);
                        return statCard;

                    case 'empty_state':
                        const emptyEl = document.createElement('div');
                        emptyEl.className = 'um-empty-state';
                        emptyEl.style.cssText = 'text-align: center; padding: 48px 24px; margin-bottom: 16px;';
                        emptyEl.innerHTML = `
                            ${{props.icon ? `<div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">${{props.icon}}</div>` : ''}}
                            <h3 style="font-size: 18px; font-weight: 600; color: var(--um-color-text, #0f172a); margin-bottom: 8px;">${{props.title || 'No data'}}</h3>
                            <p style="font-size: 14px; color: var(--um-color-text-secondary, #64748b); margin-bottom: 16px;">${{props.description || ''}}</p>
                        `;
                        children?.forEach(child => emptyEl.appendChild(this.renderComponent(child)));
                        this.applyStyle(emptyEl, style);
                        return emptyEl;

                    case 'loading_skeleton':
                        const skelEl = document.createElement('div');
                        skelEl.className = 'um-skeleton';
                        skelEl.style.cssText = `height: ${{props.height || '20px'}}; width: ${{props.width || '100%'}}; background: linear-gradient(90deg, var(--um-color-border, #e2e8f0) 25%, var(--um-color-background-secondary, #f8fafc) 50%, var(--um-color-border, #e2e8f0) 75%); background-size: 200% 100%; animation: skeleton-loading 1.5s infinite; border-radius: ${{props.rounded ? '9999px' : '8px'}}; margin-bottom: 8px;`;
                        return skelEl;

                    case 'timeline':
                        const tlWrapper = document.createElement('div');
                        tlWrapper.className = 'um-timeline';
                        tlWrapper.style.cssText = 'position: relative; padding-left: 24px; margin-bottom: 16px;';
                        (props.items || []).forEach((item, i) => {{
                            const tlItem = document.createElement('div');
                            tlItem.style.cssText = 'position: relative; padding-bottom: 24px;';
                            tlItem.innerHTML = `
                                <div style="position: absolute; left: -24px; width: 12px; height: 12px; border-radius: 50%; background: var(--um-color-primary, #6366f1); border: 2px solid var(--um-color-surface, #fff);"></div>
                                ${{i < (props.items.length - 1) ? '<div style="position: absolute; left: -19px; top: 16px; bottom: 0; width: 2px; background: var(--um-color-border, #e2e8f0);"></div>' : ''}}
                                <div style="font-weight: 600; margin-bottom: 4px;">${{item.title}}</div>
                                <div style="font-size: 14px; color: var(--um-color-text-secondary, #64748b);">${{item.description || ''}}</div>
                                ${{item.time ? `<div style="font-size: 12px; color: var(--um-color-text-secondary, #64748b); margin-top: 4px;">${{item.time}}</div>` : ''}}
                            `;
                            tlWrapper.appendChild(tlItem);
                        }});
                        this.applyStyle(tlWrapper, style);
                        return tlWrapper;

                    case 'steps':
                        const stepsWrapper = document.createElement('div');
                        stepsWrapper.className = 'um-steps';
                        stepsWrapper.style.cssText = 'display: flex; margin-bottom: 24px;';
                        (props.items || []).forEach((item, i) => {{
                            const stepItem = document.createElement('div');
                            stepItem.style.cssText = 'flex: 1; display: flex; flex-direction: column; align-items: center; position: relative;';
                            const isActive = i <= (props.currentStep || 0);
                            stepItem.innerHTML = `
                                <div style="width: 32px; height: 32px; border-radius: 50%; background: ${{isActive ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-border, #e2e8f0)'}}; color: ${{isActive ? 'white' : 'var(--um-color-text-secondary, #64748b)'}}; display: flex; align-items: center; justify-content: center; font-weight: 600; z-index: 1;">${{i + 1}}</div>
                                <div style="font-size: 14px; margin-top: 8px; text-align: center; color: ${{isActive ? 'var(--um-color-text, #0f172a)' : 'var(--um-color-text-secondary, #64748b)'}};">${{item}}</div>
                                ${{i < (props.items.length - 1) ? `<div style="position: absolute; top: 16px; left: calc(50% + 20px); right: calc(-50% + 20px); height: 2px; background: ${{i < (props.currentStep || 0) ? 'var(--um-color-primary, #6366f1)' : 'var(--um-color-border, #e2e8f0)'}};"></div>` : ''}}
                            `;
                            stepsWrapper.appendChild(stepItem);
                        }});
                        this.applyStyle(stepsWrapper, style);
                        return stepsWrapper;

                    case 'number_input':
                        const numWrapper = document.createElement('div');
                        numWrapper.className = 'um-number-input';
                        numWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const numLabel = document.createElement('label');
                            numLabel.textContent = props.label;
                            numLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            numWrapper.appendChild(numLabel);
                        }}

                        const numInputGroup = document.createElement('div');
                        numInputGroup.style.cssText = 'display: flex; align-items: center;';

                        const numDecBtn = document.createElement('button');
                        numDecBtn.textContent = '−';
                        numDecBtn.style.cssText = 'width: 36px; height: 36px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px 0 0 8px; background: var(--um-color-background-secondary, #f8fafc); cursor: pointer; font-size: 18px;';
                        numDecBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, Math.max(props.min || -Infinity, (props.value || 0) - (props.step || 1)));

                        const numInput = document.createElement('input');
                        numInput.type = 'number';
                        numInput.value = props.value || 0;
                        numInput.min = props.min;
                        numInput.max = props.max;
                        numInput.step = props.step || 1;
                        numInput.style.cssText = 'width: 80px; height: 36px; border: 1px solid var(--um-color-border, #e2e8f0); border-left: none; border-right: none; text-align: center; font-size: 14px; -moz-appearance: textfield;';
                        numInput.onchange = (e) => this.sendStateUpdate(props.stateKey || id, parseFloat(e.target.value));

                        const numIncBtn = document.createElement('button');
                        numIncBtn.textContent = '+';
                        numIncBtn.style.cssText = 'width: 36px; height: 36px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 0 8px 8px 0; background: var(--um-color-background-secondary, #f8fafc); cursor: pointer; font-size: 18px;';
                        numIncBtn.onclick = () => this.sendStateUpdate(props.stateKey || id, Math.min(props.max || Infinity, (props.value || 0) + (props.step || 1)));

                        numInputGroup.appendChild(numDecBtn);
                        numInputGroup.appendChild(numInput);
                        numInputGroup.appendChild(numIncBtn);
                        numWrapper.appendChild(numInputGroup);
                        this.applyStyle(numWrapper, style);
                        return numWrapper;

                    case 'rating':
                        const ratingWrapper = document.createElement('div');
                        ratingWrapper.className = 'um-rating';
                        ratingWrapper.style.cssText = 'display: flex; gap: 4px; margin-bottom: 16px;';
                        const maxRating = props.max || 5;
                        const currentRating = props.value || 0;
                        for (let i = 1; i <= maxRating; i++) {{
                            const star = document.createElement('button');
                            star.textContent = i <= currentRating ? '★' : '☆';
                            star.style.cssText = `background: none; border: none; font-size: 24px; cursor: pointer; color: ${{i <= currentRating ? 'var(--um-color-warning, #f59e0b)' : 'var(--um-color-border, #e2e8f0)'}};`;
                            star.onclick = () => this.sendStateUpdate(props.stateKey || id, i);
                            ratingWrapper.appendChild(star);
                        }}
                        this.applyStyle(ratingWrapper, style);
                        return ratingWrapper;

                    case 'code':
                        const codeWrapper = document.createElement('div');
                        codeWrapper.className = 'um-code-block';
                        codeWrapper.style.cssText = 'margin-bottom: 16px; border-radius: 8px; overflow: hidden;';

                        if (props.language) {{
                            const codeLang = document.createElement('div');
                            codeLang.style.cssText = 'background: #1e293b; color: #94a3b8; padding: 8px 16px; font-size: 12px; font-family: monospace;';
                            codeLang.textContent = props.language;
                            codeWrapper.appendChild(codeLang);
                        }}

                        const codeEl = document.createElement('pre');
                        codeEl.style.cssText = 'background: #0f172a; color: #e2e8f0; padding: 16px; margin: 0; overflow-x: auto; font-family: "JetBrains Mono", monospace; font-size: 14px; line-height: 1.6;';
                        const codeContent = document.createElement('code');
                        codeContent.textContent = props.content || '';
                        codeEl.appendChild(codeContent);
                        codeWrapper.appendChild(codeEl);

                        this.applyStyle(codeWrapper, style);
                        return codeWrapper;

                    case 'markdown':
                        const mdEl = document.createElement('div');
                        mdEl.className = 'um-markdown';
                        mdEl.style.cssText = 'margin-bottom: 16px; line-height: 1.7;';
                        // Simple markdown rendering
                        let mdContent = props.content || '';
                        mdContent = mdContent.replace(/^### (.+)$/gm, '<h3 style="font-size: 1.25rem; font-weight: 600; margin: 1em 0 0.5em;">$1</h3>');
                        mdContent = mdContent.replace(/^## (.+)$/gm, '<h2 style="font-size: 1.5rem; font-weight: 600; margin: 1em 0 0.5em;">$1</h2>');
                        mdContent = mdContent.replace(/^# (.+)$/gm, '<h1 style="font-size: 2rem; font-weight: 700; margin: 1em 0 0.5em;">$1</h1>');
                        mdContent = mdContent.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
                        mdContent = mdContent.replace(/\*(.+?)\*/g, '<em>$1</em>');
                        mdContent = mdContent.replace(/`(.+?)`/g, '<code style="background: var(--um-color-background-secondary, #f1f5f9); padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>');
                        mdContent = mdContent.replace(/\\n/g, '<br>');
                        mdEl.innerHTML = mdContent;
                        this.applyStyle(mdEl, style);
                        return mdEl;

                    case 'json_viewer':
                        const jsonWrapper = document.createElement('div');
                        jsonWrapper.className = 'um-json-viewer';
                        jsonWrapper.style.cssText = 'background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; font-family: monospace; font-size: 13px; margin-bottom: 16px;';
                        try {{
                            const formatted = JSON.stringify(props.data, null, 2);
                            jsonWrapper.innerHTML = `<pre style="margin: 0;">${{formatted}}</pre>`;
                        }} catch (e) {{
                            jsonWrapper.textContent = String(props.data);
                        }}
                        this.applyStyle(jsonWrapper, style);
                        return jsonWrapper;

                    case 'html':
                        const htmlWrapper = document.createElement('div');
                        htmlWrapper.className = 'um-html';
                        htmlWrapper.innerHTML = props.content || '';
                        this.applyStyle(htmlWrapper, style);
                        return htmlWrapper;

                    case 'iframe':
                        const iframeWrapper = document.createElement('div');
                        iframeWrapper.className = 'um-iframe-wrapper';
                        iframeWrapper.style.cssText = 'margin-bottom: 16px; border-radius: 8px; overflow: hidden;';
                        const iframeEl = document.createElement('iframe');
                        iframeEl.src = props.src || '';
                        iframeEl.style.cssText = `width: ${{props.width || '100%'}}; height: ${{props.height || '400px'}}; border: none;`;
                        iframeWrapper.appendChild(iframeEl);
                        this.applyStyle(iframeWrapper, style);
                        return iframeWrapper;

                    case 'line_chart':
                    case 'bar_chart':
                    case 'area_chart':
                    case 'pie_chart':
                        const chartWrapper = document.createElement('div');
                        chartWrapper.className = `um-chart um-${{type}}`;
                        chartWrapper.style.cssText = `height: ${{props.height || '300px'}}; background: var(--um-color-surface, #fff); border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 12px; padding: 16px; margin-bottom: 16px; display: flex; align-items: center; justify-content: center;`;
                        chartWrapper.innerHTML = `<div style="text-align: center; color: var(--um-color-text-secondary, #64748b);"><div style="font-size: 32px; margin-bottom: 8px;">📊</div><div>Chart: ${{props.title || type}}</div><div style="font-size: 12px; margin-top: 4px;">Connect a charting library for full visualization</div></div>`;
                        this.applyStyle(chartWrapper, style);
                        return chartWrapper;

                    case 'grid':
                        const gridEl = document.createElement('div');
                        gridEl.className = 'um-grid';
                        gridEl.style.cssText = `display: grid; grid-template-columns: repeat(${{props.columns || 3}}, 1fr); gap: ${{props.gap || '16px'}}; margin-bottom: 16px;`;
                        children?.forEach(child => gridEl.appendChild(this.renderComponent(child)));
                        this.applyStyle(gridEl, style);
                        return gridEl;

                    case 'text_area':
                        const taWrapper = document.createElement('div');
                        taWrapper.className = 'um-textarea-wrapper';
                        taWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const taLabel = document.createElement('label');
                            taLabel.textContent = props.label;
                            taLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            taWrapper.appendChild(taLabel);
                        }}

                        const taEl = document.createElement('textarea');
                        taEl.value = props.value || '';
                        taEl.placeholder = props.placeholder || '';
                        taEl.rows = props.rows || 4;
                        taEl.style.cssText = 'width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; resize: vertical; font-family: inherit; outline: none;';
                        taEl.onfocus = () => taEl.style.borderColor = 'var(--um-color-primary, #6366f1)';
                        taEl.onblur = () => taEl.style.borderColor = 'var(--um-color-border, #e2e8f0)';
                        taEl.oninput = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                        taWrapper.appendChild(taEl);
                        this.applyStyle(taWrapper, style);
                        return taWrapper;

                    case 'radio':
                        const radioWrapper = document.createElement('div');
                        radioWrapper.className = 'um-radio-group';
                        radioWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const radioGroupLabel = document.createElement('div');
                            radioGroupLabel.textContent = props.label;
                            radioGroupLabel.style.cssText = 'font-size: 14px; font-weight: 500; margin-bottom: 8px;';
                            radioWrapper.appendChild(radioGroupLabel);
                        }}

                        (props.options || []).forEach(opt => {{
                            const optValue = typeof opt === 'object' ? opt.value : opt;
                            const optLabel = typeof opt === 'object' ? opt.label : opt;

                            const radioItem = document.createElement('label');
                            radioItem.style.cssText = 'display: flex; align-items: center; gap: 8px; cursor: pointer; margin-bottom: 8px;';

                            const radioInput = document.createElement('input');
                            radioInput.type = 'radio';
                            radioInput.name = id;
                            radioInput.value = optValue;
                            radioInput.checked = props.value === optValue;
                            radioInput.style.cssText = 'width: 18px; height: 18px; accent-color: var(--um-color-primary, #6366f1);';
                            radioInput.onchange = () => this.sendStateUpdate(props.stateKey || id, optValue);

                            const radioLabel = document.createElement('span');
                            radioLabel.textContent = optLabel;
                            radioLabel.style.cssText = 'font-size: 14px;';

                            radioItem.appendChild(radioInput);
                            radioItem.appendChild(radioLabel);
                            radioWrapper.appendChild(radioItem);
                        }});

                        this.applyStyle(radioWrapper, style);
                        return radioWrapper;

                    case 'date_input':
                        const dateWrapper = document.createElement('div');
                        dateWrapper.className = 'um-date-input';
                        dateWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const dateLabel = document.createElement('label');
                            dateLabel.textContent = props.label;
                            dateLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            dateWrapper.appendChild(dateLabel);
                        }}

                        const dateInput = document.createElement('input');
                        dateInput.type = 'date';
                        dateInput.value = props.value || '';
                        dateInput.style.cssText = 'width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; outline: none;';
                        dateInput.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                        dateWrapper.appendChild(dateInput);
                        this.applyStyle(dateWrapper, style);
                        return dateWrapper;

                    case 'time_input':
                        const timeWrapper = document.createElement('div');
                        timeWrapper.className = 'um-time-input';
                        timeWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const timeLabel = document.createElement('label');
                            timeLabel.textContent = props.label;
                            timeLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            timeWrapper.appendChild(timeLabel);
                        }}

                        const timeInput = document.createElement('input');
                        timeInput.type = 'time';
                        timeInput.value = props.value || '';
                        timeInput.style.cssText = 'width: 100%; padding: 10px 14px; border: 1px solid var(--um-color-border, #e2e8f0); border-radius: 8px; font-size: 14px; outline: none;';
                        timeInput.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);
                        timeWrapper.appendChild(timeInput);
                        this.applyStyle(timeWrapper, style);
                        return timeWrapper;

                    case 'color_picker':
                        const colorWrapper = document.createElement('div');
                        colorWrapper.className = 'um-color-picker';
                        colorWrapper.style.cssText = 'margin-bottom: 16px;';

                        if (props.label) {{
                            const colorLabel = document.createElement('label');
                            colorLabel.textContent = props.label;
                            colorLabel.style.cssText = 'display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px;';
                            colorWrapper.appendChild(colorLabel);
                        }}

                        const colorInputGroup = document.createElement('div');
                        colorInputGroup.style.cssText = 'display: flex; align-items: center; gap: 12px;';

                        const colorInput = document.createElement('input');
                        colorInput.type = 'color';
                        colorInput.value = props.value || '#6366f1';
                        colorInput.style.cssText = 'width: 48px; height: 48px; border: none; border-radius: 8px; cursor: pointer;';
                        colorInput.onchange = (e) => this.sendStateUpdate(props.stateKey || id, e.target.value);

                        const colorValue = document.createElement('span');
                        colorValue.textContent = props.value || '#6366f1';
                        colorValue.style.cssText = 'font-family: monospace; font-size: 14px;';

                        colorInputGroup.appendChild(colorInput);
                        colorInputGroup.appendChild(colorValue);
                        colorWrapper.appendChild(colorInputGroup);
                        this.applyStyle(colorWrapper, style);
                        return colorWrapper;

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
