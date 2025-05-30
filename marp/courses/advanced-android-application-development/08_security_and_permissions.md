# Security and Permissions
## Implementing Android Security Best Practices

---

## Security Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter09.md/0.png)

---

## Runtime Permission Implementation

```java
public class PermissionManager {
    private static final int PERMISSION_REQUEST_CODE = 100;

    public void requestCameraPermission(Activity activity) {
        if (ContextCompat.checkSelfPermission(
                activity,
                Manifest.permission.CAMERA
            ) != PackageManager.PERMISSION_GRANTED) {

            // Should we show explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(
                    activity,
                    Manifest.permission.CAMERA)) {
                showPermissionRationale(activity);
            } else {
                // Request permission
                ActivityCompat.requestPermissions(
                    activity,
                    new String[]{Manifest.permission.CAMERA},
                    PERMISSION_REQUEST_CODE
                );
            }
        }
    }

    private void showPermissionRationale(Activity activity) {
        new AlertDialog.Builder(activity)
            .setTitle("Camera Permission Needed")
            .setMessage("This app needs camera access to take pictures.")
            .setPositiveButton("OK", (dialog, which) -> {
                ActivityCompat.requestPermissions(
                    activity,
                    new String[]{Manifest.permission.CAMERA},
                    PERMISSION_REQUEST_CODE
                );
            })
            .setNegativeButton("Cancel", null)
            .create()
            .show();
    }
}
```

---

## Data Encryption

```java
public class EncryptionManager {
    private static final String TRANSFORMATION =
        "AES/GCM/NoPadding";
    private final KeyStore keyStore;

    public void encryptData(String data) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, getSecretKey());

        byte[] iv = cipher.getIV();
        byte[] encrypted = cipher.doFinal(data.getBytes());

        // Save IV and encrypted data
        saveEncryptedData(iv, encrypted);
    }

    public String decryptData(byte[] encrypted, byte[] iv)
            throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        GCMParameterSpec spec = new GCMParameterSpec(128, iv);
        cipher.init(Cipher.DECRYPT_MODE, getSecretKey(), spec);

        byte[] decrypted = cipher.doFinal(encrypted);
        return new String(decrypted);
    }

    private SecretKey getSecretKey() throws Exception {
        if (!keyStore.containsAlias("secret_key")) {
            generateKey();
        }
        return (SecretKey) keyStore.getKey("secret_key", null);
    }
}
```

---

## Secure SharedPreferences

```java
public class SecurePreferences {
    private final SharedPreferences preferences;
    private final EncryptionManager encryptionManager;

    public void saveSecurely(String key, String value) {
        try {
            String encrypted = encryptionManager.encrypt(value);
            preferences.edit()
                .putString(key, encrypted)
                .apply();
        } catch (Exception e) {
            Log.e(TAG, "Error saving secure preference", e);
        }
    }

    public String getSecurely(String key, String defaultValue) {
        try {
            String encrypted = preferences.getString(key, null);
            if (encrypted != null) {
                return encryptionManager.decrypt(encrypted);
            }
        } catch (Exception e) {
            Log.e(TAG, "Error reading secure preference", e);
        }
        return defaultValue;
    }
}
```

---

## Network Security Configuration

```xml
<!-- network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set>
            <!-- Valid until: 2025-01-01 -->
            <pin digest="SHA-256">k3XnEYVCqKB4YX...</pin>
            <!-- Backup pin -->
            <pin digest="SHA-256">B0WqlmAKC7...</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

---

## SSL Pinning Implementation

```java
public class SSLPinningManager {
    private static final String HOSTNAME = "api.example.com";
    private static final Set<String> PINS = new HashSet<>(
        Arrays.asList(
            "sha256/k3XnEYVCqKB4YX...",
            "sha256/B0WqlmAKC7..."
        )
    );

    public OkHttpClient createPinnedClient() {
        CertificatePinner certificatePinner = new CertificatePinner.Builder()
            .add(HOSTNAME, PINS.toArray(new String[0]))
            .build();

        return new OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            .build();
    }
}
```

---

## ProGuard Configuration

```groovy
-keepclassmembers class * implements java.io.Serializable {
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

-keep class com.example.app.models.** { *; }
-keepclassmembers class com.example.app.api.** {
    @retrofit2.http.* <methods>;
}

-keepattributes Signature
-keepattributes *Annotation*
```

---

## Security Best Practices

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter09.md/1.png)

---

## Anti-Tampering Checks

```java
public class SecurityChecker {
    public boolean isEmulator() {
        return Build.FINGERPRINT.startsWith("generic") ||
            Build.FINGERPRINT.contains("test-keys");
    }

    public boolean isRooted() {
        String[] paths = {
            "/system/app/Superuser.apk",
            "/system/xbin/su",
            "/system/bin/su"
        };

        for (String path : paths) {
            if (new File(path).exists()) return true;
        }
        return false;
    }

    public boolean isDebuggable(Context context) {
        return (context.getApplicationInfo().flags &
            ApplicationInfo.FLAG_DEBUGGABLE) != 0;
    }
}
```

---

## Secure Database Implementation

```java
public class SecureDatabase {
    private static final String DB_NAME = "secure.db";

    public SQLiteDatabase getEncryptedDatabase(Context context) {
        SQLiteDatabaseHook hook = new SQLiteDatabaseHook() {
            public void preKey(SQLiteDatabase database) {}
            public void postKey(SQLiteDatabase database) {
                database.rawExecSQL("PRAGMA cipher_compatibility = 3");
                database.rawExecSQL("PRAGMA kdf_iter = 64000");
                database.rawExecSQL("PRAGMA cipher_page_size = 4096");
            }
        };

        return SQLiteDatabase.openOrCreateDatabase(
            context.getDatabasePath(DB_NAME),
            getEncryptionKey(),
            null,
            hook
        );
    }
}
```

---

## Permission Groups and Categories

| Permission Group | Common Permissions | Protection Level |
|-----------------|-------------------|------------------|
| STORAGE | READ_EXTERNAL_STORAGE | Dangerous |
| LOCATION | ACCESS_FINE_LOCATION | Dangerous |
| CAMERA | CAMERA | Dangerous |
| CONTACTS | READ_CONTACTS | Dangerous |

---

## Assignment Preview
### Security Implementation

Create an application that:
1. Implements runtime permissions
1. Uses encryption for data storage
1. Implements SSL pinning
1. Configures ProGuard rules
1. Implements security checks
1. Uses secure SharedPreferences

---

## Resources

- Android Security Documentation
- Encryption Guidelines
- ProGuard Manual
- Network Security Guide
- Permission Best Practices
