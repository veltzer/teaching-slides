---
tags:
  - tools:unity
  - languages:csharp
level: beginner
category: game-development
audience:
  - audiences:developers

---
# Scripting Game Objects

---
## What This Chapter Covers

- Attaching scripts to GameObjects
- Reading and writing component values
- Handling user input
- Moving objects with Transform and Rigidbody
- Spawning new objects with Instantiate
- A working "shooter" example, piece by piece

---
## Attaching a Script

- Right-click in Project &#8594; Create &#8594; C# Script &#8594; name it `PlayerController`
- Drag the script onto a GameObject in the Hierarchy or Inspector
- The script appears as a Component in the Inspector
- Public fields show up as editable values right there
- One GameObject can have any number of scripts attached

---
## Update vs FixedUpdate

```csharp
void Update() {
    // every frame; use for input, animation, UI
}

void FixedUpdate() {
    // every physics step; use for Rigidbody forces
}
```

- `Update` is called once per *rendered* frame — variable frequency
- `FixedUpdate` is called once per *physics* step — fixed frequency (50/s default)
- Use `Time.deltaTime` in Update to get frame-rate independent motion
- Use `Time.fixedDeltaTime` in FixedUpdate (or just trust the cadence)

---
## Reading Input

```csharp
void Update() {
    if (Input.GetKey(KeyCode.W)) {
        transform.Translate(Vector3.forward * Time.deltaTime * speed);
    }
    if (Input.GetKeyDown(KeyCode.Space)) {
        Jump();
    }
}
```

- `GetKey`: held this frame
- `GetKeyDown`: pressed this frame (only true once per press)
- `GetKeyUp`: released this frame
- Mouse: `Input.GetMouseButton(0)`, `Input.mousePosition`
- Newer alternative: the Input System package — covered in advanced courses

---
## The Transform Component

- Every GameObject has a Transform; it's how Unity knows where it is
- `transform.position`: world-space position (Vector3)
- `transform.rotation`: orientation (Quaternion)
- `transform.localScale`: scale relative to the parent
- `transform.localPosition`: position relative to the parent

---
## Moving With Transform

```csharp
transform.position += Vector3.forward * Time.deltaTime * 5f;
transform.Translate(Vector3.up * Time.deltaTime * 2f);
transform.Rotate(0, 90 * Time.deltaTime, 0);
```

- Direct edit: snappy, no physics
- Use for UI elements, AI navigation, anything that doesn't collide
- For physically-realistic motion, use Rigidbody instead

---
## Moving With Rigidbody

```csharp
private Rigidbody rb;

void Awake() {
    rb = GetComponent<Rigidbody>();
}

void FixedUpdate() {
    rb.AddForce(Vector3.forward * 10f);
}
```

- Add a Rigidbody component for physics-driven motion
- Forces, gravity, collisions all just work
- Always update Rigidbodies in `FixedUpdate`, not `Update`
- Cache `GetComponent<Rigidbody>()` in `Awake` — it's not free

---
## Accessing Other Components

```csharp
private Renderer rend;
private AudioSource audio;

void Awake() {
    rend = GetComponent<Renderer>();
    audio = GetComponent<AudioSource>();
}

void OnHit() {
    rend.material.color = Color.red;
    audio.Play();
}
```

- `GetComponent<T>()` returns the first matching component on the same GameObject
- `GetComponentInChildren<T>()`, `GetComponentInParent<T>()` walk the hierarchy
- Returns `null` if not found — protect against that or fail loudly

---
## Inspector-Visible References

```csharp
public class Turret : MonoBehaviour
{
    [SerializeField] private GameObject bulletPrefab;
    [SerializeField] private Transform muzzle;
    [SerializeField] private float fireRate = 2f;
}
```

- `[SerializeField]` exposes a *private* field in the Inspector
- Drag a prefab or scene object onto the slot to wire it up
- Better than `GameObject.Find("Bullet")` — typo-proof, refactor-safe
- Always-public fields work too but encapsulation is generally better

---
## Spawning With Instantiate

```csharp
[SerializeField] private GameObject bulletPrefab;
[SerializeField] private Transform muzzle;

void Fire() {
    Instantiate(bulletPrefab, muzzle.position, muzzle.rotation);
}
```

- Creates a copy of the prefab at runtime
- Returns the new GameObject — keep the reference if you need to talk to it
- The prefab is the *template*; the instance is the *thing in the scene*
- Pair with `Destroy(go)` or you'll leak GameObjects forever

---
## Destroy

```csharp
void OnCollisionEnter(Collision c) {
    Destroy(gameObject);          // remove me
    Destroy(c.gameObject, 1f);    // remove the other one in 1 second
}
```

- `Destroy(gameObject)` removes the whole GameObject
- `Destroy(this)` removes only this script component
- Optional second argument: delay in seconds
- For frequent spawn/despawn, prefer object pooling — covered later

---
## Collisions and Triggers

```csharp
void OnCollisionEnter(Collision other) {
    Debug.Log("Hit " + other.gameObject.name);
}

void OnTriggerEnter(Collider other) {
    if (other.CompareTag("Pickup"))
        Destroy(other.gameObject);
}
```

- Both objects need a Collider; at least one needs a Rigidbody
- `OnCollision*` fires for solid collisions (objects bounce off)
- `OnTrigger*` fires when one Collider has "Is Trigger" ticked — passes through
- Use tags for cheap categorisation; layers for physics filtering

---
## Tags and Layers

- Tags: human-readable label per GameObject ("Player", "Enemy", "Pickup")
- Layers: numeric category, used by physics and rendering for filtering
- Set both in the Inspector
- Compare with `gameObject.CompareTag("Player")` (avoids string allocation)
- Don't overuse tags for state — that's what scripts are for

---
## Public Methods Called From the Editor

```csharp
public class HighScore : MonoBehaviour {
    public void Reset() {
        PlayerPrefs.SetInt("score", 0);
    }
}
```

- A `public void` with no parameters can be wired to UI buttons
- The Button component has an `OnClick` event with a slot for this
- Drag the GameObject in, pick the method from the dropdown
- Saves writing event-handler code by hand

---
## Putting It Together

![object_interaction](svg/courses/unity/introduction-to-game-development-with-unity/04_scripting_game_objects/object_interaction.svg)

---
## Common Mistakes

- Calling `GetComponent<T>()` in Update every frame instead of caching in Awake
- Using `Update` for physics — frame-rate dependent, jittery
- Forgetting `Time.deltaTime` — movement speeds depend on FPS
- `null` references when a `[SerializeField]` slot was never wired in the Inspector
- Spawning thousands of bullets without pooling — GC pauses
