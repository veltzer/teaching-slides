# Rust Libraries and Advanced Exercises

Error Handling, Utilities, HTTP, Web Programming, and Async

---

## Overview

- **Error Handling**: `anyhow` and `thiserror`
- **Utilities**: `serde_json`
- **HTTP Client**: `reqwest`
- **Web Programming**: `hyper`, `tower`, `axum`
- **Async Programming**: `tokio`

---
## Error Handling in Rust

`anyhow` and `thiserror`

---

## Why Error Handling Libraries?

- Rust's `Result<T, E>` is powerful but verbose
- Standard library provides basic error types
- Real applications need:
    - Better error context
    - Error chaining
    - Custom error types
    - User-friendly messages

---

## `anyhow` - Error Handling Made Easy

```toml
[dependencies]
anyhow = "1.0"
```

- Provides a single error type: `anyhow::Error`
- Great for applications (not libraries)
- Automatic error conversion
- Context adding

---

## Basic `anyhow` Usage

```rust
use anyhow::Result;

fn get_user(id: u32) -> Result<User> {
    let user = database::find_user(id)?;  // ? works with any error
    Ok(user)
}

fn main() -> Result<()> {
    let user = get_user(42)?;
    println!("Found user: {}", user.name);
    Ok(())
}
```

---

## Adding Context with `anyhow`

```rust
use anyhow::{Context, Result};

fn read_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&content)
        .context("Invalid TOML in config file")?;

    Ok(config)
}
```

---

## Creating Errors with `anyhow`

```rust
use anyhow::{anyhow, bail, ensure};

fn validate_age(age: u32) -> Result<()> {
    ensure!(age >= 18, "Must be 18 or older");

    if age > 150 {
        bail!("Invalid age: {}", age);
    }

    Ok(())
}

// Or use anyhow! macro
Err(anyhow!("Something went wrong: {}", reason))
```

---

## `thiserror` - Custom Error Types

```toml
[dependencies]
thiserror = "1.0"
```

- Derive macro for custom error types
- Perfect for libraries
- Generates `std::error::Error` implementation
- Type-safe error handling

---

## Basic `thiserror` Usage

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataError {
    #[error("data not found")]
    NotFound,

    #[error("invalid header (expected {expected:?}, found {found:?})")]
    InvalidHeader {
        expected: String,
        found: String,
    },

    #[error("unknown data error")]
    Unknown,
}
```

---

## `thiserror` with Source Errors

```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("io error")]
    Io(#[from] std::io::Error),

    #[error("validation error: {0}")]
    Validation(String),

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}
```

---

## When to Use Which?

**Use `anyhow` when:**
- Building applications
- You want simple error handling
- Error types don't matter to callers

**Use `thiserror` when:**
- Building libraries
- You need specific error types
- Callers need to match on errors
---
## JSON Processing
---
## `serde_json` Overview

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

- Part of the Serde ecosystem
- Serialize Rust structs to JSON
- Deserialize JSON to Rust structs
- Support for arbitrary JSON values

---

## Basic Serialization

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    name: String,
    age: u32,
    email: Option<String>,
}

let user = User {
    name: "Alice".to_string(),
    age: 30,
    email: Some("alice@example.com".to_string()),
};

let json = serde_json::to_string(&user)?;
// {"name":"Alice","age":30,"email":"alice@example.com"}
```

---

## Pretty Printing and Deserialization

```rust
// Pretty print
let pretty = serde_json::to_string_pretty(&user)?;

// Deserialize from string
let json_str = r#"{"name":"Bob","age":25,"email":null}"#;
let user: User = serde_json::from_str(json_str)?;

// To/from bytes
let bytes = serde_json::to_vec(&user)?;
let user: User = serde_json::from_slice(&bytes)?;
```

---

## Working with Dynamic JSON

```rust
use serde_json::{json, Value};

// Create JSON using macro
let data = json!({
    "name": "Alice",
    "age": 30,
    "phones": ["+1234567", "+9876543"]
});

// Parse arbitrary JSON
let v: Value = serde_json::from_str(r#"{"x": 1.0, "y": 2.0}"#)?;

// Access fields
println!("x = {}", v["x"]);  // x = 1.0
```

---

## Serde Attributes

```rust
#[derive(Serialize, Deserialize)]
struct Config {
    #[serde(rename = "serverPort")]
    server_port: u16,

    #[serde(default)]
    debug: bool,

    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,

    #[serde(flatten)]
    extra: HashMap<String, Value>,
}
```

---

<!-- _class: lead -->

## HTTP Client Programming

`reqwest`

---

## `reqwest` Overview

```toml
[dependencies]
reqwest = { version = "0.11", features = ["json"] }
tokio = { version = "1", features = ["full"] }
```

- High-level HTTP client
- Built on `hyper`
- Async and blocking APIs
- Automatic decompression
- Cookie support

---

## Basic GET Request

```rust
use reqwest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("https://api.github.com/users/rust-lang")
        .await?
        .text()
        .await?;

    println!("Body: {}", response);
    Ok(())
}
```

---

## JSON Responses

```rust
#[derive(Deserialize, Debug)]
struct GithubUser {
    login: String,
    id: u64,
    public_repos: u32,
}

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let user: GithubUser = reqwest::get("https://api.github.com/users/rust-lang")
        .await?
        .json()
        .await?;

    println!("User: {} has {} repos", user.login, user.public_repos);
    Ok(())
}
```

---

## POST Requests with JSON

```rust
use serde_json::json;

let client = reqwest::Client::new();
let response = client
    .post("https://httpbin.org/post")
    .json(&json!({
        "name": "Alice",
        "job": "Developer"
    }))
    .send()
    .await?;

println!("Status: {}", response.status());
```

---

## Request Builder Pattern

```rust
let client = reqwest::Client::new();
let response = client
    .get("https://api.example.com/data")
    .header("User-Agent", "My-App/0.1.0")
    .header("Authorization", "Bearer token123")
    .query(&[("page", "1"), ("limit", "10")])
    .timeout(Duration::from_secs(10))
    .send()
    .await?;
```

---

## Error Handling with reqwest

```rust
match reqwest::get("https://api.example.com/data").await {
    Ok(response) => {
        if response.status().is_success() {
            let data = response.text().await?;
            println!("Success: {}", data);
        } else {
            println!("HTTP Error: {}", response.status());
        }
    }
    Err(e) => {
        if e.is_timeout() {
            println!("Request timed out");
        } else if e.is_connect() {
            println!("Network connection failed");
        }
    }
}
```

---

<!-- _class: lead -->

## Web Server Programming

`hyper`, `tower`, and `axum`

---

## Web Framework Ecosystem

- **hyper**: Low-level HTTP implementation
- **tower**: Middleware and service abstractions
- **axum**: High-level web framework

Built in layers for maximum flexibility!

---

## `hyper` - Low Level HTTP

```rust
use hyper::{Body, Request, Response, Server};
use hyper::service::{make_service_fn, service_fn};

async fn handle(_req: Request<Body>) -> Result<Response<Body>, Infallible> {
    Ok(Response::new(Body::from("Hello, World!")))
}

#[tokio::main]
async fn main() {
    let addr = ([127, 0, 0, 1], 3000).into();
    let make_svc = make_service_fn(|_conn| async {
        Ok::<_, Infallible>(service_fn(handle))
    });

    Server::bind(&addr).serve(make_svc).await.unwrap();
}
```

---

## `tower` - Service Trait

```rust
use tower::{Service, ServiceBuilder};
use std::time::Duration;

let service = ServiceBuilder::new()
    .timeout(Duration::from_secs(30))
    .rate_limit(5, Duration::from_secs(1))
    .concurrency_limit(100)
    .service(my_service);
```

Tower provides composable middleware for:
- Rate limiting
- Timeouts
- Load balancing
- Retries

---

## `axum` - Modern Web Framework

```toml
[dependencies]
axum = "0.6"
tokio = { version = "1", features = ["full"] }
```

- Built on `hyper` and `tower`
- Type-safe routing
- Powerful extractors
- Middleware support

---

## Basic Axum Server

```rust
use axum::{Router, routing::get};

async fn hello() -> &'static str {
    "Hello, World!"
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(hello));

    let addr = "127.0.0.1:3000".parse().unwrap();
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

---

## Axum Routing

```rust
use axum::{Router, routing::{get, post}};

let app = Router::new()
    .route("/", get(index))
    .route("/users", get(list_users).post(create_user))
    .route("/users/:id", get(get_user).delete(delete_user))
    .nest("/api", api_routes())
    .fallback(not_found);
```

---

## Axum Extractors

```rust
use axum::{extract::{Path, Query, Json}, http::StatusCode};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

async fn create_user(Json(user): Json<CreateUser>) -> StatusCode {
    // Create user in database
    StatusCode::CREATED
}

async fn get_user(Path(id): Path<u32>) -> Json<User> {
    Json(User { id, name: "Alice".into() })
}
```

---

## Axum State Management

```rust
use axum::{extract::State, Router};
use std::sync::Arc;

struct AppState {
    db: sqlx::PgPool,
}

async fn handler(State(state): State<Arc<AppState>>) -> String {
    // Use state.db
    "OK".to_string()
}

let state = Arc::new(AppState { db: pool });
let app = Router::new()
    .route("/", get(handler))
    .with_state(state);
```

---

## Axum Middleware

```rust
use axum::{middleware, Router};
use tower_http::cors::CorsLayer;

async fn auth_middleware(req: Request, next: Next) -> Response {
    // Check authentication
    next.run(req).await
}

let app = Router::new()
    .route("/", get(handler))
    .layer(CorsLayer::permissive())
    .layer(middleware::from_fn(auth_middleware));
```

---
## Async Programming

`tokio`

---

## `tokio` Overview

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

- Async runtime for Rust
- Task scheduling
- Async I/O
- Timers and intervals
- Synchronization primitives

---

## Basic Tokio Usage

```rust
#[tokio::main]
async fn main() {
    println!("Hello from async main!");

    let result = do_something_async().await;
    println!("Result: {}", result);
}

async fn do_something_async() -> String {
    tokio::time::sleep(Duration::from_secs(1)).await;
    "Done!".to_string()
}
```

---

## Spawning Tasks

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // Background task
        println!("Running in background");
        42
    });

    // Do other work...

    let result = handle.await.unwrap();
    println!("Task returned: {}", result);
}
```

---

## Concurrent Tasks

```rust
use tokio::join;

async fn fetch_user() -> User { /* ... */ }
async fn fetch_posts() -> Vec<Post> { /* ... */ }

#[tokio::main]
async fn main() {
    // Run concurrently
    let (user, posts) = join!(
        fetch_user(),
        fetch_posts()
    );

    println!("User: {:?}, Posts: {}", user, posts.len());
}
```

---

## Tokio Channels

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        tx.send("Hello").await.unwrap();
        tx.send("World").await.unwrap();
    });

    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}
```

---

## File I/O with Tokio

```rust
use tokio::fs;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

async fn read_file() -> std::io::Result<String> {
    fs::read_to_string("data.txt").await
}

async fn write_file(content: &str) -> std::io::Result<()> {
    let mut file = fs::File::create("output.txt").await?;
    file.write_all(content.as_bytes()).await?;
    Ok(())
}
```

---
## Best Practices

1. **Error Handling**: Use `anyhow` for apps, `thiserror` for libraries
1. **JSON**: Always derive `Serialize`/`Deserialize` for type safety
1. **HTTP**: Use connection pooling with `reqwest::Client`
1. **Web Servers**: Start with `axum` for most applications
1. **Async**: Don't block the runtime, use `tokio::task::spawn_blocking`
