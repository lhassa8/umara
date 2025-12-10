"""
Umara v0.6.0 Features Demo
Test the new caching, fragments, and connections modules.
"""

import time
import random
from datetime import datetime

import umara as um
from umara.cache import (
    cache,
    memoize,
    async_cache,
    cache_resource,
    cache_embedding,
    cache_llm_response,
    clear_all_caches,
    get_cache_stats,
    cleanup_expired,
)
from umara.fragments import (
    FragmentManager,
    FragmentConfig,
    FragmentGroup,
    get_all_fragment_stats,
)
from umara.connections import (
    ConnectionManager,
    ConnectionPool,
    temp_connection,
    list_connections,
    get_connection_info,
    close_all_connections,
)

# Initialize state
if "call_counts" not in um.session_state:
    um.session_state.call_counts = {
        "expensive_calc": 0,
        "fibonacci": 0,
        "simulated_api": 0,
        "embedding": 0,
        "llm_response": 0,
    }

if "fragment_outputs" not in um.session_state:
    um.session_state.fragment_outputs = {}

if "connection_log" not in um.session_state:
    um.session_state.connection_log = []


# ============== CACHING EXAMPLES ==============

@cache(ttl=10.0, namespace="demo")
def expensive_calculation(x: int, y: int) -> int:
    """Simulates an expensive calculation with 10s TTL cache."""
    um.session_state.call_counts["expensive_calc"] += 1
    time.sleep(0.5)  # Simulate work
    return x * y + random.randint(1, 100)


@memoize
def fibonacci(n: int) -> int:
    """Memoized fibonacci - efficient recursive calculation."""
    um.session_state.call_counts["fibonacci"] += 1
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache(ttl=5.0, namespace="api")
def simulated_api_call(endpoint: str) -> dict:
    """Simulates an API call with 5s TTL cache."""
    um.session_state.call_counts["simulated_api"] += 1
    time.sleep(0.3)  # Simulate network delay
    return {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "data": f"Response from {endpoint}",
        "random_id": random.randint(1000, 9999),
    }


@cache_embedding()
def get_fake_embedding(text: str) -> list:
    """Simulates getting text embeddings (cached indefinitely)."""
    um.session_state.call_counts["embedding"] += 1
    time.sleep(0.2)
    # Generate fake embedding vector
    return [random.random() for _ in range(5)]


@cache_llm_response(ttl=30.0)
def get_fake_llm_response(prompt: str) -> str:
    """Simulates LLM response (cached for 30s)."""
    um.session_state.call_counts["llm_response"] += 1
    time.sleep(0.4)
    responses = [
        f"I understand you're asking about '{prompt}'. Here's my response...",
        f"Great question about '{prompt}'! Let me explain...",
        f"Regarding '{prompt}', I can tell you that...",
    ]
    return random.choice(responses)


@cache_resource()
def get_shared_config() -> dict:
    """Returns a cached resource (singleton pattern)."""
    return {
        "app_name": "Demo App",
        "version": "0.6.0",
        "created_at": datetime.now().isoformat(),
    }


# ============== FRAGMENTS EXAMPLES ==============

fragment_manager = FragmentManager()
demo_group = FragmentGroup(name="demo_fragments")


# ============== CONNECTIONS EXAMPLES ==============

conn_manager = ConnectionManager()


class MockDatabaseConnection:
    """Mock database connection for demo purposes."""

    def __init__(self, name: str):
        self.name = name
        self.connected = True
        self.query_count = 0

    def query(self, sql: str) -> list:
        self.query_count += 1
        return [{"result": f"Data for: {sql}", "rows": random.randint(1, 100)}]

    def close(self):
        self.connected = False


# Create a connection pool
db_pool = ConnectionPool(
    factory=lambda: MockDatabaseConnection(f"conn_{random.randint(1000, 9999)}"),
    size=3
)


# ============== UI ==============

um.title("Umara v0.6.0 Features Demo")
um.text("Test the new caching, fragments, and connections modules.")

with um.tabs(["Caching", "Fragments", "Connections"], key="demo_tabs"):

    # ============== CACHING TAB ==============
    with um.tab(0):
        um.subheader("Cache Module Demo")

        with um.columns(2):
            with um.column():
                with um.card():
                    um.text("**@cache Decorator**", size="lg")
                    um.text("Cache with TTL (time-to-live)")

                    x = um.number_input("X value", value=5, min_value=1, max_value=100, key="cache_x")
                    y = um.number_input("Y value", value=10, min_value=1, max_value=100, key="cache_y")

                    if um.button("Calculate (cached 10s)", key="calc_btn"):
                        start = time.time()
                        result = expensive_calculation(int(x), int(y))
                        elapsed = time.time() - start
                        um.success(f"Result: {result}")
                        um.info(f"Time: {elapsed:.3f}s | Calls: {um.session_state.call_counts['expensive_calc']}")

                with um.card():
                    um.text("**@memoize Decorator**", size="lg")
                    um.text("Permanent memoization for recursive functions")

                    n = um.slider("Fibonacci N", min_value=1, max_value=35, value=10, key="fib_n")

                    if um.button("Calculate Fibonacci", key="fib_btn"):
                        # Reset counter for this calculation
                        um.session_state.call_counts["fibonacci"] = 0
                        start = time.time()
                        result = fibonacci(int(n))
                        elapsed = time.time() - start
                        um.success(f"fib({int(n)}) = {result}")
                        um.info(f"Time: {elapsed:.6f}s | Unique calls: {um.session_state.call_counts['fibonacci']}")

            with um.column():
                with um.card():
                    um.text("**API Caching**", size="lg")
                    um.text("Simulate cached API calls (5s TTL)")

                    endpoint = um.select(
                        "Select endpoint",
                        options=["/users", "/posts", "/comments", "/products"],
                        key="api_endpoint"
                    )

                    if um.button("Call API", key="api_btn"):
                        start = time.time()
                        result = simulated_api_call(endpoint)
                        elapsed = time.time() - start
                        um.json(result)
                        um.info(f"Time: {elapsed:.3f}s | Total API calls: {um.session_state.call_counts['simulated_api']}")

                with um.card():
                    um.text("**AI-Specific Caching**", size="lg")

                    text_input = um.input("Text for embedding", value="Hello world", key="embed_text")
                    if um.button("Get Embedding", key="embed_btn"):
                        embedding = get_fake_embedding(text_input)
                        um.text(f"Embedding (first 5 dims): {[f'{v:.3f}' for v in embedding[:5]]}")
                        um.info(f"Embedding calls: {um.session_state.call_counts['embedding']}")

                    prompt_input = um.input("LLM Prompt", value="What is Python?", key="llm_prompt")
                    if um.button("Get LLM Response", key="llm_btn"):
                        response = get_fake_llm_response(prompt_input)
                        um.text(response)
                        um.info(f"LLM calls: {um.session_state.call_counts['llm_response']}")

        um.divider()

        um.subheader("Cache Statistics & Management")

        with um.columns(3):
            with um.column():
                if um.button("Get Cache Stats", key="stats_btn", variant="secondary"):
                    stats = get_cache_stats()
                    um.json(stats)

            with um.column():
                if um.button("Cleanup Expired", key="cleanup_btn", variant="secondary"):
                    removed = cleanup_expired()
                    um.info(f"Removed {removed} expired entries")

            with um.column():
                if um.button("Clear All Caches", key="clear_btn", variant="danger"):
                    clear_all_caches()
                    um.session_state.call_counts = {k: 0 for k in um.session_state.call_counts}
                    um.success("All caches cleared!")

    # ============== FRAGMENTS TAB ==============
    with um.tab(1):
        um.subheader("Fragments Module Demo")
        um.text("Fragments allow partial UI updates without full page reruns.")

        with um.columns(2):
            with um.column():
                with um.card():
                    um.text("**Fragment Registration**", size="lg")
                    um.text("Register and manage UI fragments")

                    frag_name = um.input("Fragment name", value="my_fragment", key="frag_name")
                    run_every = um.number_input("Auto-run interval (seconds, 0=disabled)",
                                                 value=0, min_value=0, max_value=60, key="frag_interval")

                    if um.button("Register Fragment", key="reg_frag_btn"):
                        config = FragmentConfig(
                            run_every=float(run_every) if run_every > 0 else None
                        )
                        state = fragment_manager.register(
                            f"demo:{frag_name}",
                            frag_name,
                            config
                        )
                        um.success(f"Registered fragment: {state.name} (id: {state.id})")

                    if um.button("Mark for Rerun", key="rerun_btn"):
                        fragment_manager.mark_for_rerun(f"demo:{frag_name}")
                        um.info(f"Fragment '{frag_name}' marked for rerun")

                with um.card():
                    um.text("**Fragment Groups**", size="lg")
                    um.text("Group related fragments together")

                    if um.button("Add to Demo Group", key="add_group_btn"):
                        frag_id = f"demo:{frag_name}"
                        if frag_id not in demo_group._fragment_ids:
                            demo_group._fragment_ids.append(frag_id)
                            um.success(f"Added {frag_name} to demo_group")
                        else:
                            um.warning(f"{frag_name} already in group")

                    if um.button("Rerun All in Group", key="rerun_group_btn"):
                        demo_group.rerun_all()
                        um.info("All fragments in group marked for rerun")

                    um.text(f"Group members: {demo_group.fragment_ids}")

            with um.column():
                with um.card():
                    um.text("**Fragment State**", size="lg")

                    check_frag = um.input("Check fragment ID", value="demo:my_fragment", key="check_frag")

                    if um.button("Get State", key="get_state_btn"):
                        state = fragment_manager.get_state(check_frag)
                        if state:
                            um.json({
                                "id": state.id,
                                "name": state.name,
                                "run_count": state.run_count,
                                "last_run": state.last_run,
                                "is_running": state.is_running,
                                "has_error": state.error is not None,
                            })
                        else:
                            um.warning(f"Fragment '{check_frag}' not found")

                    if um.button("Record Run", key="record_run_btn"):
                        fragment_manager.record_run(check_frag, output=f"Run at {datetime.now()}")
                        um.success("Run recorded!")

                    if um.button("Check Auto-Rerun", key="check_auto_btn"):
                        should = fragment_manager.should_auto_rerun(check_frag)
                        um.info(f"Should auto-rerun: {should}")

                with um.card():
                    um.text("**Pending Reruns**", size="lg")

                    if um.button("Get Pending Reruns", key="pending_btn"):
                        pending = fragment_manager.get_pending_reruns()
                        if pending:
                            um.text(f"Pending: {pending}")
                        else:
                            um.info("No pending reruns")

        um.divider()
        um.subheader("All Fragment Statistics")

        if um.button("Refresh Stats", key="refresh_frag_stats"):
            stats = get_all_fragment_stats()
            if stats:
                um.json(stats)
            else:
                um.info("No fragments registered yet")

    # ============== CONNECTIONS TAB ==============
    with um.tab(2):
        um.subheader("Connections Module Demo")
        um.text("Manage database connections and API clients with automatic caching.")

        with um.columns(2):
            with um.column():
                with um.card():
                    um.text("**Connection Manager**", size="lg")
                    um.text("Register and manage named connections")

                    conn_name = um.input("Connection name", value="db_main", key="conn_name")

                    if um.button("Register Connection", key="reg_conn_btn"):
                        conn = MockDatabaseConnection(conn_name)
                        conn_manager.register(conn_name, conn)
                        um.session_state.connection_log.append(f"Registered: {conn_name}")
                        um.success(f"Registered connection: {conn_name}")

                    if um.button("Get Connection", key="get_conn_btn"):
                        conn = conn_manager.get(conn_name)
                        if conn:
                            um.success(f"Got connection: {conn.name}, connected: {conn.connected}")
                            info = conn_manager.get_info(conn_name)
                            um.json({
                                "name": info.name,
                                "use_count": info.use_count,
                                "is_active": info.is_active,
                                "age_seconds": round(time.time() - info.created_at, 2),
                            })
                        else:
                            um.warning(f"Connection '{conn_name}' not found")

                    if um.button("Close Connection", key="close_conn_btn"):
                        result = conn_manager.close(conn_name)
                        if result:
                            um.session_state.connection_log.append(f"Closed: {conn_name}")
                            um.success(f"Closed connection: {conn_name}")
                        else:
                            um.warning(f"Could not close '{conn_name}'")

                with um.card():
                    um.text("**Connection Pool**", size="lg")
                    um.text(f"Pool size: {db_pool.size} | Available: {db_pool.available} | In use: {db_pool.in_use}")

                    if um.button("Acquire & Query", key="pool_query_btn"):
                        with db_pool.acquire() as conn:
                            result = conn.query("SELECT * FROM users")
                            um.json(result)
                            um.info(f"Connection: {conn.name}, Queries: {conn.query_count}")

                    if um.button("Close All Pool Connections", key="close_pool_btn"):
                        db_pool.close_all()
                        um.success("All pool connections closed")

            with um.column():
                with um.card():
                    um.text("**Temp Connection**", size="lg")
                    um.text("Auto-cleanup context manager")

                    if um.button("Use Temp Connection", key="temp_conn_btn"):
                        with temp_connection(lambda: MockDatabaseConnection("temp_db")) as conn:
                            result = conn.query("SELECT NOW()")
                            um.json(result)
                            um.info(f"Temp connection: {conn.name}")
                        um.success("Temp connection auto-closed!")

                with um.card():
                    um.text("**All Connections**", size="lg")

                    if um.button("List Connections", key="list_conn_btn"):
                        connections = list_connections()
                        if connections:
                            um.text(f"Active connections: {connections}")
                        else:
                            um.info("No active connections")

                    if um.button("Get All Info", key="all_info_btn"):
                        info = get_connection_info()
                        if info:
                            um.json(info)
                        else:
                            um.info("No connection info available")

                    if um.button("Close All Connections", key="close_all_btn", variant="danger"):
                        closed = close_all_connections()
                        um.session_state.connection_log.append(f"Closed all: {closed} connections")
                        um.success(f"Closed {closed} connections")

                with um.card():
                    um.text("**Connection Log**", size="lg")
                    for entry in um.session_state.connection_log[-10:]:
                        um.text(f"- {entry}")
                    if not um.session_state.connection_log:
                        um.text("_No activity yet_")

um.divider()
um.caption(f"Umara v0.6.0 - Current time: {datetime.now().strftime('%H:%M:%S')}")
