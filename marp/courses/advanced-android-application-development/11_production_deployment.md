# Production Deployment
## Preparing and Deploying Android Applications

---

## Deployment Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Build</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Test</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Sign</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Upload</text>
  <line x1="400" y1="370" x2="400" y2="400" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="410" width="120" height="50" rx="8" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="400" y="440" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Release</text>
</svg>

---

## Build Configuration

```groovy
android {
    defaultConfig {
        applicationId "com.example.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    signingConfigs {
        release {
            storeFile file("release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile(
                'proguard-android-optimize.txt'
            ), 'proguard-rules.pro'
            signingConfig signingConfigs.release
        }

        staging {
            initWith release
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
        }
    }

    productFlavors {
        free {
            applicationIdSuffix ".free"
            dimension "version"
        }

        pro {
            applicationIdSuffix ".pro"
            dimension "version"
        }
    }
}
```

---

## CI/CD Pipeline Configuration

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  ANDROID_COMPILE_SDK: "34"
  ANDROID_BUILD_TOOLS: "34.0.0"
  ANDROID_SDK_TOOLS:   "9477386"

test:
  stage: test
  script:
    - ./gradlew test

lint:
  stage: test
  script:
    - ./gradlew lint
  artifacts:
    paths:
      - app/build/reports/lint-results.html

build_release:
  stage: build
  script:
    - ./gradlew assembleRelease
  artifacts:
    paths:
      - app/build/outputs/apk/release/

deploy_play_store:
  stage: deploy
  script:
    - fastlane deploy
  only:
    - master
```

---

## App Bundle Configuration

```groovy
android {
    bundle {
        language {
            enableSplit = true
        }
        density {
            enableSplit = true
        }
        abi {
            enableSplit = true
        }

        dynamicFeatures = [":feature_chat", ":feature_map"]
    }
}

dependencies {
    dynamicFeature project(":feature_chat")
    dynamicFeature project(":feature_map")
}
```

---

## Version Management

```java
public class VersionManager {
    public static String getVersionInfo(Context context) {
        try {
            PackageInfo pInfo = context.getPackageManager()
                .getPackageInfo(context.getPackageName(), 0);

            return String.format(
                "Version %s (%d)",
                pInfo.versionName,
                pInfo.versionCode
            );
        } catch (PackageManager.NameNotFoundException e) {
            return "Version Unknown";
        }
    }

    public static boolean isUpdateRequired(String minVersion) {
        return BuildConfig.VERSION_CODE <
            Integer.parseInt(minVersion);
    }
}
```

---

## Dynamic Feature Loading

```java
public class FeatureManager {
    public void downloadFeature(Context context, String featureName) {
        SplitInstallManager manager =
            SplitInstallManagerFactory.create(context);

        SplitInstallRequest request = SplitInstallRequest
            .newBuilder()
            .addModule(featureName)
            .build();

        manager.startInstall(request)
            .addOnSuccessListener(sessionId -> {
                // Feature installed successfully
                loadFeature(featureName);
            })
            .addOnFailureListener(exception -> {
                // Handle failure
                handleError(exception);
            });
    }
}
```

---

## Crash Reporting Setup

```java
public class CrashReporter {
    public static void initialize(Application app) {
        if (!BuildConfig.DEBUG) {
            FirebaseCrashlytics.getInstance()
                .setCrashlyticsCollectionEnabled(true);

            Thread.setDefaultUncaughtExceptionHandler(
                (thread, throwable) -> {
                    FirebaseCrashlytics.getInstance()
                        .recordException(throwable);
                }
            );
        }
    }

    public static void logEvent(String event, Bundle params) {
        FirebaseAnalytics.getInstance(context)
            .logEvent(event, params);
    }
}
```

---

## Release Checklist

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Deployment Steps</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="145" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">App</text>
  <text x="200" y="160" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Bundle</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Signing</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Play</text>
  <text x="200" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Console</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Monitoring</text>
</svg>

---

## FastLane Configuration

```ruby
# fastfile
default_platform(:android)

platform :android do
  desc "Deploy to Play Store"
  lane :deploy do
    gradle(
      task: "clean assembleRelease",
      properties: {
        "android.injected.signing.store.file" =>
          ENV["KEYSTORE_FILE"],
        "android.injected.signing.store.password" =>
          ENV["STORE_PASSWORD"],
        "android.injected.signing.key.alias" =>
          ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" =>
          ENV["KEY_PASSWORD"],
      }
    )

    upload_to_play_store(
      track: 'internal',
      json_key: 'path/to/service-account.json',
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true,
      aab: 'app/build/outputs/bundle/release/app-release.aab'
    )
  end
end
```

---

## Best Practices

| Category | Practice | Benefit |
|----------|----------|---------|
| Signing | Use CI Variables | Secure keys |
| Testing | Automated Tests | Reliable releases |
| Deployment | Staged Rollout | Control risks |
| Monitoring | Crash Reporting | Quick fixes |

---

## Assignment Preview
### Production Deployment

Prepare an application for production:
1. Configure build variants
1. Setup CI/CD pipeline
1. Implement app bundle
1. Configure crash reporting
1. Setup automated deployment
1. Implement version checking

---

## Resources

- Android Deployment Guide
- Play Console Documentation
- CI/CD Best Practices
- App Bundle Guide
- Fastlane Documentation
