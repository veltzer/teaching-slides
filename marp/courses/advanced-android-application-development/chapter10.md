# Chapter 10: Testing and Debugging
## Building Reliable Android Applications

---

# Testing Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter10.md/0.png)

---

# Unit Testing Setup

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

# Espresso UI Testing

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

# Integration Testing

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

# Memory Leak Detection

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

# Performance Profiling

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter10.md/1.png)

---

# Debug Logging

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

# Testing Best Practices

| Category | Practice | Benefit |
|----------|----------|---------|
| Unit Tests | Test one thing | Clear failures |
| Mock Dependencies | Isolate tests | Reliable tests |
| UI Tests | Test user flows | Catch regressions |
| Integration Tests | Test components | Verify integration |

---

# Debug Build Configuration

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

# Testing Pyramid

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter10.md/2.png)

---

# Assignment Preview
## Testing Implementation

Create tests for an application:
1. Write unit tests
2. Implement UI tests
3. Add integration tests
4. Setup performance monitoring
5. Implement debug logging
6. Handle memory leaks

---

# Resources

- Android Testing Documentation
- JUnit Documentation
- Espresso Guide
- Memory Leak Detection Guide
- Performance Testing Guide
