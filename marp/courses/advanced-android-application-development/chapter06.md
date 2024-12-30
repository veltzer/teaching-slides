# Chapter 6: Network Operations
## Building Robust Networked Applications

---

## Network Architecture Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter6.md/0.png)

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

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter6.md/1.png)

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

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter6.md/2.png)

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

![3](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter6.md/3.png)

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
