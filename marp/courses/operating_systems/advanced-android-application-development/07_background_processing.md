---
tags:
  - infrastructure:android
  - concepts:mobile-development
  - concepts:concurrency
level: advanced
category: mobile
audience:
  - audiences:developers

---
# Background Processing
## Managing Background Tasks and Services

---

## Background Processing Options

![background_processing_options](svg/courses/operating_systems/advanced-android-application-development/07_background_processing/background_processing_options.svg)

---

## Service Lifecycle

![service_lifecycle](svg/courses/operating_systems/advanced-android-application-development/07_background_processing/service_lifecycle.svg)

---

## Foreground Service Implementation

```java
public class DownloadService extends Service {
    private static final int NOTIFICATION_ID = 1;
    private static final String CHANNEL_ID = "download_channel";

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        createNotificationChannel();
        startForeground(NOTIFICATION_ID, createNotification());

        // Start download operation
        new Thread(() -> {
            performDownload();
            stopForeground(true);
            stopSelf();
        }).start();

        return START_NOT_STICKY;
    }
```

---

## Foreground Service: Notification Helpers

```java
    private Notification createNotification() {
        return new NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Downloading")
            .setSmallIcon(R.drawable.ic_download)
            .setProgress(100, 0, true)
            .build();
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel(
            CHANNEL_ID,
            "Downloads",
            NotificationManager.IMPORTANCE_LOW
        );
        NotificationManager manager = getSystemService(
            NotificationManager.class
        );
        manager.createNotificationChannel(channel);
    }
}
```

---

## WorkManager Setup

```java
public class DataSyncWorker extends Worker {
    public DataSyncWorker(
            Context context,
            WorkerParameters params) {
        super(context, params);
    }

    @Override
    public Result doWork() {
        try {
            // Perform sync operation
            syncData();
            return Result.success();
        } catch (Exception e) {
            return Result.retry();
        }
    }
}

// Scheduling work
WorkManager workManager = WorkManager.getInstance(context);

WorkRequest syncWork = new OneTimeWorkRequest.Builder(
    DataSyncWorker.class)
    .setConstraints(new Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .setRequiresBatteryNotLow(true)
        .build())
    .setBackoffCriteria(
        BackoffPolicy.LINEAR,
        OneTimeWorkRequest.MIN_BACKOFF_MILLIS,
        TimeUnit.MILLISECONDS)
    .build();

workManager.enqueue(syncWork);
```

---

## Periodic Work with WorkManager

```java
public class PeriodicSyncManager {
    public void schedulePeriodicSync() {
        PeriodicWorkRequest syncWork =
            new PeriodicWorkRequest.Builder(
                DataSyncWorker.class,
                15,
                TimeUnit.MINUTES)
                .setConstraints(new Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build())
                .build();

        WorkManager.getInstance(context)
            .enqueueUniquePeriodicWork(
                "periodic_sync",
                ExistingPeriodicWorkPolicy.KEEP,
                syncWork);
    }
}
```

---

## Chained Work Requests

```java
public class WorkChainManager {
    public void startWorkChain() {
        WorkManager workManager = WorkManager.getInstance(context);

        WorkRequest downloadWork = new OneTimeWorkRequest.Builder(
            DownloadWorker.class).build();

        WorkRequest processWork = new OneTimeWorkRequest.Builder(
            ProcessWorker.class).build();

        WorkRequest uploadWork = new OneTimeWorkRequest.Builder(
            UploadWorker.class).build();

        workManager.beginWith(downloadWork)
            .then(processWork)
            .then(uploadWork)
            .enqueue();
    }
}
```

---

## BroadcastReceiver Implementation

```java
public class NetworkChangeReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (ConnectivityManager.CONNECTIVITY_ACTION.equals(
                intent.getAction())) {

            ConnectivityManager cm = (ConnectivityManager)
                context.getSystemService(Context.CONNECTIVITY_SERVICE);

            NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            boolean isConnected = activeNetwork != null &&
                activeNetwork.isConnectedOrConnecting();

            if (isConnected) {
                // Handle connected state
                scheduleSync(context);
            }
        }
    }
}

// Registration in Activity/Fragment
IntentFilter filter = new IntentFilter(
    ConnectivityManager.CONNECTIVITY_ACTION);
registerReceiver(new NetworkChangeReceiver(), filter);
```

---

## AlarmManager Usage

```java
public class AlarmScheduler {
    public void scheduleAlarm(Context context) {
        AlarmManager alarmManager = (AlarmManager)
            context.getSystemService(Context.ALARM_SERVICE);

        Intent intent = new Intent(context, AlarmReceiver.class);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT |
            PendingIntent.FLAG_IMMUTABLE
        );

        // Schedule exact alarm
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            alarmManager.setExactAndAllowWhileIdle(
                AlarmManager.RTC_WAKEUP,
                System.currentTimeMillis() + TimeUnit.HOURS.toMillis(1),
                pendingIntent
            );
        }
    }
}
```

---

## Battery Optimization

![battery_optimization](svg/courses/operating_systems/advanced-android-application-development/07_background_processing/battery_optimization.svg)

---

## Background Task Priority

| Task Type | Tool | When to Use |
|-----------|------|-------------|
| Immediate | Foreground Service | User-initiated tasks |
| Deferred | WorkManager | Background sync |
| Periodic | PeriodicWorkRequest | Regular updates |
| System Events | BroadcastReceiver | Event responses |

---

## Error Handling in Background Tasks

```java
public class RobustWorker extends Worker {
    @Override
    public Result doWork() {
        try {
            // Attempt work
            performTask();
            return Result.success();
        } catch (NetworkException e) {
            // Retry on network errors
            return Result.retry();
        } catch (Exception e) {
            // Fail on other errors
            return Result.failure();
        }
    }

    private void performTask() {
        int retryCount = 0;
        while (retryCount < MAX_RETRIES) {
            try {
                // Perform work
                return;
            } catch (Exception e) {
                retryCount++;
                Thread.sleep(RETRY_DELAY_MS);
            }
        }
        throw new TaskException("Max retries exceeded");
    }
}
```

---

## Best Practices

![best_practices](svg/courses/operating_systems/advanced-android-application-development/07_background_processing/best_practices.svg)

---

## Assignment Preview
### Background Processing Implementation

Create an application that:
1. Uses Foreground Service
1. Implements WorkManager
1. Handles system events
1. Manages periodic tasks
1. Implements battery optimization
1. Provides error handling

---

## Resources

- Android Services Guide
- WorkManager Documentation
- BroadcastReceiver Guide
- AlarmManager Documentation
- Battery Optimization Guide
