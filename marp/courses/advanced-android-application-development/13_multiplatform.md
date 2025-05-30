# Multi-Platform Development and Modern Architecture
## Building Cross-Platform and Scalable Applications

---

## Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter14.md/0.png)

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

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter14.md/1.png)

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

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter14.md/2.png)

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
