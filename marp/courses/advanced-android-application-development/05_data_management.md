# Data Management
## Efficient Data Storage and Retrieval in Android

---

## Data Storage Options

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Central node -->
  <circle cx="400" cy="300" r="80" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="300" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Android Storage</text>

  <!-- Room Database branch -->
  <line x1="320" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="60" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="200" y="150" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Room Database</text>

  <!-- Room sub-branches -->
  <line x1="140" y1="110" x2="80" y2="60" stroke="#999" stroke-width="1"/>
  <rect x="40" y="45" width="80" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="80" y="65" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Entities</text>

  <line x1="140" y1="150" x2="80" y2="150" stroke="#999" stroke-width="1"/>
  <rect x="40" y="135" width="80" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="80" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">DAOs</text>

  <line x1="140" y1="190" x2="80" y2="240" stroke="#999" stroke-width="1"/>
  <rect x="40" y="225" width="80" height="30" rx="5" fill="#E3F2FD" stroke="#1976D2"/>
  <text x="80" y="245" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Relations</text>

  <!-- SharedPreferences branch -->
  <line x1="480" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="60" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="600" y="145" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Shared</text>
  <text x="600" y="165" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Preferences</text>

  <!-- SharedPreferences sub-branches -->
  <line x1="660" y1="110" x2="720" y2="60" stroke="#999" stroke-width="1"/>
  <rect x="670" y="45" width="100" height="30" rx="5" fill="#FFF3E0" stroke="#F57C00"/>
  <text x="720" y="65" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Key-Value Pairs</text>

  <line x1="660" y1="190" x2="720" y2="240" stroke="#999" stroke-width="1"/>
  <rect x="680" y="225" width="80" height="30" rx="5" fill="#FFF3E0" stroke="#F57C00"/>
  <text x="720" y="245" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Settings</text>

  <!-- File System branch -->
  <line x1="320" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="60" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="200" y="450" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">File System</text>

  <!-- File System sub-branches -->
  <line x1="140" y1="420" x2="80" y2="380" stroke="#999" stroke-width="1"/>
  <rect x="30" y="365" width="100" height="30" rx="5" fill="#F3E5F5" stroke="#7B1FA2"/>
  <text x="80" y="385" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Internal Storage</text>

  <line x1="140" y1="480" x2="80" y2="520" stroke="#999" stroke-width="1"/>
  <rect x="30" y="505" width="100" height="30" rx="5" fill="#F3E5F5" stroke="#7B1FA2"/>
  <text x="80" y="525" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">External Storage</text>

  <!-- ContentProvider branch -->
  <line x1="480" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="60" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="600" y="445" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Content</text>
  <text x="600" y="465" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Provider</text>

  <!-- ContentProvider sub-branches -->
  <line x1="660" y1="420" x2="720" y2="380" stroke="#999" stroke-width="1"/>
  <rect x="670" y="365" width="100" height="30" rx="5" fill="#FFEBEE" stroke="#D32F2F"/>
  <text x="720" y="385" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Data Sharing</text>

  <line x1="660" y1="480" x2="720" y2="520" stroke="#999" stroke-width="1"/>
  <rect x="680" y="505" width="80" height="30" rx="5" fill="#FFEBEE" stroke="#D32F2F"/>
  <text x="720" y="525" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">Content URI</text>
</svg>

---

## Room Database Architecture

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Entity -->
  <rect x="350" y="40" width="100" height="60" rx="10" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="400" y="75" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Entity</text>

  <!-- Arrow from Entity to DAO -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="400" y1="100" x2="400" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- DAO -->
  <rect x="350" y="150" width="100" height="60" rx="10" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="400" y="185" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">DAO</text>

  <!-- Arrow from DAO to Database -->
  <line x1="400" y1="210" x2="400" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Database -->
  <rect x="350" y="260" width="100" height="60" rx="10" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="400" y="295" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Database</text>

  <!-- Arrow from Database to Repository -->
  <line x1="400" y1="320" x2="400" y2="360" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Repository -->
  <rect x="350" y="370" width="100" height="60" rx="10" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="400" y="405" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Repository</text>

  <!-- Arrow from Repository to ViewModel -->
  <line x1="400" y1="430" x2="400" y2="470" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- ViewModel -->
  <rect x="350" y="480" width="100" height="60" rx="10" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="400" y="515" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">ViewModel</text>

  <!-- Arrow from ViewModel to UI -->
  <line x1="400" y1="540" x2="400" y2="580" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- UI (not shown as it would be cut off, but the arrow points to it) -->
  <text x="400" y="595" font-family="Arial, sans-serif" font-size="14" font-style="italic" text-anchor="middle" fill="#666">UI Layer</text>
</svg>

---

## Entity Definition

```java
@Entity(tableName = "users")
public class User {
    @PrimaryKey
    @NonNull
    private String id;

    @ColumnInfo(name = "first_name")
    private String firstName;

    @ColumnInfo(name = "last_name")
    private String lastName;

    @ColumnInfo(name = "email")
    private String email;

    @ColumnInfo(name = "created_at")
    private long createdAt;

    // Constructor, getters, and setters
}
```

---

## DAO Implementation

```java
@Dao
public interface UserDao {
    @Query("SELECT * FROM users")
    List<User> getAllUsers();

    @Query("SELECT * FROM users WHERE id = :userId")
    User getUserById(String userId);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertUser(User user);

    @Delete
    void deleteUser(User user);

    @Query("SELECT * FROM users WHERE email LIKE :email")
    List<User> findUsersByEmail(String email);
}
```

---

## Database Setup

```java
@Database(entities = {User.class, Profile.class}, version = 1)
public abstract class AppDatabase extends RoomDatabase {
    public abstract UserDao userDao();
    public abstract ProfileDao profileDao();

    private static volatile AppDatabase INSTANCE;

    public static AppDatabase getInstance(Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                        context.getApplicationContext(),
                        AppDatabase.class,
                        "app_database"
                    ).build();
                }
            }
        }
        return INSTANCE;
    }
}
```

---

## Relationships in Room

```java
@Entity
public class Book {
    @PrimaryKey
    public int bookId;

    public String title;
    public int authorId;
}

@Entity
public class Author {
    @PrimaryKey
    public int authorId;

    public String name;
}

public class BookWithAuthor {
    @Embedded
    public Book book;

    @Relation(
        parentColumn = "authorId",
        entityColumn = "authorId"
    )
    public Author author;
}
```

---

## SharedPreferences Implementation

```java
public class PreferenceManager {
    private static final String PREF_NAME = "AppPrefs";
    private final SharedPreferences prefs;

    public PreferenceManager(Context context) {
        prefs = context.getSharedPreferences(
            PREF_NAME,
            Context.MODE_PRIVATE
        );
    }

    public void saveUserSettings(UserSettings settings) {
        prefs.edit()
            .putString("theme", settings.getTheme())
            .putBoolean("notifications", settings.isNotificationsEnabled())
            .putInt("refresh_interval", settings.getRefreshInterval())
            .apply();
    }

    public UserSettings getUserSettings() {
        return new UserSettings(
            prefs.getString("theme", "light"),
            prefs.getBoolean("notifications", true),
            prefs.getInt("refresh_interval", 30)
        );
    }
}
```

---

## File System Operations

```java
public class FileManager {
    private final Context context;

    public void saveFile(String filename, String content) {
        try (FileOutputStream fos =
                context.openFileOutput(filename, Context.MODE_PRIVATE)) {
            fos.write(content.getBytes());
        } catch (IOException e) {
            Log.e(TAG, "Error saving file", e);
        }
    }

    public String readFile(String filename) {
        try (FileInputStream fis = context.openFileInput(filename)) {
            byte[] bytes = new byte[fis.available()];
            fis.read(bytes);
            return new String(bytes);
        } catch (IOException e) {
            Log.e(TAG, "Error reading file", e);
            return null;
        }
    }
}
```

---

## ContentProvider Implementation

```java
public class UserProvider extends ContentProvider {
    private static final String AUTHORITY =
        "com.example.app.provider";
    private static final Uri CONTENT_URI =
        Uri.parse("content://" + AUTHORITY + "/users");

    @Override
    public Cursor query(Uri uri, String[] projection,
            String selection, String[] selectionArgs,
            String sortOrder) {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        return db.query("users", projection, selection,
            selectionArgs, null, null, sortOrder);
    }

    // Other CRUD operations...
}
```

---

## Data Migration Strategy

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Old Schema -->
  <rect x="50" y="50" width="120" height="60" rx="10" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="110" y="85" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Old Schema</text>

  <!-- Arrow to Migration Plan -->
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="170" y1="80" x2="300" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Migration Plan (center) -->
  <rect x="320" y="180" width="140" height="60" rx="10" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="390" y="215" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Migration Plan</text>

  <!-- Arrow to New Schema -->
  <line x1="460" y1="200" x2="590" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- New Schema -->
  <rect x="600" y="50" width="120" height="60" rx="10" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="660" y="85" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">New Schema</text>

  <!-- Arrow to Data Backup -->
  <line x1="350" y1="240" x2="200" y2="360" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Data Backup -->
  <rect x="100" y="370" width="120" height="60" rx="10" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="160" y="405" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Data Backup</text>

  <!-- Arrow to Version Update -->
  <line x1="430" y1="240" x2="580" y2="360" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Version Update -->
  <rect x="550" y="370" width="130" height="60" rx="10" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="615" y="405" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Version Update</text>

  <!-- Arrow from Version Update to Schema Validation -->
  <line x1="615" y1="430" x2="480" y2="480" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Schema Validation -->
  <rect x="380" y="490" width="140" height="60" rx="10" fill="#00BCD4" stroke="#006064" stroke-width="2"/>
  <text x="450" y="525" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Schema Validation</text>

  <!-- Arrow from Schema Validation to Migration Testing -->
  <line x1="380" y1="520" x2="250" y2="520" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Migration Testing -->
  <rect x="100" y="490" width="140" height="60" rx="10" fill="#795548" stroke="#4E342E" stroke-width="2"/>
  <text x="170" y="525" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">Migration Testing</text>
</svg>

---

## Database Migration Example

```java
@Database(
    entities = {User.class},
    version = 2
)
public abstract class AppDatabase extends RoomDatabase {
    static final Migration MIGRATION_1_2 =
        new Migration(1, 2) {
        @Override
        public void migrate(SupportSQLiteDatabase db) {
            db.execSQL(
                "ALTER TABLE users "
                + "ADD COLUMN last_login INTEGER"
            );
        }
    };

    public static AppDatabase getInstance(Context context) {
        return Room.databaseBuilder(context,
                AppDatabase.class, "database-name")
                .addMigrations(MIGRATION_1_2)
                .build();
    }
}
```

---

## Data Backup Strategies

```java
public class BackupManager {
    public void backupDatabase(Context context) {
        File dbFile = context.getDatabasePath("app_database");
        File backupFile = new File(
            context.getExternalFilesDir(null),
            "backup_" + System.currentTimeMillis()
        );

        try (FileInputStream fis = new FileInputStream(dbFile);
             FileOutputStream fos = new FileOutputStream(backupFile)) {
            byte[] buffer = new byte[1024];
            int length;
            while ((length = fis.read(buffer)) > 0) {
                fos.write(buffer, 0, length);
            }
        } catch (IOException e) {
            Log.e(TAG, "Backup failed", e);
        }
    }
}
```

---

## Performance Optimization

| Technique | Implementation | Benefit |
|-----------|---------------|----------|
| Indexing | `@ColumnInfo(index = true)` | Faster queries |
| Lazy Loading | `@Relation` with lazy fetch | Memory efficient |
| Batch Operations | `@Insert(onConflict = ...)` | Better throughput |
| Caching | `LiveData` caching | Reduced DB calls |

---

## Best Practices

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Central node -->
  <rect x="250" y="50" width="300" height="60" rx="10" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
  <text x="400" y="85" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="white">Data Management Best Practices</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Use Room for Complex Data -->
  <line x1="200" y1="110" x2="100" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="30" y="190" width="200" height="50" rx="8" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="130" y="220" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Use Room for Complex Data</text>

  <!-- SharedPreferences for Simple Data -->
  <line x1="300" y1="110" x2="200" y2="270" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="30" y="280" width="240" height="50" rx="8" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
  <text x="150" y="310" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">SharedPreferences for Simple Data</text>

  <!-- Implement Proper Migration -->
  <line x1="400" y1="110" x2="400" y2="360" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="280" y="370" width="240" height="50" rx="8" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
  <text x="400" y="400" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Implement Proper Migration</text>

  <!-- Regular Backups -->
  <line x1="500" y1="110" x2="600" y2="270" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="530" y="280" width="140" height="50" rx="8" fill="#F44336" stroke="#C62828" stroke-width="2"/>
  <text x="600" y="310" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Regular Backups</text>

  <!-- Handle Edge Cases -->
  <line x1="600" y1="110" x2="700" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="620" y="190" width="150" height="50" rx="8" fill="#00BCD4" stroke="#006064" stroke-width="2"/>
  <text x="695" y="220" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Handle Edge Cases</text>

  <!-- Optimize Queries -->
  <line x1="400" y1="110" x2="400" y2="470" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="325" y="480" width="150" height="50" rx="8" fill="#795548" stroke="#4E342E" stroke-width="2"/>
  <text x="400" y="510" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Optimize Queries</text>
</svg>

---

## Assignment Preview
### Data-Driven Application

Create an application that:
1. Implements Room Database
1. Handles complex relationships
1. Performs data migrations
1. Implements backup/restore
1. Uses SharedPreferences
1. Optimizes performance

---

## Resources

- Room Documentation
- SQLite Documentation
- Android Storage Guide
- Sample Code Repository
- Migration Guide
