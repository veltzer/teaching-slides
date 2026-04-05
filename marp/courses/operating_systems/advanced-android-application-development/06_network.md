# Network Operations
## Building Robust Networked Applications

---

## Network Architecture Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Android App -->
  <rect x="350" y="30" width="100" height="50" rx="8" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="400" y="60" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Android App</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrowNet" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- To Network Layer -->
  <line x1="400" y1="80" x2="400" y2="120" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>

  <!-- Network Layer -->
  <rect x="350" y="130" width="100" height="50" rx="8" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="400" y="160" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Network Layer</text>

  <!-- To Retrofit Client -->
  <line x1="400" y1="180" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>

  <!-- Retrofit Client -->
  <rect x="350" y="230" width="100" height="50" rx="8" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Retrofit Client</text>

  <!-- To OkHttp Client -->
  <line x1="400" y1="280" x2="400" y2="320" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>

  <!-- OkHttp Client -->
  <rect x="350" y="330" width="100" height="50" rx="8" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="400" y="360" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">OkHttp Client</text>

  <!-- To Internet -->
  <line x1="400" y1="380" x2="400" y2="420" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>

  <!-- Internet -->
  <ellipse cx="400" cy="460" rx="60" ry="30" fill="#00BCD4" stroke="#006064" stroke-width="2"/>
  <text x="400" y="465" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Internet</text>

  <!-- WebSocket branch -->
  <line x1="350" y1="155" x2="250" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>
  <rect x="150" y="130" width="90" height="50" rx="8" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="195" y="160" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">WebSocket</text>

  <!-- Image Loading branch -->
  <line x1="450" y1="155" x2="550" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>
  <rect x="560" y="130" width="100" height="50" rx="8" fill="#795548" stroke="#4E342E" stroke-width="2"/>
  <text x="610" y="160" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Image Loading</text>

  <!-- To Interceptors -->
  <line x1="350" y1="355" x2="250" y2="355" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>

  <!-- Interceptors -->
  <rect x="150" y="330" width="90" height="50" rx="8" fill="#607D8B" stroke="#37474F" stroke-width="2"/>
  <text x="195" y="360" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Interceptors</text>

  <!-- Authentication -->
  <line x1="150" y1="355" x2="80" y2="300" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>
  <rect x="20" y="270" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="70" y="295" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Authentication</text>

  <!-- Caching -->
  <line x1="150" y1="380" x2="80" y2="420" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>
  <rect x="20" y="410" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="70" y="435" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Caching</text>

  <!-- Logging -->
  <line x1="195" y1="380" x2="195" y2="470" stroke="#666" stroke-width="2" marker-end="url(#arrowNet)"/>
  <rect x="145" y="480" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="195" y="505" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Logging</text>
</svg>

---

## Retrofit Setup

```java
public interface ApiService {
    @GET("users/{id}")
    Call<User> getUser(@Path("id") String userId);

    @POST("users")
    Call<User> createUser(@Body User user);

    @PUT("users/{id}")
    Call<User> updateUser(
        @Path("id") String userId,
        @Body User user
    );

    @DELETE("users/{id}")
    Call<Void> deleteUser(@Path("id") String userId);
}

public class NetworkModule {
    private static final String BASE_URL =
        "https://api.example.com/";

    public static ApiService createApiService() {
        return new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .client(createOkHttpClient())
            .build()
            .create(ApiService.class);
    }
}
```

---

## OkHttp Configuration

```java
private static OkHttpClient createOkHttpClient() {
    HttpLoggingInterceptor logging =
        new HttpLoggingInterceptor();
    logging.setLevel(HttpLoggingInterceptor.Level.BODY);

    return new OkHttpClient.Builder()
        .addInterceptor(logging)
        .addInterceptor(new AuthInterceptor())
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .cache(new Cache(cacheDir, cacheSize))
        .build();
}

public class AuthInterceptor implements Interceptor {
    @Override
    public Response intercept(Chain chain) throws IOException {
        Request original = chain.request();
        Request.Builder builder = original.newBuilder()
            .header("Authorization", "Bearer " + getToken())
            .method(original.method(), original.body());

        return chain.proceed(builder.build());
    }
}
```

---

## API Response Handling

```java
public class NetworkResult<T> {
    private T data;
    private String error;
    private boolean isLoading;

    // Success constructor
    public NetworkResult(T data) {
        this.data = data;
        this.error = null;
        this.isLoading = false;
    }

    // Error constructor
    public NetworkResult(String error) {
        this.data = null;
        this.error = error;
        this.isLoading = false;
    }

    // Loading constructor
    public NetworkResult() {
        this.data = null;
        this.error = null;
        this.isLoading = true;
    }
}
```

---

## Repository Implementation

```java
public class UserRepository {
    private final ApiService apiService;
    private final UserDao userDao;

    public LiveData<NetworkResult<User>> getUser(String userId) {
        MutableLiveData<NetworkResult<User>> result =
            new MutableLiveData<>();

        result.setValue(new NetworkResult<>()); // Loading

        apiService.getUser(userId).enqueue(
            new Callback<User>() {
                @Override
                public void onResponse(
                        Call<User> call,
                        Response<User> response) {
                    if (response.isSuccessful()) {
                        result.setValue(
                            new NetworkResult<>(response.body())
                        );
                        // Cache user
                        userDao.insertUser(response.body());
                    } else {
                        result.setValue(
                            new NetworkResult<>("Error: " +
                                response.code())
                        );
                    }
                }

                @Override
                public void onFailure(Call<User> call, Throwable t) {
                    result.setValue(
                        new NetworkResult<>("Network error: " +
                            t.getMessage())
                    );
                }
            }
        );

        return result;
    }
}
```

---

## WebSocket Implementation

```java
public class WebSocketManager {
    private WebSocket webSocket;
    private final OkHttpClient client;

    public void connect(String url) {
        Request request = new Request.Builder()
            .url(url)
            .build();

        WebSocketListener listener = new WebSocketListener() {
            @Override
            public void onMessage(
                    WebSocket webSocket,
                    String text) {
                handleMessage(text);
            }

            @Override
            public void onFailure(
                    WebSocket webSocket,
                    Throwable t,
                    Response response) {
                handleFailure(t);
            }
        };

        webSocket = client.newWebSocket(request, listener);
    }

    public void sendMessage(String message) {
        webSocket.send(message);
    }
}
```

---

## Image Loading with Glide

```java
public class ImageLoader {
    public static void loadImage(
            ImageView imageView,
            String url) {
        Glide.with(imageView.getContext())
            .load(url)
            .transition(DrawableTransitionOptions.withCrossFade())
            .transform(new CenterCrop(), new RoundedCorners(8))
            .placeholder(R.drawable.placeholder)
            .error(R.drawable.error)
            .into(imageView);
    }

    public static void loadImageWithCache(
            ImageView imageView,
            String url) {
        Glide.with(imageView.getContext())
            .load(url)
            .diskCacheStrategy(DiskCacheStrategy.ALL)
            .priority(Priority.HIGH)
            .into(imageView);
    }
}
```

---

## Error Handling

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Network Request -->
  <rect x="50" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="110" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Network Request</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrowErr" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- To Success? -->
  <line x1="110" y1="100" x2="110" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>

  <!-- Success Decision -->
  <path d="M 110 160 L 160 190 L 110 220 L 60 190 Z" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="110" y="195" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Success?</text>

  <!-- Yes branch -->
  <line x1="160" y1="190" x2="250" y2="190" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <text x="205" y="180" font-family="Arial, sans-serif" font-size="12" fill="#4CAF50">Yes</text>

  <!-- Parse Response -->
  <rect x="260" y="165" width="110" height="50" rx="8" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="315" y="195" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Parse Response</text>

  <!-- To Valid Data? -->
  <line x1="315" y1="215" x2="315" y2="270" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>

  <!-- Valid Data Decision -->
  <path d="M 315 280 L 365 310 L 315 340 L 265 310 Z" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="315" y="315" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Valid Data?</text>

  <!-- Yes to Update UI -->
  <line x1="365" y1="310" x2="450" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <text x="405" y="300" font-family="Arial, sans-serif" font-size="12" fill="#4CAF50">Yes</text>

  <!-- Update UI -->
  <rect x="460" y="285" width="100" height="50" rx="8" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="510" y="315" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Update UI</text>

  <!-- No to Show Error -->
  <line x1="315" y1="340" x2="315" y2="400" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <text x="330" y="370" font-family="Arial, sans-serif" font-size="12" fill="#F44336">No</text>

  <!-- Show Error -->
  <rect x="260" y="410" width="110" height="50" rx="8" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="315" y="440" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Show Error</text>

  <!-- No branch to Handle Error -->
  <line x1="60" y1="190" x2="-30" y2="190" stroke="#666" stroke-width="2"/>
  <line x1="-30" y1="190" x2="-30" y2="310" stroke="#666" stroke-width="2"/>
  <line x1="-30" y1="310" x2="50" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <text x="10" y="180" font-family="Arial, sans-serif" font-size="12" fill="#F44336">No</text>

  <!-- Handle Error -->
  <rect x="60" y="285" width="100" height="50" rx="8" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="110" y="315" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Handle Error</text>

  <!-- To Check Error Type -->
  <line x1="110" y1="335" x2="110" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>

  <!-- Check Error Type -->
  <rect x="50" y="390" width="120" height="50" rx="8" fill="#795548" stroke="#4E342E" stroke-width="2"/>
  <text x="110" y="420" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Check Error Type</text>

  <!-- Network Error -->
  <line x1="50" y1="440" x2="20" y2="490" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <rect x="-40" y="500" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="10" y="525" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Network Error</text>

  <!-- Server Error -->
  <line x1="110" y1="440" x2="110" y2="490" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <rect x="60" y="500" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="110" y="525" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Server Error</text>

  <!-- Auth Error -->
  <line x1="170" y1="440" x2="200" y2="490" stroke="#666" stroke-width="2" marker-end="url(#arrowErr)"/>
  <rect x="160" y="500" width="100" height="40" rx="6" fill="#FFC107" stroke="#F57C00" stroke-width="1"/>
  <text x="210" y="525" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Auth Error</text>
</svg>

---

## Network Security

```java
public class NetworkSecurity {
    private static final String CERTIFICATE_HASH = "sha256/...";

    public static OkHttpClient createSecureClient() {
        return new OkHttpClient.Builder()
            .certificatePinner(new CertificatePinner.Builder()
                .add("api.example.com", CERTIFICATE_HASH)
                .build())
            .connectionSpecs(Arrays.asList(
                ConnectionSpec.MODERN_TLS,
                ConnectionSpec.COMPATIBLE_TLS))
            .build();
    }
}
```

---

## Caching Strategy

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Request -->
  <rect x="50" y="250" width="80" height="50" rx="8" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="90" y="280" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Request</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrowCache" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- To Cache Valid? -->
  <line x1="130" y1="275" x2="200" y2="275" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>

  <!-- Cache Valid Decision -->
  <path d="M 250 250 L 300 275 L 250 300 L 200 275 Z" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="250" y="275" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="white">Cache</text>
  <text x="250" y="290" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="white">Valid?</text>

  <!-- Yes branch to Use Cache -->
  <line x1="250" y1="250" x2="250" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>
  <text x="270" y="215" font-family="Arial, sans-serif" font-size="12" fill="#4CAF50">Yes</text>

  <!-- Use Cache -->
  <rect x="200" y="130" width="100" height="50" rx="8" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="250" y="160" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Use Cache</text>

  <!-- No branch to Network Request -->
  <line x1="300" y1="275" x2="380" y2="275" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>
  <text x="340" y="265" font-family="Arial, sans-serif" font-size="12" fill="#F44336">No</text>

  <!-- Network Request -->
  <rect x="390" y="250" width="120" height="50" rx="8" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="450" y="280" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Network Request</text>

  <!-- To Success? -->
  <line x1="510" y1="275" x2="580" y2="275" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>

  <!-- Success Decision -->
  <path d="M 630 250 L 680 275 L 630 300 L 580 275 Z" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="630" y="280" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="white">Success?</text>

  <!-- Yes to Update Cache -->
  <line x1="630" y1="250" x2="630" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>
  <text x="650" y="215" font-family="Arial, sans-serif" font-size="12" fill="#4CAF50">Yes</text>

  <!-- Update Cache -->
  <rect x="575" y="130" width="110" height="50" rx="8" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="630" y="160" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Update Cache</text>

  <!-- No to Use Stale Cache -->
  <line x1="630" y1="300" x2="630" y2="370" stroke="#666" stroke-width="2" marker-end="url(#arrowCache)"/>
  <text x="650" y="335" font-family="Arial, sans-serif" font-size="12" fill="#F44336">No</text>

  <!-- Use Stale Cache -->
  <rect x="570" y="380" width="120" height="50" rx="8" fill="#795548" stroke="#4E342E" stroke-width="2"/>
  <text x="630" y="410" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Use Stale Cache</text>
</svg>

---

## Network Performance Optimization

| Technique | Implementation | Benefit |
|-----------|---------------|----------|
| Response Caching | OkHttp Cache | Reduces requests |
| Image Caching | Glide disk cache | Faster loading |
| Connection Pooling | OkHttp pool | Resource reuse |
| Compression | GZIP | Reduced data usage |

---

## Best Practices

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Central node -->
  <circle cx="400" cy="300" r="80" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="295" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Network Best</text>
  <text x="400" y="315" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Practices</text>

  <!-- Security branch -->
  <line x1="320" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="50" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Security</text>

  <!-- Security sub-branches -->
  <line x1="150" y1="120" x2="80" y2="80" stroke="#999" stroke-width="1"/>
  <rect x="30" y="60" width="100" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="80" y="80" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">SSL Pinning</text>

  <line x1="150" y1="150" x2="80" y2="150" stroke="#999" stroke-width="1"/>
  <rect x="20" y="135" width="110" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="75" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Token Management</text>

  <line x1="150" y1="180" x2="80" y2="220" stroke="#999" stroke-width="1"/>
  <rect x="25" y="205" width="105" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="77" y="225" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Data Encryption</text>

  <!-- Performance branch -->
  <line x1="480" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="50" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Performance</text>

  <!-- Performance sub-branches -->
  <line x1="650" y1="120" x2="720" y2="80" stroke="#999" stroke-width="1"/>
  <rect x="680" y="60" width="80" height="30" rx="5" fill="#FFF3E0" stroke="#F57C00"/>
  <text x="720" y="80" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Caching</text>

  <line x1="650" y1="150" x2="720" y2="150" stroke="#999" stroke-width="1"/>
  <rect x="670" y="135" width="90" height="30" rx="5" fill="#FFF3E0" stroke="#F57C00"/>
  <text x="715" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Compression</text>

  <line x1="650" y1="180" x2="720" y2="220" stroke="#999" stroke-width="1"/>
  <rect x="670" y="205" width="100" height="30" rx="5" fill="#FFF3E0" stroke="#F57C00"/>
  <text x="720" y="225" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Batch Requests</text>

  <!-- Error Handling branch -->
  <line x1="400" y1="380" x2="400" y2="480" stroke="#666" stroke-width="2"/>
  <circle cx="400" cy="500" r="50" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="400" y="495" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Error</text>
  <text x="400" y="510" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Handling</text>

  <!-- Error Handling sub-branches -->
  <line x1="350" y1="520" x2="280" y2="540" stroke="#999" stroke-width="1"/>
  <rect x="230" y="530" width="80" height="30" rx="5" fill="#F3E5F5" stroke="#7B1FA2"/>
  <text x="270" y="550" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Retry Logic</text>

  <line x1="400" y1="550" x2="400" y2="580" stroke="#999" stroke-width="1"/>
  <rect x="340" y="580" width="120" height="30" rx="5" fill="#F3E5F5" stroke="#7B1FA2"/>
  <text x="400" y="600" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Fallback Strategy</text>

  <line x1="450" y1="520" x2="520" y2="540" stroke="#999" stroke-width="1"/>
  <rect x="490" y="530" width="100" height="30" rx="5" fill="#F3E5F5" stroke="#7B1FA2"/>
  <text x="540" y="550" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">User Feedback</text>
</svg>

---

## Assignment Preview
### Client-Server Application

Create an application that:
1. Implements REST API calls
1. Handles WebSocket connections
1. Implements image loading
1. Manages authentication
1. Implements caching
1. Handles errors gracefully

---

## Resources

- Retrofit Documentation
- OkHttp Documentation
- WebSocket Guide
- Glide Documentation
- Network Security Best Practices
