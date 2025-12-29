# Material Design and Animations
## Creating Engaging User Interfaces

---

## Material Design Principles

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Central Material Design node -->
  <ellipse cx="300" cy="200" rx="80" ry="40" fill="#673ab7" stroke="#333" stroke-width="3"/>
  <text x="300" y="200" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Material</text>
  <text x="300" y="218" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Design</text>

  <!-- Surface branch -->
  <ellipse cx="150" cy="100" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="12" font-weight="bold">Surface</text>

  <!-- Color branch -->
  <ellipse cx="450" cy="100" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="450" y="105" text-anchor="middle" font-size="12" font-weight="bold">Color</text>

  <!-- Typography branch -->
  <ellipse cx="150" cy="300" rx="60" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="305" text-anchor="middle" font-size="12" font-weight="bold">Typography</text>

  <!-- Motion branch -->
  <ellipse cx="450" cy="300" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="450" y="305" text-anchor="middle" font-size="12" font-weight="bold">Motion</text>

  <!-- Surface sub-elements -->
  <rect x="30" y="40" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="57" text-anchor="middle" font-size="10">Elevation</text>

  <rect x="30" y="75" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="92" text-anchor="middle" font-size="10">Shadow</text>

  <rect x="30" y="110" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="127" text-anchor="middle" font-size="10">Shape</text>

  <!-- Color sub-elements -->
  <rect x="500" y="30" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="47" text-anchor="middle" font-size="10">Primary</text>

  <rect x="500" y="60" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="77" text-anchor="middle" font-size="10">Secondary</text>

  <rect x="500" y="90" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="107" text-anchor="middle" font-size="10">Surface</text>

  <rect x="500" y="120" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="137" text-anchor="middle" font-size="10">Error</text>

  <!-- Typography sub-elements -->
  <rect x="30" y="270" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="287" text-anchor="middle" font-size="10">Scale</text>

  <rect x="30" y="300" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="317" text-anchor="middle" font-size="10">Hierarchy</text>

  <rect x="30" y="330" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="347" text-anchor="middle" font-size="10">Readability</text>

  <!-- Motion sub-elements -->
  <rect x="500" y="270" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="287" text-anchor="middle" font-size="10">Natural</text>

  <rect x="500" y="300" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="317" text-anchor="middle" font-size="10">Meaningful</text>

  <rect x="500" y="330" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="347" text-anchor="middle" font-size="10">Responsive</text>

  <!-- Connection lines -->
  <line x1="240" y1="180" x2="190" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="180" x2="410" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="240" y1="220" x2="190" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="220" x2="410" y2="280" stroke="#333" stroke-width="2"/>

  <!-- Sub-connections -->
  <line x1="100" y1="90" x2="100" y2="52" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="100" x2="100" y2="87" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="110" x2="100" y2="122" stroke="#666" stroke-width="1"/>

  <line x1="500" y1="90" x2="500" y2="42" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="100" x2="500" y2="72" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="110" x2="500" y2="102" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="120" x2="500" y2="132" stroke="#666" stroke-width="1"/>

  <line x1="100" y1="295" x2="100" y2="282" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="305" x2="100" y2="312" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="315" x2="100" y2="342" stroke="#666" stroke-width="1"/>

  <line x1="500" y1="295" x2="500" y2="282" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="305" x2="500" y2="312" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="315" x2="500" y2="342" stroke="#666" stroke-width="1"/>
</svg>

---

## Theme Implementation

```xml
<!-- styles.xml -->
<style name="AppTheme" parent="Theme.MaterialComponents.Light.NoActionBar">
    <!-- Primary brand color -->
    <item name="colorPrimary">@color/purple_500</item>
    <item name="colorPrimaryVariant">@color/purple_700</item>
    <item name="colorOnPrimary">@color/white</item>

    <!-- Secondary brand color -->
    <item name="colorSecondary">@color/teal_200</item>
    <item name="colorSecondaryVariant">@color/teal_700</item>
    <item name="colorOnSecondary">@color/black</item>

    <!-- Status bar color -->
    <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
</style>
```

---

## Material Components

| Component | Usage | Key Attributes |
|-----------|-------|----------------|
| MaterialButton | Interactive buttons | `app:cornerRadius`, `app:icon` |
| TextInputLayout | Text input fields | `app:errorEnabled`, `app:helperText` |
| Card | Content containers | `app:cardElevation`, `app:cardCornerRadius` |
| BottomNavigation | Navigation | `app:menu`, `app:labelVisibilityMode` |

---

## Custom Themes and Styles

```xml
<!-- Custom button style -->
<style name="CustomButton" parent="Widget.MaterialComponents.Button">
    <item name="android:textSize">16sp</item>
    <item name="cornerRadius">8dp</item>
    <item name="android:paddingStart">24dp</item>
    <item name="android:paddingEnd">24dp</item>
    <item name="android:letterSpacing">0.025</item>
</style>
```

---

## Typography System

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter03.md/1.png)

---

## Animation Types in Android

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter03.md/2.png)

---

## Property Animation Example

```java
public class AnimationDemo extends AppCompatActivity {
    private void animateButton(Button button) {
        ObjectAnimator scaleX = ObjectAnimator.ofFloat(
            button, "scaleX", 1f, 1.2f, 1f
        );
        ObjectAnimator scaleY = ObjectAnimator.ofFloat(
            button, "scaleY", 1f, 1.2f, 1f
        );

        AnimatorSet set = new AnimatorSet();
        set.playTogether(scaleX, scaleY);
        set.setDuration(300);
        set.setInterpolator(new OvershootInterpolator());
        set.start();
    }
}
```

---

## Motion Layout Basics

```xml
<!-- motion_scene.xml -->
<MotionScene xmlns:android="..."
    xmlns:motion="...">

    <Transition
        motion:constraintSetStart="@+id/start"
        motion:constraintSetEnd="@+id/end">
        <OnSwipe
            motion:dragDirection="dragUp"
            motion:touchAnchorId="@id/button" />
    </Transition>

    <ConstraintSet android:id="@+id/start">
        <!-- Start constraints -->
    </ConstraintSet>

    <ConstraintSet android:id="@+id/end">
        <!-- End constraints -->
    </ConstraintSet>
</MotionScene>
```

---

## Transition Framework

```java
public class TransitionDemo extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_transition);

        // Set up transition
        TransitionManager.beginDelayedTransition(
            container,
            new AutoTransition()
        );

        // Change visibility or layout params to trigger transition
        detailsView.setVisibility(
            detailsView.getVisibility() == View.GONE
                ? View.VISIBLE
                : View.GONE
        );
    }
}
```

---

## Custom View Animation

```java
public class PulseAnimation extends Animation {
    private float mStartScale;
    private float mEndScale;
    private View mView;

    @Override
    protected void applyTransformation(
            float interpolatedTime,
            Transformation t) {
        float scale = mStartScale + (mEndScale - mStartScale)
            * interpolatedTime;
        mView.setScaleX(scale);
        mView.setScaleY(scale);
    }
}
```

---

## Material Design Components in Practice

```xml
<com.google.android.material.card.MaterialCardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="16dp"
    app:cardElevation="4dp"
    app:cardCornerRadius="8dp">

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="16dp"
        app:errorEnabled="true"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox">

        <com.google.android.material.textfield.TextInputEditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Enter text"/>

    </com.google.android.material.textfield.TextInputLayout>
</com.google.android.material.card.MaterialCardView>
```

---

## Best Practices

![3](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter03.md/3.png)

---

## Assignment Preview
### Material Design Implementation

Create an app screen that demonstrates:
- Custom theme implementation
- Complex animations
- Material components usage
- Motion Layout transitions
- Responsive layout design

---

## Resources

- Material Design Guidelines
- Android Animation Documentation
- MotionLayout Code Lab
- Material Components Repository
- Animation Samples Repository
