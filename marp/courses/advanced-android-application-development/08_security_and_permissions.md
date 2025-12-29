# Security and Permissions
## Implementing Android Security Best Practices

---

## Security Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Check Permission</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Request if Needed</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Handle Result</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Proceed</text>
</svg>

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

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="290" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Security</text>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Best</text>
  <text x="400" y="320" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Practices</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Encryption</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Authentication</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Data</text>
  <text x="200" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Protection</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Secure</text>
  <text x="600" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Comm</text>
</svg>

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
