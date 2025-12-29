# Multi-Platform Development and Modern Architecture
## Building Cross-Platform and Scalable Applications

---

## Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Multiplatform</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="145" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Kotlin</text>
  <text x="200" y="160" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">MP</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Flutter</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">React</text>
  <text x="200" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Native</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Native</text>
</svg>

---

## Kotlin Multiplatform Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("multiplatform")
    id("com.android.library")
}

kotlin {
    android()
    ios()

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1")
                implementation("io.ktor:ktor-client-core:2.3.3")
            }
        }

        val androidMain by getting {
            dependencies {
                implementation("androidx.core:core-ktx:1.12.0")
            }
        }

        val iosMain by getting
    }
}
```

---

## Shared Business Logic

```kotlin
expect class Platform {
    val name: String
}

actual class Platform actual constructor() {
    actual val name: String =
        UIDevice.currentDevice.systemName()
}

class Repository {
    private val apiClient = ApiClient()

    suspend fun getUsers(): List<User> =
        withContext(Dispatchers.Default) {
            try {
                apiClient.fetchUsers()
            } catch (e: Exception) {
                handleError(e)
                emptyList()
            }
        }
}
```

---

## Jetpack Compose UI

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        when (uiState) {
            is UiState.Loading -> LoadingIndicator()
            is UiState.Success -> UserList(
                users = (uiState as UiState.Success).users
            )
            is UiState.Error -> ErrorMessage(
                message = (uiState as UiState.Error).message
            )
        }
    }
}

@Composable
fun UserList(users: List<User>) {
    LazyColumn {
        items(users) { user ->
            UserItem(user = user)
        }
    }
}
```

---

## MVI Architecture Pattern

```kotlin
sealed class UserIntent {
    object LoadUsers : UserIntent()
    data class FilterUsers(val query: String) : UserIntent()
    data class SelectUser(val user: User) : UserIntent()
}

data class UserViewState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val selectedUser: User? = null
)

class UserViewModel : ViewModel() {
    private val _viewState = MutableStateFlow(UserViewState())
    val viewState = _viewState.asStateFlow()

    fun processIntent(intent: UserIntent) {
        when (intent) {
            is UserIntent.LoadUsers -> loadUsers()
            is UserIntent.FilterUsers -> filterUsers(intent.query)
            is UserIntent.SelectUser -> selectUser(intent.user)
        }
    }

    private fun loadUsers() = viewModelScope.launch {
        _viewState.update { it.copy(isLoading = true) }
        try {
            val users = repository.getUsers()
            _viewState.update {
                it.copy(users = users, isLoading = false)
            }
        } catch (e: Exception) {
            _viewState.update {
                it.copy(
                    error = e.message,
                    isLoading = false
                )
            }
        }
    }
}
```

---

## Cross-Platform Testing

```kotlin
class RepositoryTest {
    @Test
    fun testGetUsers() = runTest {
        val repository = Repository()
        val users = repository.getUsers()

        assertTrue(users.isNotEmpty())
        assertEquals("John", users.first().name)
    }
}

expect annotation class PlatformTest()

actual typealias PlatformTest = Test

@PlatformTest
fun testPlatformSpecific() {
    // Platform-specific test implementation
}
```

---

## Resource Sharing Strategy

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Choose Platform</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Setup Project</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Share Code</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Platform Specific</text>
  <line x1="400" y1="370" x2="400" y2="400" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="410" width="120" height="50" rx="8" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="400" y="440" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Build</text>
</svg>

---

## State Management

```kotlin
sealed class UIState<out T> {
    object Loading : UIState<Nothing>()
    data class Success<T>(val data: T) : UIState<T>()
    data class Error(val message: String) : UIState<Nothing>()
}

class StateManager<T> {
    private val _state = MutableStateFlow<UIState<T>>(UIState.Loading)
    val state = _state.asStateFlow()

    fun updateState(newState: UIState<T>) {
        _state.value = newState
    }

    fun handleError(error: Throwable) {
        _state.value = UIState.Error(error.message ?: "Unknown error")
    }
}
```

---

## Performance Considerations

| Aspect | Native | Shared | Recommendation |
|--------|--------|--------|----------------|
| UI Rendering | Platform-specific | Compose | Mix based on needs |
| Business Logic | Duplicated | Shared | Share when possible |
| Platform Features | Direct access | Limited | Use expect/actual |
| Testing | Platform-specific | Common | Share business tests |

---

## Best Practices

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Code Sharing</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="145" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Business</text>
  <text x="200" y="160" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Logic</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="145" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Data</text>
  <text x="600" y="160" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Models</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Networking</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">UI</text>
  <text x="600" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Components</text>
</svg>

---

## Assignment Preview
### Multi-Platform Implementation

Create an application that:
1. Uses Kotlin Multiplatform
1. Implements Jetpack Compose UI
1. Follows MVI architecture
1. Shares business logic
1. Implements cross-platform tests
1. Handles platform-specific features

---

## Resources

- Kotlin Multiplatform Documentation
- Jetpack Compose Guide
- MVI Architecture Guide
- Cross-Platform Testing Guide
- Performance Optimization Guide
