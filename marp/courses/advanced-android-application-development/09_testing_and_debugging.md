# Testing and Debugging
## Building Reliable Android Applications

---

## Testing Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Testing Types</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="145" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Unit</text>
  <text x="200" y="160" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Tests</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Integration</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">UI</text>
  <text x="200" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Tests</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Performance</text>
</svg>

---

## Unit Testing Setup

```java
@RunWith(MockitoJUnitRunner.class)
public class UserViewModelTest {
    @Mock
    private UserRepository repository;

    @Mock
    private SavedStateHandle savedStateHandle;

    private UserViewModel viewModel;

    @Before
    public void setup() {
        viewModel = new UserViewModel(repository, savedStateHandle);
    }

    @Test
    public void getUserData_Success() {
        // Arrange
        User testUser = new User("1", "John Doe");
        when(repository.getUser("1"))
            .thenReturn(Single.just(testUser));

        // Act
        viewModel.loadUser("1");

        // Assert
        verify(repository).getUser("1");
        assertEquals(testUser,
            viewModel.getUserLiveData().getValue());
    }

    @Test
    public void getUserData_Error() {
        // Arrange
        Exception error = new Exception("Network error");
        when(repository.getUser("1"))
            .thenReturn(Single.error(error));

        // Act
        viewModel.loadUser("1");

        // Assert
        verify(repository).getUser("1");
        assertEquals(error.getMessage(),
            viewModel.getErrorLiveData().getValue());
    }
}
```

---

## Espresso UI Testing

```java
@RunWith(AndroidJUnit4.class)
public class LoginActivityTest {
    @Rule
    public ActivityScenarioRule<LoginActivity> activityRule =
        new ActivityScenarioRule<>(LoginActivity.class);

    @Test
    public void loginButton_ClickWithValidInput_NavigatesToMain() {
        // Enter email
        onView(withId(R.id.email_input))
            .perform(typeText("test@example.com"));

        // Enter password
        onView(withId(R.id.password_input))
            .perform(typeText("password123"));

        // Close keyboard
        closeSoftKeyboard();

        // Click login button
        onView(withId(R.id.login_button))
            .perform(click());

        // Verify navigation to main activity
        onView(withId(R.id.main_container))
            .check(matches(isDisplayed()));
    }

    @Test
    public void loginButton_ClickWithInvalidInput_ShowsError() {
        // Enter invalid email
        onView(withId(R.id.email_input))
            .perform(typeText("invalid-email"));

        // Close keyboard
        closeSoftKeyboard();

        // Click login button
        onView(withId(R.id.login_button))
            .perform(click());

        // Verify error message
        onView(withId(R.id.error_text))
            .check(matches(withText(R.string.invalid_email)));
    }
}
```

---

## Integration Testing

```java
@RunWith(AndroidJUnit4.class)
public class UserRepositoryTest {
    private UserDatabase database;
    private UserRepository repository;
    private ApiService apiService;

    @Before
    public void setup() {
        Context context = ApplicationProvider.getApplicationContext();
        database = Room.inMemoryDatabaseBuilder(
            context,
            UserDatabase.class
        ).build();

        apiService = mock(ApiService.class);
        repository = new UserRepository(database, apiService);
    }

    @Test
    public void getUser_CacheAndNetwork() {
        // Setup test data
        User localUser = new User("1", "Local User");
        User remoteUser = new User("1", "Remote User");

        // Insert local data
        database.userDao().insert(localUser);

        // Mock network response
        when(apiService.getUser("1"))
            .thenReturn(Single.just(remoteUser));

        // Test repository
        TestObserver<User> testObserver =
            repository.getUser("1").test();

        // Verify emissions
        testObserver.assertValues(localUser, remoteUser);
    }
}
```

---

## Memory Leak Detection

```java
public class LeakDetectionApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();

        if (BuildConfig.DEBUG) {
            LeakCanary.install(this);
        }
    }
}

public class MainActivity extends AppCompatActivity {
    private static Context leakyContext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Memory leak - storing activity context
        leakyContext = this;
    }

    // Fix: Clear reference in onDestroy
    @Override
    protected void onDestroy() {
        super.onDestroy();
        leakyContext = null;
    }
}
```

---

## Performance Profiling

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Write Test</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Run Test</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Check Results</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Fix Issues</text>
  <line x1="400" y1="370" x2="400" y2="400" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="410" width="120" height="50" rx="8" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="400" y="440" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Repeat</text>
</svg>

---

## Debug Logging

```java
public class DebugLogger {
    private static final String TAG = "AppDebug";

    public static void log(String message) {
        if (BuildConfig.DEBUG) {
            Log.d(TAG, message);
        }
    }

    public static void logMethod() {
        if (BuildConfig.DEBUG) {
            StackTraceElement[] stackTrace =
                Thread.currentThread().getStackTrace();
            Log.d(TAG, "Method: " +
                stackTrace[3].getMethodName());
        }
    }

    public static void logError(String message, Throwable e) {
        if (BuildConfig.DEBUG) {
            Log.e(TAG, message, e);
        }
    }
}
```

---

## Testing Best Practices

| Category | Practice | Benefit |
|----------|----------|---------|
| Unit Tests | Test one thing | Clear failures |
| Mock Dependencies | Isolate tests | Reliable tests |
| UI Tests | Test user flows | Catch regressions |
| Integration Tests | Test components | Verify integration |

---

## Debug Build Configuration

```groovy
android {
    buildTypes {
        debug {
            debuggable true
            minifyEnabled false
            shrinkResources false
            buildConfigField "boolean", "ENABLE_LOGGING", "true"
            buildConfigField "String", "API_URL", "\"http://dev-api.example.com\""
        }

        release {
            debuggable false
            minifyEnabled true
            shrinkResources true
            buildConfigField "boolean", "ENABLE_LOGGING", "false"
            buildConfigField "String", "API_URL", "\"https://api.example.com\""
        }
    }
}
```

---

## Testing Pyramid

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Debugging Tools</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Logcat</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Debugger</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Profiler</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Inspector</text>
</svg>

---

## Assignment Preview
### Testing Implementation

Create tests for an application:
1. Write unit tests
1. Implement UI tests
1. Add integration tests
1. Setup performance monitoring
1. Implement debug logging
1. Handle memory leaks

---

## Resources

- Android Testing Documentation
- JUnit Documentation
- Espresso Guide
- Memory Leak Detection Guide
- Performance Testing Guide
