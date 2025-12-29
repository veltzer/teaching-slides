# Performance Optimization
## Building High-Performance Android Applications

---

## Performance Areas Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Measure</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Analyze</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Optimize</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Verify</text>
</svg>

---

## Memory Management

```java
public class MemoryOptimizer {
    private WeakReference<Context> weakContext;
    private LruCache<String, Bitmap> memoryCache;

    public void initializeCache() {
        // Get max available VM memory
        final int maxMemory =
            (int) (Runtime.getRuntime().maxMemory() / 1024);

        // Use 1/8th of available memory for cache
        final int cacheSize = maxMemory / 8;

        memoryCache = new LruCache<String, Bitmap>(cacheSize) {
            @Override
            protected int sizeOf(String key, Bitmap bitmap) {
                // Size in kilobytes
                return bitmap.getByteCount() / 1024;
            }
        };
    }

    public void loadBitmap(String key, ImageView imageView) {
        Bitmap bitmap = memoryCache.get(key);
        if (bitmap != null) {
            imageView.setImageBitmap(bitmap);
        } else {
            // Load bitmap asynchronously
            loadBitmapAsync(key, imageView);
        }
    }
}
```

---

## Layout Optimization

```xml
<!-- Before Optimization -->
<LinearLayout>
    <LinearLayout>
        <LinearLayout>
            <TextView/>
            <ImageView/>
        </LinearLayout>
        <LinearLayout>
            <TextView/>
            <Button/>
        </LinearLayout>
    </LinearLayout>
</LinearLayout>

<!-- After Optimization -->
<ConstraintLayout>
    <TextView/>
    <ImageView/>
    <TextView/>
    <Button/>
</ConstraintLayout>
```

---

## View Holder Pattern

```java
public class OptimizedAdapter
        extends RecyclerView.Adapter<OptimizedAdapter.ViewHolder> {

    static class ViewHolder extends RecyclerView.ViewHolder {
        private final TextView titleView;
        private final ImageView iconView;

        ViewHolder(View view) {
            super(view);
            titleView = view.findViewById(R.id.title);
            iconView = view.findViewById(R.id.icon);
        }

        void bind(Item item) {
            titleView.setText(item.getTitle());
            Glide.with(iconView)
                .load(item.getIconUrl())
                .diskCacheStrategy(DiskCacheStrategy.ALL)
                .into(iconView);
        }
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        holder.bind(items.get(position));
    }
}
```

---

## Network Optimization

```java
public class NetworkOptimizer {
    private final OkHttpClient client;

    public NetworkOptimizer(Context context) {
        int cacheSize = 10 * 1024 * 1024; // 10 MB
        Cache cache = new Cache(
            context.getCacheDir(),
            cacheSize
        );

        client = new OkHttpClient.Builder()
            .cache(cache)
            .addInterceptor(new CacheInterceptor())
            .build();
    }

    private static class CacheInterceptor implements Interceptor {
        @Override
        public Response intercept(Chain chain) throws IOException {
            Request request = chain.request();
            Response response = chain.proceed(request);

            return response.newBuilder()
                .header("Cache-Control",
                    "public, max-age=60") // Cache for 1 minute
                .build();
        }
    }
}
```

---

## Database Optimization

```java
@Dao
public interface OptimizedDao {
    @Query("SELECT * FROM users WHERE age > :minAge " +
           "ORDER BY name ASC LIMIT :pageSize OFFSET :offset")
    List<User> getPagedUsers(int minAge, int pageSize, int offset);

    @Transaction
    @Query("SELECT * FROM users")
    List<UserWithPosts> getUsersWithPosts();

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertUsers(List<User> users);
}

// Usage with paging
public class UserRepository {
    private static final int PAGE_SIZE = 20;

    public List<User> getUsers(int page) {
        int offset = page * PAGE_SIZE;
        return userDao.getPagedUsers(18, PAGE_SIZE, offset);
    }
}
```

---

## Battery Optimization

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Optimization Areas</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Memory</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Battery</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Network</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Rendering</text>
</svg>

---

## Image Loading Optimization

```java
public class ImageOptimizer {
    public static RequestOptions getOptimizedOptions() {
        return new RequestOptions()
            .diskCacheStrategy(DiskCacheStrategy.ALL)
            .placeholder(R.drawable.placeholder)
            .error(R.drawable.error)
            .transform(new CenterCrop(),
                      new RoundedCorners(8))
            .format(DecodeFormat.PREFER_RGB_565) // Reduced memory
            .override(Target.SIZE_ORIGINAL)
            .encodeQuality(80); // Reduced quality
    }

    public static void loadOptimizedImage(
            ImageView imageView,
            String url) {
        Glide.with(imageView.getContext())
            .load(url)
            .apply(getOptimizedOptions())
            .transition(DrawableTransitionOptions.withCrossFade())
            .into(imageView);
    }
}
```

---

## Performance Monitoring

```java
public class PerformanceMonitor {
    private static final String TAG = "Performance";

    public static void startMethodTracing() {
        Debug.startMethodTracing("app_trace");
    }

    public static void stopMethodTracing() {
        Debug.stopMethodTracing();
    }

    public static void logMemoryStats() {
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = (runtime.totalMemory() -
            runtime.freeMemory()) / 1024;
        long maxMemory = runtime.maxMemory() / 1024;

        Log.d(TAG, String.format(
            "Memory - Used: %dKB, Max: %dKB",
            usedMemory,
            maxMemory
        ));
    }
}
```

---

## ANR Prevention

```java
public class BackgroundTaskManager {
    private final ExecutorService executor;
    private final Handler mainHandler;

    public void performLongOperation(Runnable task) {
        executor.execute(() -> {
            // Do work in background
            try {
                // Simulate long operation
                Thread.sleep(1000);
                task.run();
            } catch (InterruptedException e) {
                Log.e(TAG, "Task interrupted", e);
            }

            // Update UI on main thread
            mainHandler.post(() -> {
                updateUI();
            });
        });
    }
}
```

---

## Best Practices

| Category | Practice | Impact |
|----------|----------|---------|
| Memory | Use WeakReferences | Prevent leaks |
| Layout | Flatten hierarchies | Faster rendering |
| Network | Implement caching | Reduced bandwidth |
| Database | Use indexing | Faster queries |

---

## Assignment Preview
### Performance Optimization

Optimize an application:
1. Implement memory management
1. Optimize layouts
1. Improve network efficiency
1. Optimize database queries
1. Implement battery optimizations
1. Monitor performance

---

## Resources

- Android Performance Patterns
- Memory Management Guide
- Layout Optimization Guide
- Network Efficiency Guide
- Battery Optimization Guide
