---
tags:
  - infrastructure:android
  - concepts:mobile-development
  - concepts:databases
level: advanced
category: mobile
audience:
  - audiences:developers

---

# Data Management
## Efficient Data Storage and Retrieval in Android

---

## Data Storage Options

![data_storage_options](svg/courses/operating_systems/advanced-android-application-development/05_data_management/data_storage_options.svg)

---

## Room Database Architecture

![room_database_architecture](svg/courses/operating_systems/advanced-android-application-development/05_data_management/room_database_architecture.svg)

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

![data_migration_strategy](svg/courses/operating_systems/advanced-android-application-development/05_data_management/data_migration_strategy.svg)

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

![best_practices](svg/courses/operating_systems/advanced-android-application-development/05_data_management/best_practices.svg)

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
