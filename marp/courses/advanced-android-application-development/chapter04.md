# Chapter 4: Architecture Patterns
## Building Scalable Android Applications

---

## MVVM Architecture Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter4.md/0.png)

---

## MVVM Components

| Component | Responsibility | Example Classes |
|-----------|----------------|-----------------|
| View | UI Elements | Activity, Fragment |
| ViewModel | UI Logic & State | AndroidViewModel |
| Model | Data & Business Logic | Repository, DataSource |
| LiveData | Data Observation | MutableLiveData |

---

## ViewModel Implementation

```java
public class UserViewModel extends AndroidViewModel {
    private final MutableLiveData<User> userLiveData;
    private final UserRepository repository;

    public UserViewModel(Application application) {
        super(application);
        repository = new UserRepository(application);
        userLiveData = new MutableLiveData<>();
    }

    public LiveData<User> getUser() {
        return userLiveData;
    }

    public void loadUser(String userId) {
        repository.getUser(userId)
                 .subscribeOn(Schedulers.io())
                 .observeOn(AndroidSchedulers.mainThread())
                 .subscribe(user -> userLiveData.setValue(user));
    }
}
```

---

## Clean Architecture Layers

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter4.md/1.png)

---

## Repository Pattern

```java
public class UserRepository {
    private final UserLocalDataSource localDataSource;
    private final UserRemoteDataSource remoteDataSource;

    public Observable<User> getUser(String userId) {
        return Observable.concat(
            localDataSource.getUser(userId),
            remoteDataSource.getUser(userId)
                .doOnNext(user -> localDataSource.saveUser(user))
        ).firstElement().toObservable();
    }
}
```

---

## Dependency Injection with Dagger

```java
@Module
public class AppModule {
    @Provides
    @Singleton
    UserRepository provideUserRepository(
        UserLocalDataSource local,
        UserRemoteDataSource remote
    ) {
        return new UserRepository(local, remote);
    }
}

@Component(modules = {AppModule.class})
@Singleton
public interface AppComponent {
    void inject(MainActivity activity);
    void inject(UserFragment fragment);
}
```

---

## Use Case Implementation

```java
public class GetUserUseCase {
    private final UserRepository repository;

    @Inject
    public GetUserUseCase(UserRepository repository) {
        this.repository = repository;
    }

    public Observable<User> execute(String userId) {
        return repository.getUser(userId)
                        .map(this::transformUser)
                        .subscribeOn(Schedulers.io())
                        .observeOn(AndroidSchedulers.mainThread());
    }

    private User transformUser(User user) {
        // Apply business logic transformations
        return user;
    }
}
```

---

## Event Handling Pattern

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter4.md/2.png)

```java
public class UserEvents {
    public static class LoadUser {
        public final String userId;
        public LoadUser(String userId) {
            this.userId = userId;
        }
    }

    public static class UpdateUser {
        public final User user;
        public UpdateUser(User user) {
            this.user = user;
        }
    }
}
```

---

## State Management

```java
public class UserState {
    private final User user;
    private final boolean isLoading;
    private final String error;

    public UserState(User user, boolean isLoading, String error) {
        this.user = user;
        this.isLoading = isLoading;
        this.error = error;
    }

    // Getters and builder pattern
}
```

---

## Activity Implementation

```java
public class UserActivity extends AppCompatActivity {
    @Inject
    UserViewModel viewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user);
        
        // Inject dependencies
        ((App) getApplication()).getAppComponent().inject(this);
        
        // Observe ViewModel
        viewModel.getUser().observe(this, this::updateUI);
        
        // Handle events
        buttonLoad.setOnClickListener(v -> 
            viewModel.dispatch(new LoadUser("123"))
        );
    }
}
```

---

## Testing Architecture Components

```java
@RunWith(JUnit4.class)
public class UserViewModelTest {
    @Rule
    public InstantTaskExecutorRule instantTaskExecutorRule = 
        new InstantTaskExecutorRule();

    @Mock
    private UserRepository repository;
    
    private UserViewModel viewModel;

    @Test
    public void loadUser_Success() {
        // Given
        User user = new User("123", "John");
        when(repository.getUser("123"))
            .thenReturn(Observable.just(user));

        // When
        viewModel.loadUser("123");

        // Then
        verify(repository).getUser("123");
        assertEquals(user, viewModel.getUser().getValue());
    }
}
```

---

## Best Practices

![3](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter4.md/3.png)

---

## Assignment Preview
### Refactor Application

Tasks:
1. Implement MVVM architecture
1. Add Clean Architecture layers
1. Set up Dagger DI
1. Write unit tests
1. Implement state management

---

## Resources

- Android Architecture Components
- Dagger Documentation
- Clean Architecture Book
- Sample Code Repository
- Testing Guidelines
