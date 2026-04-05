# Location and Maps
## Implementing Location-Based Services

---

## Location Services Overview

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Location Services</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">GPS</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Network</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Sensors</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="445" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Maps</text>
  <text x="600" y="460" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">API</text>
</svg>

---

## Location Permissions

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

## FusedLocationProvider Implementation

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

## Google Maps Integration

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

## Geofencing Implementation

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

## Places API Integration

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

## Activity Recognition

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

## Location Battery Optimization

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect x="340" y="50" width="120" height="50" rx="8" fill="#4CAF50" stroke="#4CAF00" stroke-width="2"/>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Request Permission</text>
  <line x1="400" y1="100" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="140" width="120" height="50" rx="8" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="400" y="170" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Get Location</text>
  <line x1="400" y1="190" x2="400" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="230" width="120" height="50" rx="8" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="260" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Process Data</text>
  <line x1="400" y1="280" x2="400" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="340" y="320" width="120" height="50" rx="8" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Update UI</text>
</svg>

---

## Best Practices

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="300" r="70" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Map Features</text>
  <line x1="330" y1="250" x2="200" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="150" r="45" fill="#2196F3" stroke="#219600" stroke-width="2"/>
  <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Markers</text>
  <line x1="470" y1="250" x2="600" y2="150" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="150" r="45" fill="#FF9800" stroke="#FF9800" stroke-width="2"/>
  <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Overlays</text>
  <line x1="330" y1="350" x2="200" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="200" cy="450" r="45" fill="#9C27B0" stroke="#9C2700" stroke-width="2"/>
  <text x="200" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Routes</text>
  <line x1="470" y1="350" x2="600" y2="450" stroke="#666" stroke-width="2"/>
  <circle cx="600" cy="450" r="45" fill="#F44336" stroke="#F44300" stroke-width="2"/>
  <text x="600" y="455" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Gestures</text>
</svg>

---

## Error Handling

| Scenario | Solution | Implementation |
|----------|----------|----------------|
| No GPS | Fall back to network | Switch provider |
| No permissions | Request or explain | Show dialog |
| Location disabled | Prompt settings | Open settings |
| Geofence limit | Remove old fences | Manage list |

---

## Assignment Preview
### Location-Aware Application

Create an application that:
1. Tracks user location
1. Displays Google Maps
1. Implements geofencing
1. Uses Places API
1. Handles activity recognition
1. Implements battery optimization

---

## Resources

- Google Maps Documentation
- FusedLocationProvider Guide
- Geofencing Documentation
- Places API Guide
- Activity Recognition Guide
