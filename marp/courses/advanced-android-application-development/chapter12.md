# Chapter 12: Production Deployment
## Preparing and Deploying Android Applications

---

# Deployment Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter12.md/0.png)

---

# Build Configuration

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

# CI/CD Pipeline Configuration

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

# App Bundle Configuration

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

# Version Management

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

# Dynamic Feature Loading

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

# Crash Reporting Setup

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

# Release Checklist

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter12.md/1.png)

---

# FastLane Configuration

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

# Best Practices

| Category | Practice | Benefit |
|----------|----------|---------|
| Signing | Use CI Variables | Secure keys |
| Testing | Automated Tests | Reliable releases |
| Deployment | Staged Rollout | Control risks |
| Monitoring | Crash Reporting | Quick fixes |

---

# Assignment Preview
## Production Deployment

Prepare an application for production:
1. Configure build variants
2. Setup CI/CD pipeline
3. Implement app bundle
4. Configure crash reporting
5. Setup automated deployment
6. Implement version checking

Due: End of Chapter 12

---

# Resources

- Android Deployment Guide
- Play Console Documentation
- CI/CD Best Practices
- App Bundle Guide
- Fastlane Documentation
