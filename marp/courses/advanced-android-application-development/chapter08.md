# Chapter 8: Location and Maps
## Implementing Location-Based Services

---

# Location Services Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter8.md/0.png)

---

# Location Permissions

```java
public class LocationPermissionManager {
    private static final int PERMISSION_REQUEST_CODE = 123;
    
    public boolean checkLocationPermission(Activity activity) {
        if (ContextCompat.checkSelfPermission(
                activity, 
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED) {
            
            ActivityCompat.requestPermissions(
                activity,
                new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                },
                PERMISSION_REQUEST_CODE
            );
            return false;
        }
        return true;
    }

    public void onRequestPermissionsResult(
            int requestCode, 
            String[] permissions,
            int[] grantResults) {
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && 
                grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, initialize location updates
                initializeLocationUpdates();
            }
        }
    }
}
```

---

# FusedLocationProvider Implementation

```java
public class LocationManager {
    private FusedLocationProviderClient fusedLocationClient;
    private LocationCallback locationCallback;
    private LocationRequest locationRequest;

    public void startLocationUpdates() {
        locationRequest = LocationRequest.create()
            .setPriority(Priority.PRIORITY_HIGH_ACCURACY)
            .setInterval(10000)
            .setFastestInterval(5000);

        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult result) {
                for (Location location : result.getLocations()) {
                    updateLocation(location);
                }
            }
        };

        if (ActivityCompat.checkSelfPermission(
                context, 
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED) {
            
            fusedLocationClient.requestLocationUpdates(
                locationRequest,
                locationCallback,
                Looper.getMainLooper()
            );
        }
    }

    public void stopLocationUpdates() {
        fusedLocationClient.removeLocationUpdates(locationCallback);
    }
}
```

---

# Google Maps Integration

```java
public class MapActivity extends AppCompatActivity 
        implements OnMapReadyCallback {
    
    private GoogleMap googleMap;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);
        
        SupportMapFragment mapFragment = (SupportMapFragment) 
            getSupportFragmentManager()
            .findFragmentById(R.id.map);
            
        mapFragment.getMapAsync(this);
    }

    @Override
    public void onMapReady(GoogleMap map) {
        googleMap = map;
        
        // Configure map settings
        googleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        googleMap.setMyLocationEnabled(true);
        googleMap.getUiSettings().setZoomControlsEnabled(true);
        
        // Add markers, polylines, etc.
        addMapMarkers();
    }

    private void addMapMarkers() {
        LatLng position = new LatLng(37.7749, -122.4194);
        MarkerOptions markerOptions = new MarkerOptions()
            .position(position)
            .title("San Francisco")
            .snippet("California, USA");
            
        googleMap.addMarker(markerOptions);
        googleMap.animateCamera(
            CameraUpdateFactory.newLatLngZoom(position, 12)
        );
    }
}
```

---

# Geofencing Implementation

```java
public class GeofenceManager {
    private GeofencingClient geofencingClient;
    private PendingIntent geofencePendingIntent;

    public void createGeofence(LatLng location, float radius) {
        Geofence geofence = new Geofence.Builder()
            .setRequestId("geofence_1")
            .setCircularRegion(
                location.latitude,
                location.longitude,
                radius
            )
            .setExpirationDuration(Geofence.NEVER_EXPIRE)
            .setTransitionTypes(
                Geofence.GEOFENCE_TRANSITION_ENTER |
                Geofence.GEOFENCE_TRANSITION_EXIT
            )
            .build();

        GeofencingRequest geofencingRequest = 
            new GeofencingRequest.Builder()
                .setInitialTrigger(
                    GeofencingRequest.INITIAL_TRIGGER_ENTER
                )
                .addGeofence(geofence)
                .build();

        geofencingClient.addGeofences(
            geofencingRequest,
            getGeofencePendingIntent()
        );
    }

    private PendingIntent getGeofencePendingIntent() {
        if (geofencePendingIntent != null) {
            return geofencePendingIntent;
        }
        Intent intent = new Intent(
            context, 
            GeofenceBroadcastReceiver.class
        );
        geofencePendingIntent = PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT |
            PendingIntent.FLAG_IMMUTABLE
        );
        return geofencePendingIntent;
    }
}
```

---

# Places API Integration

```java
public class PlacesManager {
    private PlacesClient placesClient;

    public void initializePlaces() {
        Places.initialize(context, "YOUR_API_KEY");
        placesClient = Places.createClient(context);
    }

    public void searchNearbyPlaces(LatLng location) {
        FindCurrentPlaceRequest request = 
            FindCurrentPlaceRequest.newInstance(
                Arrays.asList(
                    Place.Field.NAME,
                    Place.Field.LAT_LNG,
                    Place.Field.TYPES
                )
            );

        Task<FindCurrentPlaceResponse> placeResponse = 
            placesClient.findCurrentPlace(request);

        placeResponse.addOnCompleteListener(task -> {
            if (task.isSuccessful()) {
                FindCurrentPlaceResponse response = task.getResult();
                for (PlaceLikelihood placeLikelihood : 
                        response.getPlaceLikelihoods()) {
                    Place place = placeLikelihood.getPlace();
                    addPlaceToMap(place);
                }
            }
        });
    }
}
```

---

# Activity Recognition

```java
public class ActivityRecognitionManager {
    private ActivityRecognitionClient client;
    private PendingIntent pendingIntent;

    public void startActivityRecognition() {
        Intent intent = new Intent(
            context, 
            ActivityRecognitionReceiver.class
        );
        pendingIntent = PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT |
            PendingIntent.FLAG_IMMUTABLE
        );

        Task<Void> task = client.requestActivityUpdates(
            30000, // 30 seconds
            pendingIntent
        );

        task.addOnSuccessListener(result -> {
            // Started activity recognition
        });
    }
}
```

---

# Location Battery Optimization

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter8.md/1.png)

---

# Best Practices

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter8.md/2.png)

---

# Error Handling

| Scenario | Solution | Implementation |
|----------|----------|----------------|
| No GPS | Fall back to network | Switch provider |
| No permissions | Request or explain | Show dialog |
| Location disabled | Prompt settings | Open settings |
| Geofence limit | Remove old fences | Manage list |

---

# Assignment Preview
## Location-Aware Application

Create an application that:
1. Tracks user location
2. Displays Google Maps
3. Implements geofencing
4. Uses Places API
5. Handles activity recognition
6. Implements battery optimization

---

# Resources

- Google Maps Documentation
- FusedLocationProvider Guide
- Geofencing Documentation
- Places API Guide
- Activity Recognition Guide
