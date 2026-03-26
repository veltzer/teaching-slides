# Architecture Patterns
## Building Scalable Android Applications

---

## MVVM Architecture Overview

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <!-- View component -->
  <rect x="50" y="100" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="130" text-anchor="middle" font-size="14" font-weight="bold">View</text>

  <!-- ViewModel component -->
  <rect x="250" y="100" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="130" text-anchor="middle" font-size="14" font-weight="bold">ViewModel</text>

  <!-- Model component -->
  <rect x="450" y="100" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="130" text-anchor="middle" font-size="14" font-weight="bold">Model</text>

  <!-- Bidirectional arrows between components -->
  <line x1="150" y1="125" x2="250" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow_mvvm)"/>
  <line x1="250" y1="135" x2="150" y2="135" stroke="#333" stroke-width="2" marker-end="url(#arrow_mvvm)"/>

  <line x1="350" y1="125" x2="450" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow_mvvm)"/>
  <line x1="450" y1="135" x2="350" y2="135" stroke="#333" stroke-width="2" marker-end="url(#arrow_mvvm)"/>

  <!-- Observes relationship -->
  <path d="M 100 100 Q 100 60, 300 60 Q 300 80, 300 100" stroke="#4c9aff" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow_mvvm)"/>
  <text x="200" y="55" text-anchor="middle" font-size="11" fill="#4c9aff">Observes</text>

  <!-- Updates relationship -->
  <path d="M 300 150 Q 300 180, 500 180 Q 500 170, 500 150" stroke="#ff6b6b" stroke-width="2" fill="none" marker-end="url(#arrow_mvvm)"/>
  <text x="400" y="195" text-anchor="middle" font-size="11" fill="#ff6b6b">Updates</text>

  <!-- Notifies relationship -->
  <path d="M 500 100 Q 500 40, 300 40 Q 300 60, 300 100" stroke="#51cf66" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow_mvvm)"/>
  <text x="400" y="35" text-anchor="middle" font-size="11" fill="#51cf66">Notifies</text>

  <defs>
    <marker id="arrow_mvvm" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="450" xmlns="http://www.w3.org/2000/svg">
  <!-- Main layers -->
  <rect x="150" y="30" width="300" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="65" text-anchor="middle" font-size="14" font-weight="bold">Presentation Layer</text>

  <rect x="150" y="120" width="300" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="155" text-anchor="middle" font-size="14" font-weight="bold">Domain Layer</text>

  <rect x="150" y="210" width="300" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="245" text-anchor="middle" font-size="14" font-weight="bold">Data Layer</text>

  <rect x="150" y="300" width="300" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="335" text-anchor="middle" font-size="14" font-weight="bold">Framework</text>

  <!-- Layer connections -->
  <line x1="300" y1="90" x2="300" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow_clean)"/>
  <line x1="300" y1="180" x2="300" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow_clean)"/>
  <line x1="300" y1="270" x2="300" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow_clean)"/>

  <!-- Presentation sublayers -->
  <rect x="20" y="40" width="110" height="35" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="55" text-anchor="middle" font-size="11">Activities/Fragments</text>
  <text x="75" y="68" text-anchor="middle" font-size="10">UI</text>

  <rect x="470" y="40" width="100" height="35" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="520" y="55" text-anchor="middle" font-size="11">ViewModels</text>
  <text x="520" y="68" text-anchor="middle" font-size="10">Presenters</text>

  <!-- Domain sublayers -->
  <rect x="20" y="130" width="110" height="35" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="145" text-anchor="middle" font-size="11">Use Cases</text>
  <text x="75" y="158" text-anchor="middle" font-size="10">Business Logic</text>

  <rect x="470" y="130" width="100" height="35" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="520" y="145" text-anchor="middle" font-size="11">Entities</text>
  <text x="520" y="158" text-anchor="middle" font-size="10">Domain Models</text>

  <!-- Data sublayers -->
  <rect x="20" y="220" width="110" height="35" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="235" text-anchor="middle" font-size="11">Repositories</text>
  <text x="75" y="248" text-anchor="middle" font-size="10">Data Sources</text>

  <rect x="470" y="220" width="100" height="35" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="520" y="235" text-anchor="middle" font-size="11">Models</text>
  <text x="520" y="248" text-anchor="middle" font-size="10">DTOs</text>

  <!-- Framework sublayers -->
  <rect x="20" y="310" width="110" height="35" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="325" text-anchor="middle" font-size="11">Android Framework</text>
  <text x="75" y="338" text-anchor="middle" font-size="10">System APIs</text>

  <rect x="470" y="310" width="100" height="35" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="520" y="325" text-anchor="middle" font-size="11">External Libraries</text>
  <text x="520" y="338" text-anchor="middle" font-size="10">Third Party</text>

  <!-- Connections to sublayers -->
  <line x1="150" y1="60" x2="130" y2="57" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>
  <line x1="450" y1="60" x2="470" y2="57" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>

  <line x1="150" y1="150" x2="130" y2="147" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>
  <line x1="450" y1="150" x2="470" y2="147" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>

  <line x1="150" y1="240" x2="130" y2="237" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>
  <line x1="450" y1="240" x2="470" y2="237" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>

  <line x1="150" y1="330" x2="130" y2="327" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>
  <line x1="450" y1="330" x2="470" y2="327" stroke="#666" stroke-width="1" marker-end="url(#arrow_clean)"/>

  <defs>
    <marker id="arrow_clean" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- View -->
  <rect x="50" y="75" width="80" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="105" text-anchor="middle" font-size="14" font-weight="bold">View</text>

  <!-- ViewModel -->
  <rect x="200" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="105" text-anchor="middle" font-size="14" font-weight="bold">ViewModel</text>

  <!-- UseCase -->
  <rect x="370" y="75" width="80" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="105" text-anchor="middle" font-size="14" font-weight="bold">UseCase</text>

  <!-- View back to itself for State update -->
  <rect x="500" y="75" width="80" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="105" text-anchor="middle" font-size="14" font-weight="bold">View</text>

  <!-- Event flow -->
  <line x1="130" y1="100" x2="200" y2="100" stroke="#4c9aff" stroke-width="2" marker-end="url(#arrow_event)"/>
  <text x="165" y="95" text-anchor="middle" font-size="11" fill="#4c9aff">Event</text>

  <!-- Command flow -->
  <line x1="300" y1="100" x2="370" y2="100" stroke="#ff6b6b" stroke-width="2" marker-end="url(#arrow_event)"/>
  <text x="335" y="95" text-anchor="middle" font-size="11" fill="#ff6b6b">Command</text>

  <!-- Result flow back -->
  <path d="M 410 125 Q 410 150, 250 150 Q 250 140, 250 125" stroke="#51cf66" stroke-width="2" fill="none" marker-end="url(#arrow_event)"/>
  <text x="330" y="165" text-anchor="middle" font-size="11" fill="#51cf66">Result</text>

  <!-- State flow -->
  <path d="M 250 75 Q 250 40, 540 40 Q 540 60, 540 75" stroke="#ffa726" stroke-width="2" fill="none" marker-end="url(#arrow_event)"/>
  <text x="395" y="35" text-anchor="middle" font-size="11" fill="#ffa726">State</text>

  <defs>
    <marker id="arrow_event" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Central Architecture node -->
  <ellipse cx="300" cy="200" rx="80" ry="40" fill="#673ab7" stroke="#333" stroke-width="3"/>
  <text x="300" y="205" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Architecture</text>

  <!-- Separation of Concerns branch -->
  <ellipse cx="150" cy="100" rx="90" ry="35" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="95" text-anchor="middle" font-size="12" font-weight="bold">Separation of</text>
  <text x="150" y="110" text-anchor="middle" font-size="12" font-weight="bold">Concerns</text>

  <!-- Dependency Injection branch -->
  <ellipse cx="450" cy="100" rx="85" ry="35" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="450" y="95" text-anchor="middle" font-size="12" font-weight="bold">Dependency</text>
  <text x="450" y="110" text-anchor="middle" font-size="12" font-weight="bold">Injection</text>

  <!-- Testing branch -->
  <ellipse cx="150" cy="300" rx="60" ry="35" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="305" text-anchor="middle" font-size="12" font-weight="bold">Testing</text>

  <!-- Error Handling branch -->
  <ellipse cx="450" cy="300" rx="75" ry="35" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="450" y="295" text-anchor="middle" font-size="12" font-weight="bold">Error</text>
  <text x="450" y="310" text-anchor="middle" font-size="12" font-weight="bold">Handling</text>

  <!-- Separation of Concerns sub-items -->
  <rect x="10" y="30" width="120" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="70" y="47" text-anchor="middle" font-size="10">UI Logic in ViewModel</text>

  <rect x="10" y="60" width="130" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="77" text-anchor="middle" font-size="10">Business Logic in UseCases</text>

  <rect x="10" y="120" width="125" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="72" y="137" text-anchor="middle" font-size="10">Data Logic in Repository</text>

  <!-- Dependency Injection sub-items -->
  <rect x="490" y="30" width="90" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="47" text-anchor="middle" font-size="10">Dagger Setup</text>

  <rect x="470" y="60" width="110" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="525" y="77" text-anchor="middle" font-size="10">Module Organization</text>

  <rect x="480" y="120" width="100" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="530" y="137" text-anchor="middle" font-size="10">Scope Management</text>

  <!-- Testing sub-items -->
  <rect x="30" y="250" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="267" text-anchor="middle" font-size="10">Unit Tests</text>

  <rect x="20" y="280" width="90" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="297" text-anchor="middle" font-size="10">Integration Tests</text>

  <rect x="30" y="330" width="60" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="60" y="347" text-anchor="middle" font-size="10">UI Tests</text>

  <!-- Error Handling sub-items -->
  <rect x="490" y="250" width="80" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="530" y="267" text-anchor="middle" font-size="10">Error States</text>

  <rect x="470" y="330" width="110" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="525" y="347" text-anchor="middle" font-size="10">Recovery Strategies</text>

  <!-- Connection lines -->
  <line x1="240" y1="180" x2="190" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="180" x2="410" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="240" y1="220" x2="190" y2="275" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="220" x2="410" y2="275" stroke="#333" stroke-width="2"/>

  <!-- Sub-connections -->
  <line x1="90" y1="85" x2="70" y2="55" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="95" x2="75" y2="85" stroke="#666" stroke-width="1"/>
  <line x1="90" y1="115" x2="72" y2="120" stroke="#666" stroke-width="1"/>

  <line x1="490" y1="85" x2="535" y2="55" stroke="#666" stroke-width="1"/>
  <line x1="480" y1="95" x2="525" y2="85" stroke="#666" stroke-width="1"/>
  <line x1="490" y1="115" x2="530" y2="120" stroke="#666" stroke-width="1"/>

  <line x1="110" y1="285" x2="65" y2="275" stroke="#666" stroke-width="1"/>
  <line x1="110" y1="300" x2="65" y2="305" stroke="#666" stroke-width="1"/>
  <line x1="110" y1="315" x2="60" y2="330" stroke="#666" stroke-width="1"/>

  <line x1="490" y1="285" x2="530" y2="275" stroke="#666" stroke-width="1"/>
  <line x1="490" y1="315" x2="525" y2="330" stroke="#666" stroke-width="1"/>
</svg>

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
